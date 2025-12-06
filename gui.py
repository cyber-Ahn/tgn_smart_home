from tgnLIB import *
import paho.mqtt.client as mqtt
import binascii
import json
import PIL
import thingspeak
from subprocess import call
from multiprocessing import Process
from tkinter import *
from PIL import Image, ImageTk
from tkinter.colorchooser import *
from mcstatus import MinecraftServer

colorSet = 9
REMOTE_SERVER = "www.google.com"
main_topic = "tgn/#"
phat = "/home/pi/tgn_smart_home/icons/"
NFC_ADDRESS = 0x24
bn1 = "x1"
bn2 = "x2"
bn3 = "x3"
bn4 = "x4"
bn5 = "x5"
bn6 = "x6"
bn7 = "x7"
bn8 = "x8"
bn9 = "x9"
b1 = 0
b2 = 0
b3 = 0
b4 = 0
b5 = 0
b6 = 0
b7 = 0
b8 = 0
b9 = 0
ond = "yes"
pushbulletkey = "1234567890"
openweatherkey = "1234567890"
zipcode = 1234567
rssurl = ""
ttiv = 50000
textswitch = ""

screen = 0
spr_phat = ""
spr = "de"
menu_on = 0
version = "V.1.8"
ontime = "10:19|10:21"
offtime = "10:20|10:22"
onoff_day = ["Mon","Tue","Wed","Thu","Fri","xxx","xxx"]
alarm_s = "off"
alarm_t = "17:30"
s1 = "0"
s2 = "0"
s3 = "0"
s4 = "0"
buttons = ["1", "2", "3", "4", "5", "6","7","8","9"]
button_width_a = 13
button_width_b = 9
speech = 0
slider_length = 480
feed_pos_x = 450
feed_pos_y = 20
rssfeed = "no feed"
font_size_a = 14
font_size_b = 16
font_size_c = 20
feed_size_width = 453
feed_size_height = 40
power_air = ""
bground = "black"
fground = "green"
abground = "gray"
afground = "black"
afbground = "black"
buttona = "red"
buttonb = "black"
#ESP8622/1
esp_temp = "0.02"
esp_hum = "1.1"
esp_rssi = "--"
esp_li = "100"
#ESP8622/2
esp_temp_2 = "0.05"
esp_rssi_2 = "--"
esp_li_2 = "100"
esp_b1_2 = "off"


def on_message(client, userdata, message):
	global screen
	global spr
	global menu_on
	global version
	global ontime
	global offtime
	global onoff_day
	global alarm_s
	global alarm_t
	global s1
	global s2
	global s3
	global s4
	global button_width_a
	global button_width_b
	global speech
	global slider_length
	global buttons
	global bn1
	global bn2
	global bn3
	global bn4
	global bn5
	global bn6
	global bn7
	global bn8
	global bn9
	global b1 
	global b2
	global b3
	global b4
	global b5
	global b6
	global b7
	global b8
	global b9
	global feed_pos_x
	global feed_pos_y
	global font_size_a
	global font_size_b
	global font_size_c
	global feed_size_width
	global feed_size_height
	global power_air
	global esp_temp
	global esp_hum
	global esp_rssi
	global esp_li
	global esp_temp_2
	global esp_rssi_2
	global esp_li_2
	global esp_b1_2
	global bground
	global fground
	global abground
	global afground
	global afbground
	global buttona
	global buttonb

	if(message.topic=="tgn/gui/screen"):
		screen = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/spr"):
		spr = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/menu_on"):
		menu_on = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/sversion"):
		version = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/ontime"):
		ontime = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/offtime"):
		offtime = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/onoff_day"):
		onoff_day_cach = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/alarm_s"):
		alarm_s = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/alarm_t"):
		alarm_t = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/s1"):
		s1 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/s2"):
		s2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/s3"):
		s3 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/s4"):
		s4 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/button_width_a"):
		button_width_a = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/button_width_b"):
		button_width_b = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/speech"):
		speech = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/slider_length"):
		slider_length = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/name/1"):
		bn1 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/name/2"):
		bn2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/name/3"):
		bn3 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/name/4"):
		bn4 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/name/5"):
		bn5 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/name/6"):
		bn6 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/name/7"):
		bn7 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/name/8"):
		bn8 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/name/9"):
		bn9 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/1"):
		b1 = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/2"):
		b2 = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/3"):
		b3 = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/4"):
		b4 = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/5"):
		b5 = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/6"):
		b6 = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/7"):
		b7 = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/8"):
		b8 = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/9"):
		b9 = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/feed_pos_x"):
		feed_pos_x = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/feed_pos_y"):
		feed_pos_x = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/feed_size_width"):
		feed_size_width = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/feed_size_height"):
		feed_size_height = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/font_size_a"):
		font_size_a = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/font_size_b"):
		font_size_b = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/font_size_c"):
		font_size_c = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/air_conditioner/power"):
		power_air = int(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_1/temp/sensor_1"):
		esp_temp = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_1/temp/sensor_2"):
		esp_hum = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_1/wifi/rssi"):
		esp_rssi = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_1/analog/sensor_1"):
		esp_li = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/temp/sensor_1"):
		esp_temp_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/wifi/rssi"):
		esp_rssi_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/analog/sensor_1"):
		esp_li_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/button/b1"):
		esp_b1_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/bground"):
		bground = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/fground"):
		fground = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/abground"):
		abground = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/bafground"):
		afground = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/afbground "):
		afbground  = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/buttona"):
		buttona = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/gui/buttonb"):
		buttonb = str(message.payload.decode("utf-8"))

	onoff_day = []
	onoff_day_cach = onoff_day_cach.split("['")[1].split("']")[0]
	onoff_day.append(onoff_day_cach.split("', '")[0])
	onoff_day.append(onoff_day_cach.split("', '")[1])
	onoff_day.append(onoff_day_cach.split("', '")[2])
	onoff_day.append(onoff_day_cach.split("', '")[3])
	onoff_day.append(onoff_day_cach.split("', '")[4])
	onoff_day.append(onoff_day_cach.split("', '")[5])
	onoff_day.append(onoff_day_cach.split("', '")[6])

def ini(): 
	global spr_phat
	global buttons
	global pushbulletkey
	global rssurl
	global openweatherkey
	global zipcode
	spr_phat="/home/pi/tgn_smart_home/language/"+spr+"/"
	print(spr_phat)
	buttons = []
	buttons.append(bn1)
	buttons.append(bn2)
	buttons.append(bn3)
	buttons.append(bn4)
	buttons.append(bn5)
	buttons.append(bn6)
	buttons.append(bn7)
	buttons.append(bn8)
	buttons.append(bn9)
	start_add_U = 0xcf
	index = 0
	pushbulletkey = ""
	while index < 34:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_U)
		print(">>Read Byte "+str(start_add_U))
		if cach != "#":
			pushbulletkey = pushbulletkey + cach
		index = index + 1
		start_add_U = start_add_U + 1
	print(pushbulletkey)
	start_add_AG = 0x04
	index = 0
	while index < 60:
		cach = read_eeprom(1,ROM_ADDRESS,0x02,start_add_AG)
		print(">>Read Byte "+str(start_add_AG))
		if cach != "#":
			rssurl = rssurl + cach
		index = index + 1
		start_add_AG = start_add_AG + 1
		logging_tgn(rssurl,"tgn_smart_home.log")
	print(rssurl)
	start_add_T = 0xaf
	index = 0
	openweatherkey = ""
	while index < 32:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_T)
		print(">>Read Byte "+str(start_add_T))
		if cach != "#":
			openweatherkey = openweatherkey + cach
		index = index + 1
		start_add_T = start_add_T + 1
	start_add_S = 0xa7
	index = 0
	zipcode = ""
	while index < 7:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_S)
		print(">>Read Byte "+str(start_add_S))
		if cach != "X":
			zipcode = zipcode + cach
		index = index + 1
		start_add_S = start_add_S + 1

def callback8():
	logging_tgn("setRTC","tgn_smart_home.log")
	setRTC()
	time.sleep(5)
def callback41():
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback47():
	print("callback")
	#client.publish("tgn/esp_32_cam/record","2",qos=0,retain=True)
def callback45():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py backup"
	os.system(setn)
def callback46():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py restore"
	os.system(setn)
def callback30():
	if ifI2C(NFC_ADDRESS) == "found device":
		pn532 = Pn532_i2c()
		pn532.SAMconfigure()
		card_data = pn532.read_mifare().get_data()
		card_data = str(binascii.hexlify(card_data))
		file = open("/home/pi/tgn_smart_home/config/logfile.log","r")
		lines = file.readlines()
		file.close()
		for line in lines:
			cach = line
			cachB=cach.split("|")
			if cachB[0]==card_data:
				cachC=cachB[2]
				cachC=cachC.rstrip()
				if cachC == "b'59577873583239750a'":
					all_on()
				if cachC == "b'595778735832396d5a673d3d0a'":
					all_off()
				if cachC == "b'5a58687064413d3d0a'":
					exit()
				if cachC == "b'63326831644752766432343d0a'":
					call(['shutdown', '-h', 'now'], shell=False)
def callback39():
	global alarm_s
	if alarm_s == "on":
		alarm_s = "off"
	elif alarm_s == "off":
		alarm_s = "on"
	start_add_AC = 0x57
	index = 0
	while index < 3:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AC,"X")
		index = index + 1
		start_add_AC = start_add_AC + 1
	start_add_AC = 0x57
	index = 0 
	while index < len(alarm_s):
		letter = alarm_s[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AC,letter)
		index = index + 1
		start_add_AC = start_add_AC + 1
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback25():
	print("callback")
def callback32():
	global speech
	logging_tgn("switchLanguage","tgn_smart_home.log")
	if speech == 0:
		speech = 1
	elif speech == 1:
		speech = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0xf2,str(speech))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback34():
	global Ts
	if Ts == 0:
		Ts = 1
	elif Ts == 1:
		Ts = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0xf3,str(Ts))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback48():
	print("callback")
def auto_clock():
	global ond
	if ond == "yes":
		ond = "no"
	elif ond == "no":
		ond = "yes"
def callback19():
	logging_tgn("switchScreen","tgn_smart_home.log")
	global screen
	if screen == 1:
		screen = 0
	else:
		screen = 1
	write_eeprom(1,ROM_ADDRESS,0x00,0x67,str(screen))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback17():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py rtc"
	logging_tgn("settingsRTC","tgn_smart_home.log")
	os.system(setn)
def callback18():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py funk"
	logging_tgn("settingsFUNK","tgn_smart_home.log")
	os.system(setn)
def callback23():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py cam"
	os.system(setn)
def callback26():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py weather"
	os.system(setn)
def callback27():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py pushb"
	os.system(setn)
def callback35():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py thinkspeak"
	os.system(setn)
def callback38():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py alarm"
	os.system(setn)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback42():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py rss"
	os.system(setn)
def callback22():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py install_rom"
	logging_tgn("installRom","tgn_smart_home.log")
	os.system(setn)
def callback28():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py save_nfc"
	os.system(setn)
def callback29():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py remove_nfc"
	os.system(setn)
def callback31():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py show_nfc"
	os.system(setn)
def callback44():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/update.py"
	logging_tgn("checkUpdate","tgn_smart_home.log")
	os.system(setn)
	time.sleep(5)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback9():
	if b1 == 0:
		msg = "Turn on " + buttons[0]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/1","1",qos=0,retain=True)
	else:
		msg = "Turn off " + buttons[0]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/1","0",qos=0,retain=True)
def callback10():
	if b2 == 0:
		msg = "Turn on " + buttons[1]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/2","1",qos=0,retain=True)
	else:
		msg = "Turn off " + buttons[1]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/2","0",qos=0,retain=True)
def callback11():
	if b3 == 0:
		msg = "Turn on " + buttons[2]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/3","1",qos=0,retain=True)
	else:
		msg = "Turn off " + buttons[2]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/3","0",qos=0,retain=True)
def callback12():
	if b4 == 0:
		msg = "Turn on " + buttons[3]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/4","1",qos=0,retain=True)
	else:
		msg = "Turn off " + buttons[3]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/4","0",qos=0,retain=True)
def callback13():
	if b5 == 0:
		msg = "Turn on " + buttons[4]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/5","1",qos=0,retain=True)
	else:
		msg = "Turn off " + buttons[4]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/5","0",qos=0,retain=True)
def callback14():
	if b6 == 0:
		msg = "Turn on " + buttons[5]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/6","1",qos=0,retain=True)
	else:
		msg = "Turn off " + buttons[5]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/6","0",qos=0,retain=True)
def callback914():
	if b7 == 0:
		msg = "Turn on " + buttons[6]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/7","1",qos=0,retain=True)
	else:
		msg = "Turn off " + buttons[6]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/7","0",qos=0,retain=True)
def callback915():
	if b8 == 0:
		msg = "Turn on " + buttons[7]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/8","1",qos=0,retain=True)
	else:
		msg = "Turn off " + buttons[7]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/8","0",qos=0,retain=True)
def callback916():
	if b9 == 0:
		msg = "Turn on " + buttons[8]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/9","1",qos=0,retain=True)
	else:
		msg = "Turn off " + buttons[8]
		pb_send_text(pushbulletkey,msg)
		client.publish("tgn/buttons/status/9","0",qos=0,retain=True)
def callback6():
	stream()
def callback15():
	logging_tgn("Shutdown","tgn_smart_home.log")
	call(['shutdown', '-h', 'now'], shell=False)
def callback16():
	logging_tgn("Reboot","tgn_smart_home.log")
	call(['reboot', '-h', 'now'], shell=False)
def callback43():
	print("callback")
def callback100():
	print("empty button")
def callback110():
	Process(target=webplayer).start()
def callback20():
	print("callback")
def callback21():
	print("callback")
def callback40():
	print("callback")
#-------------------------------
def menu_toggle():
	global menu_on
	if menu_on == 0:
		menu_on = 1
		print("menu on")
		write_eeprom(1,ROM_ADDRESS,0x03,0x2b,str(menu_on))
		callback41()
	elif menu_on == 1:
		menu_on = 0
		print("menu off")
		write_eeprom(1,ROM_ADDRESS,0x03,0x2b,str(menu_on))
		callback41()
def red_neo():
	client.publish("tgn/esp_3/neopixel/color","255.0.0.255",qos=0,retain=True)
def green_neo():
	client.publish("tgn/esp_3/neopixel/color","0.255.0.255",qos=0,retain=True)
def blue_neo():
	client.publish("tgn/esp_3/neopixel/color","0.0.255.255",qos=0,retain=True)
def off_neo():
	client.publish("tgn/esp_3/neopixel/color","0.0.0.255",qos=0,retain=True)
def set_neo():
	client.publish("tgn/esp_3/neopixel/brightness",str(SL1.get()),qos=0,retain=True)
def color_neo():
	color = askcolor()
	cach1 = str(color).split('),')
	cach2 = cach1[0].split('(', 2)
	cach3 = cach2[2].split(', ')
	c_x = cach3[0].split('.')
	c_y = cach3[1].split('.')
	c_z = cach3[2].split('.')
	color_set = c_x[0]+"."+c_y[0]+"."+c_z[0]
	client.publish("tgn/esp_3/neopixel/color",color_set,qos=0,retain=True)
def all_off():
	logging_tgn("allOff","tgn_smart_home.log")
	subprocess.call('xset dpms force on', shell=True)
	msg = "all off"
	pb_send_text(pushbulletkey,msg)
	client.publish("tgn/buttons/status/9","0",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/8","0",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/7","0",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/6","0",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/5","0",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/4","0",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/3","0",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/2","0",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/1","0",qos=0,retain=True)
def all_on():
	logging_tgn("allOn","tgn_smart_home.log")
	subprocess.call('xset dpms force on', shell=True)
	msg = "all on"
	pb_send_text(pushbulletkey,msg)
	client.publish("tgn/buttons/status/1","1",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/2","1",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/3","1",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/4","1",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/5","1",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/6","1",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/7","1",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/8","1",qos=0,retain=True)
	time.sleep(6.0)
	client.publish("tgn/buttons/status/9","1",qos=0,retain=True)
	time.sleep(1)
def air_switch():
	global power_air
	if power_air == "on":
		power_air = "off"
	elif power_air == "off":
		power_air = "on"
	client.publish("tgn/air_conditioner/power",power_air,qos=0,retain=True)
def clearLOG():
	print("Clear Logs")
	setn = "rm -fr /home/pi/tgn_smart_home/log/sinric.log"
	os.system(setn)
	setn = "rm -fr /home/pi/tgn_smart_home/log/sonoff.log"
	os.system(setn)
	setn = "rm -fr /home/pi/tgn_smart_home/log/tgn_smart_home.log"
	os.system(setn)
	setn = "rm -fr /home/pi/tgn_smart_home/log/kasa.log"
	os.system(setn)
	setn = "rm -fr /home/pi/tgn_smart_home/log/shelly.log"
	os.system(setn)
	setn = "rm -fr /home/pi/tgn_smart_home/log/radiator.log"
	os.system(setn)
	setn = "rm -fr /home/pi/tgn_smart_home/log/room_data.log"
	os.system(setn)
	setn = "rm -fr /home/pi/tgn_smart_home/log/tasmota.log"
	os.system(setn)
def About():
	print("TGN Smart Home "+version)
def spt1():
	spr = "de"
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(1))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt2():
	spr = "en"
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(2))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt3():
	spr = "fr"
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(3))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt4():
	spr = "ru"
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(4))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt5():
	spr = "ja"
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(5))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt6():
	spr = "zh"
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(6))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)

def remove_var(name_b_c):
	if "s_" in name_b_c or "p_" in name_b_c or "y_" in name_b_c or "t_" in name_b_c :
		name_b_c = name_b_c.split("_")[1]
	return name_b_c

def webplayer():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/mediaplayer.py"
	os.system(setn)

def lcars_screen_20():
	print("Load LCARS")
	root = Tk()
	#fullscreen mode
	WMWIDTH, WMHEIGHT, WMLEFT, WMTOP = root.winfo_screenwidth(), root.winfo_screenheight(), 0, 0
	root.overrideredirect(screen) 
	root.geometry("%dx%d+%d+%d" % (WMWIDTH, WMHEIGHT, WMLEFT, WMTOP))

	try:
		f = open(spr_phat+"text.lang","r")
	except IOError:
		print("cannot open text.lang.... file not found")
	else:
		data = []
		for line in f:
			data.append(line)
			
	root.wm_title("TGN Smart Home "+version+" ("+spr+")")
	root.config(background = '#000000')
	if menu_on == 1:
		menu = Menu(root)
		root.config(menu=menu)

		filemenu = Menu(menu)
		menubar = Menu(root, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		filemenu = Menu(menubar, tearoff=0, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		menu.add_cascade(label=(data[37].rstrip()), menu=filemenu)
		filemenu.add_command(label=(data[38].rstrip()), command=callback8)
		filemenu.add_separator()
		filemenu.add_command(label=(data[132].rstrip()), command=callback41)
		filemenu.add_command(label=(data[133].rstrip()), command=callback47)
		filemenu.add_command(label=(data[134].rstrip()), command=callback45)
		filemenu.add_command(label=(data[135].rstrip()), command=callback46)
		filemenu.add_command(label=(data[40].rstrip()), command=callback30)

		setmenu = Menu(menu)
		menubar = Menu(root, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		setmenu = Menu(menubar, tearoff=0, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		menu.add_cascade(label=(data[41].rstrip()), menu=setmenu)
		setmenu.add_command(label=(data[115].rstrip()), command=callback39)
		setmenu.add_command(label=(data[42].rstrip()), command=callback25)
		setmenu.add_command(label=(data[43].rstrip()), command=callback32)
		setmenu.add_command(label=(data[44].rstrip()), command=callback34)
		setmenu.add_command(label=(data[130].rstrip()), command=callback48)
		setmenu.add_command(label=(data[131].rstrip()), command=auto_clock)

		langmenu = Menu(menu)
		menubar = Menu(root, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		langmenu = Menu(menubar, tearoff=0, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		setmenu.add_cascade(label=(data[45].rstrip()), menu=langmenu)
		langmenu.add_command(label="de", command=spt1)
		langmenu.add_command(label="en", command=spt2)
		langmenu.add_command(label="fr", command=spt3)
		langmenu.add_command(label="ru", command=spt4)
		langmenu.add_command(label="jp", command=spt5)
		langmenu.add_command(label="zh", command=spt6)

		stylemenu = Menu(menu)
		menubar = Menu(root, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		stylemenu = Menu(menubar, tearoff=0, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		setmenu.add_cascade(label=(data[46].rstrip()), menu=stylemenu)
		stylemenu.add_command(label=(data[47].rstrip()), command=callback19)

		colmenu = Menu(menu)
		menubar = Menu(root, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		colmenu = Menu(menubar, tearoff=0, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		stylemenu.add_cascade(label=(data[48].rstrip()), menu=colmenu)
		try:
			f = open("/home/pi/tgn_smart_home/config/themes.config","r")
		except IOError:
			print("cannot open themes.config.... file not found")
		else:
			data_ca = []
			color_button = [] 
			for line in f:
				data_ca.append(line)
			cou = 0
			for x in data_ca:
				index = data_ca[cou].find("#")
				if index == 0:
					bu_cach = data_ca[cou].rstrip()
					bu_cach = bu_cach[1:]
					color_button.append(bu_cach) 
				cou = cou + 1
			color_button.append("LCARS")
			color_button.append("ioBrocker")
		index_bu = len(color_button)
		if index_bu >= 1:    
			colmenu.add_command(label=color_button[0], command=lambda: key(1,color_button[0]))
		if index_bu >= 2:    
			colmenu.add_command(label=color_button[1], command=lambda: key(2,color_button[1]))
		if index_bu >= 3:    
			colmenu.add_command(label=color_button[2], command=lambda: key(3,color_button[2]))
		if index_bu >= 4:    
			colmenu.add_command(label=color_button[3], command=lambda: key(4,color_button[3]))
		if index_bu >= 5:    
			colmenu.add_command(label=color_button[4], command=lambda: key(5,color_button[4]))
		if index_bu >= 6:    
			colmenu.add_command(label=color_button[5], command=lambda: key(6,color_button[5]))
		if index_bu >= 7:    
			colmenu.add_command(label=color_button[6], command=lambda: key(7,color_button[6]))
		if index_bu >= 8:    
			colmenu.add_command(label=color_button[7], command=lambda: key(8,color_button[7]))
		if index_bu >= 9:    
			colmenu.add_command(label=color_button[8], command=lambda: key(9,color_button[8]))
		def key(method,but_name):
			global colorSet
			colorSet = method
			if but_name == "LCARS":
				colorSet = 9
			if but_name == "ioBrocker":
				colorSet = 0
			write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
			time.sleep(1)
			os.execv(sys.executable, ['python3'] + sys.argv)

		rommenu = Menu(menu)
		menubar = Menu(root, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		rommenu = Menu(menubar, tearoff=0, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		setmenu.add_cascade(label=(data[55].rstrip()), menu=rommenu)
		rommenu.add_command(label=(data[56].rstrip()), command=callback17)
		rommenu.add_command(label=(data[57].rstrip()), command=callback18)
		rommenu.add_command(label=(data[58].rstrip()), command=callback23)
		rommenu.add_command(label=(data[59].rstrip()), command=callback26)
		rommenu.add_command(label=(data[60].rstrip()), command=callback27)
		rommenu.add_command(label=(data[61].rstrip()), command=callback35)
		rommenu.add_command(label=(data[113].rstrip()), command=callback38)
		rommenu.add_command(label=(data[119].rstrip()), command=callback42)
		rommenu.add_command(label=(data[62].rstrip()), command=callback22)

		nfcmenu = Menu(menu)
		menubar = Menu(root, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		nfcmenu = Menu(menubar, tearoff=0, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		setmenu.add_cascade(label=(data[63].rstrip()), menu=nfcmenu)
		nfcmenu.add_command(label=(data[64].rstrip()), command=callback28)
		nfcmenu.add_command(label=(data[65].rstrip()), command=callback29)
		nfcmenu.add_command(label=(data[66].rstrip()), command=callback31)

		helpmenu = Menu(menu)
		menubar = Menu(root, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		helpmenu = Menu(menubar, tearoff=0, background='#4b87ff', foreground='#000000',activebackground='#fdaa30', activeforeground='#000000')
		menu.add_cascade(label=(data[67].rstrip()), menu=helpmenu)
		helpmenu.add_command(label=(data[139].rstrip()), command=clearLOG)
		helpmenu.add_command(label=(data[140].rstrip()), command=callback44)
		helpmenu.add_command(label=(data[68].rstrip()), command=About)

	image1 = ImageTk.PhotoImage(Image.open('/home/pi/tgn_smart_home/icons/a_lcars.jpg'))
	label1 = Label(root, image=image1)
	label1.place(x = 0,y = 0)

	app1=Window_1_lcars(root)
	app1.place(x = 735,y = 6)

	app2=Window_2_lcars(root)
	app2.place(x = 210,y = 115)

	app3=Window_3_lcars(root)
	app3.place(x = 342,y = 80)

	infLabel1 = Label(root, text=(data[11].rstrip()))
	infLabel1.configure(bg = '#000000',fg ='#4b87ff')
	infLabel1.place(x = 360,y = 450)
	oText1 = (data[12].rstrip())+ontime
	infLabel2 = Label(root, text=oText1)
	infLabel2.configure(bg = '#000000',fg ='#4b87ff')
	infLabel2.place(x = 210,y = 470)
	oText1 = (data[13].rstrip())+offtime
	infLabel3 = Label(root, text=oText1)
	infLabel3.configure(bg = '#000000',fg ='#4b87ff')
	infLabel3.place(x = 360,y = 470)
	oText1 = (data[14].rstrip())+s1+s2+s3+s4
	infLabel3 = Label(root, text=oText1)
	infLabel3.configure(bg = '#000000',fg ='#4b87ff')
	infLabel3.place(x = 480,y = 470)
	oText1 = (data[110].rstrip()) + alarm_s
	infLabel4 = Label(root, text=oText1)
	infLabel4.configure(bg = '#000000',fg ='#4b87ff')
	infLabel4.place(x = 480,y = 490)
	oText1 = (data[111].rstrip()) + alarm_t
	infLabel4 = Label(root, text=oText1)
	infLabel4.configure(bg = '#000000',fg ='#4b87ff')
	infLabel4.place(x = 360,y = 490)
	infLabel4 = Label(root, text=onoff_day)
	infLabel4.configure(bg = '#000000',fg ='#4b87ff')
	infLabel4.place(x = 210,y = 490)

	B1 = Button(root, text=remove_var(buttons[0]), highlightbackground = "#e47fe5", highlightthickness = 2, borderwidth=0, bg='#e47fe5', fg='#000000',activebackground='#e47fe5', activeforeground='#000000', width=(button_width_a-2), command=callback9)
	B1.place(x = 60,y = 125)
	B2 = Button(root, text=remove_var(buttons[1]), highlightbackground = "#4b87ff", highlightthickness = 2, borderwidth=0, bg='#4b87ff', fg='#000000',activebackground='#4b87ff', activeforeground='#000000', width=(button_width_a-2), command=callback10)
	B2.place(x = 60,y = 165)
	B3 = Button(root, text=remove_var(buttons[2]), highlightbackground = "#e47fe5", highlightthickness = 2, borderwidth=0, bg='#e47fe5', fg='#000000',activebackground='#e47fe5', activeforeground='#000000', width=(button_width_a-2), command=callback11)
	B3.place(x = 60,y = 210)
	B4 = Button(root, text=remove_var(buttons[3]), highlightbackground = "#e47fe5", highlightthickness = 2, borderwidth=0, bg='#e47fe5', fg='#000000',activebackground='#e47fe5', activeforeground='#000000', width=(button_width_a-2), command=callback12)
	B4.place(x = 60,y = 250)
	B5 = Button(root, text=remove_var(buttons[4]), highlightbackground = "#e47fe5", highlightthickness = 2, borderwidth=0, bg='#e47fe5', fg='#000000',activebackground='#e47fe5', activeforeground='#000000', width=(button_width_a-2), command=callback13)
	B5.place(x = 60,y = 295)
	B6 = Button(root, text=remove_var(buttons[5]), highlightbackground = "#e47fe5", highlightthickness = 2, borderwidth=0, bg='#e47fe5', fg='#000000',activebackground='#e47fe5', activeforeground='#000000', width=(button_width_a-2), command=callback14)
	B6.place(x = 60,y = 335)
	B13 = Button(root, text=remove_var(buttons[6]), highlightbackground = "#e47fe5", highlightthickness = 2, borderwidth=0, bg='#e47fe5', fg='#000000',activebackground='#e47fe5', activeforeground='#000000', width=(button_width_a-2), command=callback914)
	B13.place(x = 60,y = 380)
	B14 = Button(root, text=remove_var(buttons[7]), highlightbackground = "#e47fe5", highlightthickness = 2, borderwidth=0, bg='#e47fe5', fg='#000000',activebackground='#e47fe5', activeforeground='#000000', width=(button_width_a-2), command=callback915)
	B14.place(x = 60,y = 420)
	B15 = Button(root, text=remove_var(buttons[8]), highlightbackground = "#e47fe5", highlightthickness = 2, borderwidth=0, bg='#e47fe5', fg='#000000',activebackground='#e47fe5', activeforeground='#000000', width=(button_width_a-2), command=callback916)
	B15.place(x = 60,y = 465)

	B7 = Button(root, text=(data[108].rstrip()), highlightbackground = "#fbd05f", highlightthickness = 2, borderwidth=0, bg='#fbd05f', fg='#000000',activebackground='#fbd05f', activeforeground='#000000', width=(button_width_b-2), command=all_on)
	B7.place(x = 680,y = 134)
	B8 = Button(root, text=(data[109].rstrip()), highlightbackground = "#fbd05f", highlightthickness = 2, borderwidth=0, bg='#fbd05f', fg='#000000',activebackground='#fbd05f', activeforeground='#000000', width=(button_width_b-3), command=all_off)
	B8.place(x = 807,y = 134)
	if speech == 1 and is_connected(REMOTE_SERVER)=="Online":
		B9 = Button(root, text=(data[10].rstrip()), highlightbackground = "#fbd05f", highlightthickness = 2, borderwidth=0, bg='#fbd05f', fg='#000000',activebackground='#fbd05f', activeforeground='#000000', width=(button_width_b-3), command=air_switch)
		B9.place(x = 924,y = 134)
	B10 = Button(root, text=(data[139].rstrip()), highlightbackground = "#fbd05f", highlightthickness = 2, borderwidth=0, bg='#fbd05f', fg='#000000',activebackground='#fbd05f', activeforeground='#000000', width=(button_width_b-3), command=clearLOG)
	B10.place(x = 807,y = 176)
	B11 = Button(root, text=(data[38].rstrip()), highlightbackground = "#ffff9f", highlightthickness = 2, borderwidth=0, bg='#ffff9f', fg='#000000',activebackground='#ffff9f', activeforeground='#000000', width=(button_width_b-2), command=callback8)
	B11.place(x = 680,y = 176)
	B12 = Button(root, text=(data[8].rstrip()), highlightbackground = "#8588e9", highlightthickness = 2, borderwidth=0, bg='#8588e9', fg='#000000',activebackground='#8588e9', activeforeground='#000000', width=(button_width_b-3), command=callback6)
	B12.place(x = 924,y = 176)
	B13 = Button(root, text=(data[17].rstrip()), highlightbackground = "#ffff9f", highlightthickness = 2, borderwidth=0, bg='#ffff9f', fg='#000000',activebackground='#ffff9f', activeforeground='#000000', width=(button_width_b-2), command=callback15)
	B13.place(x = 680,y = 218)
	B14 = Button(root, text=(data[16].rstrip()), highlightbackground = "#ffff9f", highlightthickness = 2, borderwidth=0, bg='#ffff9f', fg='#000000',activebackground='#ffff9f', activeforeground='#000000', width=(button_width_b-3), command=callback16)
	B14.place(x = 807,y = 218)
	B15 = Button(root, text=(data[122].rstrip()), highlightbackground = "#ffff9f", highlightthickness = 2, borderwidth=0, bg='#ffff9f', fg='#000000',activebackground='#ffff9f', activeforeground='#000000', width=(button_width_b-3), command=callback43)
	B15.place(x = 924,y = 218)

	rgbLabel1 = Label(root, text=(data[123].rstrip()))
	rgbLabel1.configure(bg = '#000000',fg ='#4b87ff')
	rgbLabel1.place(x = 805,y = 320)
	B16 = Button(root, text=(data[124].rstrip()), highlightbackground = "#ffff9f", highlightthickness = 2, borderwidth=0, bg='#ffff9f', fg='#000000',activebackground='#ffff9f', activeforeground='#000000', width=(button_width_b-2), command=red_neo)
	B16.place(x = 681,y = 345)
	B17 = Button(root, text=(data[125].rstrip()), highlightbackground = "#ffcf60", highlightthickness = 2, borderwidth=0, bg='#ffcf60', fg='#000000',activebackground='#ffcf60', activeforeground='#000000', width=(button_width_b-3), command=green_neo)
	B17.place(x = 808,y = 345)
	B18 = Button(root, text=(data[126].rstrip()), highlightbackground = "#8588e9", highlightthickness = 2, borderwidth=0, bg='#8588e9', fg='#000000',activebackground='#8588e9', activeforeground='#000000', width=(button_width_b-3), command=blue_neo)
	B18.place(x = 925,y = 345)
	B19 = Button(root, text=(data[127].rstrip()), highlightbackground = "#ffff9f", highlightthickness = 2, borderwidth=0, bg='#ffff9f', fg='#000000',activebackground='#ffff9f', activeforeground='#000000', width=(button_width_b-2), command=off_neo)
	B19.place(x = 681,y = 387)
	B20 = Button(root, text=(data[128].rstrip()), highlightbackground = "#ffff9f", highlightthickness = 2, borderwidth=0, bg='#ffff9f', fg='#000000',activebackground='#ffff9f', activeforeground='#000000', width=(button_width_b-3), command=set_neo)
	B20.place(x = 808,y = 387)
	B21 = Button(root, text=(data[143].rstrip()), highlightbackground = "#ffff9f", highlightthickness = 2, borderwidth=0, bg='#ffff9f', fg='#000000',activebackground='#ffff9f', activeforeground='#000000', width=(button_width_b-3), command=color_neo)
	B21.place(x = 925,y = 387)

	brLabel1 = Label(root, text=(data[129].rstrip()))
	brLabel1.configure(bg = '#000000',fg ='#4b87ff')
	brLabel1.place(x = 805,y = 430)
	SL1 = Scale(root, from_=0, to=255,  length=(slider_length-70), troughcolor="#ffcf60", highlightbackground = "#000000", bd=0, bg='#000000', fg='#4b87ff', tickinterval=20, label="", orient=HORIZONTAL)
	SL1.place(x = 630,y = 450)
	SL1.set(10)

	B22 = Button(root, text="Menu", highlightbackground = "#8588e9", highlightthickness = 2, borderwidth=0, bg='#8588e9', fg='#000000',activebackground='#8588e9', activeforeground='#000000', width=(button_width_b-3), command=menu_toggle)
	B22.place(x = 810,y = 284)
	
	root.mainloop()

# updating window (Clock and Temps)
the_time=''
TIME = newtime = time.time()
class Window_1_lcars(Frame):
	def __init__(self,master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()
	def create_widgets(self):
		self.display_time=Label(self, text=the_time)
		self.display_time.grid(row=0, column=1)
		def change_value_the_time():
			client.on_message=on_message
			client.loop_start()
			client.subscribe([("MQTChroma/*",1),(main_topic,0)])
			time.sleep(2)
			client.loop_stop()
			global the_time
			newtime = time.time()
			if newtime != the_time:
				stats = ""
				try:
					client.publish("tgn/cpu/temp",str(round(getCpuTemperature(),1)),qos=0,retain=True)
				except:
					client.connect(get_ip())
					client.loop_start()
				if b1 == 0:
					stats=stats+'Off|'
				if b1 == 1:
					stats=stats+'On|'
				if b2 == 0:
					stats=stats+'Off|'
				if b2 == 1:
					stats=stats+'On|'
				if b3 == 0:
					stats=stats+'Off|'
				if b3 == 1:
					stats=stats+'On|'
				if b4 == 0:
					stats=stats+'Off|'
				if b4 == 1:
					stats=stats+'On|'
				if b5 == 0:
					stats=stats+'Off|'
				if b5 == 1:
					stats=stats+'On|'
				if b6 == 0:
					stats=stats+'Off|'
				if b6 == 1:
					stats=stats+'On|'
				if b7 == 0:
					stats=stats+'Off|'
				if b7 == 1:
					stats=stats+'On|'
				if b8 == 0:
					stats=stats+'Off|'
				if b8 == 1:
					stats=stats+'On|'
				if b9 == 0:
					stats=stats+'Off'
				if b9 == 1:
					stats=stats+'On'
				cach_time = pcf8563ReadTime()
				the_time= format_time(cach_time)+"\nAutomatic: "+ond+"\n"+stats
				client.publish("tgn/system/time",format_time(cach_time),qos=0,retain=True)
				global afbground
				global fground
				if colorSet == 9 or colorSet == 0:
					afbground = '#000000'
					fground = '#003f7e'
				self.display_time.config(text=the_time, font=('times', (font_size_a-1), 'bold'), bg=afbground, fg='#fdaa30')
			self.display_time.after(15000, change_value_the_time)
		change_value_the_time()

# updating window (Weather and PiHole)
the_timeb=''
class Window_2_lcars(Frame):
	def __init__(self,master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()
	def create_widgets(self):
		self.display_time=Label(self, text=the_timeb)
		self.display_time.grid(row=0, column=1)
		def change_value_the_timeb():
			subprocess.call('xset dpms force on', shell=True)
			global the_timeb
			temp_data = "Room Luxmeter:"
			newtime = time.time()
			if newtime != the_timeb:
				try:
					f = open(spr_phat+"text.lang","r")
				except IOError:
					print("cannot open text.lang.... file not found")
				else:
					dataText = []
					for line in f:
						dataText.append(line)
				output = ''
				if is_connected(REMOTE_SERVER)=="Online":
					global rssfeed
					global ttiv
					if int(esp_li)==50:
						ttiv = 50000
					else:
						ttiv = 1200000
					setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 10 emeter"
					os.system(setn)
					if rssurl == "empty":
						rssfeed = "Please set a Newsfeed"
					else:
						print("Read RSS")
						rssfeed = rss(rssurl,10)
					print("Load Weather")
					if allowed_key(openweatherkey) == "yes":
						data = weather_info(zipcode,openweatherkey)
						output = output+(dataText[24].rstrip())+data['city']+','+data['country']+'\n'
						output = output+str(data['temp'])+'°C  '+data['sky']+' '
						output = output+(dataText[25].rstrip())+str(data['temp_max'])+'°C, '+(dataText[26].rstrip())+str(data['temp_min'])+'°C\n'
						output = output+(dataText[27].rstrip())+str(data['wind'])+'km/h \n'
						output = output+(dataText[28].rstrip())+str(data['humidity'])+'% \n'
						output = output+(dataText[29].rstrip())+str(data['cloudiness'])+'% \n'
						output = output+(dataText[30].rstrip())+str(data['pressure'])+'hpa \n'
						output = output+(dataText[31].rstrip())+str(data['sunrise'])+"\n"+(dataText[32].rstrip())+str(data['sunset'])+'\n'
						output = output+'---------------------------------------------------------\n'
						output = output+'ESP:'+esp_temp+'°C / '+esp_hum+'% / '+esp_rssi+'dbm / '+str(format_lux(int(esp_li)))+'LUX\n'
						output = output+'ESP2:'+esp_temp_2+'°C / '+esp_b1_2+' / '+esp_rssi_2+'dbm / '+str(format_lux(int(esp_li_2)))+'LUX\n'
						output = output+'---------------------------------------------------------\n'
						output = output+temp_data+" / "+str(format_lux(int(esp_li)))+'LUX\n'
						global weather_t
						global weather_c
						global weather_w
						global weather_h
						weather_t = float(data['temp'])
						weather_c = int(data['cloudiness'])
						weather_w = float(data['wind'])
						weather_h = int(data['humidity'])
						client.publish("tgn/weather/temp_min",float(data['temp_min']),qos=0,retain=True)
						client.publish("tgn/weather/temp_max",float(data['temp_max']),qos=0,retain=True)
						client.publish("tgn/weather/temp",weather_t,qos=0,retain=True)
						client.publish("tgn/weather/clouds",weather_c,qos=0,retain=True)
						client.publish("tgn/weather/wind",weather_w,qos=0,retain=True)
						client.publish("tgn/weather/humidity",weather_h,qos=0,retain=True)
						client.publish("tgn/room/temp",temp_data,qos=0,retain=True)
						client.publish("tgn/room/light",readLight(),qos=0,retain=True)
						client.publish("tgn/weather/icon",str(data['icon']),qos=0,retain=True)
						global we_cach
						we_cach = "Temperature "+str(weather_t)+"°C \n Max Temperature "+str(data['temp_max'])+" °C \n Sky "+data['sky']+"\n Windspeed "+str(data['wind'])
					else:
						output = output+(dataText[35].rstrip())+'\n'
					output = output+'---------------------------------------------------------\n'
				timespl = format_time(pcf8563ReadTime()).split(" ")
				client.publish("tgn/system/update",timespl[3],qos=0,retain=True)
				global afbground
				global fground
				if colorSet == 9 or colorSet == 0:
					afbground = '#000000'
					fground = '#eaa424'
				self.display_time.config(text=output, font=('times', font_size_b, 'bold'), bg=afbground, fg=fground)
				if is_connected(REMOTE_SERVER)=="Online":
					if allowed_key(openweatherkey) == "yes":
						phatI = phat+get_icon_name(str(data['icon']))
						load = Image.open(phatI)
						render = ImageTk.PhotoImage(load)
						img = Label(self, image=render)
						img.image = render
						img.config(bg=afbground)
						img.place(x=0, y=60)
			self.display_time.after(ttiv, change_value_the_timeb)
		change_value_the_timeb()

#window (RSS Feed)
class Window_3_lcars(Frame):
	def __init__(self,master):
		global afbground
		global fground
		if colorSet == 9 or colorSet == 0:
			afbground = '#cf0209'
			fground = '#ffffff'
		Frame.__init__(self, master)
		self.grid()
		self.canvas = Canvas(self, bg=afbground, highlightthickness=0, width=(feed_size_width+320), height=(feed_size_height-12))
		self.canvas.pack(expand=True)
		xpos = feed_pos_x
		ypos = feed_pos_y
		self.canvas.create_text(xpos, (ypos-5), anchor='w', text=rssfeed, font=('Helvetica', font_size_b, 'bold'), fill=fground, tags='text')
		text_begin = self.canvas.bbox('text')[0]
		text_end = self.canvas.bbox('text')[2]
		self.text_length = text_end - text_begin
		self.scroll_text()
	def scroll_text(self):
		self.canvas.move('text', -3, 0)
		text_end = self.canvas.bbox('text')[2]
		if text_end < 0:
			self.canvas.itemconfig('text',text=rssfeed)
			text_begin = self.canvas.bbox('text')[0]
			text_end = self.canvas.bbox('text')[2]
			self.text_length = text_end - text_begin
			self.canvas.move('text', 450 + self.text_length, 0)
		self.canvas.after(50, self.scroll_text)



def normal_screen(colorSet):
	print("Load Normal Screen - Mode:"+str(colorSet))
	root = Tk()
	#fullscreen mode
	WMWIDTH, WMHEIGHT, WMLEFT, WMTOP = root.winfo_screenwidth(), root.winfo_screenheight(), 0, 0
	root.overrideredirect(screen) 
	root.geometry("%dx%d+%d+%d" % (WMWIDTH, WMHEIGHT, WMLEFT, WMTOP))

	try:
		f = open(spr_phat+"text.lang","r")
	except IOError:
			print("cannot open text.lang.... file not found")
	else:
		data = []
		for line in f:
			data.append(line)
	root.wm_title("TGN Smart Home "+version+" ("+spr+")")
	menu = Menu(root)
	root.config(background = bground, menu=menu)

	filemenu = Menu(menu)
	menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
	filemenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
	menu.add_cascade(label=(data[37].rstrip()), menu=filemenu)
	filemenu.add_command(label=(data[38].rstrip()), command=callback8)
	filemenu.add_separator()
	filemenu.add_command(label=(data[132].rstrip()), command=callback41)
	filemenu.add_command(label=(data[133].rstrip()), command=callback47)
	filemenu.add_command(label=(data[134].rstrip()), command=callback45)
	filemenu.add_command(label=(data[135].rstrip()), command=callback46)
	filemenu.add_command(label=(data[40].rstrip()), command=callback30)

	setmenu = Menu(menu)
	menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
	setmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
	menu.add_cascade(label=(data[41].rstrip()), menu=setmenu)
	setmenu.add_command(label=(data[115].rstrip()), command=callback39)
	setmenu.add_command(label=(data[42].rstrip()), command=callback25)
	setmenu.add_command(label=(data[43].rstrip()), command=callback32)
	setmenu.add_command(label=(data[44].rstrip()), command=callback34)
	setmenu.add_command(label=(data[130].rstrip()), command=callback48)
	setmenu.add_command(label=(data[131].rstrip()), command=auto_clock)

	langmenu = Menu(menu)
	menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
	langmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
	setmenu.add_cascade(label=(data[45].rstrip()), menu=langmenu)
	langmenu.add_command(label="de", command=spt1)
	langmenu.add_command(label="en", command=spt2)
	langmenu.add_command(label="fr", command=spt3)
	langmenu.add_command(label="ru", command=spt4)
	langmenu.add_command(label="jp", command=spt5)
	langmenu.add_command(label="zh", command=spt6)

	stylemenu = Menu(menu)
	menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
	stylemenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
	setmenu.add_cascade(label=(data[46].rstrip()), menu=stylemenu)
	stylemenu.add_command(label=(data[47].rstrip()), command=callback19)

	colmenu = Menu(menu)
	menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
	colmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
	stylemenu.add_cascade(label=(data[48].rstrip()), menu=colmenu)
	try:
		print(">>Load themes.config")
		f = open("/home/pi/tgn_smart_home/config/themes.config","r")
	except IOError:
		print("cannot open themes.config.... file not found")
	else:
		data_ca = []
		color_button = [] 
		for line in f:
			data_ca.append(line)
		cou = 0
		for x in data_ca:
			index = data_ca[cou].find("#")
			if index == 0:
				bu_cach = data_ca[cou].rstrip()
				bu_cach = bu_cach[1:]
				color_button.append(bu_cach) 
			cou = cou + 1
		color_button.append("LCARS")
		color_button.append("ioBrocker")
	index_bu = len(color_button)
	if index_bu >= 1:    
		colmenu.add_command(label=color_button[0], command=lambda: key(1,color_button[0]))
	if index_bu >= 2:    
		colmenu.add_command(label=color_button[1], command=lambda: key(2,color_button[1]))
	if index_bu >= 3:    
		colmenu.add_command(label=color_button[2], command=lambda: key(3,color_button[2]))
	if index_bu >= 4:    
		colmenu.add_command(label=color_button[3], command=lambda: key(4,color_button[3]))
	if index_bu >= 5:    
		colmenu.add_command(label=color_button[4], command=lambda: key(5,color_button[4]))
	if index_bu >= 6:    
		colmenu.add_command(label=color_button[5], command=lambda: key(6,color_button[5]))
	if index_bu >= 7:    
		colmenu.add_command(label=color_button[6], command=lambda: key(7,color_button[6]))
	if index_bu >= 8:    
		colmenu.add_command(label=color_button[7], command=lambda: key(8,color_button[7]))
	if index_bu >= 9:    
		colmenu.add_command(label=color_button[8], command=lambda: key(9,color_button[8]))
	def key(method,but_name):
		global colorSet
		colorSet = method
		if but_name == "LCARS":
			colorSet = 9
		if but_name == "ioBrocker":
			colorSet = 0
		write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
		time.sleep(1)
		os.execv(sys.executable, ['python3'] + sys.argv)

	rommenu = Menu(menu)
	menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
	rommenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
	setmenu.add_cascade(label=(data[55].rstrip()), menu=rommenu)
	rommenu.add_command(label=(data[56].rstrip()), command=callback17)
	rommenu.add_command(label=(data[57].rstrip()), command=callback18)
	rommenu.add_command(label=(data[58].rstrip()), command=callback23)
	rommenu.add_command(label=(data[59].rstrip()), command=callback26)
	rommenu.add_command(label=(data[60].rstrip()), command=callback27)
	rommenu.add_command(label=(data[61].rstrip()), command=callback35)
	rommenu.add_command(label=(data[113].rstrip()), command=callback38)
	rommenu.add_command(label=(data[119].rstrip()), command=callback42)
	rommenu.add_command(label=(data[62].rstrip()), command=callback22)

	nfcmenu = Menu(menu)
	menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
	nfcmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
	setmenu.add_cascade(label=(data[63].rstrip()), menu=nfcmenu)
	nfcmenu.add_command(label=(data[64].rstrip()), command=callback28)
	nfcmenu.add_command(label=(data[65].rstrip()), command=callback29)
	nfcmenu.add_command(label=(data[66].rstrip()), command=callback31)

	helpmenu = Menu(menu)
	menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
	helpmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
	menu.add_cascade(label=(data[67].rstrip()), menu=helpmenu)
	helpmenu.add_command(label=(data[139].rstrip()), command=clearLOG)
	helpmenu.add_command(label=(data[140].rstrip()), command=callback44)
	helpmenu.add_command(label=(data[68].rstrip()), command=About)

	leftFrame = Frame(root, width=WMWIDTH/2, height = WMHEIGHT)
	leftFrame.configure(background=bground)
	leftFrame.grid(row=0, column=0, padx=10, pady=3)

	infFrame1 = Frame(leftFrame)
	infFrame1.configure(background=bground)
	infFrame1.grid(row=0, column=0, padx=10, pady=3)

	rightFrame = Frame(root, width=WMWIDTH/2, height = WMHEIGHT)
	rightFrame.configure(background=bground)
	rightFrame.grid(row=0, column=1, padx=10, pady=3)

	app=Window(rightFrame)

	buttonFrame1 = Frame(rightFrame)
	buttonFrame1.configure(background=bground)
	buttonFrame1.grid(row=3, column=0, padx=10, pady=3)
	buttonLabel1 = Label(buttonFrame1, text=(data[9].rstrip()))
	buttonLabel1.configure(background=bground, foreground=fground)
	buttonLabel1.grid(row=0, column=1, padx=10, pady=3)

	B1 = Button(buttonFrame1, text=remove_var(buttons[0]), bg=buttonb, fg=fground, width=button_width_a, command=callback9)
	B1.grid(row=1, column=0, padx=10, pady=3) 
	B2 = Button(buttonFrame1, text=remove_var(buttons[1]), bg=buttonb, fg=fground, width=button_width_a, command=callback10)
	B2.grid(row=1, column=1, padx=10, pady=3)
	B3 = Button(buttonFrame1, text=remove_var(buttons[2]), bg=buttonb, fg=fground, width=button_width_a, command=callback11)
	B3.grid(row=1, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame1, text=remove_var(buttons[3]), bg=buttonb, fg=fground, width=button_width_a, command=callback12)
	B4.grid(row=2, column=0, padx=10, pady=3)
	B5 = Button(buttonFrame1, text=remove_var(buttons[4]), bg=buttonb, fg=fground, width=button_width_a, command=callback13)
	B5.grid(row=2, column=1, padx=10, pady=3)
	B6 = Button(buttonFrame1, text=remove_var(buttons[5]), bg=buttonb, fg=fground, width=button_width_a, command=callback14)
	B6.grid(row=2, column=2, padx=10, pady=3)
	B13 = Button(buttonFrame1, text=remove_var(buttons[6]), bg=buttonb, fg=fground, width=button_width_a, command=callback914)
	B13.grid(row=3, column=0, padx=10, pady=3)
	B14 = Button(buttonFrame1, text=remove_var(buttons[7]), bg=buttonb, fg=fground, width=button_width_a, command=callback915)
	B14.grid(row=3, column=1, padx=10, pady=3)
	B15 = Button(buttonFrame1, text=remove_var(buttons[8]), bg=buttonb, fg=fground, width=button_width_a, command=callback916)
	B15.grid(row=3, column=2, padx=10, pady=3)
	B7 = Button(buttonFrame1, text=(data[108].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=all_on)
	B7.grid(row=4, column=0, padx=10, pady=3)
	B8 = Button(buttonFrame1, text=(data[109].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=all_off)
	B8.grid(row=4, column=1, padx=10, pady=3)
	if speech == 1 and is_connected(REMOTE_SERVER)=="Online":
		B9 = Button(buttonFrame1, text=(data[10].rstrip()), bg=buttona, fg=fground, width=button_width_a, command=air_switch)
		B9.grid(row=4, column=2, padx=10, pady=3)
	B10 = Button(buttonFrame1, text=(data[139].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=clearLOG)
	B10.grid(row=5, column=0, padx=10, pady=3)
	B11 = Button(buttonFrame1, text=(data[38].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=callback8)
	B11.grid(row=5, column=1, padx=10, pady=3)
	B12 = Button(buttonFrame1, text=(data[8].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=callback6)
	B12.grid(row=5, column=2, padx=10, pady=3)

	buttonFrame2 = Frame(rightFrame)
	buttonFrame2.configure(background=bground)
	buttonFrame2.grid(row=4, column=0, padx=10, pady=3)
	buttonLabel2 = Label(buttonFrame2, text=(data[15].rstrip()))
	buttonLabel2.configure(background=bground, foreground=fground)
	buttonLabel2.grid(row=0, column=1, padx=10, pady=3)

	B1 = Button(buttonFrame2, text=(data[17].rstrip()), bg=buttonb, fg=fground, width=button_width_b, command=callback15)
	B1.grid(row=1, column=0, padx=10, pady=3)
	B2 = Button(buttonFrame2, text=(data[16].rstrip()), bg=buttonb, fg=fground, width=button_width_b, command=callback16)
	B2.grid(row=1, column=1, padx=10, pady=3)
	if ifI2C(NFC_ADDRESS) == "found device":
		B3 = Button(buttonFrame2, text=(data[18].rstrip()), bg=buttona, fg=fground, width=button_width_b, command=callback30)
		B3.grid(row=1, column=2, padx=10, pady=3)
	else:
		B3 = Button(buttonFrame2, text=(data[141].rstrip()), bg=buttona, fg=fground, width=button_width_b, command=callback100)
		B3.grid(row=1, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame2, text=(data[142].rstrip()), bg=buttonb, fg=fground, width=button_width_b, command=callback110)
	B4.grid(row=1, column=3, padx=10, pady=3)

	buttonFrame3 = Frame(rightFrame)
	buttonFrame3.configure(background=bground)
	buttonFrame3.grid(row=5, column=0, padx=10, pady=3)

	B1 = Button(buttonFrame3, text=(data[22].rstrip()), bg=buttonb, fg=fground, width=button_width_b, command=callback20)
	B1.grid(row=0, column=0, padx=10, pady=3) 
	B2 = Button(buttonFrame3, text=(data[23].rstrip()), bg=buttonb, fg=fground, width=button_width_b, command=callback21)
	B2.grid(row=0, column=1, padx=10, pady=3)
	B3 = Button(buttonFrame3, text=(data[118].rstrip()), bg=buttonb, fg=fground, width=button_width_b, command=callback40)
	B3.grid(row=0, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame3, text=(data[122].rstrip()), bg=buttonb, fg=fground, width=button_width_b, command=callback43)
	B4.grid(row=0, column=3, padx=10, pady=3)

	buttonFrame4 = Frame(rightFrame)
	buttonFrame4.configure(background=bground)
	buttonFrame4.grid(row=6, column=0, padx=10, pady=3)
	buttonLabel4 = Label(buttonFrame4, text=(data[123].rstrip()))
	buttonLabel4.configure(background=bground, foreground=fground)
	buttonLabel4.grid(row=0, column=1, padx=10, pady=3)

	B1 = Button(buttonFrame4, text=(data[124].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=red_neo)
	B1.grid(row=1, column=0, padx=10, pady=3)
	B2 = Button(buttonFrame4, text=(data[125].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=green_neo)
	B2.grid(row=1, column=1, padx=10, pady=3)
	B3 = Button(buttonFrame4, text=(data[126].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=blue_neo)
	B3.grid(row=1, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame4, text=(data[127].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=off_neo)
	B4.grid(row=2, column=0, padx=10, pady=3)
	B5 = Button(buttonFrame4, text=(data[128].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=set_neo)
	B5.grid(row=2, column=1, padx=10, pady=3)
	B6 = Button(buttonFrame4, text=(data[143].rstrip()), bg=buttonb, fg=fground, width=button_width_a, command=color_neo)
	B6.grid(row=2, column=2, padx=10, pady=3)

	buttonFrame5 = Frame(rightFrame)
	buttonFrame5.configure(background=bground)
	buttonFrame5.grid(row=7, column=0, padx=10, pady=3)

	SL1 = Scale(buttonFrame5, from_=0, to=255,  length=slider_length, bg=buttonb, fg=fground, tickinterval=20, label=(data[129].rstrip()), orient=HORIZONTAL)
	SL1.grid(row=0, column=1, padx=10, pady=3)
	SL1.set(10)

	app=WindowB(leftFrame)

	seperatorFrame4 = Frame(leftFrame)
	seperatorFrame4.configure(background=bground)
	seperatorFrame4.grid(row=2, column=0, padx=5, pady=3)
	seperatorLabel1 = Label(seperatorFrame4, text="")
	seperatorLabel1.configure(background=bground)
	seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

	app=WindowC(leftFrame)

	seperatorFrame3 = Frame(leftFrame)
	seperatorFrame3.configure(background=bground)
	seperatorFrame3.grid(row=4, column=0, padx=5, pady=3)
	seperatorLabel1 = Label(seperatorFrame3, text="")
	seperatorLabel1.configure(background=bground)
	seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

	infFrame1 = Frame(leftFrame)
	infFrame1.configure(background=bground)
	infFrame1.grid(row=4, column=0, padx=10, pady=3)
	infLabel1 = Label(infFrame1, text=(data[11].rstrip()))
	infLabel1.configure(background=bground, foreground=fground)
	infLabel1.grid(row=0, column=1, padx=10, pady=3)
	oText1 = (data[12].rstrip())+ontime
	infLabel2 = Label(infFrame1, text=oText1)
	infLabel2.configure(background=bground, foreground=fground)
	infLabel2.grid(row=1, column=0, padx=10, pady=3)
	oText2 = (data[13].rstrip())+offtime
	infLabel3 = Label(infFrame1, text=oText2)
	infLabel3.configure(background=bground, foreground=fground)
	infLabel3.grid(row=1, column=2, padx=10, pady=3)
	oText3 = (data[14].rstrip())+s1+s2+s3+s4
	infLabel4 = Label(infFrame1, text=oText3)
	infLabel4.configure(background=bground, foreground=fground)
	infLabel4.grid(row=1, column=1, padx=10, pady=3)
	oText4 = (data[110].rstrip()) + alarm_s
	infLabel5 = Label(infFrame1, text=oText4)
	infLabel5.configure(background=bground, foreground=fground)
	infLabel5.grid(row=2, column=0, padx=10, pady=3)
	oText5 = (data[111].rstrip()) + alarm_t
	infLabel6 = Label(infFrame1, text=oText5)
	infLabel6.configure(background=bground, foreground=fground)
	infLabel6.grid(row=2, column=2, padx=10, pady=3)
	oText6 = onoff_day
	infLabel6 = Label(infFrame1, text=oText6)
	infLabel6.configure(background=bground, foreground=fground)
	infLabel6.grid(row=2, column=1, padx=10, pady=3)

	root.mainloop()

# updating window (Clock and Temps)
the_time=''
TIME = newtime = time.time()
class Window(Frame):
	def __init__(self,master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()
	def create_widgets(self):
		self.display_time=Label(self, text=the_time)
		self.display_time.grid(row=0, column=1)
		def change_value_the_time():
			client.on_message=on_message
			client.loop_start()
			client.subscribe([("MQTChroma/*",1),(main_topic,0)])
			time.sleep(2)
			client.loop_stop()
			global the_time
			stats = textswitch
			newtime = time.time()
			if newtime != the_time:
				try:
					client.publish("tgn/cpu/temp",str(round(getCpuTemperature(),1)),qos=0,retain=True)
				except:
					client.connect(get_ip())
					client.loop_start()
				if b1 == 0:
					stats=stats+'Off|'
				if b1 == 1:
					stats=stats+'On|'
				if b2 == 0:
					stats=stats+'Off|'
				if b2 == 1:
					stats=stats+'On|'
				if b3 == 0:
					stats=stats+'Off|'
				if b3 == 1:
					stats=stats+'On|'
				if b4 == 0:
					stats=stats+'Off|'
				if b4 == 1:
					stats=stats+'On|'
				if b5 == 0:
					stats=stats+'Off|'
				if b5 == 1:
					stats=stats+'On|'
				if b6 == 0:
					stats=stats+'Off|'
				if b6 == 1:
					stats=stats+'On|'
				if b7 == 0:
					stats=stats+'Off|'
				if b7 == 1:
					stats=stats+'On|'
				if b8 == 0:
					stats=stats+'Off|'
				if b8 == 1:
					stats=stats+'On|'
				if b9 == 0:
					stats=stats+'Off'
				if b9 == 1:
					stats=stats+'On'
				rca = ""
				cach_time = pcf8563ReadTime()
				the_time= format_time(cach_time)+" / Automatic: "+ond+" "+rca+"\n"+stats
				client.publish("tgn/system/time",format_time(cach_time),qos=0,retain=True)
				global afbground
				global fground
				if colorSet == 9 or colorSet == 0:
					afbground = '#000000'
					fground = '#003f7e'
				self.display_time.config(text=the_time, font=('times', font_size_a, 'bold'), bg=afbground, fg=fground)
			self.display_time.after(5000, change_value_the_time)
		change_value_the_time()

# updating window (Weather and PiHole)
the_timeb=''
class WindowB(Frame):
	def __init__(self,master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()
	def create_widgets(self):
		self.display_time=Label(self, text=the_timeb)
		self.display_time.grid(row=0, column=1)
		def change_value_the_timeb():
			subprocess.call('xset dpms force on', shell=True)
			global the_timeb
			newtime = time.time()
			if newtime != the_timeb:
				temp_data = "Room Luxmeter:"
				try:
					f = open(spr_phat+"text.lang","r")
				except IOError:
					print("cannot open text.lang.... file not found")
				else:
					dataText = []
					for line in f:
						dataText.append(line)
				output = ''
				if is_connected(REMOTE_SERVER)=="Online":
					global esp_ls
					global rssfeed
					global ttiv
					if rssurl == "empty":
						rssfeed = "Please set a Newsfeed"
					else:
						print("Read RSS")
						print(rssurl)
						rssfeed = rss(rssurl,10)
					if int(esp_li)==50:
						ttiv = 50000
					else:
						ttiv = 1200000
					print("Load Weather")
					if allowed_key(openweatherkey) == "yes":
						data = weather_info(zipcode,openweatherkey)
						output = output+(dataText[24].rstrip())+data['city']+','+data['country']+'\n'
						output = output+str(data['temp'])+'°C  '+data['sky']+' '
						output = output+(dataText[25].rstrip())+str(data['temp_max'])+'°C, '+(dataText[26].rstrip())+str(data['temp_min'])+'°C\n'
						output = output+(dataText[27].rstrip())+str(data['wind'])+'km/h \n'
						output = output+(dataText[28].rstrip())+str(data['humidity'])+'% \n'
						output = output+(dataText[29].rstrip())+str(data['cloudiness'])+'% \n'
						output = output+(dataText[30].rstrip())+str(data['pressure'])+'hpa \n'
						output = output+(dataText[31].rstrip())+str(data['sunrise'])+"\n"+(dataText[32].rstrip())+str(data['sunset'])+'\n'
						output = output+'---------------------------------------------------------\n'
						output = output+'ESP:'+esp_temp+'°C / '+esp_hum+'% / '+esp_rssi+'dbm / '+str(esp_li)+'LUX\n'
						output = output+'ESP2:'+esp_temp_2+'°C / '+esp_b1_2+' / '+esp_rssi_2+'dbm / '+str(esp_li_2)+'LUX\n'
						output = output+'---------------------------------------------------------\n'
						output = output+temp_data+" / "+str(format_lux(int(esp_li)))+'LUX\n'
						global weather_t
						global weather_c
						global weather_w
						global weather_h
						weather_t = float(data['temp'])
						weather_c = int(data['cloudiness'])
						weather_w = float(data['wind'])
						weather_h = int(data['humidity'])
						client.publish("tgn/weather/temp_min",float(data['temp_min']),qos=0,retain=True)
						client.publish("tgn/weather/temp_max",float(data['temp_max']),qos=0,retain=True)
						client.publish("tgn/weather/temp",weather_t,qos=0,retain=True)
						client.publish("tgn/weather/clouds",weather_c,qos=0,retain=True)
						client.publish("tgn/weather/wind",weather_w,qos=0,retain=True)
						client.publish("tgn/weather/humidity",weather_h,qos=0,retain=True)
						client.publish("tgn/room/temp",temp_data,qos=0,retain=True)
						client.publish("tgn/room/light",readLight(),qos=0,retain=True)
						client.publish("tgn/weather/icon",str(data['icon']),qos=0,retain=True)
						global we_cach
						we_cach = "Temperature "+str(weather_t)+"°C \n Max Temperature "+str(data['temp_max'])+" °C \n Sky "+data['sky']+"\n Windspeed "+str(data['wind'])
					else:
						output = output+(dataText[35].rstrip())+'\n'
					output = output+'---------------------------------------------------------\n'
				global cpu_t
				cpu_t = getCpuTemperature()
				timespl = format_time(pcf8563ReadTime()).split(" ")
				output = output+'\n'+(dataText[36].rstrip()+' Update:'+timespl[3])
				client.publish("tgn/system/update",timespl[3],qos=0,retain=True)
				global afbground
				global fground
				if colorSet == 9 or colorSet == 0:
					afbground = '#000000'
					fground = '#eaa424'
				self.display_time.config(text=output, font=('times', font_size_b, 'bold'), bg=afbground, fg=fground)
				if is_connected(REMOTE_SERVER)=="Online":
					if allowed_key(openweatherkey) == "yes":
						phatI = phat+get_icon_name(str(data['icon']))
						load = Image.open(phatI)
						render = ImageTk.PhotoImage(load)
						img = Label(self, image=render)
						img.image = render
						img.config(bg=afbground)
						img.place(x=0, y=60)
			self.display_time.after(ttiv, change_value_the_timeb)
		change_value_the_timeb()

class WindowC(Frame):
	def __init__(self,master):
		global afbground
		global fground
		if colorSet == 9 or colorSet == 0:
			afbground = '#000000'
			fground = '#eaa424'
		Frame.__init__(self, master)
		self.grid()
		self.canvas = Canvas(self, bg=afbground, highlightthickness=0, width=feed_size_width, height=feed_size_height)
		self.canvas.pack(expand=True)
		xpos = feed_pos_x
		ypos = feed_pos_y
		self.canvas.create_text(xpos, ypos, anchor='w', text=rssfeed, font=('Helvetica', font_size_c, 'bold'), fill=fground, tags='text')
		text_begin = self.canvas.bbox('text')[0]
		text_end = self.canvas.bbox('text')[2]
		self.text_length = text_end - text_begin
		self.scroll_text()
	def scroll_text(self):
		self.canvas.move('text', -3, 0)
		text_end = self.canvas.bbox('text')[2]
		if text_end < 0:
			self.canvas.itemconfig('text',text=rssfeed)
			text_begin = self.canvas.bbox('text')[0]
			text_end = self.canvas.bbox('text')[2]
			self.text_length = text_end - text_begin
			self.canvas.move('text', 450 + self.text_length, 0)
		self.canvas.after(50, self.scroll_text)

colorSet = int(sys.argv[1])
print("read mqtt")
client = mqtt.Client("TGN Smart Home GUI")
client.on_message=on_message
client.connect(get_ip())
client.loop_start()
client.subscribe([("MQTChroma/*",1),(main_topic,0)])
time.sleep(2)
ini() #first mqtt read trigger
print("Colorset:" +str(colorSet))
if colorSet == 9:
	lcars_screen_20()
if colorSet <= 8:
	print("Load normal: "+str(colorSet))
	normal_screen(colorSet)
	