# load Libs
import binascii
import PIL
import paho.mqtt.client as mqtt
import subprocess
from subprocess import call
from tkinter import *
from PIL import Image, ImageTk
from tkinter.colorchooser import *
from multiprocessing import Process
from tgnLIB import *
# var
ROM_ADDRESS = 0x53
LCD_ADDRESS = 0x3f
MCP_ADDRESS = 0x20
NFC_ADDRESS = 0x24
MCP_num_gpios = 16
main_topic = "tgn/#"
channel_id = 43245
write_key = "8WQB01T3F5JE0EZ"
read_key = "PJGJDHMEUU1TAXQ"
pushbulletkey = "o.luRM2iMEGKnns3pzkOUiEAGX3IxxVxZ"
openweatherkey = "3aef357118b7ea5d700123785674b45"
zipcode = 6947479
version = "V.1.8"
counterLCD = 0
backlight = 1
LCDpower = 0
MCPpower = 0
screen = 0
RTCpower = 0
spr = "en"
spr_phat = ""
textcpu = ""
textswitch = ""
su = 1
Ts = 0
pw = "0"
buttons = ["1", "2", "3", "4", "5", "6"]
b1 = 0
b2 = 0
b3 = 0
b4 = 0
b5 = 0
b6 = 0
weather_t = -0.41
weather_c = 0
weather_w = 4.1
weather_h = 10
we_cach = "no data"
cpu_t = 57.458
bground = "black"
fground = "green"
abground = "gray"
afground = "black"
afbground = "black"
buttona = "red"
buttonb = "black"
colorSet = 9
s1 = "0"
s2 = "0"
s3 = "0"
s4 = "0"
son = 0
soff = 0
speech = 0
alarm_s = "off"
alarm_t = "17:30"
alarm_p = 0
mcp = ""
mylcd = ""
ontime = "10:19|10:21"
offtime = "10:20|10:22"
phat = "/home/pi/tgn_smart_home/icons/"
color_button = []
#ESP8622/1
esp_ls = 0
esp_switch = 70
esp_switch_b = 120
esp_temp = "0.02"
esp_hum = "--"
esp_rssi = "--"
esp_li = "100"
#ESP8622/2
esp_ip_2 = "---.---.---.---"
esp_pr_2 = "--"
esp_temp_2 = "0.05"
esp_hum_2 = "--"
esp_rssi_2 = "--"
esp_li_2 = "100"
esp_b1_2 = "off"
esp_switch_2 = 70
esp_switch_2_b = 120
esp_ls_2 = 0
esp_2_button = "5"
esp2_cou = 0
#RSS
rssfeed = "no feed"
rssurl = "empty"
rsslang = "en"
#PiHole
api_url = 'http://localhost/admin/api.php'

#functions
def seven_seg(data):
	cachseven = "0"+str(data)
	lenseven = len(cachseven)
	if(lenseven == 3):
		cachseven = "0"+cachseven
	if(lenseven == 2):
		cachseven = "00"+cachseven
	if(lenseven == 1):
		cachseven = "000"+cachseven
	listseven = []
	for char in cachseven:
		listseven.append(int(char))
	sevenseg.Show(listseven)
def ini():
	global sevenseg
	sevenseg = TM1637(12,16,BRIGHT_TYPICAL)
	sevenseg.Clear()
	time.sleep(1)
	anzeige = [0,0,0,0]
	sevenseg.Show(anzeige)
	TextToSpeech("7 Segment Display configured",spr)
	time.sleep(2)
	os.system('clear')
	#MCP23017 I2C
	print(">>initialize MCP23017")
	if ifI2C(MCP_ADDRESS) == "found device":
		global MCPpower
		MCPpower = 1
		global mcp
		mcp = MCP230XX(busnum = 1, address = MCP_ADDRESS, num_gpios = MCP_num_gpios)
		for i in range(int(MCP_num_gpios/2)):
			mcp.config(i, 0)
			mcp.output(i, 0)
		for i in range(int(MCP_num_gpios/2), MCP_num_gpios):
			mcp.config(i, 1)
			mcp.pullup(i, 1)
		print(">>MCP23017 configured")
		TextToSpeech("MCP23017 configured",spr)
	else:
		print(">>MCP23017 not found")
		TextToSpeech("MCP23017 not found",spr)
	#LCD
	time.sleep(2)
	print(">>initialize LCD Display")
	if ifI2C(LCD_ADDRESS) == "found device":
		global LCDpower
		LCDpower = 1
		global mylcd
		mylcd = lcd()
		mylcd.backlight(0)
		time.sleep(1)
		mylcd.lcd_clear()
		time.sleep(2)
		mylcd.backlight(1)
		mylcd.lcd_display_string("TGN Smart Home", 1, 1)
		mylcd.lcd_display_string("Loading....", 2, 0)
		print(">>LCD Display configured")
		TextToSpeech("LCD Display configured",spr)
	else:
		print(">>LCD Display not found")
		TextToSpeech("LCD Display not found",spr)
	global ontime
	global offtime
	global s1
	global s2
	global s3
	global s4
	global ondays
	global b1
	global b2
	global b3
	global b4
	global b5
	global b6
	global colorSet
	global bground
	global fground
	global abground
	global afground
	global afbground
	global buttona
	global buttonb
	global screen
	global version
	global su
	global buttons
	global openweatherkey
	global zipcode
	global pushbulletkey
	global speech
	global Ts
	global channel_id
	global write_key
	global read_key
	global spr
	global spr_phat
	global textcpu
	global textswitch
	global RTCpower
	global alarm_s
	global alarm_t
	global pw
	global com_typ
	global esp_address
	global esp_2_button
	global rssurl
	global rsslang
	global client
	if ifI2C(address) == "found device":
		RTCpower = 1
	print(">>initialize EEPROM")
	if ifI2C(ROM_ADDRESS) == "found device":
		start_add_U = 0xcf
		TextToSpeech("Read EEPROM",spr)
		index = 0
		pushbulletkey = ""
		while index < 34:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_U)
			print(">>Read Byte "+str(start_add_U))
			if cach != "#":
				pushbulletkey = pushbulletkey + cach
			index = index + 1
			start_add_U = start_add_U + 1
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
		start_add_C = 0x2a
		index = 0
		b1A = ""
		while index < 10:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_C)
			print(">>Read Byte "+str(start_add_C))
			if cach != "X":
				b1A = b1A + cach
			index = index + 1
			start_add_C = start_add_C + 1
		start_add_D = 0x34
		index = 0 
		b2A = ""
		while index < 10:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_D)
			print(">>Read Byte "+str(start_add_D))
			if cach != "X":
				b2A = b2A + cach
			index = index + 1
			start_add_D = start_add_D + 1
		start_add_E = 0x3e
		index = 0 
		b3A = ""
		while index < 10:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_E)
			print(">>Read Byte "+str(start_add_E))
			if cach != "X":
				b3A = b3A + cach
			index = index + 1
			start_add_E = start_add_E + 1
		start_add_F = 0x48
		index = 0 
		b4A = ""
		while index < 10:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_F)
			print(">>Read Byte "+str(start_add_F))
			if cach != "X":
				b4A = b4A + cach
			index = index + 1
			start_add_F = start_add_F + 1
		start_add_G = 0x52
		index = 0 
		b5A = ""
		while index < 10:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_G)
			print(">>Read Byte "+str(start_add_G))
			if cach != "X":
				b5A = b5A + cach
			index = index + 1
			start_add_G = start_add_G + 1
		start_add_H = 0x5c
		index = 0 
		b6A = ""
		while index < 10:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_H)
			print(">>Read Byte "+str(start_add_H))
			if cach != "X":
				b6A = b6A + cach
			index = index + 1
			start_add_H = start_add_H + 1
		buttons = []
		buttons.append(b1A)
		buttons.append(b2A)
		buttons.append(b3A)
		buttons.append(b4A)
		buttons.append(b5A)
		buttons.append(b6A)
		s1 = read_eeprom(1,ROM_ADDRESS,0x00,0x08)
		s2 = read_eeprom(1,ROM_ADDRESS,0x00,0x09)
		s3 = read_eeprom(1,ROM_ADDRESS,0x00,0x0a)
		s4 = read_eeprom(1,ROM_ADDRESS,0x00,0x0b)
		start_add_A = 0x0c
		index = 0 
		ontime = ""
		while index < 11:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_A)
			print(">>Read Byte "+str(start_add_A))
			if cach != "X":
				ontime = ontime + cach
			index = index + 1
			start_add_A = start_add_A + 1	
		start_add_B = 0x18
		index = 0 
		offtime = ""
		while index < 11:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_B)
			print(">>Read Byte "+str(start_add_B))
			if cach != "X":
				offtime = offtime + cach
			index = index + 1
			start_add_B = start_add_B + 1
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x01)
		b1=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x02)
		b2=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x03)
		b3=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x04)
		b4=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x05)
		b5=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x06)
		b6=int(dataX)
		esp_2_button = read_eeprom(1,ROM_ADDRESS,0x01,0x5b)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x07)
		colorSet=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x67)
		screen=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0xf2)
		speech=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0xf3)
		Ts=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0xa6)
		su=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x01,0x50)
		pw=dataX
		if su==1:
			if colorSet <= 8:
				os.system('mpg321 /home/pi/tgn_smart_home/sounds/startup.mp3 &')
			else:
				os.system('mpg321 /home/pi/tgn_smart_home/sounds/lcars-startup.mp3 &')
		start_add_I = 0x68
		index = 0 
		ver = ""
		while index < 5:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_I)
			print(">>Read Byte "+str(start_add_I))
			if cach != "X":
				ver = ver + cach
			index = index + 1
			start_add_I = start_add_I + 1
		version = ver
		start_add_V = 0x01
		index = 0
		channel_id = ""
		while index < 6:
			cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_V)
			print(">>Read Byte "+str(start_add_V))
			if cach != "X":
				channel_id = channel_id + cach
			index = index + 1
			start_add_V = start_add_V + 1
		start_add_W = 0x07
		index = 0
		write_key = ""
		while index < 16:
			cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_W)
			print(">>Read Byte "+str(start_add_W))
			if cach != "#":
				write_key = write_key + cach
			index = index + 1
			start_add_W = start_add_W + 1
		start_add_X = 0x18
		index = 0
		read_key = ""
		while index < 16:
			cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_X)
			print(">>Read Byte "+str(start_add_X))
			if cach != "#":
				read_key = read_key + cach
			index = index + 1
			start_add_X = start_add_X + 1
		start_add_AB = 0x51
		index = 0
		alarm_t = ""
		while index < 5:
			cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_AB)
			print(">>Read Byte "+str(start_add_AB))
			if cach != "X":
				alarm_t = alarm_t + cach
			index = index + 1
			start_add_AB = start_add_AB + 1
		start_add_AC = 0x57
		index = 0
		alarm_s = ""
		while index < 3:
			cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_AC)
			print(">>Read Byte "+str(start_add_AC))
			if cach != "X":
				alarm_s = alarm_s + cach
			index = index + 1
			start_add_AC = start_add_AC + 1
		dataX = read_eeprom(1,ROM_ADDRESS,0x01,0x2a)
		xx=int(dataX)
		if xx == 1:
			spr = "de"
		if xx == 2:
			spr = "en"
		if xx == 3:
			spr = "fr"
		if xx == 4:
			spr = "ru"
		if xx == 5:
			spr = "ja"
		if xx == 6:
			spr = "zh"
		start_add_AD = 0x5b
		index = 0
		com_typ = ""
		while index < 3:
			cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_AD)
			print(">>Read Byte "+str(start_add_AD))
			if cach != "X":
				com_typ = com_typ + cach
			index = index + 1
			start_add_AD = start_add_AD + 1
		start_add_AE = 0x5f
		index = 0
		esp_address = ""
		while index < 30:
			cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_AE)
			print(">>Read Byte "+str(start_add_AE))
			if cach != "#":
				esp_address = esp_address + cach
			index = index + 1
			start_add_AE = start_add_AE + 1
		rssurl = ""
		rsslang = ""
		start_add_AF = 0x01
		index = 0
		while index < 2:
			cach = read_eeprom(1,ROM_ADDRESS,0x02,start_add_AF)
			print(">>Read Byte "+str(start_add_AF))
			if cach != "#":
				rsslang = rsslang + cach
			index = index + 1
			start_add_AF = start_add_AF + 1
		start_add_AG = 0x04
		index = 0
		while index < 60:
			cach = read_eeprom(1,ROM_ADDRESS,0x02,start_add_AG)
			print(">>Read Byte "+str(start_add_AG))
			if cach != "#":
				rssurl = rssurl + cach
			index = index + 1
			start_add_AG = start_add_AG + 1
	else:
		print(">>EEPROM not found")
		TextToSpeech("EEPROM not found",spr)
	if MCPpower == 1:
		print(">>MCP23017 test Input and Output")
		print("%d: %x" % (8, mcp.input(8) >> 8))
		print("%d: %x" % (9, mcp.input(9) >> 9))
		print("%d: %x" % (10, mcp.input(10) >> 10))
		print("%d: %x" % (11, mcp.input(11) >> 11))
		print("%d: %x" % (12, mcp.input(12) >> 12))
		print("%d: %x" % (13, mcp.input(13) >> 13))
		print("%d: %x" % (14, mcp.input(14) >> 14))
		print("%d: %x" % (15, mcp.input(15) >> 15))
		for i in range(int(MCP_num_gpios/2)):
			mcp.output(i, 1)
			time.sleep(0.5)
		for i in range(int(MCP_num_gpios/2)):
			mcp.output(i, 0)
		time.sleep(0.5)
	if colorSet <= 8:
		try:
			print(">>Load themes.config")
			f = open("/home/pi/tgn_smart_home/config/themes.config","r")
		except IOError:
				print("cannot open themes.config.... file not found")
		else:
			data = []
			for line in f:
				data.append(line)
			if colorSet == 1:
				startLine = 1
			else:
				startLine = ((colorSet - 1)*8)+1
			c1 = (data[startLine].rstrip())
			c2 = (data[(startLine+1)].rstrip())
			c3 = (data[(startLine+2)].rstrip())
			c4 = (data[(startLine+3)].rstrip())
			c5 = (data[(startLine+4)].rstrip())
			c6 = (data[(startLine+5)].rstrip())
			c7 = (data[(startLine+6)].rstrip())
			d,bground = c1.split("=")
			d,fground = c2.split("=")
			d,abground = c3.split("=")
			d,afground = c4.split("=")
			d,afbground = c5.split("=")
			d,buttona = c6.split("=")
			d,buttonb = c7.split("=")
	if LCDpower == 1:
		mylcd.lcd_clear()
	spr_phat="/home/pi/tgn_smart_home/language/"+spr+"/"
	try:
		f = open(spr_phat+"text.config","r")
	except IOError:
    		print("cannot open text.config.... file not found")
	else:
		data = []
		for line in f:
			data.append(line)
	textcpu=(data[20].rstrip())
	textswitch=(data[19].rstrip())
	#connect mqtt
	client = mqtt.Client("TGN Smart Home")
	client.connect(get_ip())
	client.loop_start()
	#send status to mqtt
	client.publish("tgn/ip",get_ip(),qos=0,retain=True)
	client.publish("tgn/system/shutdown","0",qos=0,retain=True)
	client.publish("tgn/system/reboot","0",qos=0,retain=True)
	client.publish("tgn/system/weather","0",qos=0,retain=True)
	client.publish("tgn/system/mic","0",qos=0,retain=True)
	client.publish("tgn/esp_1/analog/sensor_1","100",qos=0,retain=True)
	client.publish("tgn/esp_2/analog/sensor_1","100",qos=0,retain=True)
	client.publish("tgn/language",spr,qos=0,retain=True)
	client.publish("tgn/version",version,qos=0,retain=True)
	client.publish("tgn/buttons/status/1",b1,qos=0,retain=True)
	client.publish("tgn/buttons/status/2",b2,qos=0,retain=True)
	client.publish("tgn/buttons/status/3",b3,qos=0,retain=True)
	client.publish("tgn/buttons/status/4",b4,qos=0,retain=True)
	client.publish("tgn/buttons/status/5",b5,qos=0,retain=True)
	client.publish("tgn/buttons/status/6",b6,qos=0,retain=True)
	client.publish("tgn/buttons/name/1",b1A,qos=0,retain=True)
	client.publish("tgn/buttons/name/2",b2A,qos=0,retain=True)
	client.publish("tgn/buttons/name/3",b3A,qos=0,retain=True)
	client.publish("tgn/buttons/name/4",b4A,qos=0,retain=True)
	client.publish("tgn/buttons/name/5",b5A,qos=0,retain=True)
	client.publish("tgn/buttons/name/6",b6A,qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/color","0.0.0.255",qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/color_cach","-65279",qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/brightness","10",qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/mode","normal",qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/setneo","nothing",qos=0,retain=True)
	if MCPpower == 1:
		client.publish("tgn/i2c/mcp","online",qos=0,retain=True)
	else:
		client.publish("tgn/i2c/mcp","offline",qos=0,retain=True)
	if RTCpower == 1:
		client.publish("tgn/i2c/rtc","online",qos=0,retain=True)
	else:
		client.publish("tgn/i2c/rtc","offline",qos=0,retain=True)
	if ifI2C(ROM_ADDRESS) == "found device":
		client.publish("tgn/i2c/eeprom","online",qos=0,retain=True)
	else:
		client.publish("tgn/i2c/eeprom","offline",qos=0,retain=True)
	if LCDpower == 1:
		client.publish("tgn/i2c/lcd","online",qos=0,retain=True)
	else:
		client.publish("tgn/i2c/lcd","offline",qos=0,retain=True)
def on():
	global son
	global soff
	if son == 0:
		soff = 0
		son = 1
		sound()
		msg = "Automatic_on"
		TextToSpeech((data[23].rstrip()),spr)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		if s1 == "1":
			client.publish("tgn/buttons/status/1","1",qos=0,retain=True)
		if s2 == "1":
			client.publish("tgn/buttons/status/2","1",qos=0,retain=True)
		if s3 == "1":
			client.publish("tgn/buttons/status/3","1",qos=0,retain=True)
		if s4 == "1":
			client.publish("tgn/buttons/status/4","1",qos=0,retain=True)
def off():
	global son
	global soff
	if soff == 0:
		soff = 1
		son = 0
		sound()
		msg = "Automatic_off"
		TextToSpeech((data[24].rstrip()),spr)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		if s1 == "1":
			client.publish("tgn/buttons/status/1","0",qos=0,retain=True)
		if s2 == "1":
			client.publish("tgn/buttons/status/2","0",qos=0,retain=True)
		if s3 == "1":
			client.publish("tgn/buttons/status/3","0",qos=0,retain=True)
		if s4 == "1":
			client.publish("tgn/buttons/status/4","0",qos=0,retain=True)
def sound():
	if su==1:
		if colorSet <= 8:
			os.system('mpg321 /home/pi/tgn_smart_home/sounds/button.mp3 &')
		else:
			os.system('mpg321 /home/pi/tgn_smart_home/sounds/lcars-button.mp3 &')
def alarm_go():
	global alarm_p
	if alarm_p == 0:
		if su==1:
			if colorSet <= 8:
				os.system('mpg321 /home/pi/tgn_smart_home/sounds/alarm.mp3 &')
			else:
				os.system('mpg321 /home/pi/tgn_smart_home/sounds/lcars-alarm.mp3 &')
		alarm_p = 1
	elif alarm_p == 1:
		time.sleep(60)
		alarm_p = 0	
def pcf8563ReadTimeB():
	cach_time = ""
	time_out = ""
	if RTCpower == 1:
		t = bus.read_i2c_block_data(address,register,7);
		t[0] = t[0]&0x7F  #sec
		t[1] = t[1]&0x7F  #min
		t[2] = t[2]&0x3F  #hour
		t[3] = t[3]&0x3F  #day
		t[4] = t[4]&0x07  #month   -> dayname
		t[5] = t[5]&0x1F  #dayname -> month
		cach_time = ("%x:%x" %(t[2],t[1]))
		time_out = "%s  20%x/%x/%x %x:%x" %(w[t[4]],t[6],t[5],t[3],t[2],t[1])
	else:
		from time import localtime
		time_out = strftime("%Y-%m-%d %H:%M:%S", localtime())
		hour = strftime("%H", localtime())
		min = strftime("%M", localtime())
		h1 = hour.find("0")
		m1 = min.find("0")
		if h1 == 0:
			h2 = hour.split("0")
			hour = h2[1]
		if m1 == 0:
			m2 = min.split("0")
			min = m2[1]
		cach_time = hour+":"+min
	on1,on2 = ontime.split("|")
	off1,off2 = offtime.split("|")
	ond = "yes"
	if ond == "yes" and cach_time == on1 or cach_time == on2:
		on()
	if ond == "yes" and cach_time == off1 or cach_time == off2:
		off()
	if alarm_s == "on" and alarm_t == cach_time:
		alarm_go()
	return(time_out)
def About():
	print("TGN Smart Home "+version)
	sound()
def callback1():
	setn = "python3 /home/pi/tgn_smart_home/libs/auto_cam.py video "+E1.get()
	sound()
	os.system(setn)
def callback2():
	setn = "python3 /home/pi/tgn_smart_home/libs/auto_cam.py capture 0"
	sound()
	os.system(setn)
def callback3():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/auto_cam.py timer 0"
	sound()
	os.system(setn)
def callback4():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/camGpio.py"
	sound()
	os.system(setn)
def callback5():
	setn = "python3 /home/pi/tgn_smart_home/libs/auto_cam.py preview 0"
	sound()
	TextToSpeech((data[15].rstrip()),spr)
	os.system(setn)
def callback6():
	sound()
	stream()
def callback7():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/digi-cam.py"
	sound()
	TextToSpeech((data[17].rstrip()),spr)
	os.system(setn)
def callback8():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	setRTC()
	time.sleep(5)
	if MCPpower == 1:
		mcp.output(2, 0)
		mcp.output(3, 1)
def callback9():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b1 == 0:
		msg = "Turn_on_" + buttons[0]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/1","1",qos=0,retain=True)
	else:
		msg = "Turn_off_" + buttons[0]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/1","0",qos=0,retain=True)
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback10():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b2 == 0:
		msg = "Turn_on_" + buttons[1]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/2","1",qos=0,retain=True)
	else:
		msg = "Turn_off_" + buttons[1]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/2","0",qos=0,retain=True)
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback11():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b3 == 0:
		msg = "Turn_on_" + buttons[2]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/3","1",qos=0,retain=True)
	else:
		msg = "Turn_off_" + buttons[2]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/3","0",qos=0,retain=True)
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback12():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b4 == 0:
		msg = "Turn_on_" + buttons[3]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/4","1",qos=0,retain=True)
	else:
		msg = "Turn_off_" + buttons[3]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/4","0",qos=0,retain=True)
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback13():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b5 == 0:
		msg = "Turn_on_" + buttons[4]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/5","1",qos=0,retain=True)
	else:
		msg = "Turn_off_" + buttons[4]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/5","0",qos=0,retain=True)
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback14():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b6 == 0:
		msg = "Turn_on_" + buttons[5]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/6","1",qos=0,retain=True)
	else:
		msg = "Turn_off_" + buttons[5]
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		client.publish("tgn/buttons/status/6","0",qos=0,retain=True)
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback15():
	sound()
	if MCPpower == 1:
		for i in range(int(MCP_num_gpios/2)):
			mcp.output(i, 0)
	mylcd.lcd_clear()
	mylcd.backlight(0)
	sevenseg.Clear()
	TextToSpeech((data[18].rstrip()),spr)
	call(['shutdown', '-h', 'now'], shell=False)
def callback16():
	sound()
	if MCPpower == 1:
		for i in range(int(MCP_num_gpios/2)):
			mcp.output(i, 0)
	mylcd.lcd_clear()
	mylcd.backlight(0)
	sevenseg.Clear()
	TextToSpeech((data[19].rstrip()),spr)
	call(['reboot', '-h', 'now'], shell=False)
def callback17():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py rtc"
	os.system(setn)
def callback18():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py funk"
	os.system(setn)
def callback19():
	sound()
	global screen
	if screen == 1:
		screen = 0
	else:
		screen = 1
	write_eeprom(1,ROM_ADDRESS,0x00,0x67,str(screen))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback20():
	sound()
	global LCDpower
	TextToSpeech((data[21].rstrip()),spr)
	if LCDpower == 1:
		LCDpower = 0
		mylcd.lcd_clear()
		mylcd.backlight(0)
		sevenseg.Clear()
	else:
		LCDpower = 1
		mylcd.lcd_display_string("TGN Smart Home", 1, 1)
		mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
		mylcd.backlight(1)
def callback21():
	sound()
	global backlight
	TextToSpeech((data[22].rstrip()),spr)
	if backlight == 1:
		backlight = 0
		mylcd.backlight(0)
	else:
		backlight = 1
		mylcd.backlight(1)
def callback22():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py install_rom"
	sound()
	os.system(setn)
def callback23():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py cam"
	sound()
	os.system(setn)
def callback24():
	subprocess.call('xset dpms force on', shell=True)
	sound()
def callback25():
	global su
	if su == 1:
		su = 0
		sound()
	else:
		su = 1
	write_eeprom(1,ROM_ADDRESS,0x00,0xa6,str(su))
def callback26():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py weather"
	os.system(setn)
def callback27():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py pushb"
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
def exit():
	if su==1 and is_connected(REMOTE_SERVER)=="Online":
		try:
			print(">>Load voice.config")
			f = open(spr_phat+"voice.config","r")
		except IOError:
    			print("cannot open voice.config.... file not found")
		else:
			data = []
			for line in f:
				data.append(line)
			TextToSpeech((data[5].rstrip()),spr)
	if LCDpower == 1:
		mylcd.backlight(0)
		time.sleep(1)
		mylcd.lcd_clear()
		time.sleep(1)
		mylcd.backlight(0)
	if MCPpower == 1:
		for i in range(int(MCP_num_gpios/2)):
			mcp.output(i, 0)
	root.quit()
def all_off():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	subprocess.call('xset dpms force on', shell=True)
	msg = "all_off"
	TextToSpeech((data[14].rstrip()),spr)
	os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
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
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def all_on():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	subprocess.call('xset dpms force on', shell=True)
	msg = "all_on"
	TextToSpeech((data[13].rstrip()),spr)
	os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
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
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
	time.sleep(1)
def callback30():
	if ifI2C(NFC_ADDRESS) == "found device":
		pn532 = Pn532_i2c()
		pn532.SAMconfigure()
		TextToSpeech((data[20].rstrip()),spr)
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
					if LCDpower == 1:
						mylcd.backlight(0)
						time.sleep(1)
						mylcd.lcd_clear()
						time.sleep(1)
						mylcd.backlight(0)
					call(['shutdown', '-h', 'now'], shell=False)
def callback33():
	client.publish("tgn/system/mic","0",qos=0,retain=True)
	sound()
	try:
		f = open(spr_phat+"voice.config","r")
	except IOError:
    		print("cannot open voice.config.... file not found")
	else:
		data = []
		for line in f:
			data.append(line)
		keyword1 = (data[0].rstrip())
		keyword2 = (data[1].rstrip())
		keyword3 = (data[2].rstrip())
		keyword4 = (data[3].rstrip())
		keyword5 = buttons[0]
		keyword6 = buttons[1]
		keyword7 = buttons[2]
		keyword8 = buttons[3]
		keyword9 = buttons[4]
		keyword10 = buttons[5]
		output3 = (data[6].rstrip())
	tex = SpeechToText(spr,"AIzaSyDDzPM2W74MU3NvWgRKG85b3-UWaNOAjQo")
	if tex == keyword3.lower():
		exit()
	elif tex == keyword4.lower():
		if LCDpower == 1:
			mylcd.backlight(0)
			time.sleep(1)
			mylcd.lcd_clear()
			time.sleep(1)
			mylcd.backlight(0)
		call(['shutdown', '-h', 'now'], shell=False)
	elif tex == keyword2.lower():
		all_off()
	elif tex == keyword1.lower():
		all_on()
	elif tex == keyword5.lower():
		callback9()
	elif tex == keyword6.lower():
		callback10()
	elif tex == keyword7.lower():
		callback11()
	elif tex == keyword8.lower():
		callback12()
	elif tex == keyword9.lower():
		callback13()
	elif tex == keyword10.lower():
		callback14()
	else:
		if su==1 and is_connected(REMOTE_SERVER)=="Online":
			TextToSpeech(output3+tex,spr)
def callback32():
	global speech
	if speech == 0:
		speech = 1
	elif speech == 1:
		speech = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0xf2,str(speech))
	sound()
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback34():
	global Ts
	if Ts == 0:
		Ts = 1
	elif Ts == 1:
		Ts = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0xf3,str(Ts))
	sound()
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback35():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py thinkspeak"
	os.system(setn)
def callback36():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py webapp"
	os.system(setn)
def callback38():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py alarm"
	os.system(setn)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback39():
	global alarm_s
	if alarm_s == "on":
		alarm_s = "off"
	elif alarm_s == "off":
		alarm_s = "on"
	start_add_AC = 0x57
	index = 0
	sound()
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
def callback40():
    TextToSpeech(we_cach,spr)
def callback41():
	sound()
	TextToSpeech((data[25].rstrip()),spr)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback42():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py rss"
	os.system(setn)
def callback43():
    TextToSpeech(rssfeed,rsslang)
def callback44():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/update.py"
	sound()
	os.system(setn)
	time.sleep(5)
	os.execv(sys.executable, ['python3'] + sys.argv)
#broker mesage
def on_message(client, userdata, message):
	global esp_temp
	global esp_hum
	global esp_temp_2
	global esp_hum_2
	global esp_rssi
	global esp_li
	global b6
	global b5
	global b4
	global b3
	global b2
	global b1
	global esp_pr_2
	global esp_rssi_2 
	global esp_li_2
	global esp_b1_2
	if(message.topic=="tgn/esp_2/wifi/pre"):
		esp_pr_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/wifi/rssi"):
		esp_rssi_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/analog/sensor_1"):
		esp_li_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/button/b1"):
		esp_b1_2 = str(message.payload.decode("utf-8"))
		if(esp_b1_2 == "off"):
			mcp.output(6, 1)
			mcp.output(7, 0)
			esp_b1_2 = "No Rain"
		else:
			mcp.output(7, 1)
			mcp.output(6, 0)
			esp_b1_2 = "Rain"	
	if(message.topic=="tgn/esp_1/temp/sensor_1"):
		esp_temp = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_1/temp/sensor_2"):
		esp_hum = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/temp/sensor_1"):
    		esp_temp_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/temp/sensor_2"):
		esp_hum_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_1/wifi/rssi"):
		esp_rssi = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_1/analog/sensor_1"):
		esp_li = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/6"):
		if(int(message.payload.decode("utf-8")) != b6):
			b6 = int(message.payload.decode("utf-8"))
			send(6,b6)
			write_eeprom(1,ROM_ADDRESS,0x00,0x06,str(b6))
			TextToSpeech(buttons[5],spr)
	if(message.topic=="tgn/buttons/status/5"):
		if(int(message.payload.decode("utf-8")) != b5):
			b5 = int(message.payload.decode("utf-8"))
			send(5,b5)
			write_eeprom(1,ROM_ADDRESS,0x00,0x05,str(b5))
			TextToSpeech(buttons[4],spr)
	if(message.topic=="tgn/buttons/status/4"):
		if(int(message.payload.decode("utf-8")) != b4):
			b4 = int(message.payload.decode("utf-8"))
			send(4,b4)
			write_eeprom(1,ROM_ADDRESS,0x00,0x04,str(b4))
			TextToSpeech(buttons[3],spr)
	if(message.topic=="tgn/buttons/status/3"):
		if(int(message.payload.decode("utf-8")) != b3):
			b3 = int(message.payload.decode("utf-8"))
			send(3,b3)
			write_eeprom(1,ROM_ADDRESS,0x00,0x03,str(b3))
			TextToSpeech(buttons[2],spr)
	if(message.topic=="tgn/buttons/status/2"):
		if(int(message.payload.decode("utf-8")) != b2):
			b2 = int(message.payload.decode("utf-8"))
			send(2,b2)
			write_eeprom(1,ROM_ADDRESS,0x00,0x02,str(b2))
			TextToSpeech(buttons[1],spr)
	if(message.topic=="tgn/buttons/status/1"):
		if(int(message.payload.decode("utf-8")) != b1):
			b1 = int(message.payload.decode("utf-8"))
			send(1,b1)
			write_eeprom(1,ROM_ADDRESS,0x00,0x01,str(b1))
			TextToSpeech(buttons[0],spr)
	if(message.topic=="tgn/system/shutdown"):
		if(int(message.payload.decode("utf-8")) == 1):
			TextToSpeech("Shutdown",spr)
			sound()
			if MCPpower == 1:
				mcp.output(3, 0)
			mylcd.lcd_clear()
			mylcd.backlight(0)
			call(['shutdown', '-h', 'now'], shell=False)
	if(message.topic=="tgn/system/reboot"):
		if(int(message.payload.decode("utf-8")) == 1):
			TextToSpeech("Reboot",spr)
			sound()
			if MCPpower == 1:
				mcp.output(3, 0)
			mylcd.lcd_clear()
			mylcd.backlight(0)
			call(['reboot', '-h', 'now'], shell=False)
	if(message.topic=="tgn/system/weather"):
		if(int(message.payload.decode("utf-8")) == 1):
			client.publish("tgn/system/weather","0",qos=0,retain=True)
			callback40()
	if(message.topic=="tgn/system/mic"):
		if(int(message.payload.decode("utf-8")) == 1):
			client.publish("tgn/system/mic","0",qos=0,retain=True)
			callback33()
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
			client.subscribe(main_topic)
			time.sleep(2)
			client.loop_stop()
			global the_time
			global counterLCD
			newtime = time.time()
			if newtime != the_time:
				if float(esp_temp) >= float(esp_temp_2):
					print("open window")
					mcp.output(0, 1)
				if MCPpower == 1:
					if mcp.input(8) >> 8 == 1:
						callback7() #digi-cam
					if mcp.input(9) >> 9 == 1:
						callback12() #light(button[3])
					if mcp.input(10) >> 10 == 1:
						callback24() #xste dpms
					if mcp.input(11) >> 11 == 1:
						all_off()    #all off
					if mcp.input(12) >> 12 == 1:
						all_on()     #all on
					if mcp.input(15) >> 15 == 1:
						callback15()     #shutdown
				stats = textswitch
				try:
					client.publish("tgn/cpu/temp",str(round(getCpuTemperature(),1)),qos=0,retain=True)
				except:
					client.connect(get_ip())
					client.loop_start()
				if b1 == 0:
					stats=stats+'OFF|'
				if b1 == 1:
					stats=stats+'On|'
				if b2 == 0:
					stats=stats+'OFF|'
				if b2 == 1:
					stats=stats+'On|'
				if b3 == 0:
					stats=stats+'OFF|'
				if b3 == 1:
					stats=stats+'On|'
				if b4 == 0:
					stats=stats+'OFF|'
				if b4 == 1:
					stats=stats+'On|'
				if b5 == 0:
					stats=stats+'OFF|'
				if b5 == 1:
					stats=stats+'On|'
				if b6 == 0:
					stats=stats+'OFF|'
				if b6 == 1:
					stats=stats+'On|'
				if LCDpower == 1:
					counterLCD = counterLCD + 1
				if counterLCD == 30 and LCDpower == 1:
					mylcd.lcd_clear()
					mylcd.lcd_display_string("TGN Smart Home", 1, 1)
					mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
					sevenseg.Clear()
				if counterLCD == 60 and LCDpower == 1:
					mylcd.lcd_clear()
					r = requests.get(api_url)
					dataPIhole = json.loads(r.text)
					DNSQUERIES = dataPIhole['dns_queries_today']
					ADSBLOCKED = dataPIhole['ads_blocked_today']
					CLIENTS = dataPIhole['unique_clients']
					mylcd.lcd_display_string("Ad Blocked:"+str(ADSBLOCKED), 1, 0)
					mylcd.lcd_display_string("Queries:"+str(DNSQUERIES), 2, 0)
					seven_seg(str(ADSBLOCKED))
					counterLCD = 0
				if backlight == 0 and LCDpower == 1:
					mylcd.backlight(0)
				trigger = pcf8563ReadTimeB()
				the_time= format_time(pcf8563ReadTime())+"\n"+textcpu+" "+str(round(getCpuTemperature(),1))+"°C\n"+stats
				global afbground
				global fground
				if colorSet == 9:
					afbground = '#000000'
					fground = '#003f7e'
				self.display_time.config(text=the_time, font=('times', 18, 'bold'), bg=afbground, fg=fground)
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
				r = requests.get(api_url)
				dataPIhole = json.loads(r.text)
				DNSQUERIES = dataPIhole['dns_queries_today']
				ADSBLOCKED = dataPIhole['ads_blocked_today']
				CLIENTS = dataPIhole['unique_clients']
				temp_data = "Room Luxmeter:"
				try:
					f = open(spr_phat+"text.config","r")
				except IOError:
    					print("cannot open text.config.... file not found")
				else:
					dataText = []
					for line in f:
						dataText.append(line)
				output = ''
				if is_connected(REMOTE_SERVER)=="Online":
					global esp_ls
					global rssfeed
					if rssurl == "empty":
						rssfeed = "Please set a Newsfeed"
					else:
						rssfeed = rss(rssurl,10)
					if esp_ls == 0 and int(esp_li) < esp_switch:
						esp_ls = 1
						on()
					elif esp_ls == 1 and int(esp_li) > esp_switch_b:
						esp_ls = 0
						off()
					if allowed_key(openweatherkey) == "yes":
						data = weather_info(zipcode,openweatherkey)
						m_symbol = '\xb0' + 'C'
						output = output+(dataText[24].rstrip())+data['city']+','+data['country']+'\n'
						output = output+str(data['temp'])+'°C  '+data['sky']+' '
						output = output+(dataText[25].rstrip())+str(data['temp_max'])+'°C, '+(dataText[26].rstrip())+str(data['temp_min'])+'°C\n'
						output = output+(dataText[27].rstrip())+str(data['wind'])+'km/h \n'
						output = output+(dataText[28].rstrip())+str(data['humidity'])+'% \n'
						output = output+(dataText[29].rstrip())+str(data['cloudiness'])+'% \n'
						output = output+(dataText[30].rstrip())+str(data['pressure'])+'hpa \n'
						output = output+(dataText[31].rstrip())+str(data['sunrise'])+" "+(dataText[32].rstrip())+str(data['sunset'])+'\n'
						output = output+'---------------------------------------------------------\n'
						output = output+'ESP:'+esp_temp+'°C / '+esp_hum+'% / '+esp_rssi+'dbm / '+esp_li+'LUX\n'
						output = output+'ESP2:'+esp_temp_2+'°C / '+esp_b1_2+' / '+esp_rssi_2+'dbm / '+esp_li_2+'LUX\n'
						output = output+'---------------------------------------------------------\n'
						output = output+temp_data+" / "+str(readLight())+'LUX\n'
						global weather_t
						global weather_c
						global weather_w
						global weather_h
						weather_t = float(data['temp'])
						weather_c = int(data['cloudiness'])
						weather_w = float(data['wind'])
						weather_h = int(data['humidity'])
						client.publish("tgn/weather/temp",weather_t,qos=0,retain=True)
						client.publish("tgn/weather/clouds",weather_c,qos=0,retain=True)
						client.publish("tgn/weather/wind",weather_w,qos=0,retain=True)
						client.publish("tgn/weather/humidity",weather_h,qos=0,retain=True)
						client.publish("tgn/pihole/adBlock",ADSBLOCKED,qos=0,retain=True)
						client.publish("tgn/pihole/queries",DNSQUERIES,qos=0,retain=True)
						client.publish("tgn/pihole/clients",CLIENTS,qos=0,retain=True)
						client.publish("tgn/room/temp",temp_data,qos=0,retain=True)
						client.publish("tgn/room/light",readLight(),qos=0,retain=True)
						client.publish("tgn/weather/icon",str(data['icon']),qos=0,retain=True)
						global we_cach
						we_cach = "Temperature "+str(weather_t)+"°C \n Max Temperature "+str(data['temp_max'])+" °C \n Sky "+data['sky']+"\n Windspeed "+str(data['wind'])
					else:
						output = output+(dataText[35].rstrip())+'\n'
					output = output+'---------------------------------------------------------\n'
				output = output+'Ad Blocked:'+str(ADSBLOCKED)+' Client:'+str(CLIENTS)+' DNS Queries:'+str(DNSQUERIES)
				#channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
				global cpu_t
				cpu_t = getCpuTemperature()
				if Ts == 1:
					timespl = format_time(pcf8563ReadTime()).split(" ")
					#print(write_ts(channel,esp_temp_2,esp_hum_2,weather_t,weather_c,weather_w,cpu_t,weather_h))
					output = output+'\n'+(dataText[36].rstrip()+' Update:'+timespl[3])
					client.publish("tgn/system/update",timespl[3],qos=0,retain=True)
				global afbground
				global fground
				if colorSet == 9:
					afbground = '#000000'
					fground = '#eaa424'
				self.display_time.config(text=output, font=('times', 17, 'bold'), bg=afbground, fg=fground)
				if is_connected(REMOTE_SERVER)=="Online":
					if allowed_key(openweatherkey) == "yes":
						phatI = phat+get_icon_name(str(data['icon']))
						load = Image.open(phatI)
						render = ImageTk.PhotoImage(load)
						img = Label(self, image=render)
						img.image = render
						img.config(bg=afbground)
						img.place(x=0, y=60)
			self.display_time.after(1200000, change_value_the_timeb)
		change_value_the_timeb()
#window (RSS Feed)
class WindowC(Frame):
	def __init__(self,master):
		global afbground
		global fground
		if colorSet == 9:
			afbground = '#000000'
			fground = '#eaa424'
		Frame.__init__(self, master)
		self.grid()
		self.canvas = Canvas(self, bg=afbground, highlightthickness=0, width=453, height=40)
		self.canvas.pack(expand=True)
		xpos = 450
		ypos = 20
		self.canvas.create_text(xpos, ypos, anchor='w', text=rssfeed,font=('Helvetica 20 bold'), fill=fground, tags='text')
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
def spt1():
	global spr
	spr = "de"
	sound()
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(1))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt2():
	global spr
	spr = "en"
	sound()
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(2))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt3():
	global spr
	spr = "fr"
	sound()
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(3))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt4():
	global spr
	spr = "ru"
	sound()
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(4))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt5():
	global spr
	spr = "ja"
	sound()
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(5))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def spt6():
	global spr
	spr = "zh"
	sound()
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(6))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback45():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py backup"
	sound()
	os.system(setn)
def callback46():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py restore"
	sound()
	os.system(setn)
def callback100():
	print("empty button")
	sound()
def set_neo():
	sound()
	client.publish("tgn/esp_3/neopixel/brightness",str(SL1.get()),qos=0,retain=True)
	TextToSpeech((data[11].rstrip()),spr)
def red_neo():
	client.publish("tgn/esp_3/neopixel/color","255.0.0.255",qos=0,retain=True)
	sound()
	TextToSpeech((data[7].rstrip()),spr)
def green_neo():
	client.publish("tgn/esp_3/neopixel/color","0.255.0.255",qos=0,retain=True)
	sound()
	TextToSpeech((data[8].rstrip()),spr)
def blue_neo():
	client.publish("tgn/esp_3/neopixel/color","0.0.255.255",qos=0,retain=True)
	sound()
	TextToSpeech((data[9].rstrip()),spr)
def off_neo():
	client.publish("tgn/esp_3/neopixel/color","0.0.0.255",qos=0,retain=True)
	sound()
	TextToSpeech((data[10].rstrip()),spr)
def color_neo():
	color = askcolor()
	TextToSpeech((data[12].rstrip()),spr)
	cach1 = str(color).split('),')
	cach2 = cach1[0].split('(', 2)
	cach3 = cach2[2].split(', ')
	c_x = cach3[0].split('.')
	c_y = cach3[1].split('.')
	c_z = cach3[2].split('.')
	color_set = c_x[0]+"."+c_y[0]+"."+c_z[0]
	client.publish("tgn/esp_3/neopixel/color",color_set,qos=0,retain=True)
	sound()
def splash():
	import tkinter as tk
	root = tk.Tk()
	root.overrideredirect(True)
	WMWIDTH, WMHEIGHT, WMLEFT, WMTOP = root.winfo_screenwidth(), root.winfo_screenheight(), 0, 0
	root.geometry("%dx%d+%d+%d" % (WMWIDTH, WMHEIGHT, WMLEFT, WMTOP))
	image_file = "/home/pi/tgn_smart_home/icons/splashScreen.gif"
	image = tk.PhotoImage(file=image_file)
	canvas = tk.Canvas(root, height=WMHEIGHT, width=WMWIDTH, bg="black")
	canvas.create_image(WMWIDTH/2, WMHEIGHT/2, image=image)
	canvas.pack()
	root.after(45000, root.destroy)
	root.mainloop()
#Main Prog
Process(target=splash).start()
ini()
if LCDpower == 1:
	mylcd.lcd_display_string("TGN Smart Home", 1, 1)
	mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
if MCPpower == 1:
	mcp.output(3, 1)
if su==1 and is_connected(REMOTE_SERVER)=="Online":
	try:
		f = open(spr_phat+"voice.config","r")
	except IOError:
    		print("cannot open voice.config.... file not found")
	else:
		data = []
		for line in f:
			data.append(line)
		if spr != "zh":
			print("Start Voice Modul")
			TextToSpeech((data[4].rstrip()),spr)
sevenseg.Clear()

def normal_screen():
	root = Tk()
	#sfullscreen mode
	WMWIDTH, WMHEIGHT, WMLEFT, WMTOP = root.winfo_screenwidth(), root.winfo_screenheight(), 0, 0
	root.overrideredirect(screen) 
	root.geometry("%dx%d+%d+%d" % (WMWIDTH, WMHEIGHT, WMLEFT, WMTOP))

	try:
		f = open(spr_phat+"text.config","r")
	except IOError:
			print("cannot open text.config.... file not found")
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
	filemenu.add_command(label=(data[39].rstrip()), command=callback7)
	filemenu.add_separator()
	filemenu.add_command(label="Reload", command=callback41)
	filemenu.add_command(label=(data[40].rstrip()), command=callback30)
	filemenu.add_command(label="Backup Rom", command=callback45)
	filemenu.add_command(label="Restore Rom", command=callback46)

	setmenu = Menu(menu)
	menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
	setmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
	menu.add_cascade(label=(data[41].rstrip()), menu=setmenu)
	setmenu.add_command(label=(data[115].rstrip()), command=callback39)
	setmenu.add_command(label=(data[42].rstrip()), command=callback25)
	setmenu.add_command(label=(data[43].rstrip()), command=callback32)
	setmenu.add_command(label=(data[44].rstrip()), command=callback34)

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
	helpmenu.add_command(label="Update", command=callback44)
	helpmenu.add_command(label=(data[68].rstrip()), command=About)

	leftFrame = Frame(root, width=400, height = 400)
	leftFrame.configure(background=bground)
	leftFrame.grid(row=0, column=0, padx=10, pady=3)

	infFrame1 = Frame(leftFrame)
	infFrame1.configure(background=bground)
	infFrame1.grid(row=0, column=0, padx=10, pady=3)

	rightFrame = Frame(root, width=400, height = 400)
	rightFrame.configure(background=bground)
	rightFrame.grid(row=0, column=1, padx=10, pady=3)

	app=Window(rightFrame)

	buttonFrame = Frame(rightFrame)
	buttonFrame.configure(background=bground)
	buttonFrame.grid(row=2, column=0, padx=10, pady=3)
	buttonLabel1 = Label(buttonFrame, text=(data[0].rstrip()))
	buttonLabel1.configure(background=bground, foreground=fground)
	buttonLabel1.grid(row=0, column=1, padx=10, pady=3)
	B4 = Button(buttonFrame, text=(data[3].rstrip()), bg=buttonb, fg=fground, width=15, command=callback5)
	B4.grid(row=3, column=0, padx=10, pady=3)
	B7 = Button(buttonFrame, text=(data[7].rstrip()), bg=buttonb, fg=fground, width=15, command=callback7)
	B7.grid(row=3, column=1, padx=10, pady=3)
	B6 = Button(buttonFrame, text=(data[8].rstrip()), bg=buttonb, fg=fground, width=15, command=callback6)
	B6.grid(row=3, column=2, padx=10, pady=3)

	buttonFrame1 = Frame(rightFrame)
	buttonFrame1.configure(background=bground)
	buttonFrame1.grid(row=3, column=0, padx=10, pady=3)
	buttonLabel1 = Label(buttonFrame1, text=(data[9].rstrip()))
	buttonLabel1.configure(background=bground, foreground=fground)
	buttonLabel1.grid(row=0, column=1, padx=10, pady=3)

	B1 = Button(buttonFrame1, text=buttons[0], bg=buttonb, fg=fground, width=15, command=callback9)
	B1.grid(row=1, column=0, padx=10, pady=3) 
	B2 = Button(buttonFrame1, text=buttons[1], bg=buttonb, fg=fground, width=15, command=callback10)
	B2.grid(row=1, column=1, padx=10, pady=3)
	B3 = Button(buttonFrame1, text=buttons[2], bg=buttonb, fg=fground, width=15, command=callback11)
	B3.grid(row=1, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame1, text=buttons[3], bg=buttonb, fg=fground, width=15, command=callback12)
	B4.grid(row=2, column=0, padx=10, pady=3)
	B5 = Button(buttonFrame1, text=buttons[4], bg=buttonb, fg=fground, width=15, command=callback13)
	B5.grid(row=2, column=1, padx=10, pady=3)
	B6 = Button(buttonFrame1, text=buttons[5], bg=buttonb, fg=fground, width=15, command=callback14)
	B6.grid(row=2, column=2, padx=10, pady=3)
	B7 = Button(buttonFrame1, text=(data[108].rstrip()), bg=buttonb, fg=fground, width=15, command=all_on)
	B7.grid(row=3, column=0, padx=10, pady=3)
	B8 = Button(buttonFrame1, text=(data[109].rstrip()), bg=buttonb, fg=fground, width=15, command=all_off)
	B8.grid(row=3, column=1, padx=10, pady=3)
	if speech == 1 and is_connected(REMOTE_SERVER)=="Online":
		B9 = Button(buttonFrame1, text=(data[10].rstrip()), bg=buttona, fg=fground, width=15, command=callback33)
		B9.grid(row=3, column=2, padx=10, pady=3)

	buttonFrame2 = Frame(rightFrame)
	buttonFrame2.configure(background=bground)
	buttonFrame2.grid(row=4, column=0, padx=10, pady=3)
	buttonLabel2 = Label(buttonFrame2, text=(data[15].rstrip()))
	buttonLabel2.configure(background=bground, foreground=fground)
	buttonLabel2.grid(row=0, column=1, padx=10, pady=3)

	B1 = Button(buttonFrame2, text=(data[17].rstrip()), bg=buttonb, fg=fground, width=15, command=callback15)
	B1.grid(row=1, column=0, padx=10, pady=3)
	B2 = Button(buttonFrame2, text=(data[16].rstrip()), bg=buttonb, fg=fground, width=15, command=callback16)
	B2.grid(row=1, column=1, padx=10, pady=3)
	if ifI2C(NFC_ADDRESS) == "found device":
		B3 = Button(buttonFrame2, text=(data[18].rstrip()), bg=buttona, fg=fground, width=15, command=callback30)
		B3.grid(row=1, column=2, padx=10, pady=3)
	else:
		B3 = Button(buttonFrame2, text=("xxx"), bg=buttona, fg=fground, width=15, command=callback100)
		B3.grid(row=1, column=2, padx=10, pady=3)

	buttonFrame3 = Frame(rightFrame)
	buttonFrame3.configure(background=bground)
	buttonFrame3.grid(row=5, column=0, padx=10, pady=3)

	B1 = Button(buttonFrame3, text=(data[22].rstrip()), bg=buttonb, fg=fground, width=10, command=callback20)
	B1.grid(row=0, column=0, padx=10, pady=3) 
	B2 = Button(buttonFrame3, text=(data[23].rstrip()), bg=buttonb, fg=fground, width=10, command=callback21)
	B2.grid(row=0, column=1, padx=10, pady=3)
	B3 = Button(buttonFrame3, text=(data[118].rstrip()), bg=buttonb, fg=fground, width=10, command=callback40)
	B3.grid(row=0, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame3, text=(data[122].rstrip()), bg=buttonb, fg=fground, width=9, command=callback43)
	B4.grid(row=0, column=3, padx=10, pady=3)

	buttonFrame4 = Frame(rightFrame)
	buttonFrame4.configure(background=bground)
	buttonFrame4.grid(row=6, column=0, padx=10, pady=3)
	buttonLabel4 = Label(buttonFrame4, text=(data[123].rstrip()))
	buttonLabel4.configure(background=bground, foreground=fground)
	buttonLabel4.grid(row=0, column=1, padx=10, pady=3)

	B1 = Button(buttonFrame4, text=(data[124].rstrip()), bg=buttonb, fg=fground, width=15, command=red_neo)
	B1.grid(row=1, column=0, padx=10, pady=3)
	B2 = Button(buttonFrame4, text=(data[125].rstrip()), bg=buttonb, fg=fground, width=15, command=green_neo)
	B2.grid(row=1, column=1, padx=10, pady=3)
	B3 = Button(buttonFrame4, text=(data[126].rstrip()), bg=buttonb, fg=fground, width=15, command=blue_neo)
	B3.grid(row=1, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame4, text=(data[127].rstrip()), bg=buttonb, fg=fground, width=15, command=off_neo)
	B4.grid(row=2, column=0, padx=10, pady=3)
	B5 = Button(buttonFrame4, text=(data[128].rstrip()), bg=buttonb, fg=fground, width=15, command=set_neo)
	B5.grid(row=2, column=1, padx=10, pady=3)
	B6 = Button(buttonFrame4, text=("ColorPicker"), bg=buttonb, fg=fground, width=15, command=color_neo)
	B6.grid(row=2, column=2, padx=10, pady=3)

	buttonFrame5 = Frame(rightFrame)
	buttonFrame5.configure(background=bground)
	buttonFrame5.grid(row=7, column=0, padx=10, pady=3)

	SL1 = Scale(buttonFrame5, from_=0, to=255,  length=480, bg=buttonb, fg=fground, tickinterval=20, label=(data[129].rstrip()), orient=HORIZONTAL)
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

	root.mainloop()

def lcars_screen():
	root = Tk()
	#sfullscreen mode
	WMWIDTH, WMHEIGHT, WMLEFT, WMTOP = root.winfo_screenwidth(), root.winfo_screenheight(), 0, 0
	root.overrideredirect(screen) 
	root.geometry("%dx%d+%d+%d" % (WMWIDTH, WMHEIGHT, WMLEFT, WMTOP))

	try:
		f = open(spr_phat+"text.config","r")
	except IOError:
			print("cannot open text.config.... file not found")
	else:
		data = []
		for line in f:
			data.append(line)
	root.wm_title("TGN Smart Home "+version+" ("+spr+")")
	menu = Menu(root)
	root.config(background = bground, menu=menu)

	filemenu = Menu(menu)
	menubar = Menu(root, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	filemenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	menu.add_cascade(label=(data[37].rstrip()), menu=filemenu)
	filemenu.add_command(label=(data[38].rstrip()), command=callback8)
	filemenu.add_command(label=(data[39].rstrip()), command=callback7)
	filemenu.add_separator()
	filemenu.add_command(label="Reload", command=callback41)
	filemenu.add_command(label=(data[40].rstrip()), command=callback30)
	filemenu.add_command(label="Backup Rom", command=callback45)
	filemenu.add_command(label="Restore Rom", command=callback46)

	setmenu = Menu(menu)
	menubar = Menu(root, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	setmenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	menu.add_cascade(label=(data[41].rstrip()), menu=setmenu)
	setmenu.add_command(label=(data[115].rstrip()), command=callback39)
	setmenu.add_command(label=(data[42].rstrip()), command=callback25)
	setmenu.add_command(label=(data[43].rstrip()), command=callback32)
	setmenu.add_command(label=(data[44].rstrip()), command=callback34)

	langmenu = Menu(menu)
	menubar = Menu(root, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	langmenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	setmenu.add_cascade(label=(data[45].rstrip()), menu=langmenu)
	langmenu.add_command(label="de", command=spt1)
	langmenu.add_command(label="en", command=spt2)
	langmenu.add_command(label="fr", command=spt3)
	langmenu.add_command(label="ru", command=spt4)
	langmenu.add_command(label="jp", command=spt5)
	langmenu.add_command(label="zh", command=spt6)

	stylemenu = Menu(menu)
	menubar = Menu(root, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	stylemenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	setmenu.add_cascade(label=(data[46].rstrip()), menu=stylemenu)
	stylemenu.add_command(label=(data[47].rstrip()), command=callback19)

	colmenu = Menu(menu)
	menubar = Menu(root, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	colmenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
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
			color_set = 9
		write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
		time.sleep(1)
		os.execv(sys.executable, ['python3'] + sys.argv)

	rommenu = Menu(menu)
	menubar = Menu(root, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	rommenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
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
	menubar = Menu(root, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	nfcmenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	setmenu.add_cascade(label=(data[63].rstrip()), menu=nfcmenu)
	nfcmenu.add_command(label=(data[64].rstrip()), command=callback28)
	nfcmenu.add_command(label=(data[65].rstrip()), command=callback29)
	nfcmenu.add_command(label=(data[66].rstrip()), command=callback31)

	helpmenu = Menu(menu)
	menubar = Menu(root, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	helpmenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
	menu.add_cascade(label=(data[67].rstrip()), menu=helpmenu)
	helpmenu.add_command(label="Update", command=callback44)
	helpmenu.add_command(label=(data[68].rstrip()), command=About)

	leftFrame = Frame(root, width=400, height = 400)
	leftFrame.configure(background=bground)
	leftFrame.grid(row=0, column=0, padx=10, pady=3)

	infFrame1 = Frame(leftFrame)
	infFrame1.configure(background=bground)
	infFrame1.grid(row=0, column=0, padx=10, pady=3)

	rightFrame = Frame(root, width=400, height = 400)
	rightFrame.configure(background=bground)
	rightFrame.grid(row=0, column=1, padx=10, pady=3)

	app=Window(rightFrame)

	buttonFrame = Frame(rightFrame)
	buttonFrame.configure(background='#000000')
	buttonFrame.grid(row=2, column=0, padx=10, pady=3)
	buttonLabel1 = Label(buttonFrame, text=(data[0].rstrip()))
	buttonLabel1.configure(background='#000000', foreground='#eaa424')
	buttonLabel1.grid(row=0, column=1, padx=10, pady=3)
	B4 = Button(buttonFrame, text=(data[3].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback5)
	B4.grid(row=3, column=0, padx=10, pady=3)
	B7 = Button(buttonFrame, text=(data[7].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback7)
	B7.grid(row=3, column=1, padx=10, pady=3)
	B6 = Button(buttonFrame, text=(data[8].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback6)
	B6.grid(row=3, column=2, padx=10, pady=3)

	buttonFrame1 = Frame(rightFrame)
	buttonFrame1.configure(background='#000000')
	buttonFrame1.grid(row=3, column=0, padx=10, pady=3)
	buttonLabel1 = Label(buttonFrame1, text=(data[9].rstrip()))
	buttonLabel1.configure(background='#000000', foreground='#eaa424')
	buttonLabel1.grid(row=0, column=1, padx=10, pady=3)

	B1 = Button(buttonFrame1, text=buttons[0], bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback9)
	B1.grid(row=1, column=0, padx=10, pady=3) 
	B2 = Button(buttonFrame1, text=buttons[1], bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback10)
	B2.grid(row=1, column=1, padx=10, pady=3)
	B3 = Button(buttonFrame1, text=buttons[2], bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback11)
	B3.grid(row=1, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame1, text=buttons[3], bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback12)
	B4.grid(row=2, column=0, padx=10, pady=3)
	B5 = Button(buttonFrame1, text=buttons[4], bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback13)
	B5.grid(row=2, column=1, padx=10, pady=3)
	B6 = Button(buttonFrame1, text=buttons[5], bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback14)
	B6.grid(row=2, column=2, padx=10, pady=3)
	B7 = Button(buttonFrame1, text=(data[108].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=all_on)
	B7.grid(row=3, column=0, padx=10, pady=3)
	B8 = Button(buttonFrame1, text=(data[109].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=all_off)
	B8.grid(row=3, column=1, padx=10, pady=3)
	if speech == 1 and is_connected(REMOTE_SERVER)=="Online":
		B9 = Button(buttonFrame1, text=(data[10].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback33)
		B9.grid(row=3, column=2, padx=10, pady=3)

	buttonFrame2 = Frame(rightFrame)
	buttonFrame2.configure(background='#000000')
	buttonFrame2.grid(row=4, column=0, padx=10, pady=3)
	buttonLabel2 = Label(buttonFrame2, text=(data[15].rstrip()))
	buttonLabel2.configure(background='#000000', foreground='#eaa424')
	buttonLabel2.grid(row=0, column=1, padx=10, pady=3)

	B1 = Button(buttonFrame2, text=(data[17].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback15)
	B1.grid(row=1, column=0, padx=10, pady=3)
	B2 = Button(buttonFrame2, text=(data[16].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback16)
	B2.grid(row=1, column=1, padx=10, pady=3)
	if ifI2C(NFC_ADDRESS) == "found device":
		B3 = Button(buttonFrame2, text=(data[18].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback30)
		B3.grid(row=1, column=2, padx=10, pady=3)
	else:
		B3 = Button(buttonFrame2, text=("xxx"), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=callback100)
		B3.grid(row=1, column=2, padx=10, pady=3)

	buttonFrame3 = Frame(rightFrame)
	buttonFrame3.configure(background=bground)
	buttonFrame3.grid(row=5, column=0, padx=10, pady=3)

	B1 = Button(buttonFrame3, text=(data[22].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=callback20)
	B1.grid(row=0, column=0, padx=10, pady=3) 
	B2 = Button(buttonFrame3, text=(data[23].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=callback21)
	B2.grid(row=0, column=1, padx=10, pady=3)
	B3 = Button(buttonFrame3, text=(data[118].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=callback40)
	B3.grid(row=0, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame3, text=(data[122].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=9, command=callback43)
	B4.grid(row=0, column=3, padx=10, pady=3)

	buttonFrame4 = Frame(rightFrame)
	buttonFrame4.configure(background='#000000')
	buttonFrame4.grid(row=6, column=0, padx=10, pady=3)
	buttonLabel4 = Label(buttonFrame4, text=(data[123].rstrip()))
	buttonLabel4.configure(background='#000000', foreground='#eaa424')
	buttonLabel4.grid(row=0, column=1, padx=10, pady=3)

	B1 = Button(buttonFrame4, text=(data[124].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=red_neo)
	B1.grid(row=1, column=0, padx=10, pady=3)
	B2 = Button(buttonFrame4, text=(data[125].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=green_neo)
	B2.grid(row=1, column=1, padx=10, pady=3)
	B3 = Button(buttonFrame4, text=(data[126].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=blue_neo)
	B3.grid(row=1, column=2, padx=10, pady=3)
	B4 = Button(buttonFrame4, text=(data[127].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=off_neo)
	B4.grid(row=2, column=0, padx=10, pady=3)
	B5 = Button(buttonFrame4, text=(data[128].rstrip()), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=set_neo)
	B5.grid(row=2, column=1, padx=10, pady=3)
	B6 = Button(buttonFrame4, text=("ColorPicker"), bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=15, command=color_neo)
	B6.grid(row=2, column=2, padx=10, pady=3)

	buttonFrame5 = Frame(rightFrame)
	buttonFrame5.configure(background='#000000')
	buttonFrame5.grid(row=7, column=0, padx=10, pady=3)

	SL1 = Scale(buttonFrame5, from_=0, to=255,  length=480, bg='#003f7e', fg='#000000', tickinterval=20, label=(data[129].rstrip()), orient=HORIZONTAL)
	SL1.grid(row=0, column=1, padx=10, pady=3)
	SL1.set(10)

	app=WindowB(leftFrame)

	seperatorFrame4 = Frame(leftFrame)
	seperatorFrame4.configure(background='#000000')
	seperatorFrame4.grid(row=2, column=0, padx=5, pady=3)
	seperatorLabel1 = Label(seperatorFrame4, text="")
	seperatorLabel1.configure(background='#000000')
	seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

	app=WindowC(leftFrame)

	seperatorFrame3 = Frame(leftFrame)
	seperatorFrame3.configure(background='#000000')
	seperatorFrame3.grid(row=4, column=0, padx=5, pady=3)
	seperatorLabel1 = Label(seperatorFrame3, text="")
	seperatorLabel1.configure(background='#000000')
	seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

	infFrame1 = Frame(leftFrame)
	infFrame1.configure(background='#000000')
	infFrame1.grid(row=4, column=0, padx=10, pady=3)
	infLabel1 = Label(infFrame1, text=(data[11].rstrip()))
	infLabel1.configure(background='#000000', foreground='#eaa424')
	infLabel1.grid(row=0, column=1, padx=10, pady=3)
	oText1 = (data[12].rstrip())+ontime
	infLabel2 = Label(infFrame1, text=oText1)
	infLabel2.configure(background='#000000', foreground='#eaa424')
	infLabel2.grid(row=1, column=0, padx=10, pady=3)
	oText2 = (data[13].rstrip())+offtime
	infLabel3 = Label(infFrame1, text=oText2)
	infLabel3.configure(background='#000000', foreground='#eaa424')
	infLabel3.grid(row=1, column=2, padx=10, pady=3)
	oText3 = (data[14].rstrip())+s1+s2+s3+s4
	infLabel4 = Label(infFrame1, text=oText3)
	infLabel4.configure(background='#000000', foreground='#eaa424')
	infLabel4.grid(row=1, column=1, padx=10, pady=3)
	oText4 = (data[110].rstrip()) + alarm_s
	infLabel5 = Label(infFrame1, text=oText4)
	infLabel5.configure(background='#000000', foreground='#eaa424')
	infLabel5.grid(row=2, column=0, padx=10, pady=3)
	oText5 = (data[111].rstrip()) + alarm_t
	infLabel6 = Label(infFrame1, text=oText5)
	infLabel6.configure(background='#000000', foreground='#eaa424')
	infLabel6.grid(row=2, column=2, padx=10, pady=3)

	root.mainloop()

if colorSet <= 8:
	normal_screen()
else:
    lcars_screen()
