import os
import paho.mqtt.client as mqtt
import platform
import psutil
import socket
import sys
from datetime import datetime

def bytes_to_GB(bytes):
    gb = bytes/(1024*1024*1024)
    gb = round(gb, 2)
    return gb

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

#connect mqtt
client = mqtt.Client("TGN Smart Info")
client.connect(get_ip())
client.loop_start()
#send status to mqtt
client.publish("tgn/info/status","connected",qos=0,retain=True)
print("[+] Architecture :", platform.architecture()[0])
client.publish("tgn/info/architecture",platform.architecture()[0],qos=0,retain=True)
print("[+] Operating System Release : " + platform.system() + " " +platform.release())
client.publish("tgn/info/release",platform.system() + " " +platform.release(),qos=0,retain=True)
print("[+] Node :", platform.node())
client.publish("tgn/info/node",platform.node(),qos=0,retain=True)
with open("/proc/cpuinfo", "r") as f:
    file_info = f.readlines()
cpuinfo = [x.strip().split(":")[1] for x in file_info if "Model" in x]
for index, item in enumerate(cpuinfo):
    print("[+] Model : " + item)
    client.publish("tgn/info/model",item,qos=0,retain=True)
print("[+] Platform :", platform.platform())
client.publish("tgn/info/platform",platform.platform(),qos=0,retain=True)
boot_time = datetime.fromtimestamp(psutil.boot_time())
print("[+] System Boot Time :", boot_time)
client.publish("tgn/info/boot-time",str(boot_time),qos=0,retain=True)
pids = []
for subdir in os.listdir('/proc'):
    if subdir.isdigit():
        pids.append(subdir)
print('[+] Total number of processes : {0}'.format(len(pids)))
client.publish("tgn/info/processes",format(len(pids)),qos=0,retain=True)
print("[+] Python " + sys.version)
client.publish("tgn/info/python","Python " + sys.version,qos=0,retain=True)
#mqtt version
virtual_memory = psutil.virtual_memory()
print("[+] Total Memory present :", bytes_to_GB(virtual_memory.total), "Gb")
print("[+] Total Memory Available :", bytes_to_GB(virtual_memory.available), "Gb")
print("[+] Total Memory Used :", bytes_to_GB(virtual_memory.used), "Gb")
print("[+] Percentage Used :", virtual_memory.percent, "%")
client.publish("tgn/info/memory/present",str(bytes_to_GB(virtual_memory.total))+"Gb",qos=0,retain=True)
client.publish("tgn/info/memory/available",str(bytes_to_GB(virtual_memory.available))+"Gb",qos=0,retain=True)
client.publish("tgn/info/memory/used",str(bytes_to_GB(virtual_memory.used))+"Gb",qos=0,retain=True)
client.publish("tgn/info/memory/precent",str(virtual_memory.percent)+"%",qos=0,retain=True)
disk_partitions = psutil.disk_partitions()
for partition in disk_partitions:
    if partition.device == '/dev/root':
        print("[+] Partition Device : ", partition.device)
        print("[+] File System : ", partition.fstype)
        disk_usage = psutil.disk_usage(partition.mountpoint)
        print("[+] Total Disk Space :", bytes_to_GB(disk_usage.total), "GB")
        print("[+] Free Disk Space :", bytes_to_GB(disk_usage.free), "GB")
        print("[+] Used Disk Space :", bytes_to_GB(disk_usage.used), "GB")
        print("[+] Percentage Used :", disk_usage.percent, "%")
    client.publish("tgn/info/disk/device",partition.device,qos=0,retain=True)
    client.publish("tgn/info/disk/file-sys",partition.fstype,qos=0,retain=True)
    client.publish("tgn/info/disk/total",str(bytes_to_GB(disk_usage.total))+"Gb",qos=0,retain=True)
    client.publish("tgn/info/disk/free",str(bytes_to_GB(disk_usage.free))+"Gb",qos=0,retain=True)
    client.publish("tgn/info/disk/used",str(bytes_to_GB(disk_usage.used))+"Gb",qos=0,retain=True)
    client.publish("tgn/info/disk/precent",str(disk_usage.percent)+"%",qos=0,retain=True)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        if interface_name == 'eth0':
            client.publish("tgn/info/network/name",interface_name,qos=0,retain=True)
            print(f"[+] Interface :", interface_name)
            if str(address.family) == 'AddressFamily.AF_INET':
                print("[+] IP Address :", address.address)
                print("[+] Netmask :", address.netmask)
                print("[+] Broadcast IP :", address.broadcast)
                client.publish("tgn/info/network/ip",address.address,qos=0,retain=True)
                client.publish("tgn/info/network/netmask",address.netmask,qos=0,retain=True)
                client.publish("tgn/info/network/broadcast",address.broadcast,qos=0,retain=True)
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                client.publish("tgn/info/network/mac",address.address,qos=0,retain=True)
                print("[+] MAC Address :", address.address)