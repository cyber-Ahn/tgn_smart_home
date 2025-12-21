#---load-libs---
from tgnLIB import *
import paho.mqtt.client as mqtt
import json
import thingspeak
from subprocess import call
from multiprocessing import Process
from tkinter import *
from tkinter.colorchooser import *
from mcstatus import MinecraftServer

#---var---
#i2c address list
LCD_ADDRESS = 0x00
MCP_ADDRESS = 0x00
NFC_ADDRESS = 0x00
ROM_CACH = 0x00
CLOCK_CACH = 0x00
GPS_CACH = 0x00

#thing speak
channel_id = 43245
write_key = "1234567890"
read_key = "1234567890"
#pushbullet, openweather key 
pushbulletkey = "1234567890"
openweatherkey = "1234567890"
zipcode = 1234567
#shelly door
shelly_topic = "shellies/#"
shelly_cach = {"wifi_sta":{"ssid": "Matrix"},}
shelly_message = "no data"
#system var
menu_on = 0
MCP_num_gpios = 16
main_topic = "tgn/#"
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
buttons = ["1", "2", "3", "4", "5", "6","7","8","9"]
b1 = 0
b2 = 0
b3 = 0
b4 = 0
b5 = 0
b6 = 0
b7 = 0
b8 = 0
b9 = 0
b1A = ""
b2A = ""
b3A = ""
b4A = ""
b5A = ""
b6A = ""
b7A = ""
b8A = ""
b9A = ""
weather_t = -0.41
weather_c = 0
weather_w = 4.1
weather_h = 10
we_cach = "no data"
cpu_t = 57.458
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
onoff_day = ["Mon","Tue","Wed","Thu","Fri","xxx","xxx"]
ond = "yes"
phat = "/home/pi/tgn_smart_home/icons/"
color_button = []
mqtt_msg = "empty"
mqtt_msg_cach = "empty"
day_n = ""
count_pos_b = "1"
hum_1 = "50.0"
hum_2 = "50.0"
hum_3 = "50.0"
hum_4 = "50.0"
counter_loop = 0
make_loop = 5 # 172 for 20 min ((20*60)/7)
#Pico
pico_temp = "0.02"
pico_temp_5 = "0.02"
pico_temp_6 = "0.02"
#ESP8622/1
esp_ls = 0
esp_switch = 27000
esp_switch_b = 40000
esp_temp = "0.02"
esp_hum = "1.1"
esp_rssi = "--"
esp_li = "100"
#ESP8622/2
esp_ip_2 = "---.---.---.---"
esp_pr_2 = "--"
esp_temp_2 = "0.05"
esp_hum_2 = "1.1"
esp_rssi_2 = "--"
esp_li_2 = "100"
esp_b1_2 = "off"
esp_switch_2 = 27000
esp_switch_2_b = 40000
esp_ls_2 = 0
esp_2_button = "5"
esp2_cou = 0
#ESP8622/3
esp_3_color = "0.0.0.255"
esp_3_game = "0"
#autoHum
autohum_stat = 0
autohum_stat_b = 0
autohum_on_time = "00:01"
autohum_off_time = "01:00"
autohum_on_var = "50.0"
autohum_botton = "0"
pico_hum = "76.0"
#RSS
rssfeed = "no feed"
rsslang = "en"
#PiHole
pihole_url = "http://192.168.0.00"
pihole_pw = 'pihole_pw'
DNSQUERIES = "xxx"
ADSBLOCKED = "xxx"
CLIENTS = "xxx"
DNSONLIST = "xxx"
PIHOLECSTATUS = "0"
#radar_cam
radar_on = 0
radar_sen = 0
radar_sw_pin = 25
radar_sw_state = 1
#minecraft server address
mc_add_s = "192.168.0.90"
mc_add_sV6 = "2a02:908:521:b820:2393:5e67:dba1:ebfb"
#test server
REMOTE_SERVER = "www.google.com"
#air conditioner
power_air = "off"
sol_temp = 25.1
sol_hum = 75.1
start_temp_cooler = 23.1
delay = 0.6
temp_is = 0.0
hum_is = 0.0
temp_out = 0.0
stat_air = 0
first_boot = "yes"
cach_air = 0
# ir Vars
ir_power = "x"
ir_fan = "x"
ir_cool = "x"
ir_dry = "x"
ir_up = "x"
ir_down = "x"
ir_topic = "x"


#---funktions---
def ini():
	logging_tgn("check_files","tgn_smart_home.log")
	os.system('clear')
	global spr
	global su
	Process(target=splash).start()
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
		if(su==1):
			Process(target=TextToSpeech, args=("MCP23017 configured",spr)).start()
	else:
		print(">>MCP23017 not found")
		if(su==1):
			Process(target=TextToSpeech, args=("MCP23017 not found",spr)).start()
	#LCD
	time.sleep(4)
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
		if(su==1):
			Process(target=TextToSpeech, args=("LCD Display configured",spr)).start()
	else:
		print(">>LCD Display not found")
		if(su==1):
			Process(target=TextToSpeech, args=("LCD Display not found",spr)).start()
	time.sleep(2)
	if ifI2C(ROM_ADDRESS) == "found device":
		if(su==1):
			Process(target=TextToSpeech, args=("ROM configured",spr)).start()
	else:
		print(">>ROM not found")
		if(su==1):
			Process(target=TextToSpeech, args=("ROM not found",spr)).start()
	global ontime
	global offtime
	global s1
	global s2
	global s3
	global s4
	global b1
	global b2
	global b3
	global b4
	global b5
	global b6
	global b7
	global b8
	global b9
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
	global buttons
	global openweatherkey
	global zipcode
	global pushbulletkey
	global speech
	global Ts
	global channel_id
	global write_key
	global read_key
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
	global b1A
	global b2A
	global b3A
	global b4A
	global b5A
	global b6A
	global b7A
	global b8A
	global b9A
	global menu_on
	if ifI2C(address) == "found device":
		RTCpower = 1
	print(">>initialize EEPROM")
	time.sleep(3)
	if ifI2C(ROM_ADDRESS) == "found device" or ifI2C(ROM_ADDRESS) == "not found":
		logging_tgn("Boot System - Read ROM","tgn_smart_home.log")
		start_add_U = 0xcf
		if(su==1):
			Process(target=TextToSpeech, args=("Read Rom",spr)).start()
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
		# code button
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
		start_add_AAA = 0x6d
		index = 0 
		b7A = ""
		while index < 10:
			cach = read_eeprom(1,ROM_ADDRESS,0x02,start_add_AAA)
			print(">>Read Byte "+str(start_add_AAA))
			if cach != "X":
				b7A = b7A + cach
			index = index + 1
			start_add_AAA = start_add_AAA+ 1
		start_add_AAB = 0x78
		index = 0 
		b8A = ""
		while index < 10:
			cach = read_eeprom(1,ROM_ADDRESS,0x02,start_add_AAB)
			print(">>Read Byte "+str(start_add_AAB))
			if cach != "X":
				b8A = b8A + cach
			index = index + 1
			start_add_AAB = start_add_AAB+ 1
		start_add_AAC = 0x83
		index = 0 
		b9A = ""
		while index < 10:
			cach = read_eeprom(1,ROM_ADDRESS,0x02,start_add_AAC)
			print(">>Read Byte "+str(start_add_AAC))
			if cach != "X":
				b9A = b9A + cach
			index = index + 1
			start_add_AAC = start_add_AAC+ 1
		buttons = []
		buttons.append(b1A)
		buttons.append(b2A)
		buttons.append(b3A)
		buttons.append(b4A)
		buttons.append(b5A)
		buttons.append(b6A)
		buttons.append(b7A)
		buttons.append(b8A)
		buttons.append(b9A)
		logging_tgn(b1A,"tgn_smart_home.log")
		logging_tgn(b2A,"tgn_smart_home.log")
		logging_tgn(b3A,"tgn_smart_home.log")
		logging_tgn(b4A,"tgn_smart_home.log")
		logging_tgn(b5A,"tgn_smart_home.log")
		logging_tgn(b6A,"tgn_smart_home.log")
		logging_tgn(b7A,"tgn_smart_home.log")
		logging_tgn(b8A,"tgn_smart_home.log")
		logging_tgn(b9A,"tgn_smart_home.log")
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
		dataX = read_eeprom(1,ROM_ADDRESS,0x02,0x6a)		
		b7=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x02,0x6b)
		b8=int(dataX)
		dataX = read_eeprom(1,ROM_ADDRESS,0x02,0x6c)
		b9=int(dataX)
		esp_2_button = read_eeprom(1,ROM_ADDRESS,0x01,0x5b)
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x07)
		colorSet=int(dataX)
		logging_tgn(str(colorSet),"tgn_smart_home.log")
		dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x67)
		screen=int(dataX)

		logging_tgn(str(screen),"tgn_smart_home.log")
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
		logging_tgn(version,"tgn_smart_home.log")
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
		logging_tgn(spr,"tgn_smart_home.log")
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
		logging_tgn(rssurl,"tgn_smart_home.log")
		menu_on = int(read_eeprom(1,ROM_ADDRESS,0x03,0x2b))
		print("Menu:"+str(menu_on))
	else:
		print(">>EEPROM not found")
		if(su==1):
			Process(target=TextToSpeech, args=("EEPROM not found",spr)).start()
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
		f = open(spr_phat+"text.lang","r")
	except IOError:
		print("cannot open text.lang.... file not found")
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
	
	try:
		f_d = open("/home/pi/tgn_smart_home/config/system.config","r")
		global onoff_day
		onoff_day = []
		count_d = 0
		line_cach = line.rstrip().split(":")
		for line in f_d:
			count_d = count_d + 1
			if count_d <= 7:
				onoff_day.append(line.rstrip().split(":")[1])
			if count_d == 9:
				global phat
				phat = line.rstrip().split(":")[1]
			if count_d == 10:
				global esp_switch
				esp_switch = int(line.rstrip().split(":")[1])
			if count_d == 11:
				global esp_switch_b
				esp_switch_b = int(line.rstrip().split(":")[1])
			if count_d == 12:
				global pihole_url
				pihole_url = line.rstrip().split("*")[1]
			if count_d == 15:
				global font_size_a
				font_size_a = int(line.rstrip().split(":")[1])
			if count_d == 16:
				global font_size_b
				font_size_b = int(line.rstrip().split(":")[1])
			if count_d == 17:
				global font_size_c
				font_size_c = int(line.rstrip().split(":")[1])
			if count_d == 18:
				global feed_size_width
				feed_size_width = int(line.rstrip().split(":")[1])
			if count_d == 19:
				global feed_size_height
				feed_size_height = int(line.rstrip().split(":")[1])
			if count_d == 20:
				global feed_pos_x
				feed_pos_x = int(line.rstrip().split(":")[1])
			if count_d == 21:
				global feed_pos_y
				feed_pos_y = int(line.rstrip().split(":")[1])
			if count_d == 22:
				global button_width_a
				button_width_a = int(line.rstrip().split(":")[1])
			if count_d == 23:
				global button_width_b
				button_width_b = int(line.rstrip().split(":")[1])
			if count_d == 24:
				global slider_length
				slider_length = int(line.rstrip().split(":")[1])
			if count_d == 26:
				global pihole_pw
				pihole_pw = decode(line.rstrip().split("*")[1])
			if count_d == 28:
				global autohum_on_time
				autohum_on_time = line.rstrip().split("*")[1]
			if count_d == 29:
				global autohum_off_time
				autohum_off_time = line.rstrip().split("*")[1]
			if count_d == 30:
				global autohum_on_var
				autohum_on_var = line.rstrip().split("*")[1]
			if count_d == 31:
				global autohum_botton
				autohum_botton = line.rstrip().split("*")[1]
			if count_d == 32:
				global sol_temp
				sol_temp = float(line.rstrip().split("*")[1])
			if count_d == 33:
				global sol_hum
				sol_hum = float(line.rstrip().split("*")[1])
			if count_d == 34:
				global start_temp_cooler
				start_temp_cooler= float(line.rstrip().split("*")[1])
			if count_d == 35:
				global delay
				delay= float(line.rstrip().split("*")[1])
			if count_d == 36:
				global ir_power
				ir_power = str(line.rstrip().split("*")[1])
			if count_d == 37:
				global ir_fan
				ir_fan = str(line.rstrip().split("*")[1])
			if count_d == 38:
				global ir_cool
				ir_cool = str(line.rstrip().split("*")[1])
			if count_d == 39:
				global ir_dry
				ir_dry = str(line.rstrip().split("*")[1])
			if count_d == 40:
				global ir_up
				ir_up = str(line.rstrip().split("*")[1])
			if count_d == 41:
				global ir_down
				ir_down = str(line.rstrip().split("*")[1])
			if count_d == 42:
				global ir_topic
				ir_topic = str(line.rstrip().split("*")[1])
		print(onoff_day)
	except IOError:
		print("cannot open system.config.... file not found")
	num_ip = 0
	try:
		print(">>Load ip_socket_list.config")
		f = open("/home/pi/tgn_smart_home/config/ip_socket_list.config","r")
	except IOError:
		print("cannot open ip_socket_list.config.... file not found")
	else:
		for line in f:
			num_ip = num_ip + 1
			print(str(num_ip)+":"+line.rstrip())
			client.publish("tgn/buttons/ip/"+str(num_ip),line.rstrip(),qos=0,retain=True)
	#send status to mqtt
	set_mqtt_start()

def set_mqtt_start():
	client.publish("tgn/pico/shutdown","0",qos=0,retain=True)
	client.publish("tgn/system/automatic","0",qos=0,retain=True)
	client.publish("tgn/system/autohum","0",qos=0,retain=True)
	client.publish("tgn/system/reboot","0",qos=0,retain=True)
	client.publish("tgn/system/reboot/esp1","0",qos=0,retain=True)
	client.publish("tgn/system/reboot/esp2","0",qos=0,retain=True)
	client.publish("tgn/system/reboot/esp3","0",qos=0,retain=True)
	client.publish("tgn/system/reboot/esp4","0",qos=0,retain=True)
	client.publish("tgn/system/reboot/cam","0",qos=0,retain=True)
	client.publish("tgn/system/reboot/sonoff","0",qos=0,retain=True)
	client.publish("tgn/ip",get_ip(),qos=0,retain=True)
	client.publish("tgn/system/shutdown","0",qos=0,retain=True)
	client.publish("tgn/system/radar","0",qos=0,retain=True)
	client.publish("tgn/bot/shutdown","0",qos=0,retain=True)
	client.publish("tgn/bot/status","offline",qos=0,retain=True)
	client.publish("tgn/system/weather","0",qos=0,retain=True)
	client.publish("tgn/system/mic","0",qos=0,retain=True)
	client.publish("tgn/system/clock","0",qos=0,retain=True)
	client.publish("tgn/esp_1/analog/sensor_1","50",qos=0,retain=True)
	client.publish("tgn/esp_2/analog/sensor_1","200",qos=0,retain=True)
	client.publish("tgn/language",spr,qos=0,retain=True)
	client.publish("tgn/version",version,qos=0,retain=True)
	client.publish("tgn/buttons/status/1",b1,qos=0,retain=True)
	client.publish("tgn/buttons/status/2",b2,qos=0,retain=True)
	client.publish("tgn/buttons/status/3",b3,qos=0,retain=True)
	client.publish("tgn/buttons/status/4",b4,qos=0,retain=True)
	client.publish("tgn/buttons/status/5",b5,qos=0,retain=True)
	client.publish("tgn/buttons/status/6",b6,qos=0,retain=True)
	client.publish("tgn/buttons/status/7",b7,qos=0,retain=True)
	client.publish("tgn/buttons/status/8",b8,qos=0,retain=True)
	client.publish("tgn/buttons/status/9",b9,qos=0,retain=True)
	client.publish("tgn/buttons/name/1",b1A,qos=0,retain=True)
	client.publish("tgn/buttons/name/2",b2A,qos=0,retain=True)
	client.publish("tgn/buttons/name/3",b3A,qos=0,retain=True)
	client.publish("tgn/buttons/name/4",b4A,qos=0,retain=True)
	client.publish("tgn/buttons/name/5",b5A,qos=0,retain=True)
	client.publish("tgn/buttons/name/6",b6A,qos=0,retain=True)
	client.publish("tgn/buttons/name/7",b7A,qos=0,retain=True)
	client.publish("tgn/buttons/name/8",b8A,qos=0,retain=True)
	client.publish("tgn/buttons/name/9",b9A,qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/color","0.0.0.255",qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/color_cach","-65279",qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/brightness","10",qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/mode","normal",qos=0,retain=True)
	client.publish("tgn/esp_3/neopixel/setneo","nothing",qos=0,retain=True)
	client.publish("tgn/mqtt-msg","System Online",qos=0,retain=True)
	client.publish("tgn/gesture/touch","0",qos=0,retain=True)
	client.publish("tgn/gesture/btn_ni_li","6",qos=0,retain=True)
	client.publish("tgn/weather/rain","no Rain",qos=0,retain=True)
	out_size=format_byte_size(get_dir_size(r"/home/pi/tgn_smart_home/log"))
	client.publish("tgn/system/log",out_size,qos=0,retain=True)
	client.publish("tgn/esp_1/temp/sensor_1","21.0",qos=0,retain=True)
	client.publish("tgn/esp_2/temp/sensor_1","21.0",qos=0,retain=True)
	client.publish("tgn/pico_1/temp/sensor_2","40.0",qos=0,retain=True)
	client.publish("tgn/pico_1/temp/sensor_1","21.0",qos=0,retain=True)
	client.publish("tgn/pico_5/temp/sensor_2","40.0",qos=0,retain=True)
	client.publish("tgn/pico_5/temp/sensor_1","21.0",qos=0,retain=True)
	client.publish("tgn/pico_6/temp/sensor_2","40.0",qos=0,retain=True)
	client.publish("tgn/pico_6/temp/sensor_1","21.0",qos=0,retain=True)
	client.publish("tgn/buttons/status/8","0",qos=0,retain=True)
	client.publish("tgn/android/pmsg","V1.9",qos=0,retain=True)
	client.publish("tgn/i2c/add/gps",GPS_CACH,qos=0,retain=True)
	client.publish("tgn/i2c/add/rom",ROM_CACH,qos=0,retain=True)
	client.publish("tgn/i2c/add/nfc",NFC_ADDRESS,qos=0,retain=True)
	client.publish("tgn/i2c/add/lcd",LCD_ADDRESS,qos=0,retain=True)
	client.publish("tgn/i2c/add/mcp",MCP_ADDRESS,qos=0,retain=True)
	client.publish("tgn/i2c/add/clock",CLOCK_CACH,qos=0,retain=True)
	client.publish("tgn/esp_1/name","Room 1",qos=0,retain=True)
	client.publish("tgn/esp_2/name","Outside",qos=0,retain=True)
	client.publish("tgn/pico_1/name","Room 2",qos=0,retain=True)
	client.publish("tgn/pico_5/name","Room 3",qos=0,retain=True)
	client.publish("tgn/pico_6/name","Room 4",qos=0,retain=True)
	client.publish("tgn/air_conditioner/power","off",qos=0,retain=True)
	client.publish("tgn/air_conditioner/stat",stat_air,qos=0,retain=True)
	client.publish("tgn/air_conditioner/delay",delay,qos=0,retain=True)
	client.publish("tgn/air_conditioner/sol_temp",sol_temp,qos=0,retain=True)
	client.publish("tgn/air_conditioner/sol_hum",sol_hum,qos=0,retain=True)

	#gui
	client.publish("tgn/gui/screen",screen,qos=0,retain=True)
	client.publish("tgn/gui/spr",spr,qos=0,retain=True)
	client.publish("tgn/gui/menu_on",menu_on,qos=0,retain=True)
	client.publish("tgn/gui/version",version,qos=0,retain=True)
	client.publish("tgn/gui/ontime",ontime,qos=0,retain=True)
	client.publish("tgn/gui/offtime",offtime,qos=0,retain=True)
	client.publish("tgn/gui/s1",s1,qos=0,retain=True)
	client.publish("tgn/gui/s2",s2,qos=0,retain=True)
	client.publish("tgn/gui/s3",s3,qos=0,retain=True)
	client.publish("tgn/gui/s4",s4,qos=0,retain=True)
	client.publish("tgn/gui/alarm_s",alarm_s,qos=0,retain=True)
	client.publish("tgn/gui/alarm_t",alarm_t,qos=0,retain=True)
	client.publish("tgn/gui/onoff_day",str(onoff_day),qos=0,retain=True)
	client.publish("tgn/gui/button_width_a",button_width_a,qos=0,retain=True)
	client.publish("tgn/gui/button_width_b",button_width_b,qos=0,retain=True)
	client.publish("tgn/gui/speech",speech,qos=0,retain=True)
	client.publish("tgn/gui/slider_length",slider_length,qos=0,retain=True)
	client.publish("tgn/gui/feed_pos_x",feed_pos_x,qos=0,retain=True)
	client.publish("tgn/gui/feed_pos_y",feed_pos_y,qos=0,retain=True)
	client.publish("tgn/gui/feed_size_width",feed_size_width,qos=0,retain=True)
	client.publish("tgn/gui/feed_size_height",feed_size_height,qos=0,retain=True)
	client.publish("tgn/gui/font_size_a",font_size_a,qos=0,retain=True)
	client.publish("tgn/gui/font_size_b",font_size_b,qos=0,retain=True)
	client.publish("tgn/gui/font_size_c",font_size_c,qos=0,retain=True)
	client.publish("tgn/gui/bground",bground,qos=0,retain=True)
	client.publish("tgn/gui/fground",fground,qos=0,retain=True)
	client.publish("tgn/gui/abground",abground,qos=0,retain=True)
	client.publish("tgn/gui/afground",afground,qos=0,retain=True)
	client.publish("tgn/gui/afbground",afbground,qos=0,retain=True)
	client.publish("tgn/gui/buttona",buttona,qos=0,retain=True)
	client.publish("tgn/gui/buttonb",buttonb,qos=0,retain=True)

def splash():
	import tkinter as tk
	root = tk.Tk()
	root.overrideredirect(True)
	WMWIDTH, WMHEIGHT, WMLEFT, WMTOP = root.winfo_screenwidth(), root.winfo_screenheight(), 0, 0
	root.geometry("%dx%d+%d+%d" % (WMWIDTH, WMHEIGHT, WMLEFT, WMTOP))
	image_file = "/home/pi/tgn_smart_home/icons/splashScreen.gif"
	fra = 40
	frames = [tk.PhotoImage(file=image_file,format = 'gif -index %i' %(i)) for i in range(fra)]
	def update(ind):
		frame = frames[ind]
		ind += 1
		if ind >= fra:
			ind = 1
		label.configure(image=frame)
		root.after(100, update, ind)
	label = tk.Label(root, height=WMHEIGHT, width=WMWIDTH, bg="black")
	label.pack()
	root.after(0, update, 0)
	root.after(9000, root.destroy)
	root.mainloop()

def info_sys():
	subprocess.call('python3 /home/pi/tgn_smart_home/libs/sys_info.py', shell=True)
	
def read_infos():
	setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 4 info"
	os.system(setn)
	time.sleep(0.5)
	setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 10 emeter"
	os.system(setn)
	
def browser_start():
	subprocess.call('chromium  --password-store=basic  --kiosk http://192.168.0.98:8082/vis/index.html#Start', shell=True)

def remove_var(name_b_c):
	if "s_" in name_b_c or "p_" in name_b_c or "y_" in name_b_c or "t_" in name_b_c :
		name_b_c = name_b_c.split("_")[1]
	return name_b_c

def log_temp_hum(data_th):
    logging_tgn(data_th,"room_data.log")

def sonoff_set(mod, stati):
	setn = "python3 /home/pi/tgn_smart_home/libs/tgn_sonoff.py "+mod+" 0 "+stati+" "+get_ip()
	os.system(setn)
def tasmota_set(mod, stati):
	setn = "python3 /home/pi/tgn_smart_home/libs/tasmota.py "+mod+" 0 "+stati+" "+get_ip()
	os.system(setn)

def sound():
	if su==1:
		if colorSet <= 8:
			os.system('mpg321 /home/pi/tgn_smart_home/sounds/button.mp3 &')
		else:
			os.system('mpg321 /home/pi/tgn_smart_home/sounds/lcars-button.mp3 &')

def shutdown_other():
	cmd='ssh pi@192.168.0.90 "sudo systemctl stop minecraft"'
	os.system(cmd)
	time.sleep(60)
	cmd='ssh pi@192.168.0.90 "sudo shutdown -h"'
	os.system(cmd)
	cmd='ssh pi@192.168.0.94 "sudo shutdown -h"'
	os.system(cmd)
	cmd='ssh root@192.168.0.31 "shutdown -h now"'
	os.system(cmd)

def on():
	global son
	global soff
	if son == 0:
		soff = 0
		son = 1
		pb_send_text(pushbulletkey,"Automatic on")
		logging_tgn("AutomaticOn","tgn_smart_home.log")
		if s1 != "0":
			client.publish("tgn/buttons/status/"+s1,"1",qos=0,retain=True)
		if s2 != "0":
			client.publish("tgn/buttons/status/"+s2,"1",qos=0,retain=True)
		if s3 != "0":
			client.publish("tgn/buttons/status/"+s3,"1",qos=0,retain=True)
		if s4 != "0":
			client.publish("tgn/buttons/status/"+s4,"1",qos=0,retain=True)
		if(su==1):
			Process(target=TextToSpeech, args=((data[23].rstrip()),spr)).start()
		client.publish("tgn/system/automatic","1",qos=0,retain=True)

def off():
	global son
	global soff
	if soff == 0:
		soff = 1
		son = 0
		pb_send_text(pushbulletkey,"Automatic Off")
		logging_tgn("AutomaticOff","tgn_smart_home.log")
		if s1 != "0":
			client.publish("tgn/buttons/status/"+s1,"0",qos=0,retain=True)
		if s2 != "0":
			client.publish("tgn/buttons/status/"+s2,"0",qos=0,retain=True)
		if s3 != "0":
			client.publish("tgn/buttons/status/"+s3,"0",qos=0,retain=True)
		if s4 != "0":
			client.publish("tgn/buttons/status/"+s4,"0",qos=0,retain=True)
		if(su==1):
			Process(target=TextToSpeech, args=((data[24].rstrip()),spr)).start()
		client.publish("tgn/system/automatic","0",qos=0,retain=True)

def mc_check(ipadd, ipV6add):
	server = MinecraftServer.lookup(ipadd)
	try:
		status = server.status()
		onlpl=status.players.online
		servtim=status.latency
		client.publish("tgn/mc_server/status","online",qos=0,retain=True)
		client.publish("tgn/mc_server/ping",servtim,qos=0,retain=True)
		client.publish("tgn/mc_server/player",onlpl,qos=0,retain=True)
		client.publish("tgn/mc_server/ip",ipadd,qos=0,retain=True)
		client.publish("tgn/mc_server/ipV6",ipV6add,qos=0,retain=True)
	except:
		client.publish("tgn/mc_server/status","offline",qos=0,retain=True)
		client.publish("tgn/mc_server/ping","0",qos=0,retain=True)
		client.publish("tgn/mc_server/player","0",qos=0,retain=True)
		client.publish("tgn/mc_server/ip",ipadd,qos=0,retain=True)
		client.publish("tgn/mc_server/ipV6",ipV6add,qos=0,retain=True)

def get_pihole_data(url, pw):
    global DNSQUERIES
    global ADSBLOCKED
    global CLIENTS
    global DNSONLIST
    global PIHOLECSTATUS
    try:
        session = requests.Session()
        session.post(url+"/admin/login", {'pw': pw})
        response_data = session.get(url+"/api.php")
        dataPIhole = json.loads(response_data.text)
        DNSQUERIES = dataPIhole['dns_queries_today']
        ADSBLOCKED = dataPIhole['ads_blocked_today']
        CLIENTS = dataPIhole['unique_clients']
        DNSONLIST = dataPIhole['domains_being_blocked']
        PIHOLECSTATUS = dataPIhole['status']
        client.publish("tgn/pihole/adBlock",ADSBLOCKED,qos=0,retain=True)
        client.publish("tgn/pihole/queries",DNSQUERIES,qos=0,retain=True)
        client.publish("tgn/pihole/clients",CLIENTS,qos=0,retain=True)
        client.publish("tgn/pihole/dnslist",DNSONLIST,qos=0,retain=True)
        client.publish("tgn/pihole/status",PIHOLECSTATUS,qos=0,retain=True)
    except: 
        print("Pihole not found")
        DNSQUERIES = "xxx"
        ADSBLOCKED = "xxx"
        CLIENTS = "xxx"
        DNSONLIST = "xxx"
        PIHOLECSTATUS = "0"

def on_message(client, userdata, message):
	global esp_temp
	global pico_temp
	global pico_temp_5
	global pico_temp_6
	global esp_hum
	global esp_temp_2
	global esp_hum_2
	global esp_rssi
	global esp_li
	global pico_hum
	global b9
	global b8
	global b7
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
	global mqtt_msg
	global radar_sen
	global count_pos_b
	global esp_3_color
	global esp_3_game
	global power_air
	global sol_temp
	global sol_hum
	global delay
	global hum_1
	global hum_2
	global hum_3
	global hum_4
	global shelly_cach
	if(message.topic=="shellies/shellydw2-1B7C9D/info"):
		shelly_cach = (message.payload.decode("utf-8"))
	if(message.topic=="tgn/air_conditioner/power"):
		power_air = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/air_conditioner/delay"):
		delay = float(message.payload.decode("utf-8"))
	if(message.topic=="tgn/air_conditioner/sol_temp"):
		sol_temp = float(message.payload.decode("utf-8"))
	if(message.topic=="tgn/air_conditioner/sol_hum"):
		sol_hum = float(message.payload.decode("utf-8"))
	if(message.topic=="MQTChroma/GameMode"):
		if(str(message.payload.decode("utf-8"))=="1"):
			esp_3_game = "1"
		else:
			esp_3_game = "0"
	if(message.topic=="tgn/esp_3/neopixel/color"):
		if(esp_3_game == "0"):
			if(str(message.payload.decode("utf-8"))=="0.0.0.255"):
				esp_3_color = "255,0,0"
			else:
				cach4 = str(message.payload.decode("utf-8")).split(".")
				esp_3_color = cach4[0] + "," + cach4[1] + "," + cach4[2]
			client.publish("MQTChroma/RGB",esp_3_color,qos=0,retain=True)
	if(message.topic=="MQTChroma/RGB"):
		if(esp_3_game == "1"):
			cach5 = str(message.payload.decode("utf-8")).split(",")
			cach6 = cach5[0] + "." + cach5[1] + "." + cach5[2] + ".255"
			client.publish("tgn/esp_3/neopixel/color",cach6,qos=0,retain=True)
	if(message.topic=="tgn/bot/shutdown"):
		if(str(message.payload.decode("utf-8"))=="1"):
			Process(target=shutdown_other).start()
	if(message.topic=="tgn/mqtt-msg"):
		mqtt_msg = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/wifi/pre"):
		esp_pr_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/pico_1/temp/sensor_2"):
		pico_hum = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/wifi/rssi"):
		esp_rssi_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/analog/sensor_1"):
		esp_li_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_2/button/b1"):
		esp_b1_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/esp_1/temp/sensor_1"):
		esp_temp = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/pico_1/temp/sensor_1"):
		pico_temp = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/pico_5/temp/sensor_1"):
		pico_temp_5 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/pico_6/temp/sensor_1"):
		pico_temp_6 = str(message.payload.decode("utf-8"))
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
	if(message.topic=="tgn/esp_1/temp/sensor_2"):
		hum_1 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/pico_1/temp/sensor_2"):
		hum_2 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/pico_5/temp/sensor_2"):
		hum_3 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/pico_6/temp/sensor_2"):
		hum_4 = str(message.payload.decode("utf-8"))
	if(message.topic=="tgn/buttons/status/9"):
		if(int(message.payload.decode("utf-8")) != b9):
			b9 = int(message.payload.decode("utf-8"))
			logging_tgn("Button9:"+str(b9),"tgn_smart_home.log")
			if "s_" in buttons[8]:
				sonoff_set("9", str(b9))
			elif "t_" in buttons[8]:
				tasmota_set("9", str(b9))
			elif "p_" in buttons[8]:
				setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 9 " + str(b9)
				os.system(setn)
			elif "y_" in buttons[8]:
				setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 9 " + str(b9)
				Process(target=TextToSpeech, args=(buttons[8].split("_")[1],spr)).start()
	if(message.topic=="tgn/buttons/status/8"):
		if(int(message.payload.decode("utf-8")) != b8):
			b8 = int(message.payload.decode("utf-8"))
			logging_tgn("Button8:"+str(b8),"tgn_smart_home.log")
			if "s_" in buttons[7]:
				sonoff_set("8", str(b8))
			elif "t_" in buttons[7]:
				tasmota_set("8", str(b8))
			elif "p_" in buttons[7]:
				setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 8 " + str(b8)
				os.system(setn)
			elif "y_" in buttons[7]:
				setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 8 " + str(b8)
				os.system(setn)
			else:
				send(8,b8)
			write_eeprom(1,ROM_ADDRESS,0x02,0x6b,str(b8))
			if(su==1):
				Process(target=TextToSpeech, args=(buttons[7].split("_")[1],spr)).start()
	if(message.topic=="tgn/buttons/status/7"):
		if(int(message.payload.decode("utf-8")) != b7):
			b7 = int(message.payload.decode("utf-8"))
			logging_tgn("Button7:"+str(b7),"tgn_smart_home.log")
			if "s_" in buttons[6]:
				sonoff_set("7", str(b7))
			elif "t_" in buttons[6]:
				tasmota_set("7", str(b7))
			elif "p_" in buttons[6]:
				setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 7 " + str(b7)
				os.system(setn)
			elif "y_" in buttons[6]:
				setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 7 " + str(b7)
				os.system(setn)
			else:
				send(7,b7)
			write_eeprom(1,ROM_ADDRESS,0x02,0x6a,str(b7))
			if(su==1):
				Process(target=TextToSpeech, args=(buttons[6].split("_")[1],spr)).start()
	if(message.topic=="tgn/buttons/status/6"):
		if(int(message.payload.decode("utf-8")) != b6):
			b6 = int(message.payload.decode("utf-8"))
			logging_tgn("Button6:"+str(b6),"tgn_smart_home.log")
			if "s_" in buttons[5]:
				sonoff_set("6", str(b6))
			elif "t_" in buttons[5]:
				tasmota_set("6", str(b6))
			elif "p_" in buttons[5]:
				setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 6 " + str(b6)
				os.system(setn)
			elif "y_" in buttons[5]:
				setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 6 " + str(b6)
				os.system(setn)
			else:
				send(6,b6)
			write_eeprom(1,ROM_ADDRESS,0x00,0x06,str(b6))
			if(su==1):
				Process(target=TextToSpeech, args=(buttons[5].split("_")[1],spr)).start()
	if(message.topic=="tgn/buttons/status/5"):
		if(int(message.payload.decode("utf-8")) != b5):
			b5 = int(message.payload.decode("utf-8"))
			logging_tgn("Button5:"+str(b5),"tgn_smart_home.log")
			if "s_" in buttons[4]:
				sonoff_set("5", str(b5))
			elif "t_" in buttons[4]:
				tasmota_set("5", str(b5))
			elif "p_" in buttons[4]:
				setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 5 " + str(b5)
				os.system(setn)
			elif "y_" in buttons[4]:
				setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 5 " + str(b5)
				os.system(setn)
			else:
				send(5,b5)
			write_eeprom(1,ROM_ADDRESS,0x00,0x05,str(b5))
			if(su==1):
				Process(target=TextToSpeech, args=(buttons[4].split("_")[1],spr)).start()
	if(message.topic=="tgn/buttons/status/4"):
		if(int(message.payload.decode("utf-8")) != b4):
			b4 = int(message.payload.decode("utf-8"))
			logging_tgn("Button4:"+str(b4),"tgn_smart_home.log")
			if "s_" in buttons[3]:
				sonoff_set("4", str(b4))
			elif "t_" in buttons[3]:
				tasmota_set("4", str(b4))
			elif "p_" in buttons[3]:
				setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 4 " + str(b4)
				os.system(setn)
			elif "y_" in buttons[3]:
				setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 4 " + str(b4)
				os.system(setn)
			else:
				send(4,b4)
			write_eeprom(1,ROM_ADDRESS,0x00,0x04,str(b4))
			if(su==1):
				Process(target=TextToSpeech, args=(buttons[3].split("_")[1],spr)).start()
	if(message.topic=="tgn/buttons/status/3"):
		if(int(message.payload.decode("utf-8")) != b3):
			b3 = int(message.payload.decode("utf-8"))
			logging_tgn("Button3:"+str(b3),"tgn_smart_home.log")
			if "s_" in buttons[2]:
				sonoff_set("3", str(b3))
			elif "t_" in buttons[2]:
				tasmota_set("3", str(b3))
			elif "p_" in buttons[2]:
				setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 3 " + str(b3)
				os.system(setn)
			elif "y_" in buttons[2]:
				setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 3 " + str(b3)
				os.system(setn)
			else:
				send(3,b3)
			write_eeprom(1,ROM_ADDRESS,0x00,0x03,str(b3))
			if(su==1):
				Process(target=TextToSpeech, args=(buttons[2].split("_")[1],spr)).start()
	if(message.topic=="tgn/buttons/status/2"):
		if(int(message.payload.decode("utf-8")) != b2):
			b2 = int(message.payload.decode("utf-8"))
			logging_tgn("Button2:"+str(b2),"tgn_smart_home.log")
			if "s_" in buttons[1]:
				sonoff_set("2", str(b2))
			elif "t_" in buttons[1]:
				tasmota_set("2", str(b2))
			elif "p_" in buttons[1]:
				setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 2 " + str(b2)
				os.system(setn)
			elif "y_" in buttons[1]:
				setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 2 " + str(b2)
				os.system(setn)
			else:
				send(2,b2)
			write_eeprom(1,ROM_ADDRESS,0x00,0x02,str(b2))
			if(su==1):
				Process(target=TextToSpeech, args=(buttons[1].split("_")[1],spr)).start()
	if(message.topic=="tgn/buttons/status/1"):
		if(int(message.payload.decode("utf-8")) != b1):
			b1 = int(message.payload.decode("utf-8"))
			logging_tgn("Button1:"+str(b1),"tgn_smart_home.log")
			if "s_" in buttons[0]:
				sonoff_set("1", str(b1))
			elif "t_" in buttons[0]:
				tasmota_set("1", str(b1))
			elif "p_" in buttons[0]:
				setn = "python3 /home/pi/tgn_smart_home/libs/kasa_hs100.py 1 " + str(b1)
				os.system(setn)
			elif "y_" in buttons[8]:
				setn = "python3 /home/pi/tgn_smart_home/libs/shelly.py 1 " + str(b1)
				os.system(setn)
			else:
				send(1,b1)
			write_eeprom(1,ROM_ADDRESS,0x00,0x01,str(b1))
			if(su==1):
				Process(target=TextToSpeech, args=(buttons[0].split("_")[1],spr)).start()
	if(message.topic=="tgn/system/shutdown"):
		if(int(message.payload.decode("utf-8")) == 1):
			if(su==1):
				Process(target=TextToSpeech, args=("Shutdown",spr)).start()
			set_mqtt_start()
			time.sleep(5)
			call(['shutdown', '-h', 'now'], shell=False)
	if(message.topic=="tgn/system/reboot"):
		if(int(message.payload.decode("utf-8")) == 1):
			if(su==1):
				Process(target=TextToSpeech, args=("Reboot",spr)).start()
			call(['reboot', '-h', 'now'], shell=False)
	if(message.topic=="tgn/system/clock"):
		if(int(message.payload.decode("utf-8")) == 1):
			client.publish("tgn/system/clock","0",qos=0,retain=True)
			Process(target=setRTC).start()

def decode_shelly(data_shelly):
	global shelly_message
	json_data = json.loads(data_shelly)
	shelly_ip = json_data['wifi_sta']['ip']
	shelly_temp = json_data['tmp']['value']
	shelly_lux = json_data['lux']['value']
	shelly_door = json_data['sensor']['state']
	shelly_bat_prec = json_data['bat']['value']
	shelly_bat_vol = json_data['bat']['voltage']
	if shelly_message != shelly_door:
		shelly_message = shelly_door
		print("Message: "+shelly_message)
		client.publish("tgn/android/pmsg","Door: "+shelly_message,qos=0,retain=True)
	print("--------------------------------------------")
	#print("IP:"+shelly_ip+"\nTemp:"+str(shelly_temp)+"C\nLux:"+str(shelly_lux)+"Lux\nDoor State:"+shelly_door+"\nBattery:"+str(shelly_bat_prec)+"%\nBat. Voltage:"+str(shelly_bat_vol)+"V")
	#print("--------------------------------------------")

def pcf8563ReadTimeB():
	time_out = ""
	global cach_time
	global day_n
	if RTCpower == 1:
		if address == 0x68:
			register = 0x00
			t = bus.read_i2c_block_data(address,register,7)
			t[0] = t[0]&0x7F  #sec
			t[1] = t[1]&0x7F  #min
			t[2] = t[2]&0x3F  #hour
			t[3] = t[3]&0x07  #week = dayname
			t[4] = t[4]&0x3F  #day
			t[5] = t[5]&0x1F  #month
			cach_time = ("%x:%x" %(t[2],t[1]))
			day_n = w[t[3]]
			#return("%s  20%x/%x/%x %x:%x:%x" %(w[t[3]],t[6],t[5],t[4],t[2],t[1],t[0]))
		else:
			t = bus.read_i2c_block_data(address,register,7)
			t[0] = t[0]&0x7F  #sec
			t[1] = t[1]&0x7F  #min
			t[2] = t[2]&0x3F  #hour
			t[3] = t[3]&0x3F  #day
			t[4] = t[4]&0x07  #month   -> dayname
			t[5] = t[5]&0x1F  #dayname -> month
			cach_time = ("%x:%x" %(t[2],t[1]))
			day_n = w[t[3]]
			#return("%s  20%x/%x/%x %x:%x:%x" %(w[t[4]],t[6],t[5],t[3],t[2],t[1],t[0]))
	else:
		from time import localtime
		time_out = strftime("%a  %Y/%m/%d %H:%M:%S", localtime())
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
		day_n = strftime("%a", localtime())
	on1,on2 = ontime.split("|")
	off1,off2 = offtime.split("|")
	if (day_n in onoff_day and int(esp_li) < esp_switch and ond == "yes") and (cach_time == on1 or cach_time == on2):
		on()
	if ond == "yes" and (cach_time == off1 or cach_time == off2):
		off()
	return(time_out)

def air_conditioner_check():
	global stat_air
	global cach_air
	global first_boot
	temp_is = float(esp_temp)
	hum_is = float(esp_hum)
	temp_out = float(esp_temp_2)
	if power_air == "on":
		if str(temp_is) != "nan" and str(temp_out) != "nan":
			if int(sol_temp) <= int(temp_is):
				if int(temp_out) <= int(sol_temp):
					stat_air = 1
				else:
					stat_air = 2
			elif hum_is >= sol_hum:
				stat_air = 3
			else:
				stat_air = 0
	else:
		stat_air = 0
	if cach_air != stat_air:
		print("Staus Air:" + str(stat_air))
		client.publish("tgn/air_conditioner/stat",stat_air,qos=0,retain=True)
		if  stat_air != 0 and cach_air == 9 or cach_air == 0:
			print("power on")
			client.publish(ir_topic,ir_power)
			time.sleep(20)
		if stat_air == 1:
			print("fan")
			client.publish(ir_topic,ir_fan)
		if stat_air == 2:
			print("cool")
			client.publish(ir_topic,ir_cool)
			time.sleep(10)
			if first_boot == "yes":
				num_loop = ((sol_temp-start_temp_cooler)+1)
				for i in range(int(num_loop)):
					print("up")
					client.publish(ir_topic,ir_up)
					time.sleep(3)
				first_boot = "no"
		if stat_air == 3:
			print("dry")
			client.publish(ir_topic,ir_dry)
		if stat_air == 0:
			print("power off")
			client.publish(ir_topic,ir_power)
			time.sleep(2)
			client.publish(ir_topic,ir_down)
		cach_air = stat_air
	decode_shelly(shelly_cach)

def hum_check(time_in):
	#autohum_botton
	day_c = time_in.split(" ")[0]
	hour_c = time_in.split(" ")[3].split(":")[0]
	global autohum_stat
	global autohum_stat_b
	if ((float(pico_hum) >= float(autohum_on_var)) and (day_c == "Sun" or day_c == "Sat")):
		if (autohum_stat == 0):
			print("On Hum Day")
			client.publish("tgn/system/autohum","1",qos=0,retain=True)
			autohum_stat = 1
			client.publish("tgn/buttons/status/8","1",qos=0,retain=True)
	elif ((float(pico_hum) >= float(autohum_on_var)) and (float(hour_c) < float(autohum_off_time) or float(hour_c) > float(autohum_on_time))):
		if (autohum_stat == 0):
			print("On Hum on Hour")
			client.publish("tgn/system/autohum","1",qos=0,retain=True)
			autohum_stat = 1
			client.publish("tgn/buttons/status/8","1",qos=0,retain=True)
	else:
		if (autohum_stat == 1 and (float(pico_hum) <= float(autohum_on_var)-5)):
			print("Off Hum")
			client.publish("tgn/system/autohum","0",qos=0,retain=True)
			autohum_stat = 0
			client.publish("tgn/buttons/status/8","0",qos=0,retain=True)
	if ((float(esp_hum) >= float(autohum_on_var)) and (day_c == "Sun" or day_c == "Sat") and str(esp_temp) != "nan"):
		if (autohum_stat_b == 0):
			print("On Hum Day")
			client.publish("tgn/system/autohum_b","1",qos=0,retain=True)
			autohum_stat_b = 1
			client.publish("tgn/buttons/status/9","1",qos=0,retain=True)
	elif ((float(esp_hum) >= float(autohum_on_var)) and (float(hour_c) < float(autohum_off_time) or float(hour_c) > float(autohum_on_time)) and str(esp_temp) != "nan"):
		if (autohum_stat_b == 0):
			print("On Hum on Hour")
			client.publish("tgn/system/autohum_b","1",qos=0,retain=True)
			autohum_stat_b = 1
			client.publish("tgn/buttons/status/9","1",qos=0,retain=True)
	else:
		if (autohum_stat_b == 1 and str(esp_hum) != "nan" and (float(esp_hum) <= float(autohum_on_var)-5)):
			print("Off Hum")
			client.publish("tgn/system/autohum_b","0",qos=0,retain=True)
			autohum_stat_b = 0
			client.publish("tgn/buttons/status/9","0",qos=0,retain=True)
	air_conditioner_check()

def main_prog():
	global counter_loop
	global make_loop
	global the_time
	global counterLCD
	while True:
		print("5s loop")
		client.on_message=on_message
		client.loop_start()
		client.subscribe([("MQTChroma/*",1),(main_topic,0)])
		client.subscribe([("MQTChroma/*",1),(shelly_topic,0)])
		time.sleep(2)
		client.loop_stop()
		try:
			client.publish("tgn/cpu/temp",str(round(getCpuTemperature(),1)),qos=0,retain=True)
		except:
			client.connect(get_ip())
			client.loop_start()
		if LCDpower == 1:
			counterLCD = counterLCD + 1
		if counterLCD == 30 and LCDpower == 1:
			mylcd.lcd_clear()
			mylcd.lcd_display_string("TGN Smart Home", 1, 1)
			mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
		if backlight == 0 and LCDpower == 1:
			mylcd.backlight(0)
		cach_time = pcf8563ReadTime()
		client.publish("tgn/system/time",format_time(cach_time),qos=0,retain=True)
		hum_check(format_time(cach_time))
		trigger = pcf8563ReadTimeB()
		#---------------------------------
		if counter_loop == make_loop:
			print("20m loop")
			#Sun  2025/12/21 09:53:42
			ch_day = trigger.split(" ")[0]
			ch_hour = trigger.split(" ")[3].split(":")[0]
			if ch_day == "Sun" and ch_hour == "10":
				print("Valve moving")
				logging_tgn("Valve moving","tgn_smart_home.log")
				client.publish("tgn/thermostat/valve_movement","on",qos=0,retain=True)
			counter_loop = 0
			temp_data = "Room Luxmeter:"
			get_pihole_data(pihole_url, pihole_pw)
			if is_connected(REMOTE_SERVER)=="Online":
				global esp_ls
				global rssfeed
				global ttiv
				print("Check mc server")
				mc_check(mc_add_s, mc_add_sV6)
				if rssurl == "empty":
					rssfeed = "Please set a Newsfeed"
				else:
					print("Read RSS")
					print(rssurl)
					rssfeed = rss(rssurl,10)
				if int(esp_li)==50:
					make_loop = 5
				else:
					make_loop = 172
				if esp_ls == 0 and int(esp_li) < esp_switch:
					esp_ls = 1
					on()
				elif esp_ls == 1 and int(esp_li) > esp_switch_b:
					esp_ls = 0
					off()
				#---------
				print("Load Weather")
				if allowed_key(openweatherkey) == "yes":
					data = weather_info(zipcode,openweatherkey)
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
				else:
					print("Wrong Key!!")
				channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
				Process(target=read_infos).start()
				global cpu_t
				cpu_t = getCpuTemperature()
				if Ts == 1:
					timespl = format_time(pcf8563ReadTime()).split(" ")
					print(write_ts(channel,pico_temp_5,esp_temp,pico_temp,hum_1,hum_2,hum_3,hum_4))
					log_temp_hum("LR:"+esp_temp+"#"+hum_1+"|KR:"+pico_temp+"#"+hum_2+"|WC:"+pico_temp_5+"#"+hum_3+"|BR:"+pico_temp_6+"#"+hum_4)
					client.publish("tgn/system/update",timespl[3],qos=0,retain=True)
		time.sleep(5)
		counter_loop = counter_loop + 1

#---main---
ini()
time.sleep(2)
Process(target=info_sys).start()
time.sleep(2)
Process(target=read_infos).start()
if LCDpower == 1:
	mylcd.lcd_display_string("TGN Smart Home", 1, 1)
	mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
if MCPpower == 1:
	mcp.output(3, 1)
if su==1 and is_connected(REMOTE_SERVER)=="Online":
	try:
		f = open(spr_phat+"voice.lang","r")
	except IOError:
		print("cannot open voice.lang.... file not found")
	else:
		data = []
		for line in f:
			data.append(line)
		if spr != "zh":
			print("Start Voice Modul")
			Process(target=TextToSpeech, args=((data[4].rstrip()),spr)).start()
try:
	f_d = open("/home/pi/tgn_smart_home/config/i2c.config","r")
	for line in f_d:
		if "LCD_ADDRESS" in line:
			LCD_ADDRESS = int(line.rstrip().split("*")[1],16)
		if "MCP_ADDRESS" in line:
			MCP_ADDRESS = int(line.rstrip().split("*")[1],16)
		if "NFC_ADDRESS" in line:
			NFC_ADDRESS = int(line.rstrip().split("*")[1],16)
		if "ROM_ADDRESS" in line:
			ROM_CACH = int(line.rstrip().split("*")[1],16)
		if "clock_address" in line:
			CLOCK_CACH = int(line.rstrip().split("*")[1],16)
		if "gps_address" in line:
			GPS_CACH = int(line.rstrip().split("*")[1],16)
except IOError:
    print("cannot open i2c.config.... file not found")
print(str(colorSet))
if colorSet == 0:
	print("Load ioBrocker")
	Process(target=browser_start).start()
else:
	print("Load normal")
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/gui.py "+str(colorSet)
	os.system(setn)
main_prog()
