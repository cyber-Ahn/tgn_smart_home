import paho.mqtt.client as mqtt
import string
import secrets
from tgnLIB import decode, get_ip
import time
import shutil
import openpyxl
import subprocess
import os

d_out = {"API_TGN":"ok"}
phat_data = "/home/pi/tgn_smart_home/log/"
file_name = "room_data.log"

class api:
    def __init__(self):
        print("Api request")
    
    def add_dict(top_d, data_d):
        cach = top_d.split("/")
        num = len(cach)
        if num == 5:
            if cach[1] in d_out and cach[2] in d_out[cach[1]]: 
                d_out[cach[1]][cach[2]][cach[3]].update({cach[4]: data_d})
            elif cach[1] in d_out and cach[2] in d_out[cach[1]]: 
                d_out[cach[1]][cach[2]].update({cach[3]:{cach[4]: data_d}})
            elif cach[1] in d_out:
                d_out[cach[1]].update({cach[2]:{cach[3]:{cach[4]: data_d}}})
            else: 
                d_out.update({cach[1]:{cach[2]:{cach[3]:{cach[4]: data_d}}}})
        elif num == 4:
            if cach[1] in d_out and cach[2] in d_out[cach[1]]: d_out[cach[1]][cach[2]].update({cach[3]: data_d})
            elif cach[1] in d_out: d_out[cach[1]].update({cach[2]:{cach[3]: data_d}})
            else: d_out.update({cach[1]:{cach[2]:{cach[3]: data_d}}})
        elif num == 3:
            if cach[1] in d_out: d_out[cach[1]].update({cach[2]: data_d})
            else: d_out.update({cach[1]:{cach[2]: data_d}})
        else:
            d_out.update({cach[1]: data_d})
    
    def on_message(client, userdata, message):
        api.add_dict(message.topic, message.payload.decode("utf-8"))

    def read_data(data):
        data_cach = []
        data_cach.append(data.get("key"))
        uidd = data_cach[0]
        data_read = []
        try:
            f_d = open("/home/pi/tgn_smart_home/tgn-api/api.db","r")
            for line in f_d:
                data_read.append(line.rstrip())
            f_d.close()
            if( uidd in data_read):
                client = mqtt.Client("TGN Smart Home")
                client.connect(get_ip())
                client.on_message=api.on_message
                client.loop_start()
                client.subscribe([("tgn/#",0)])
                time.sleep(2)
                client.loop_stop()
                return(d_out)
        except IOError:
            return("cannot open api.db.... file not found - Please start master_key.py")

    def decode_data(data):
        data_cach = []
        data_cach.append(data.get("key"))
        data_cach.append(data.get("opt"))
        data_cach.append(data.get("butnr"))
        data_cach.append(data.get("stat"))
        uidd = data_cach[0]
        data_read = []
        read = []
        try:
            f_d = open("/home/pi/tgn_smart_home/tgn-api/api.db","r")
            for line in f_d:
                data_read.append(line.rstrip())
            f_d.close()
            if( uidd in data_read):
                if(data_cach[1] == "button"):
                    client = mqtt.Client("TGN API")
                    client.connect(get_ip())
                    client.loop_start()
                    client.publish("tgn/buttons/status/"+data_cach[2],data_cach[3],qos=0,retain=True)
                    client.loop_stop()
                    return("Button "+ data_cach[2]+ " set to "+ data_cach[3])
                elif(data_cach[1] == "IrAirConditioner"):
                    try:
                        fd = open("/home/pi/tgn_smart_home/config/system.config","r")
                        for line in fd:
                            read.append(line.rstrip())
                        fd.close()
                        ir_topic = read[42-1].split("*")[1]
                        if(data_cach[2] == "power"):
                            com = read[36-1].split("*")[1]
                            com2 = read[43-1].split("*")[1]
                            client = mqtt.Client("TGN API")
                            client.connect(get_ip())
                            client.loop_start()
                            client.publish(ir_topic,com,qos=0,retain=True)
                            time.sleep(1)
                            client.publish(ir_topic,com2,qos=0,retain=True)
                            client.loop_stop()
                            return("Air Conditioner: "+data_cach[2])
                        elif(data_cach[2] == "fan"):
                            com = read[37-1].split("*")[1]
                            client = mqtt.Client("TGN API")
                            client.connect(get_ip())
                            client.loop_start()
                            client.publish(ir_topic,com,qos=0,retain=True)
                            client.loop_stop()
                            return("Air Conditioner: "+data_cach[2])
                        elif(data_cach[2] == "cool"):
                            com = read[38-1].split("*")[1]
                            client = mqtt.Client("TGN API")
                            client.connect(get_ip())
                            client.loop_start()
                            client.publish(ir_topic,com,qos=0,retain=True)
                            client.loop_stop()
                            return("Air Conditioner: "+data_cach[2])
                        elif(data_cach[2] == "dry"):
                            com = read[39-1].split("*")[1]
                            client = mqtt.Client("TGN API")
                            client.connect(get_ip())
                            client.loop_start()
                            client.publish(ir_topic,com,qos=0,retain=True)
                            client.loop_stop()
                            return("Air Conditioner: "+data_cach[2])
                        elif(data_cach[2] == "up"):
                            com = read[40-1].split("*")[1]
                            client = mqtt.Client("TGN API")
                            client.connect(get_ip())
                            client.loop_start()
                            client.publish(ir_topic,com,qos=0,retain=True)
                            time.sleep(1)
                            client.publish(ir_topic,com,qos=0,retain=True)
                            client.loop_stop()
                            return("Air Conditioner: "+data_cach[2])
                        elif(data_cach[2] == "down"):
                            com = read[41-1].split("*")[1]
                            client = mqtt.Client("TGN API")
                            client.connect(get_ip())
                            client.loop_start()
                            client.publish(ir_topic,com,qos=0,retain=True)
                            time.sleep(1)
                            client.publish(ir_topic,com,qos=0,retain=True)
                            client.loop_stop()
                            return("Air Conditioner: "+data_cach[2])
                        else:
                            return("command not foend")
                    except IOError:
                        return("cannot open system.config")
                elif(data_cach[1] == "RPiPshutdown"):
                    client = mqtt.Client("TGN API")
                    client.connect(get_ip())
                    client.loop_start()
                    client.publish("tgn/pico/shutdown","1",qos=0,retain=True)
                    client.loop_stop()
                    return("shutdown RPIP")
                else:
                    return("command is not supported!")
            else:
                return("Key not accepted")
        except IOError:
            return("cannot open api.db.... file not found - Please start master_key.py")

    def gen_key(data):
        data_read = []
        try:
            f_d = open("/home/pi/tgn_smart_home/tgn-api/api.db","r")
            for line in f_d:
                data_read.append(line.rstrip())
            f_d.close()
            key_cach = decode(data_read[0])
            if(data == key_cach):
                alphabet = string.ascii_letters + string.digits
                uidd = ''.join(secrets.choice(alphabet) for i in range(24))
                f = open("/home/pi/tgn_smart_home/tgn-api/api.db", "a")
                f.write("\n"+uidd)
                f.close()
                return("key accepted - New User_key: " + uidd)
            else:
                return("key not accepted")
                
        except IOError:
            return("cannot open api.db.... file not found - Please start master_key.py")