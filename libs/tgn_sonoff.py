import paho.mqtt.client as mqtt
import sys
from tgnLIB import get_ip, logging_tgn, decode

sonoff_homecode = "00000"
sonoff_topic = "tgn/sonoff/data"

try:
    f_d = open("/home/pi/tgn_smart_home/config/system.config","r")
    for line in f_d:
        if "sonoff_homecode" in line:
            sonoff_homecode = decode(line.rstrip().split("*")[1])
except IOError:
    print("cannot open system.config.... file not found")

if __name__ == "__main__":
    print("python3 tgn_sonoff.py modulnumber channel status ip")

def tgn_sonoff(topic, homecode, modul, channel, status, mqtt_ip):
    logging_tgn("topic:"+topic+";modul:"+modul+";channel:"+channel+";status:"+status+";mqtt_ip:"+mqtt_ip,"sonoff.log")
    print("send")
    client = mqtt.Client("sonoff Modul")
    client.connect(mqtt_ip)
    client.loop_start()
    data_send = homecode + "-" + modul + "." + channel + "-" + status
    print(data_send)
    client.publish(topic,data_send,qos=0,retain=True)

logging_tgn("check_files","sonoff.log")
i_modul = sys.argv[1]
i_channel = sys.argv[2]
i_status = sys.argv[3]
i_ip = sys.argv[4]
tgn_sonoff(sonoff_topic,sonoff_homecode,i_modul,i_channel,i_status,i_ip)

#python3 tgn_sonoff.py 1 0 1 192.168.0.98
#python3 tgn_sonoff.py modul channel on/off mqtt-ip