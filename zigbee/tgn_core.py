import json
import paho.mqtt.client as mqtt
import time
from tgnLIB import get_ip

zig_topic = "zigbee2mqtt/#"
tgn_topic = "tgn/#"
she_topic = "shellies/#"

client = mqtt.Client("zigbee")
client.connect(get_ip())

bat_low = 25
summertemp = "12"
data_nc = []
window_1_id = "0"
thermostat_1_id = "0"
shelly_1_id = "0"
window_1_cach = "empty"
thermostat_1_cach = "empty"
door_1_cach = "empty"
summermod = "on"
t_temp = "0"
temp = 11
window_1 = "closed"
thermo_is_1 = "0"
thermo_out_1 = "0"
thermo_cal_1 = "0"
battery_name = "empty"
battery_window_1 = "0"
battery_thermostat_1 = "0"
battery_door_1 = "0"


try:
    print(">>Load zigbee.config")
    f = open("/home/pi/tgn_smart_home/zigbee/device.config","r")
except IOError:
    print("cannot open panel.config.... file not found")
else:
    for line in f:
        cach_n = line.rstrip()
        if cach_n.split(":")[0] == "window_1":
            window_1_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Window 1:     "+window_1_id)
        if cach_n.split(":")[0] == "thermostat_1":
            thermostat_1_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Thermostat 1: "+thermostat_1_id)
        if cach_n.split(":")[0] == "door_1":
            shelly_1_id = "shellies/"+cach_n.split(":")[1]+"/info"
            print("Door 1:       "+shelly_1_id)

def ini():
    client.publish("tgn/thermostat/summer_temp",summertemp,qos=0,retain=True)
    client.publish("tgn/thermostat/window_1",window_1,qos=0,retain=True)
    client.publish(thermostat_1_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    client.publish(thermostat_1_id+"/set",'{"local_temperature_calibration": 0.4}',qos=0,retain=True)
    client.publish(thermostat_1_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)

def decode_window(decode_data,num,typ):
    #print(decode_data+" Number:"+num+" Typ:"+typ)
    cach = json.loads(decode_data)
    global window_1
    global thermo_is_1
    global thermo_out_1
    global thermo_cal_1
    global battery_door_1
    global battery_thermostat_1
    global battery_window_1
    if typ == "window":
        try:
            window_1 = cach['contact']
            battery_window_1 = cach['battery']
            if window_1:
                window_1 = "closed"
            else:
                window_1 = "open"
        except:
            print("error")
        if num == "1":
            client.publish("tgn/thermostat/window_1",window_1,qos=0,retain=True)
    if typ == "thermostat":
        thermo_is_1 = cach['local_temperature']
        thermo_out_1 = cach['occupied_heating_setpoint']
        thermo_cal_1 = cach['local_temperature_calibration']
        battery_thermostat_1 = cach['battery']
        client.publish("tgn/thermostat/thermostat_1_local",thermo_is_1,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_1_setpoint",thermo_out_1,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_1__cal",thermo_cal_1,qos=0,retain=True)
    if typ == "door":
        battery_door_1 = cach['bat']['value']

def on_message(client, userdata, message):
    global t_temp
    global summertemp
    global temp
    global summermod
    global window_1_cach
    global thermostat_1_cach
    global door_1_cach
    if(message.topic=="tgn/thermostat/sol_temp"):
        t_temp = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/thermostat/summer_temp"):
        summertemp = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/esp_1/temp/sensor_1"):
        temp = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/thermostat/summer_mod"):
        summermod = (message.payload.decode("utf-8"))
    if(message.topic==window_1_id):
        window_1_cach = (message.payload.decode("utf-8"))
        decode_window(window_1_cach,"1","window")
    if(message.topic==thermostat_1_id):
        thermostat_1_cach = (message.payload.decode("utf-8"))
        decode_window(thermostat_1_cach,"1","thermostat")
    if(message.topic==shelly_1_id):
        door_1_cach = (message.payload.decode("utf-8"))
        decode_window(door_1_cach,"1","door")

def main_prog():
    print("Start zigbee modul")
    while True:
        client.on_message=on_message
        client.loop_start()
        client.subscribe([(zig_topic,0)])
        client.subscribe([(tgn_topic,0)])
        client.subscribe([(she_topic,0)])
        time.sleep(2)
        client.loop_stop()
        time.sleep(5)
        if summermod == "on":
            client.publish("tgn/thermostat/sol_temp",summertemp,qos=0,retain=True)
        if t_temp > temp:
            client.publish("tgn/thermostat/heater","On",qos=0,retain=True)
        else:
            client.publish("tgn/thermostat/heater","Off",qos=0,retain=True)
        if window_1 == "open":
            client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": 8}',qos=0,retain=True)
        elif window_1 == "closed":
            client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
        battery_name = "Battery Ok"
        client.publish("tgn/battery_empty",battery_name,qos=0,retain=True)
        if int(battery_window_1) < bat_low:
            battery_name ="window_wz"
        if int(battery_thermostat_1) < bat_low:
            battery_name ="thermostat_1"
        if int(battery_door_1) < bat_low:
            battery_name ="door_1"
        print(battery_name)
ini()
main_prog()