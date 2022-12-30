import sys
import ShellyPy
from tgnLIB import logging_tgn, get_ip
import time
import paho.mqtt.client as mqtt
import urllib.request
import requests
import json

modul_num = int(sys.argv[1])
modul_status = sys.argv[2]
data_ip = []
socket_ip = ""

def ini():
    try:
        print(">>Load ip_socket_list.config")
        f = open("/home/pi/tgn_smart_home/config/ip_socket_list.config","r")
    except IOError:
        print("cannot open ip_socket_list.config.... file not found")
    else:
        global data_ip
        for line in f:
            data_ip.append(line)
    set_socket()

def format_mac(input):
    output = ""
    for char in range(0, len(input), 2):
        output += input[char] + input[char + 1]
        if char != len(input) - 2:
            output += ":"
    return output

def set_socket():
    client = mqtt.Client("kasa_bridge")
    client.connect(get_ip())
    if(modul_status != "info"):
        print("Set socket " + str(modul_num) + " to " + modul_status)
        socket_ip = data_ip[(modul_num-1)].rstrip()

        logging_tgn("modul:"+str(modul_num)+";IP:"+socket_ip+";status:"+modul_status,"shelly.log")

        try:
            device = ShellyPy.Shelly(socket_ip)
            if modul_status == "1":
                print("Turn on")
                device.relay(0, turn=True)
                client.publish("tgn/android/pmsg","Shelly "+str(modul_num)+" On",qos=0,retain=True)
            else:
                print("Turn off")
                device.relay(0, turn=False)
                client.publish("tgn/android/pmsg","Shelly "+str(modul_num)+" Off",qos=0,retain=True)
        except:
            print("Shelly "+str(modul_num)+" not Online")
    if(modul_status == "info"):
        socket_ip = data_ip[(modul_num-1)].rstrip()
        print("Read Data from: " + socket_ip)
        get_url= urllib.request.urlopen("http://"+socket_ip)
        print("Response Status: "+ str(get_url.getcode()))
        if(str(get_url.getcode()) == "200"):
            print("Status ok")
            cach = requests.get('http://'+socket_ip+'/status').content
            #print(cach.decode("UTF8"))
            t_cach = json.loads(cach.decode("UTF8"))
            ssid = t_cach['wifi_sta']['ssid']
            ip = t_cach['wifi_sta']['ip']
            rssi = str(t_cach['wifi_sta']['rssi'])
            mac = format_mac(t_cach['mac'])
            status = str(t_cach['relays'][0]['ison'])
            if(status == "True"):
                status = "On"
            else:
                status = "Off"
            uptime = str(t_cach['uptime'])
            power = str(t_cach['meters'][0]['power'])
            out_info = ssid +"|"+ ip +"|"+ rssi +"|"+ mac +"|"+ status +"|"+ uptime +"|"+ power
            print("---------------------------------------------------------------------------------------------------------------------")
            print(out_info)
            print("---------------------------------------------------------------------------------------------------------------------")
            client.publish("tgn/shelly/info/"+ip+"/ssid",ssid,qos=0,retain=True)
            time.sleep(0.5)
            client.publish("tgn/shelly/info/"+ip+"/rssi",rssi,qos=0,retain=True)
            time.sleep(0.5)
            client.publish("tgn/shelly/info/"+ip+"/mac",mac,qos=0,retain=True)
            time.sleep(0.5)
            client.publish("tgn/shelly/info/"+ip+"/status",status,qos=0,retain=True)
            time.sleep(0.5)
            client.publish("tgn/shelly/info/"+ip+"/uptime",uptime,qos=0,retain=True)
            time.sleep(0.5)
            client.publish("tgn/shelly/info/"+ip+"/power",power,qos=0,retain=True)

ini()