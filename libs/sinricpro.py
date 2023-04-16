from sinric import SinricPro 
import asyncio
from tgnLIB import logging_tgn, read_eeprom, get_ip, decode
import paho.mqtt.client as mqtt
# test
device = []
ROM_ADDRESS = 0x00
sateOp = ["Off","On"]
APP_KEY = 'xxx'
APP_SECRET = 'xxx'

try:
    f_d = open("/home/pi/tgn_smart_home/config/i2c.config","r")
    for line in f_d:
        if "ROM_ADDRESS" in line:
            ROM_ADDRESS = int(line.rstrip().split("*")[1],16)
except IOError:
    print("cannot open i2c.config.... file not found")

def power_state(device_id, state):
    client = mqtt.Client("sinric_bridge")
    client.connect(get_ip())
    logging_tgn("device:"+device_id+";Power_State:"+state,"sinric.log")
    deviceNum = (device.index(device_id)+1)
    stateNum = sateOp.index(state)
    print(deviceNum)
    print(stateNum)
    if(deviceNum <= 9):
        topic = "tgn/buttons/status/"+str(deviceNum)
        client.publish(topic,str(stateNum),qos=0,retain=True)
    #elif for more devices
    return True, state
callbacks = {'powerState': power_state}
if __name__ == '__main__':
    try:
        print(">>Load system.config")
        f_d = open("/home/pi/tgn_smart_home/config/system.config","r")
        count_d = 0
        cach_a = ""
        for line in f_d:
            count_d = count_d + 1
            if count_d == 13:
                cach_a = line.rstrip().split(":")[1]
                device = cach_a.split(",")
            if count_d == 25:
                APP_SECRET = decode(line.rstrip().split(":")[1])
    except IOError:
        print("cannot open system.config.... file not found")
    start_add_S = 0x01
    index = 0
    APP_KEY = ""
    while index < 40:
        cach = read_eeprom(1,ROM_ADDRESS,0x03,start_add_S)
        if cach != "X":
            APP_KEY = APP_KEY + cach
        index = index + 1
        start_add_S = start_add_S + 1
    print(APP_KEY)
    print(APP_SECRET)
    for x in range(len(device)):
        print(device[x])
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, device, callbacks, enable_log=False, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())