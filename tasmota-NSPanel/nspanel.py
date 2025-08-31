import json
import paho.mqtt.client as mqtt
import time
from tgnLIB import get_ip,pcf8563ReadTime

req_topic = "tele/#"
tgn_topic = "tgn/#"

client = mqtt.Client("tasmot-nspanel")
client.connect(get_ip())
panel_status = "Offline"
tasmo_id = "123456"
data_nc = []
temp = "11"
hum = "11"
bt1 = "off"
bt2 = "off"
bt3 = "off"
bt4 = "off"
bt5 = "off"
bt6 = "off"
bt7 = "off"
bn1 = "empty"
bn2 = "empty"
bn3 = "empty"
bn4 = "empty"
bn5 = "empty"
bn6 = "empty"
bn7 = "empty"
tasmo_result = "empty"
esp_col = "0.0.0.255"
esp_br = "0"
w_temp = "0"
w_temp_min = "0"
w_temp_max = "0"
t_temp = "22"

try:
    print(">>Load panel.config")
    f = open("/home/pi/tgn_smart_home/tasmota-NSPanel/panel.config","r")
except IOError:
    print("cannot open panel.config.... file not found")
else:
    for line in f:
        data_nc.append(line)
tasmo_id = "tasmota_"+data_nc[0].rstrip()
print("NSPanel ID: "+tasmo_id)

def ini():
    if(panel_status == "Offline"):
        print("Setup Display")
        time.sleep(10)
        client.publish("cmnd/"+tasmo_id+"/NSPLocation","Cologne",qos=0,retain=True)
        time.sleep(1)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_wallpaper":1}',qos=0,retain=True)
        time.sleep(1)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_dimOpen":0}',qos=0,retain=True)
        time.sleep(1)
        for i in range(8):
            client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"index":'+str(i+1)+',"type":"delete"}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_resources":[{"index":8,"ctype":"device","id":"8","uiid":33}]}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_resources":[{"index":1,"ctype":"group","id":"1","uiid":1}]}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_resources":[{"index":2,"ctype":"group","id":"2","uiid":1}]}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_resources":[{"index":3,"ctype":"group","id":"3","uiid":1}]}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_resources":[{"index":4,"ctype":"group","id":"4","uiid":1}]}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_resources":[{"index":5,"ctype":"group","id":"5","uiid":1}]}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_resources":[{"index":6,"ctype":"group","id":"6","uiid":1}]}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_resources":[{"index":7,"ctype":"group","id":"7","uiid":1}]}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"temperature":'+temp+',"humidity":'+hum+'}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_weather":30,"HMI_outdoorTemp":{"current":'+w_temp+',"range":"-3,8"}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"ATCEnable":1,"ATCMode":0}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"ATCMode":0,"ATCExpect0":'+t_temp+'}',qos=0,retain=True)
        print("end Setup Display")
        set_clock()

def set_clock():    
        current_time = pcf8563ReadTime()
        weekday = str(current_time).split(" ")[0]
        year = str(current_time).split(" ")[2].split("/")[0]
        mon = str(current_time).split(" ")[2].split("/")[1]
        if(mon != "10"):
            mon = str(current_time).split(" ")[2].split("/")[1].replace("0", "")
        day = str(current_time).split(" ")[2].split("/")[2]
        if(day != "10" and day != "20" and day != "30"):
            day = str(current_time).split(" ")[2].split("/")[2].replace("0", "")
        hour = str(current_time).split(" ")[3].split(":")[0]
        if(hour == "00"):
            hour = "0"
        elif(hour != "10" and hour != "20"):
            hour = str(current_time).split(" ")[3].split(":")[0].replace("0", "")
        min = str(current_time).split(" ")[3].split(":")[1]
        if(min == "00"):
            min = "0"
        elif(min != "10" and min != "20" and min != "30" and min != "40" and min != "50"):    
            min = str(current_time).split(" ")[3].split(":")[1].replace("0", "")
        days = ["x","Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        day_num = str(days.index(weekday))
        #print(weekday)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"year":'+year+',"mon":'+mon+',"day":'+day+',"hour":'+hour+',"min":'+min+',"week":'+day_num+'}',qos=0,retain=True)

def on_message(client, userdata, message):
	
    global panel_status
    global temp
    global hum
    global bt1
    global bt2
    global bt3
    global bt4
    global bt5
    global bt6
    global bt7
    global tasmo_result
    global esp_col
    global esp_br
    global w_temp
    global w_temp_min
    global w_temp_max
    global t_temp
    global bn1
    global bn2
    global bn3
    global bn4
    global bn5
    global bn6
    global bn7
    if(message.topic=="tele/"+tasmo_id+"/LWT"):
        panel_status = (message.payload.decode("utf-8"))
        ini()
    if(message.topic=="tgn/esp_1/temp/sensor_1"):
        temp = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/esp_1/temp/sensor_2"):
        hum = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/buttons/status/1"):
        bt1 = (message.payload.decode("utf-8"))
        if bt1 == "1": bt1 = "on" 
        elif bt1 == "0": bt1 = "off"
    if(message.topic=="tgn/buttons/status/2"):
        bt2 = (message.payload.decode("utf-8"))
        if bt2 == "1": bt2 = "on" 
        elif bt2 == "0": bt2 = "off"
    if(message.topic=="tgn/buttons/status/3"):
        bt3 = (message.payload.decode("utf-8"))
        if bt3 == "1": bt3 = "on" 
        elif bt3 == "0": bt3 = "off"
    if(message.topic=="tgn/buttons/status/4"):
        bt4 = (message.payload.decode("utf-8"))
        if bt4 == "1": bt4 = "on" 
        elif bt4 == "0": bt4 = "off"
    if(message.topic=="tgn/buttons/status/5"):
        bt5 = (message.payload.decode("utf-8"))
        if bt5 == "1": bt5 = "on" 
        elif bt5 == "0": bt5 = "off"
    if(message.topic=="tgn/buttons/status/6"):
        bt6 = (message.payload.decode("utf-8"))
        if bt6 == "1": bt6 = "on" 
        elif bt6 == "0": bt6 = "off"
    if(message.topic=="tgn/buttons/status/7"):
        bt7 = (message.payload.decode("utf-8"))
        if bt7 == "1": bt7 = "on" 
        elif bt7 == "0": bt7 = "off"
    if(message.topic=="tgn/buttons/name/1"):
        bn1 = (message.payload.decode("utf-8")).split("_")[1]
    if(message.topic=="tgn/buttons/name/2"):
        bn2 = (message.payload.decode("utf-8")).split("_")[1]
    if(message.topic=="tgn/buttons/name/3"):
        bn3 = (message.payload.decode("utf-8")).split("_")[1]
    if(message.topic=="tgn/buttons/name/4"):
        bn4 = (message.payload.decode("utf-8")).split("_")[1]
    if(message.topic=="tgn/buttons/name/5"):
        bn5 = (message.payload.decode("utf-8")).split("_")[1]
    if(message.topic=="tgn/buttons/name/6"):
        bn6 = (message.payload.decode("utf-8")).split("_")[1]
    if(message.topic=="tgn/buttons/name/7"):
        bn7 = (message.payload.decode("utf-8")).split("_")[1]
    if(message.topic=="tgn/esp_3/neopixel/color"):
        esp_col = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/esp_3/neopixel/brightness"):
        esp_br = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/weather/temp"):
        w_temp = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/weather/temp_min"):
        w_temp_min = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/weather/temp_max"):
        w_temp_max = (message.payload.decode("utf-8"))
    if(message.topic=="tgn/thermostat/sol_temp"):
        t_temp = (message.payload.decode("utf-8"))
    if(message.topic=="tele/"+tasmo_id+"/RESULT"):
        tasmo_result = (message.payload.decode("utf-8"))
        decode_result(tasmo_result)

def decode_result(data_res):
    print(data_res)
    cach = json.loads(data_res)
    try:
        tasmo_num = cach['NSPanel']['id']
        type = cach['NSPanel']['ctype']
    except:
        type = "device"
        tasmo_num = "x"
    try:
        atc = str(cach['NSPanel']['ATCMode'])
    except:
        atc = "1"
    if type == "group":
        tasmo_stat = cach['NSPanel']['params']['switch']
        if tasmo_stat == "on": tasmo_stat = "1"
        elif tasmo_stat == "off": tasmo_stat = "0"
        print(type+" - "+tasmo_num+" - "+tasmo_stat)
        client.publish("tgn/buttons/status/"+tasmo_num,tasmo_stat,qos=0,retain=True)
    elif tasmo_num == "8":
        try:
            bright = cach['NSPanel']['params']['bright']
            bright_r = str(int((int(bright)/100)*255))
            client.publish("tgn/esp_3/neopixel/brightness",bright_r,qos=0,retain=True)
        except:
            print("")
        try:
            red = cach['NSPanel']['params']['colorR']
            green = cach['NSPanel']['params']['colorG']
            blue = cach['NSPanel']['params']['colorB']
            colo = str(red)+"."+str(green)+"."+str(blue)+".255"
            client.publish("tgn/esp_3/neopixel/color",colo,qos=0,retain=True)
        except:
            print("")
        try:
            stat_rgb = cach['NSPanel']['params']['switch']
            if stat_rgb == "off":
                col = "0.0.0.255"
            elif stat_rgb == "on":
                col = "255.255.255.255"
            client.publish("tgn/esp_3/neopixel/color",col,qos=0,retain=True)
        except:
            print("")       
    elif atc == "0":
        t_cach = str(cach['NSPanel']['ATCExpect0'])
        if t_temp != t_cach:
            print("Set Sol_Temp: "+t_cach)
            client.publish("tgn/thermostat/sol_temp",t_cach,qos=0,retain=True)
     

def main_prog():
    while True:
        client.on_message=on_message
        client.loop_start()
        client.subscribe([(req_topic,0)])
        client.subscribe([(tgn_topic,0)])
        time.sleep(2)
        client.loop_stop()
        time.sleep(5)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"temperature":'+temp+',"humidity":'+hum+'}',qos=0,retain=True)
        client.publish("tgn/thermostat/is_temp",temp,qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"1","name":"'+bn1+'","params":{"switch":"'+bt1+'"}}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"2","name":"'+bn2+'","params":{"switch":"'+bt2+'"}}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"3","name":"'+bn3+'","params":{"switch":"'+bt3+'"}}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"4","name":"'+bn4+'","params":{"switch":"'+bt4+'"}}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"5","name":"'+bn5+'","params":{"switch":"'+bt5+'"}}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"6","name":"'+bn6+'","params":{"switch":"'+bt6+'"}}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"7","name":"'+bn7+'","params":{"switch":"'+bt7+'"}}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"8","name":"RGB"}}',qos=0,retain=True)
        if esp_col == "0.0.0.255":
            client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"8","params":{"switch":"off"}}}',qos=0,retain=True)
        else:
            cach_col = esp_col.split(".")
            client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"8","params":{"switch":"on"}}}',qos=0,retain=True)
            client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"8","params":{"light_type":1,"colorR":'+cach_col[0]+',"colorG":'+cach_col[1]+',"colorB":'+cach_col[2]+'}}}',qos=0,retain=True)
        esp_br_r = str((int(esp_br)/255)*100)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"relation":{"id":"8","params":{"light_type":1,"bright":'+esp_br_r+'}}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"HMI_weather":30,"HMI_outdoorTemp":{"current":'+w_temp+',"range":"'+w_temp_min+','+w_temp_max+'"}}',qos=0,retain=True)
        client.publish("cmnd/"+tasmo_id+"/NSPSend",'{"ATCMode":0,"ATCExpect0":'+t_temp+'}',qos=0,retain=True)
        set_clock()
        
ini()
main_prog()
