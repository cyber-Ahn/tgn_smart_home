import sys
from pyHS100 import Discover
from pyHS100 import SmartPlug
from time import sleep
from tgnLIB import logging_tgn, get_ip
from pprint import pformat as pf
import paho.mqtt.client as mqtt

modul_num = int(sys.argv[1])
modul_status = sys.argv[2]
data_ip = []
socket_ip = ""

def ini():
    try:
        print(">>Load ip_socket_list.config")
        f = open("/home/pi/tgn_smart_home/config/ip_socket_list.config","r")
    except IOError:
        print("cannot open themes.config.... file not found")
    else:
        global data_ip
        for line in f:
            data_ip.append(line)
    set_socket()

def scann():
    for plug in Discover.discover().values():
        print("-----------------------")
        print("Alias: %s" % plug.alias)
        print("Host: %s" % plug.host)
        print("Current state: %s" % plug.state)
        print("Current time: %s" % plug.time)
        print("Timezone: %s" % plug.timezone)
        print("Location: %s" % plug.location)

def set_socket():
    print("Set socket " + str(modul_num) + " to " + modul_status)
    socket_ip = data_ip[(modul_num-1)].rstrip()
    client = mqtt.Client("kasa_bridge")
    client.connect(get_ip())

    logging_tgn("modul:"+str(modul_num)+";IP:"+socket_ip+";status:"+modul_status,"kasa.log")

    plug = SmartPlug(socket_ip)
    if modul_status == "info":
        print("Hardware: %s" % pf(plug.hw_info))
    elif modul_status == "fullinfo":
        print("Full sysinfo: %s" % pf(plug.get_sysinfo()))
    elif modul_status == "emeter":
        if plug.has_emeter:
            power = str(round(float(plug.current_consumption()), 2))+" W"
            voltage = str(round(float(str(plug.get_emeter_realtime()).split("'voltage_mv': ")[1].split(",")[0])/1000, 2))+" V"
            total = str(round(float(str(plug.get_emeter_daily()).split("28: ")[1].split(",")[0]), 2))+" kWh"
            print(str(socket_ip))
            print(power)
            print(voltage)
            print(total)
            client.publish("tgn/hs100/"+str(socket_ip)+"/power",power,qos=0,retain=True)
            sleep(0.5)
            client.publish("tgn/hs100/"+str(socket_ip)+"/voltage",voltage,qos=0,retain=True)
            sleep(0.5)
            client.publish("tgn/hs100/"+str(socket_ip)+"/total",total,qos=0,retain=True)
        else:
            print("No Emeter")
    elif modul_status == "1":
        try:
            print("Turn on")
            plug.turn_on()
            client.publish("tgn/android/pmsg","Kasa "+str(modul_num)+" On",qos=0,retain=True)
        except:
            client.publish("tgn/android/pmsg","Kasa "+str(modul_num)+" not Online",qos=0,retain=True)
    else:
        try:
            print("Turn off")
            plug.turn_off()
            client.publish("tgn/android/pmsg","Kasa "+str(modul_num)+" Off",qos=0,retain=True)
        except:
            client.publish("tgn/android/pmsg","Kasa "+str(modul_num)+" not Online",qos=0,retain=True)
ini()