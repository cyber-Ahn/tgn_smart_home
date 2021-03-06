import sys
import paho.mqtt.client as mqtt
from tgnLIB import get_ip, logging_tgn
from subprocess import call

logging_tgn("check_files","ha_bridge.log")
c1 = sys.argv[1]
c2 = int(sys.argv[2])

if __name__ == "__main__":
    print("python3 ha_bridge_com.py command/modulnumber status")

client = mqtt.Client("HA Brigde Com")
client.connect(get_ip())
if c1 == "shutdown":
	client.publish("tgn/system/shutdown","1",qos=0,retain=True)
elif c1 == "reboot":
	client.publish("tgn/system/reboot","1",qos=0,retain=True)
else:
	modul = "tgn/buttons/status/"+c1
	client.publish(modul,c2,qos=0,retain=True)
logging_tgn("command/modul:"+c1+";status:"+str(c2),"ha_bridge.log")