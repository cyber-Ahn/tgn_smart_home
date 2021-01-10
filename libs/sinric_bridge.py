from sinric import Sinric
from tgnLIB import get_ip
import paho.mqtt.client as mqtt

apiKey = "xxxx"
device =    ["xxx",
            "5ffac866ab25b36ddb57fb48",
            "5ffac873ab25b36ddb57fb4c",
            "5ffac8a5ab25b36ddb57fb54",
            "5ffac8c5ab25b36ddb57fb58",
            "5ffac8eeab25b36ddb57fb5e",
            "5ffac90aab25b36ddb57fb62"]
sateOp = ["OFF","ON"]

def power_state(deviceId, state):
    deviceNum = device.index(deviceId)
    stateNum = sateOp.index(state)
    client = mqtt.Client("sinric_bridge")
    client.connect(get_ip())
    topic = "tgn/buttons/status/"+str(deviceNum)
    client.publish(topic,str(stateNum),qos=0,retain=True)

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
    print(apiKey)
    ob = Sinric(apiKey, callbacks)
    ob.handle()