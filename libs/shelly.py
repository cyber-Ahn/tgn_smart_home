import sys
import ShellyPy
from tgnLIB import logging_tgn

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

def set_socket():
    print("Set socket " + str(modul_num) + " to " + modul_status)
    socket_ip = data_ip[(modul_num-1)].rstrip()

    logging_tgn("modul:"+str(modul_num)+";IP:"+socket_ip+";status:"+modul_status,"shelly.log")

    device = ShellyPy.Shelly(socket_ip)
    if modul_status == "1":
        print("Turn on")
        device.relay(0, turn=True)
    else:
        print("Turn off")
        device.relay(0, turn=False)

ini()