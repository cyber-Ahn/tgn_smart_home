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
summertemp = "0"
summermod_cach = ""
data_nc = []
window_1_id = "0"
window_1_cach = "empty"
window_1 = "closed"

thermostat_1_id = "0"
thermostat_2_id = "0"
thermostat_3_id = "0"
thermostat_4_id = "0"
thermostat_1_cach = "empty"
thermostat_2_cach = "empty"
thermostat_3_cach = "empty"
thermostat_4_cach = "empty"

thermo_is_1 = "0"
thermo_out_1 = "0"
thermo_cal_1 = "0"
thermo_is_2 = "0"
thermo_out_2 = "0"
thermo_cal_2 = "0"
thermo_is_3 = "0"
thermo_out_3 = "0"
thermo_cal_3 = "0"
thermo_is_4 = "0"
thermo_out_4 = "0"
thermo_cal_4 = "0"

shelly_1_id = "0"
door_1_cach = "empty"
summermod = "x"
t_temp = "0"
temp = 11

battery_name = "empty"
battery_window_1 = "0"
battery_door_1 = "0"
battery_thermostat_1 = "0"
battery_thermostat_2 = "0"
battery_thermostat_3 = "0"
battery_thermostat_4 = "0"


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
        if cach_n.split(":")[0] == "thermostat_2":
            thermostat_2_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Thermostat 2: "+thermostat_2_id)
        if cach_n.split(":")[0] == "thermostat_3":
            thermostat_3_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Thermostat 3: "+thermostat_3_id)
        if cach_n.split(":")[0] == "thermostat_4":
            thermostat_4_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Thermostat 4: "+thermostat_4_id)
        if cach_n.split(":")[0] == "door_1":
            shelly_1_id = "shellies/"+cach_n.split(":")[1]+"/info"
            print("Door 1:       "+shelly_1_id)

def ini():
    client.publish("tgn/thermostat/summer_temp",summertemp,qos=0,retain=True)
    client.publish("tgn/thermostat/window_1",window_1,qos=0,retain=True)
    client.publish(thermostat_1_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    client.publish(thermostat_1_id+"/set",'{"local_temperature_calibration": 0.0}',qos=0,retain=True)
    client.publish(thermostat_1_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)
    time.sleep(0.3)
    client.publish(thermostat_2_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    client.publish(thermostat_2_id+"/set",'{"local_temperature_calibration": 0.0}',qos=0,retain=True)
    client.publish(thermostat_2_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)
    time.sleep(0.3)
    client.publish(thermostat_3_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    client.publish(thermostat_3_id+"/set",'{"local_temperature_calibration": 1.0}',qos=0,retain=True)
    client.publish(thermostat_3_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)
    time.sleep(0.3)
    client.publish(thermostat_4_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    client.publish(thermostat_4_id+"/set",'{"local_temperature_calibration": 0.2}',qos=0,retain=True)
    client.publish(thermostat_4_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)

def decode_window(decode_data,num,typ):
    #print(decode_data+" Number:"+num+" Typ:"+typ)
    cach = json.loads(decode_data)
    global window_1
    global thermo_is_1
    global thermo_out_1
    global thermo_cal_1
    global thermo_is_2
    global thermo_out_2
    global thermo_cal_2
    global thermo_is_3
    global thermo_out_3
    global thermo_cal_3
    global thermo_is_4
    global thermo_out_4
    global thermo_cal_4
    global battery_door_1
    global battery_window_1
    global battery_thermostat_1
    global battery_thermostat_2
    global battery_thermostat_3
    global battery_thermostat_4
    if typ == "window" and num == "1":
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
    if typ == "thermostat" and num == "1":
        thermo_is_1 = cach['local_temperature']
        thermo_out_1 = cach['occupied_heating_setpoint']
        thermo_cal_1 = cach['local_temperature_calibration']
        battery_thermostat_1 = cach['battery']
        client.publish("tgn/thermostat/thermostat_1_local",thermo_is_1,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_1_setpoint",thermo_out_1,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_1__cal",thermo_cal_1,qos=0,retain=True)
    if typ == "thermostat" and num == "2":
        thermo_is_2 = cach['local_temperature']
        thermo_out_2 = cach['occupied_heating_setpoint']
        thermo_cal_2 = cach['local_temperature_calibration']
        battery_thermostat_2 = cach['battery']
        client.publish("tgn/thermostat/thermostat_2_local",thermo_is_2,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_2_setpoint",thermo_out_2,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_2__cal",thermo_cal_2,qos=0,retain=True)
    if typ == "thermostat" and num == "3":
        thermo_is_3 = cach['local_temperature']
        thermo_out_3 = cach['occupied_heating_setpoint']
        thermo_cal_3 = cach['local_temperature_calibration']
        battery_thermostat_3 = cach['battery']
        client.publish("tgn/thermostat/thermostat_3_local",thermo_is_3,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_3_setpoint",thermo_out_3,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_3__cal",thermo_cal_3,qos=0,retain=True)
    if typ == "thermostat" and num == "4":
        thermo_is_4 = cach['local_temperature']
        thermo_out_4 = cach['occupied_heating_setpoint']
        thermo_cal_4 = cach['local_temperature_calibration']
        battery_thermostat_4 = cach['battery']
        client.publish("tgn/thermostat/thermostat_4_local",thermo_is_4,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_4_setpoint",thermo_out_4,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_4__cal",thermo_cal_4,qos=0,retain=True)
    if typ == "door":
        battery_door_1 = cach['bat']['value']

def on_message(client, userdata, message):
    global t_temp
    global summertemp
    global temp
    global summermod
    global window_1_cach
    global thermostat_1_cach
    global thermostat_2_cach
    global thermostat_3_cach
    global thermostat_4_cach
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
    if(message.topic==thermostat_2_id):
        thermostat_2_cach = (message.payload.decode("utf-8"))
        decode_window(thermostat_2_cach,"2","thermostat")
    if(message.topic==thermostat_3_id):
        thermostat_3_cach = (message.payload.decode("utf-8"))
        decode_window(thermostat_3_cach,"3","thermostat")
    if(message.topic==thermostat_4_id):
        thermostat_4_cach = (message.payload.decode("utf-8"))
        decode_window(thermostat_4_cach,"4","thermostat")
    if(message.topic==shelly_1_id):
        door_1_cach = (message.payload.decode("utf-8"))
        decode_window(door_1_cach,"1","door")

def main_prog():
    print("Start zigbee modul")
    global summermod_cach
    while True:
        client.on_message=on_message
        client.loop_start()
        client.subscribe([(zig_topic,0)])
        client.subscribe([(tgn_topic,0)])
        client.subscribe([(she_topic,0)])
        time.sleep(2)
        client.loop_stop()
        time.sleep(5)
        if summermod != summermod_cach:
            summermod_cach = summermod
            client.publish("tgn/thermostat/sol_temp",summertemp,qos=0,retain=True)
            client.publish(thermostat_1_id+"/set",'{"system_mode": "off"}',qos=0,retain=True)
            client.publish(thermostat_2_id+"/set",'{"system_mode": "off"}',qos=0,retain=True)
            client.publish(thermostat_3_id+"/set",'{"system_mode": "off"}',qos=0,retain=True)
            client.publish(thermostat_4_id+"/set",'{"system_mode": "off"}',qos=0,retain=True)
        elif summermod == "off":
            summermod_cach = summermod
            client.publish("tgn/thermostat/sol_temp",t_temp,qos=0,retain=True)
            client.publish(thermostat_1_id+"/set",'{"system_mode": "heat"}',qos=0,retain=True)
            client.publish(thermostat_2_id+"/set",'{"system_mode": "heat"}',qos=0,retain=True)
            client.publish(thermostat_3_id+"/set",'{"system_mode": "heat"}',qos=0,retain=True)
            client.publish(thermostat_4_id+"/set",'{"system_mode": "heat"}',qos=0,retain=True)
            if window_1 == "open":
                client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
                client.publish(thermostat_2_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
                client.publish(thermostat_3_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
                client.publish(thermostat_4_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
            elif window_1 == "closed":
                client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
                client.publish(thermostat_2_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
                client.publish(thermostat_3_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
                client.publish(thermostat_4_id+"/set",'{"occupied_heating_setpoint": '+str(float(t_temp)-2.0)+'}',qos=0,retain=True)
        if t_temp > temp:
            client.publish("tgn/thermostat/heater","On",qos=0,retain=True)
        else:
            client.publish("tgn/thermostat/heater","Off",qos=0,retain=True)
        
        battery_name = "Battery Ok"
        client.publish("tgn/battery_empty",battery_name,qos=0,retain=True)
        if int(battery_window_1) < bat_low:
            battery_name ="window_wz"
        if int(battery_thermostat_1) < bat_low:
            battery_name ="thermostat_1"
        if int(battery_thermostat_2) < bat_low:
            battery_name ="thermostat_2"
        if int(battery_thermostat_3) < bat_low:
            battery_name ="thermostat_3"
        if int(battery_thermostat_4) < bat_low:
            battery_name ="thermostat_4"
        if int(battery_door_1) < bat_low:
            battery_name ="door_1"
        print(battery_name)
ini()
main_prog()