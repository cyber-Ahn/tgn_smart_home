from sinric import Sinric
from tgnLIB import get_ip, logging_tgn
from time import sleep
from subprocess import call
import paho.mqtt.client as mqtt

apiKey = "xxxx"
device =    ["xxx",
            "5ffac866ab25b36ddb57fb48",
            "5ffac873ab25b36ddb57fb4c",
            "5ffac8a5ab25b36ddb57fb54",
            "5ffac8c5ab25b36ddb57fb58",
            "5ffac8eeab25b36ddb57fb5e",
            "5ffac90aab25b36ddb57fb62",
            "",
            "",
            "",
            "5ffb5d48ab25b36ddb58135e",
            "5ffb60ecab25b36ddb581440",
            "5ffb6161ab25b36ddb581456",
            "60008edeab25b36ddb58e373"]
sateOp = ["OFF","ON"]

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
            client.publish("tgn/buttons/status/6","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/5","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/4","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/3","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/2","1",qos=0,retain=True)
            sleep(6.0)
            client.publish("tgn/buttons/status/1","1",qos=0,retain=True)
            sleep(6.0)

callbacks = {"setPowerState": power_state}
if __name__ == "__main__":
    try:
        print(">>Load system.config")
        f_d = open("/home/pi/tgn_smart_home/config/system.config","r")
        count_d = 0
        for line in f_d:
            count_d = count_d + 1
            if count_d == 13:
                global apiKey
                apiKey = line.rstrip()
    except IOError:
        print("cannot open system.config.... file not found")
    logging_tgn("check_files","sinric.log")
    ob = Sinric(apiKey, callbacks)
    ob.handle()