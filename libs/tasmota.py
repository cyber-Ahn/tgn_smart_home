import paho.mqtt.client as mqtt
import sys
from tgnLIB import logging_tgn
import time

data_ip = []
socket_ip = ""

if __name__ == "__main__":
    print("python3 tgn_sonoff.py modulnumber channel status ip")

def tasmota(modul, channel, status, mqtt_ip):
    try:
        print(">>Load tasmota.config")
        f = open("/home/pi/tgn_smart_home/config/tasmota.config","r")
    except IOError:
        print("cannot open tasmota.config.... file not found")
    else:
        global data_ip
        for line in f:
            data_ip.append(line)
    if status == "1":
        status = "ON"
    elif status == "0":
        status = "OFF"
    print("send")
    socket_ip = data_ip[(int(modul)-1)].rstrip()
    if channel == "0":
        socket_ip = "cmnd/tasmota_"+socket_ip+"/POWER"
    else:
        socket_ip = "cmnd/tasmota_"+socket_ip+"/POWER"+channel
    data_send = status + " - " + mqtt_ip  + " - " + socket_ip + " - " + modul
    print(data_send)
    logging_tgn("topic:"+socket_ip+";modul:"+modul+";channel:"+channel+";status:"+status+";mqtt_ip:"+mqtt_ip,"tasmota.log")
    client = mqtt.Client("tasmota Modul")
    client.connect(mqtt_ip)
    client.loop_start()
    client.publish(socket_ip,status,qos=0,retain=True)
    time.sleep(1)

logging_tgn("check_files","tasmota.log")
i_modul = sys.argv[1]
i_channel = sys.argv[2]
i_status = sys.argv[3]
i_ip = sys.argv[4]
tasmota(i_modul,i_channel,i_status,i_ip)