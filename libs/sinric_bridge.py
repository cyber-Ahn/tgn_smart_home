from sinric import Sinric
from tgnLIB import get_ip, logging_tgn, read_eeprom
from time import sleep
from subprocess import call
import paho.mqtt.client as mqtt

apiKey = "xxxx"
device =    []
sateOp = ["OFF","ON"]
ROM_ADDRESS = 0x53

def power_state(deviceId, state):
    logging_tgn("device:"+deviceId+";Power_State:"+state,"sinric.log")
    deviceNum = device.index(deviceId)
    stateNum = sateOp.index(state)
    client = mqtt.Client("sinric_bridge")
    client.connect(get_ip())
    if(deviceNum <= 9):
        topic = "tgn/buttons/status/"+str(deviceNum)
        client.publish(topic,str(stateNum),qos=0,retain=True)
    elif(deviceNum == 10):
        if(stateNum == 1):
            topic = "tgn/esp_3/neopixel/color"
            client.publish(topic,"248.1.255.255",qos=0,retain=True)
            topic = "tgn/esp_3/neopixel/brightness"
            client.publish(topic,"15",qos=0,retain=True)
        elif(stateNum == 0):
            topic = "tgn/esp_3/neopixel/color"
            client.publish(topic,"0.0.0.255",qos=0,retain=True)
            topic = "tgn/esp_3/neopixel/brightness"
            client.publish(topic,"10",qos=0,retain=True)
    elif(deviceNum == 11):
        call(['reboot', '-h', 'now'], shell=False)
    elif(deviceNum == 12):
        call(['shutdown', '-h', 'now'], shell=False)
    elif(deviceNum == 13):
        if(stateNum == 1):
            client.publish("tgn/buttons/status/1","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/2","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/3","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/4","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/5","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/6","1",qos=0,retain=True)
            sleep(6.0)
        elif(stateNum == 0):
            client.publish("tgn/buttons/status/6","0",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/5","0",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/4","0",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/3","0",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/2","0",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/1","0",qos=0,retain=True)
            sleep(6.0)
    elif(deviceNum == 14):
        if(stateNum == 1):
            topic = "tgn/esp_4/color"
            client.publish(topic,"0.0.0.255",qos=0,retain=True)
        elif(stateNum == 0):
            topic = "tgn/esp_4/color"
            client.publish(topic,"0.0.0.1",qos=0,retain=True)
    elif(deviceNum == 15):
        if(stateNum == 1):
            topic = "tgn/esp_4/color"
            client.publish(topic,"248.1.255.1",qos=0,retain=True)
        elif(stateNum == 0):
            topic = "tgn/esp_4/color"
            client.publish(topic,"0.0.0.255",qos=0,retain=True)
    elif(deviceNum == 16):
        topic = "MQTChroma/GameMode"
        client.publish(topic,"1",qos=0,retain=True)
        topic = "tgn/buttons/status/4"
        client.publish(topic,"0",qos=0,retain=True)
        sleep(6.0)
        topic = "tgn/esp_4/color"
        client.publish(topic,"0.255.0.1",qos=0,retain=True)
        sleep(6.0)
        topic = "tgn/esp_3/neopixel/color"
        client.publish(topic,"0.255.0.1",qos=0,retain=True)
    elif(deviceNum == 17):
        topic = "MQTChroma/GameMode"
        client.publish(topic,"0",qos=0,retain=True)
        topic = "tgn/buttons/status/4"
        client.publish(topic,"0",qos=0,retain=True)
        sleep(6.0)
        topic = "tgn/esp_4/color"
        client.publish(topic,"248.1.255.1",qos=0,retain=True)
        sleep(6.0)
        topic = "tgn/esp_3/neopixel/color"
        client.publish(topic,"248.1.255.1",qos=0,retain=True)
    elif(deviceNum == 18):
        topic = "MQTChroma/GameMode"
        client.publish(topic,"0",qos=0,retain=True)
        topic = "tgn/esp_4/color"
        client.publish(topic,"0.0.0.1",qos=0,retain=True)
        sleep(6.0)
        topic = "tgn/esp_3/neopixel/color"
        client.publish(topic,"0.0.0.255",qos=0,retain=True)
        sleep(6.0)
        topic = "tgn/buttons/status/4"
        client.publish(topic,"1",qos=0,retain=True)

        

callbacks = {"setPowerState": power_state}
if __name__ == "__main__":
    try:
        print(">>Load system.config")
        f_d = open("/home/pi/tgn_smart_home/config/system.config","r")
        count_d = 0
        cach_a = ""
        for line in f_d:
            count_d = count_d + 1
            if count_d == 13:
                cach_a = line.rstrip()
        device = cach_a.split(",")
    except IOError:
        print("cannot open system.config.... file not found")
    start_add_S = 0x01
    index = 0
    global apiKey
    apiKey = ""
    while index < 40:
        cach = read_eeprom(1,ROM_ADDRESS,0x03,start_add_S)
        if cach != "X":
            apiKey = apiKey + cach
        index = index + 1
        start_add_S = start_add_S + 1
    print(apiKey)
    print("------------------------------------------------------------------------------------")
    print(device)
    print("------------------------------------------------------------------------------------")
    logging_tgn("check_files","sinric.log")
    ob = Sinric(apiKey, callbacks)
    ob.handle()