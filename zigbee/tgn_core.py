import json
import paho.mqtt.client as mqtt
import time
from tgnLIB import get_ip, logging_tgn

zig_topic = "zigbee2mqtt/#"
tgn_topic = "tgn/#"
she_topic = "shellies/#"
log = "on"

client = mqtt.Client("zigbee")
client.connect(get_ip())

bat_low = 25
cou = 25
summertemp = "7"
summermod_cach = ""
data_nc = []
w_temp = "15.0"
accuracy_mode = "1"
accuracy_cach = "x"

window_1_id = "0"
window_1_cach = "empty"
window_cach = ""
window_1 = "closed"
window_1_stat = "xx"

motion_1_id = "0"
motion_1_timeout = "20"
motion_1_cach = "empty"
motion_1_activ = "False"
motion_1_ilu = "bright"
motion_1_stat = "off"

light_1_id = "0"
light_1_bri = "254"
light_1_behavor = "previous"
light_1_cach = "empty"

light_2_id = "0"
light_2_bri = "254"
light_2_behavor = "on"
light_2_cach = "empty"

light_2_is = "OFF"
tim_cou = 0
tim_state = "off"
tim_sol = 20
motion_1_is_cach = "off"

tgn_1_id = "0"
tgn_1_cach = "empty"
tgn_1_sate_1 = "empty"
tgn_1_sate_14 = "empty"

ir_cach = "nothing"
ir_botton = "nothing"
ir_power = "p"
ir_fan = "f"
ir_cool = "c"
ir_dry = "dr"
ir_up = "u"
ir_down = "d"
ir_empty = "e"

thermostat_1_id = "0"
thermostat_2_id = "0"
thermostat_3_id = "0"
thermostat_4_id = "0"
thermostat_5_id = "0"
thermostat_1_cach = "empty"
thermostat_2_cach = "empty"
thermostat_3_cach = "empty"
thermostat_4_cach = "empty"
thermostat_5_cach = "empty"

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
thermo_is_5 = "0"
thermo_out_5 = "0"
thermo_cal_5 = "0"

shelly_1_id = "0"
door_1_cach = "empty"
summermod = "x"
t_temp = "0"
t_temp_cach = "0"
temp_1 = 11.5
temp_3 = 11.5
temp_4 = 11.5
valve_movement = "off"

battery_name = "empty"
battery_window_1 = "0"
battery_door_1 = "0"
battery_motion_1 = "0"
battery_thermostat_1 = "0"
battery_thermostat_2 = "0"
battery_thermostat_3 = "0"
battery_thermostat_4 = "0"
battery_thermostat_5 = "100"

status_thermostat_1 = "0"
status_thermostat_2 = "0"
status_thermostat_3 = "0"
status_thermostat_4 = "0"
status_thermostat_5 = "0"

try:
    print(">>Load zigbee.config")
    f = open("/home/pi/tgn_smart_home/zigbee/device.config","r")
except IOError:
    print("cannot open system.config.... file not found")
else:
    for line in f:
        cach_n = line.rstrip()
        if cach_n.split(":")[0] == "window_1":
            window_1_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Window 1:       "+window_1_id)
        if cach_n.split(":")[0] == "thermostat_1":
            thermostat_1_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Thermostat 1:   "+thermostat_1_id)
        if cach_n.split(":")[0] == "thermostat_2":
            thermostat_2_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Thermostat 2:   "+thermostat_2_id)
        if cach_n.split(":")[0] == "thermostat_3":
            thermostat_3_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Thermostat 3:   "+thermostat_3_id)
        if cach_n.split(":")[0] == "thermostat_4":
            thermostat_4_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Thermostat 4:   "+thermostat_4_id)
        if cach_n.split(":")[0] == "thermostat_5":
            thermostat_5_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Thermostat 5:   "+thermostat_5_id)
        if cach_n.split(":")[0] == "door_1":
            shelly_1_id = "shellies/"+cach_n.split(":")[1]+"/info"
            print("Door 1:         "+shelly_1_id)
        if cach_n.split(":")[0] == "motion_1":
            motion_1_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Motion 1:       "+motion_1_id)
        if cach_n.split(":")[0] == "bat_low":
            bat_low = int(cach_n.split(":")[1])
            print("Bat_LOw:        "+str(bat_low))
        if cach_n.split(":")[0] == "motion_1_timeout":
            motion_1_timeout = cach_n.split(":")[1]
            print("Motion TimeOut: "+motion_1_timeout) 
        if cach_n.split(":")[0] == "light_1":
            light_1_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Light 1:        "+light_1_id)
        if cach_n.split(":")[0] == "light_1_bri":
            light_1_bri = cach_n.split(":")[1]
            print("Li.1 brightness:"+light_1_bri)
        if cach_n.split(":")[0] == "tgn_1":
            tgn_1_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("TGN Modul 1:    "+tgn_1_id)
        if cach_n.split(":")[0] == "light_2":
            light_2_id = "zigbee2mqtt/"+cach_n.split(":")[1]
            print("Light 2:        "+light_2_id)
        if cach_n.split(":")[0] == "light_2_bri":
            light_2_bri = cach_n.split(":")[1]
            print("Li.2 brightness:"+light_2_bri)
        if cach_n.split(":")[0] == "timer_sol":
            tim_sol = int(cach_n.split(":")[1])
            print("Timer Sol:      "+str(tim_sol))
    print("--------------------------------------------")

try:
    print(">>Load system.config")
    f = open("/home/pi/tgn_smart_home/config/system.config","r")
except IOError:
    print("cannot open system.config.... file not found")
else:
    for line in f:
        cach_n = line.rstrip()
        if cach_n.split("*")[0] == "ir_power":
            ir_power = cach_n.split("*")[1]
            print("power:"+ir_power)
        if cach_n.split("*")[0] == "ir_fan":
            ir_fan = cach_n.split("*")[1]
            print("fan:"+ir_fan)
        if cach_n.split("*")[0] == "ir_cool":
            ir_cool = cach_n.split("*")[1]
            print("cool:"+ir_cool)
        if cach_n.split("*")[0] == "ir_dry":
            ir_dry = cach_n.split("*")[1]
            print("dry:"+ir_dry)
        if cach_n.split("*")[0] == "ir_up":
            ir_up = cach_n.split("*")[1]
            print("up:"+ir_up)
        if cach_n.split("*")[0] == "ir_down":
            ir_down = cach_n.split("*")[1]
            print("down:"+ir_down)
        if cach_n.split("*")[0] == "ir_clear":
            ir_empty = cach_n.split("*")[1]
            print("empty:"+ir_empty)

def ini():
    global tgn_1_sate_1
    global tgn_1_sate_14
    client.publish("tgn/tgn_modul_1/outlet_set","OFF",qos=0,retain=True)
    client.publish("tgn/tgn_modul_1/bulb_set","OFF",qos=0,retain=True)
    client.publish("tgn/thermostat/summer_temp",summertemp,qos=0,retain=True)
    client.publish("tgn/thermostat/window_1",window_1,qos=0,retain=True)
    client.publish("tgn/air_conditioner/button",ir_cach,qos=0,retain=True)
    client.publish(thermostat_1_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    client.publish(thermostat_1_id+"/set",'{"local_temperature_calibration": 0.0}',qos=0,retain=True)
    client.publish(thermostat_1_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)
    time.sleep(0.3)
    client.publish(thermostat_2_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    client.publish(thermostat_2_id+"/set",'{"local_temperature_calibration": 0.0}',qos=0,retain=True)
    client.publish(thermostat_2_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)
    time.sleep(0.3)
    client.publish(thermostat_3_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    client.publish(thermostat_3_id+"/set",'{"local_temperature_calibration": 0.0}',qos=0,retain=True)
    client.publish(thermostat_3_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)
    time.sleep(0.3)
    client.publish(thermostat_4_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    client.publish(thermostat_4_id+"/set",'{"local_temperature_calibration": 0.0}',qos=0,retain=True)
    client.publish(thermostat_4_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)
    time.sleep(0.3)
    #client.publish(thermostat_5_id+"/set",'{"child_lock": "LOCK"}',qos=0,retain=True)
    #client.publish(thermostat_5_id+"/set",'{"local_temperature_calibration": 0.0}',qos=0,retain=True)
    #client.publish(thermostat_5_id+"/set",'{"open_window": "OFF"}',qos=0,retain=True)
    time.sleep(0.3)
    client.publish("tgn/thermostat/valve_movement","off",qos=0,retain=True)
    client.publish(motion_1_id+"/set",'{"motion_timeout": '+motion_1_timeout+'}',qos=0,retain=True)
    client.publish(light_1_id+"/set",'{"brightness": '+light_1_bri+'}',qos=0,retain=True)
    client.publish(light_1_id+"/set",'{"power_on_behavior": "'+light_1_behavor+'"}',qos=0,retain=True)
    client.publish(light_2_id+"/set",'{"brightness": '+light_2_bri+'}',qos=0,retain=True)
    client.publish(light_2_id+"/set",'{"power_on_behavior": "'+light_2_behavor+'"}',qos=0,retain=True)
    client.publish(light_1_id+"/set",'{"state": "OFF"}',qos=0,retain=True)
    client.publish(light_2_id+"/set",'{"state": "OFF"}',qos=0,retain=True)
    client.publish(tgn_1_id+"/set",'{"state_1": "ON"}',qos=0,retain=True)
    client.publish(tgn_1_id+"/set",'{"state_14": "ON"}',qos=0,retain=True)
    time.sleep(3)
    client.publish(tgn_1_id+"/set",'{"state_1": "OFF"}',qos=0,retain=True)
    client.publish(tgn_1_id+"/set",'{"state_14": "OFF"}',qos=0,retain=True)
    time.sleep(3)
    tgn_1_sate_1 = "OFF"
    tgn_1_sate_14 = "OFF"
    print("ini end")

def decode_window(decode_data,num,typ):
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
    global thermo_is_5
    global thermo_out_5
    global thermo_cal_5
    global battery_door_1
    global battery_window_1
    global battery_thermostat_1
    global battery_thermostat_2
    global battery_thermostat_3
    global battery_thermostat_4
    global battery_thermostat_5
    global battery_motion_1
    global status_thermostat_1
    global status_thermostat_2
    global status_thermostat_3
    global status_thermostat_4
    global status_thermostat_5
    global motion_1_activ
    global motion_1_ilu
    global tgn_1_sate_1
    global tgn_1_sate_14
    if typ == "window" and num == "1":
        try:
            window_1 = cach['contact']
            battery_window_1 = cach['battery']
            client.publish("tgn/thermostat/window_1_bat",battery_window_1,qos=0,retain=True)
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
        status_thermostat_1 = cach['running_state']
        client.publish("tgn/thermostat/thermostat_1_bat",battery_thermostat_1,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_1_local",thermo_is_1,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_1_setpoint",thermo_out_1,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_1__cal",thermo_cal_1,qos=0,retain=True)
        client.publish("tgn/thermostat/status/1",status_thermostat_1,qos=0,retain=True)
    if typ == "thermostat" and num == "2":
        thermo_is_2 = cach['local_temperature']
        thermo_out_2 = cach['occupied_heating_setpoint']
        thermo_cal_2 = cach['local_temperature_calibration']
        battery_thermostat_2 = cach['battery']
        status_thermostat_2 = cach['running_state']
        client.publish("tgn/thermostat/thermostat_2_bat",battery_thermostat_2,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_2_local",thermo_is_2,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_2_setpoint",thermo_out_2,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_2__cal",thermo_cal_2,qos=0,retain=True)
        client.publish("tgn/thermostat/status/2",status_thermostat_2,qos=0,retain=True)
    if typ == "thermostat" and num == "3":
        thermo_is_3 = cach['local_temperature']
        thermo_out_3 = cach['occupied_heating_setpoint']
        thermo_cal_3 = cach['local_temperature_calibration']
        battery_thermostat_3 = cach['battery']
        status_thermostat_3 = cach['running_state']
        client.publish("tgn/thermostat/thermostat_3_bat",battery_thermostat_3,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_3_local",thermo_is_3,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_3_setpoint",thermo_out_3,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_3__cal",thermo_cal_3,qos=0,retain=True)
        client.publish("tgn/thermostat/status/3",status_thermostat_3,qos=0,retain=True)
    if typ == "thermostat" and num == "4":
        thermo_is_4 = cach['local_temperature']
        thermo_out_4 = cach['occupied_heating_setpoint']
        thermo_cal_4 = cach['local_temperature_calibration']
        battery_thermostat_4 = cach['battery']
        status_thermostat_4 = cach['running_state']
        client.publish("tgn/thermostat/thermostat_4_bat",battery_thermostat_4,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_4_local",thermo_is_4,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_4_setpoint",thermo_out_4,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_4__cal",thermo_cal_4,qos=0,retain=True)
        client.publish("tgn/thermostat/status/4",status_thermostat_4,qos=0,retain=True)
    if typ == "thermostat" and num == "5":
        thermo_is_5 = cach['local_temperature']
        thermo_out_5 = cach['occupied_heating_setpoint']
        thermo_cal_5 = cach['local_temperature_calibration']
        battery_thermostat_5 = cach['battery']
        status_thermostat_5 = cach['running_state']
        client.publish("tgn/thermostat/thermostat_5_bat",battery_thermostat_5,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_5_local",thermo_is_5,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_5_setpoint",thermo_out_5,qos=0,retain=True)
        client.publish("tgn/thermostat/thermostat_5__cal",thermo_cal_5,qos=0,retain=True)
        client.publish("tgn/thermostat/status/5",status_thermostat_5,qos=0,retain=True)
    if typ == "door" and num == "1":
        battery_door_1 = cach['bat']['value']
        client.publish("tgn/thermostat/door_1_bat",battery_door_1,qos=0,retain=True)
        client.publish("tgn/thermostat/door_1",cach['sensor']['state'],qos=0,retain=True)
        client.publish("tgn/thermostat/door_1_temp",cach['tmp']['value'],qos=0,retain=True)
    if typ == "motion" and num == "1":
        battery_motion_1 = cach['battery']
        motion_1_ilu = cach['illumination']
        motion_1_activ = cach['occupancy']
        client.publish("tgn/thermostat/motion_1_bat",battery_motion_1,qos=0,retain=True)
        client.publish("tgn/thermostat/motion_1_ilumi",motion_1_ilu,qos=0,retain=True)
        client.publish("tgn/thermostat/motion_1_timeout",cach['motion_timeout'],qos=0,retain=True)
        client.publish("tgn/thermostat/motion_1_detected",motion_1_activ,qos=0,retain=True)
    if typ == "light" and num == "1":
        client.publish("tgn/thermostat/ligh_1_state",cach['state'],qos=0,retain=True)
        client.publish("tgn/thermostat/ligh_1_bri",cach['brightness'],qos=0,retain=True)
        client.publish("tgn/thermostat/ligh_1_behavior",cach['power_on_behavior'],qos=0,retain=True)
    if typ == "light" and num == "2":
        client.publish("tgn/thermostat/ligh_2_state",cach['state'],qos=0,retain=True)
        client.publish("tgn/thermostat/ligh_2_bri",cach['brightness'],qos=0,retain=True)
        client.publish("tgn/thermostat/ligh_2_behavior",cach['power_on_behavior'],qos=0,retain=True)
    if typ == "tgn" and num == "1":
        tgn_1_sate_1 = cach['state_1']
        tgn_1_sate_14 = cach['state_14']
        client.publish("tgn/tgn_modul_1/flow",cach['flow_11'],qos=0,retain=True)
        client.publish("tgn/tgn_modul_1/hum",cach['humidity_10'],qos=0,retain=True)
        client.publish("tgn/tgn_modul_1/illu",cach['illuminance_9'],qos=0,retain=True)
        client.publish("tgn/tgn_modul_1/link",cach['linkquality'],qos=0,retain=True)
        client.publish("tgn/tgn_modul_1/motion",cach['occupancy_13'],qos=0,retain=True)
        client.publish("tgn/tgn_modul_1/pressure",cach['pressure_12'],qos=0,retain=True)
        client.publish("tgn/tgn_modul_1/outlet",tgn_1_sate_1,qos=0,retain=True)
        client.publish("tgn/tgn_modul_1/bulb",tgn_1_sate_14,qos=0,retain=True)
        client.publish("tgn/tgn_modul_1/temp",cach['temperature_10'],qos=0,retain=True)

def on_message(client, userdata, message):
    global t_temp
    global summertemp
    global temp_1
    global temp_3
    global temp_4
    global summermod
    global window_1_cach
    global thermostat_1_cach
    global thermostat_2_cach
    global thermostat_3_cach
    global thermostat_4_cach
    global thermostat_5_cach
    global door_1_cach
    global ir_botton
    global w_temp
    global valve_movement
    global motion_1_cach
    global light_1_cach
    global tgn_1_cach
    global tgn_1_sate_1
    global tgn_1_sate_14
    global light_2_cach
    global light_2_is
    if(message.topic=="tgn/thermostat/ligh_2_state"):
        light_2_is = message.payload.decode("utf-8")
    if(message.topic=="tgn/thermostat/valve_movement"):
        valve_movement = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/thermostat/sol_temp"):
        t_temp = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/weather/temp"):
        w_temp = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/thermostat/summer_temp"):
        summertemp = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/esp_1/temp/sensor_1"):
        temp_1 = float((message.payload.decode("utf-8")))
    if(message.topic=="tgn/pico_6/temp/sensor_1"):
        temp_3 = float((message.payload.decode("utf-8")))
    if(message.topic=="tgn/pico_5/temp/sensor_1"):
        temp_4 = float((message.payload.decode("utf-8")))
    if(message.topic=="tgn/thermostat/summer_mod"):
        summermod = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/air_conditioner/button"):
        ir_botton = (message.payload.decode("utf-8"))
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
    if(message.topic==thermostat_5_id):
        thermostat_5_cach = (message.payload.decode("utf-8"))
        decode_window(thermostat_5_cach,"5","thermostat")
    if(message.topic==light_2_id):
        light_2_cach = (message.payload.decode("utf-8"))
        decode_window(light_2_cach,"2","light")   
    if(message.topic==shelly_1_id):
        door_1_cach = (message.payload.decode("utf-8"))
        decode_window(door_1_cach,"1","door")
    if(message.topic==motion_1_id):
        motion_1_cach = (message.payload.decode("utf-8"))
        decode_window(motion_1_cach,"1","motion")
    if(message.topic==light_1_id):
        light_1_cach = (message.payload.decode("utf-8"))
        decode_window(light_1_cach,"1","light")
    if(message.topic==tgn_1_id):
        tgn_1_cach = (message.payload.decode("utf-8"))
        decode_window(tgn_1_cach,"1","tgn")
    if(message.topic=="tgn/tgn_modul_1/outlet_set"):
        msg = message.payload.decode("utf-8")
        if(msg != tgn_1_sate_1):
            client.publish(tgn_1_id+"/set",'{"state_1": "'+msg+'"}',qos=0,retain=True)
            tgn_1_sate_1 = msg
    if(message.topic=="tgn/tgn_modul_1/bulb_set"):
        msg = message.payload.decode("utf-8")
        if(msg != tgn_1_sate_14):
            client.publish(tgn_1_id+"/set",'{"state_14": "'+msg+'"}',qos=0,retain=True)
            tgn_1_sate_14 = msg
    

def main_prog():
    print("Start zigbee modul")
    global summermod_cach
    global window_1_stat
    global t_temp_cach
    global window_cach
    global cou
    global ir_botton
    global accuracy_cach
    global accuracy_mode
    global motion_1_stat
    global motion_1_is_cach
    global tim_cou
    global tim_state
    while True:
        client.on_message=on_message
        client.loop_start()
        client.subscribe([(zig_topic,0)])
        client.subscribe([(tgn_topic,0)])
        client.subscribe([(she_topic,0)])
        time.sleep(2)
        client.loop_stop()
        if ir_botton != ir_cach:
            print("send IR:"+ir_botton)
            if ir_botton == "power":
                client.publish("cmnd/tasmota_E3DAF4/IRSend",ir_power,qos=0,retain=True)
                time.sleep(1)
                client.publish("cmnd/tasmota_E3DAF4/IRSend",ir_empty,qos=0,retain=True)
            if ir_botton == "cool":
                client.publish("cmnd/tasmota_E3DAF4/IRSend",ir_cool,qos=0,retain=True)
                client.publish("tgn/air_conditioner/modus","cool_mode",qos=0,retain=True)
            if ir_botton == "fan":
                client.publish("cmnd/tasmota_E3DAF4/IRSend",ir_fan,qos=0,retain=True)
                client.publish("tgn/air_conditioner/modus","fan_mode",qos=0,retain=True)
            if ir_botton == "dry":
                client.publish("cmnd/tasmota_E3DAF4/IRSend",ir_dry,qos=0,retain=True)
                client.publish("tgn/air_conditioner/modus","dry_mode",qos=0,retain=True)
            if ir_botton == "up":
                client.publish("cmnd/tasmota_E3DAF4/IRSend",ir_up,qos=0,retain=True)
            if ir_botton == "down":
                client.publish("cmnd/tasmota_E3DAF4/IRSend",ir_down,qos=0,retain=True)
            ir_botton = ir_cach
            client.publish("tgn/air_conditioner/button",ir_cach,qos=0,retain=True)
        if valve_movement == "on" and summermod == "on":
            print("Valve moving")
            client.publish("tgn/battery_empty","Valve moving on",qos=0,retain=True)
            time.sleep(5)
            client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            client.publish(thermostat_2_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            client.publish(thermostat_3_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            client.publish(thermostat_4_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            #client.publish(thermostat_5_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            time.sleep(10)
            client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
            client.publish(thermostat_2_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
            client.publish(thermostat_3_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
            client.publish(thermostat_4_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
            #client.publish(thermostat_5_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
            time.sleep(10)
            client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            client.publish(thermostat_2_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            client.publish(thermostat_3_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            client.publish(thermostat_4_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            #client.publish(thermostat_5_id+"/set",'{"occupied_heating_setpoint": 35}',qos=0,retain=True)
            time.sleep(10)
            client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
            client.publish(thermostat_2_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
            client.publish(thermostat_3_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
            client.publish(thermostat_4_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
            #client.publish(thermostat_5_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
            client.publish("tgn/thermostat/valve_movement","off",qos=0,retain=True)
        elif valve_movement == "on" and summermod == "off":
            client.publish("tgn/thermostat/valve_movement","off",qos=0,retain=True)
        if summermod != summermod_cach or t_temp != t_temp_cach or window_1 != window_cach:
            if summermod == "on":
                summermod_cach = summermod
                client.publish("tgn/thermostat/sol_temp",summertemp,qos=0,retain=True)
                client.publish(thermostat_1_id+"/set",'{"system_mode": "off"}',qos=0,retain=True)
                client.publish(thermostat_2_id+"/set",'{"system_mode": "off"}',qos=0,retain=True)
                client.publish(thermostat_3_id+"/set",'{"system_mode": "off"}',qos=0,retain=True)
                client.publish(thermostat_4_id+"/set",'{"system_mode": "off"}',qos=0,retain=True)
                #client.publish(thermostat_5_id+"/set",'{"system_mode": "off"}',qos=0,retain=True)
            elif summermod == "off":
                summermod_cach = summermod
                window_cach = window_1
                client.publish("tgn/thermostat/sol_temp",t_temp,qos=0,retain=True)
                client.publish(thermostat_1_id+"/set",'{"system_mode": "heat"}',qos=0,retain=True)
                client.publish(thermostat_2_id+"/set",'{"system_mode": "heat"}',qos=0,retain=True)
                client.publish(thermostat_3_id+"/set",'{"system_mode": "heat"}',qos=0,retain=True)
                client.publish(thermostat_4_id+"/set",'{"system_mode": "heat"}',qos=0,retain=True)
                #client.publish(thermostat_5_id+"/set",'{"system_mode": "heat"}',qos=0,retain=True)
                if window_1 == "open":
                    logging_tgn("Window open","zigbee.log")
                    client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
                    client.publish(thermostat_2_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
                    client.publish(thermostat_3_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
                    client.publish(thermostat_4_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
                    #client.publish(thermostat_5_id+"/set",'{"occupied_heating_setpoint": 10}',qos=0,retain=True)
                elif window_1 == "closed":
                    logging_tgn("Window closed","zigbee.log")
                    t_temp_cach = t_temp
                    client.publish(thermostat_1_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
                    client.publish(thermostat_2_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
                    client.publish(thermostat_3_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
                    client.publish(thermostat_4_id+"/set",'{"occupied_heating_setpoint": '+str(float(t_temp)-0.0)+'}',qos=0,retain=True)
                    #client.publish(thermostat_5_id+"/set",'{"occupied_heating_setpoint": '+t_temp+'}',qos=0,retain=True)
        if float(t_temp) > temp_1:
            client.publish("tgn/thermostat/heater","On",qos=0,retain=True)
        else:
            client.publish("tgn/thermostat/heater","Off",qos=0,retain=True)
        battery_name = "Battery Ok"
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
        if int(battery_thermostat_5) < bat_low:
            battery_name ="thermostat_5"
        if int(battery_door_1) < bat_low:
            battery_name ="door_1"
        if int(battery_motion_1) < bat_low:
            battery_name ="Motion_1"
        if window_1 != window_1_stat:
            window_1_stat = window_1
            if window_1 == "closed":
                battery_name = "Window_1 closed"
            else:
                battery_name = "Window_1 open"
        print(battery_name)
        client.publish("tgn/battery_empty",battery_name,qos=0,retain=True)
        if cou == 30:
            if log == "on":
                logging_tgn("Radiator 1:"+status_thermostat_1+"|"+"Radiator 2:"+status_thermostat_2+"|"+"Radiator 3:"+status_thermostat_3+"|"+"Radiator 4:"+status_thermostat_4+"|","zigbee.log")
            ocor_1 = round(temp_1 - float(thermo_is_1),2)
            ocor_2 = round(temp_1 - float(thermo_is_2),2)
            ocor_3 = round(temp_3 - float(thermo_is_3),2)
            ocor_4 = round(temp_4 - float(thermo_is_4),2)
            #ocor_5 = round(temp_4 - float(thermo_is_4),2)
            if abs(ocor_1) >= 0.5:
                ocor_1 = float(thermo_cal_1 + ocor_1)
                print("T1:"+str(ocor_1))
                client.publish(thermostat_1_id+"/set",'{"local_temperature_calibration": '+str(ocor_1)+'}',qos=0,retain=True)
                time.sleep(0.3)
            if abs(ocor_2) >= 0.5:
                ocor_2 = float(thermo_cal_2 + ocor_2)
                print("T2:"+str(ocor_2))
                client.publish(thermostat_2_id+"/set",'{"local_temperature_calibration": '+str(ocor_2)+'}',qos=0,retain=True)
                time.sleep(0.3)
            if abs(ocor_3) >= 0.5:
                ocor_3 = float(thermo_cal_3 + ocor_3)
                print("T3:"+str(ocor_3))
                client.publish(thermostat_3_id+"/set",'{"local_temperature_calibration": '+str(ocor_3)+'}',qos=0,retain=True)
                time.sleep(0.3)
            if abs(ocor_4) >= 0.5:
                ocor_4 = float(thermo_cal_4 + ocor_4)
                print("T4:"+str(ocor_4))
                client.publish(thermostat_4_id+"/set",'{"local_temperature_calibration": '+str(ocor_4)+'}',qos=0,retain=True)
            #if abs(ocor_5) >= 0.5:
                #ocor_5 = float(thermo_cal_5 + ocor_4)
                #print("T4:"+str(ocor_5))
                #client.publish(thermostat_5_id+"/set",'{"local_temperature_calibration": '+str(ocor_5)+'}',qos=0,retain=True)
            cou = 0
        cou += 1
        print("Step:"+str(cou))
        if float(w_temp) <= 8.0:
            accuracy_mode = "0"
            client.publish("tgn/thermostat/accuracy","-0.5",qos=0,retain=True)
        else:
            accuracy_mode = "1"
            client.publish("tgn/thermostat/accuracy","-1",qos=0,retain=True)
        if accuracy_cach != accuracy_mode:
            accuracy_cach = accuracy_mode
            if accuracy_mode == "1":
                print("accuracy: -1")
                logging_tgn("accuracy:-1","zigbee.log")
                client.publish(thermostat_1_id+"/set",'{"temperature_accuracy": '+str("-1")+'}',qos=0,retain=True)
                client.publish(thermostat_2_id+"/set",'{"temperature_accuracy": '+str("-1")+'}',qos=0,retain=True)
                client.publish(thermostat_3_id+"/set",'{"temperature_accuracy": '+str("-1")+'}',qos=0,retain=True)
                client.publish(thermostat_4_id+"/set",'{"temperature_accuracy": '+str("-1")+'}',qos=0,retain=True)
                #client.publish(thermostat_5_id+"/set",'{"temperature_accuracy": '+str("-1")+'}',qos=0,retain=True)
            elif accuracy_mode == "0":
                print("accuracy: -0,5")
                logging_tgn("accuracy:-0.5","zigbee.log")
                client.publish(thermostat_1_id+"/set",'{"temperature_accuracy": '+str("-0.5")+'}',qos=0,retain=True)
                client.publish(thermostat_2_id+"/set",'{"temperature_accuracy": '+str("-0.5")+'}',qos=0,retain=True)
                client.publish(thermostat_3_id+"/set",'{"temperature_accuracy": '+str("-0.5")+'}',qos=0,retain=True)
                client.publish(thermostat_4_id+"/set",'{"temperature_accuracy": '+str("-0.5")+'}',qos=0,retain=True)
                #client.publish(thermostat_5_id+"/set",'{"temperature_accuracy": '+str("-0.5")+'}',qos=0,retain=True)
        #light mode
        if motion_1_ilu == "dim" and motion_1_activ == True and motion_1_stat == "off":
            print("light on")
            logging_tgn("Motion_1_Light_on","zigbee.log")
            client.publish(light_1_id+"/set",'{"state": "ON"}',qos=0,retain=True)
            motion_1_stat = "on"
        elif motion_1_stat == "on" and motion_1_activ == False:
            print("Light off")
            logging_tgn("Motion_1_Light_off","zigbee.log")
            client.publish(light_1_id+"/set",'{"state": "OFF"}',qos=0,retain=True)
            motion_1_stat = "off"
        if motion_1_ilu == "dim" and motion_1_activ == True and light_2_is == "OFF" and motion_1_is_cach == "off":
            print("timer on")
            tim_state = "on"
            motion_1_is_cach = "on"
            client.publish(light_2_id+"/set",'{"state": "ON"}',qos=0,retain=True)
        if motion_1_ilu == "dim" and motion_1_activ == True and light_2_is == "ON" and motion_1_is_cach == "off":
            print("timer off")
            tim_state = "off"
            tim_cou = 0
            motion_1_is_cach = "on"
            client.publish(light_2_id+"/set",'{"state": "OFF"}',qos=0,retain=True)
        if motion_1_activ == False:
            motion_1_is_cach = "off"
        if tim_state == "on":
            if tim_cou == tim_sol:
                print("timer")
                tim_state = "off"
                tim_cou = 0
                client.publish(light_2_id+"/set",'{"state": "OFF"}',qos=0,retain=True)
            tim_cou += 1
ini()
main_prog()
            