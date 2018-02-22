# load Libs
from tgnLIB import *
import binascii
from subprocess import call
from tkinter import *
import subprocess
import PIL
from PIL import Image, ImageTk
# var

ROM_ADDRESS = 0x53
LCD_ADDRESS = 0x3f
MCP_ADDRESS = 0x20
NFC_ADDRESS = 0x24

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
su = 1
Ts = 0
buttons = ["1","2","3","4","5","6"]
b1 = 0
b2 = 0
b3 = 0
b4 = 0
b5 = 0
b6 = 0
room_t = 26
room_h = 40.0
weather_t = -0.41
weather_c = 0
weather_w =4.1
cpu_t = 57.458
bground = "black"
fground = "green"
abground = "gray"
afground = "black"
afbground = "black"
buttona = "red"
buttonb = "black"
colorSet = 1
s1 = "0"
s2 = "0"
s3 = "0"
s4 = "0"
son = 0
soff = 0
speech = 0
mcp = ""
mylcd = ""
ontime = "10:19|10:21"
offtime = "10:20|10:22"
phat = "/home/pi/tgn_smart_home/icons/"
#PiHole
api_url = 'http://localhost/admin/api.php'
#functions
def save_settings():
	write_eeprom(1,ROM_ADDRESS,0x00,0x01,str(b1))
	write_eeprom(1,ROM_ADDRESS,0x00,0x02,str(b2))
	write_eeprom(1,ROM_ADDRESS,0x00,0x03,str(b3))
	write_eeprom(1,ROM_ADDRESS,0x00,0x04,str(b4))
	write_eeprom(1,ROM_ADDRESS,0x00,0x05,str(b5))
	write_eeprom(1,ROM_ADDRESS,0x00,0x06,str(b6))

def ini():
	os.system('clear')
	#MCP23017 I2C
	print(">>initialize MCP23017")
	if ifI2C(MCP_ADDRESS) == "found device":
		global MCPpower
		MCPpower = 1
		global mcp
		mcp = MCP230XX(busnum = 1, address = MCP_ADDRESS, num_gpios = 16)
		mcp.config(0, 0)
		mcp.config(1, 0)
		mcp.config(2, 0)
		mcp.config(3, 0)
		mcp.pullup(4, 1)
		mcp.pullup(5, 1)
		mcp.pullup(6, 1)
		mcp.pullup(7, 1)
		print(">>MCP23017 configured")
	else:
		print(">>MCP23017 not found")
	#LCD
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
		mylcd.lcd_display_string("V1.6 Loading....", 2, 0)
		print(">>LCD Display configured")
	else:
		print(">>LCD Display not found")
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
	print(">>initialize EEPROM")
	if ifI2C(ROM_ADDRESS) == "found device":
		print(">>LCD Display configured")
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
	else:
		print(">>EEPROM not found")
	if MCPpower == 1:
		print(">>MCP23017 test Input and Output")
		print("%d: %x" % (4, mcp.input(4) >> 4))
		print("%d: %x" % (5, mcp.input(5) >> 5))
		print("%d: %x" % (6, mcp.input(6) >> 6))
		print("%d: %x" % (7, mcp.input(7) >> 7))
		mcp.output(0, 1)
		time.sleep(0.5)
		mcp.output(1, 1)
		time.sleep(0.5)
		mcp.output(2, 1)
		time.sleep(0.5)
		mcp.output(3, 1)
		time.sleep(0.5)
		mcp.output(0, 0)
		mcp.output(1, 0)
		mcp.output(2, 0)
		mcp.output(3, 0)
	try:
		print(">>Load themes.config")
		f = open("/home/pi/tgn_smart_home/config/themes.config","r")
	except IOError:
    		print("cannot open themes.config.... file not found")
	else:
		print(">>set themes")
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

def on():
	global son
	global soff
	if son == 0:
		soff = 0
		son = 1
		msg = "Automatic_on"
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		if s1 == "1":
			send(1,1)
			time.sleep(1)
			b1 = 1
		if s2 == "1":
			send(2,1)
			time.sleep(1)
			b2 = 1
		if s3 == "1":
			send(3,1)
			time.sleep(1)
			b3 = 1
		if s4 == "1":
			send(4,1)
			b4 = 1
	save_settings()

def off():
	global son
	global soff
	if soff == 0:
		soff = 1
		son = 0
		msg = "Automatic_off"
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		if s1 == "1":
			send(1,0)
			time.sleep(1)
			b1 = 0
		if s2 == "1":
			send(2,0)
			time.sleep(1)
			b2 = 0
		if s3 == "1":
			send(3,0)
			time.sleep(1)
			b3 = 0
		if s4 == "1":
			send(4,0)
			b4 = 0
	save_settings()

def sound():
	if su==1:
		os.system('mpg321 /home/pi/tgn_smart_home/sounds/button.mp3 &')

def pcf8563ReadTimeB():
	t = bus.read_i2c_block_data(address,register,7);
	t[0] = t[0]&0x7F  #sec
	t[1] = t[1]&0x7F  #min
	t[2] = t[2]&0x3F  #hour
	t[3] = t[3]&0x3F  #day
	t[4] = t[4]&0x07  #month   -> dayname
	t[5] = t[5]&0x1F  #dayname -> month
	cach = ("%x:%x" %(t[2],t[1]))
	on1,on2 = ontime.split("|")
	off1,off2 = offtime.split("|")
	ond = "yes"
	if ond == "yes" and cach == on1 or cach == on2:
		on()
	if ond == "yes" and cach == off1 or cach == off2:
		off()
	return("%s  20%x/%x/%x %x:%x:%x" %(w[t[4]],t[6],t[5],t[3],t[2],t[1],t[0]))

def About():
    print("TGN Smart Home "+version)
def callback1():
	setn = "python3 /home/pi/tgn_smart_home/libs/auto_cam.py video "+E1.get()
	os.system(setn)
def callback2():
	setn = "python3 /home/pi/tgn_smart_home/libs/auto_cam.py capture 0"
	os.system(setn)
def callback3():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/auto_cam.py timer 0"
	os.system(setn)
def callback4():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/camGpio.py"
	os.system(setn)
def callback5():
	setn = "python3 /home/pi/tgn_smart_home/libs/auto_cam.py preview 0"
	os.system(setn)
def callback6():
	stream()
def callback7():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/digi-cam.py"
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
	global b1
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b1 == 0:
		msg = "Turn_on_" + buttons[0]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(1,1)
		b1 = 1
	else:
		msg = "Turn_off_" + buttons[0]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(1,0)
		b1 = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0x01,str(b1))
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback10():
	sound()
	global b2
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b2 == 0:
		msg = "Turn_on_" + buttons[1]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(2,1)
		b2 = 1
	else:
		msg = "Turn_off_" + buttons[1]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(2,0)
		b2 = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0x02,str(b2))
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback11():
	sound()
	global b3
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b3 == 0:
		msg = "Turn_on_" + buttons[2]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(3,1)
		b3 = 1
	else:
		msg = "Turn_off_" + buttons[2]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(3,0)
		b3 = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0x03,str(b3))
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback12():
	sound()
	global b4
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b4 == 0:
		msg = "Turn_on_" + buttons[3]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(4,1)
		b4 = 1
	else:
		msg = "Turn_off_" + buttons[3]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(4,0)
		b4 = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0x04,str(b4))
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback13():
	sound()
	global b5
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b5 == 0:
		msg = "Turn_on_" + buttons[4]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(5,1)
		b5 = 1
	else:
		msg = "Turn_off_" + buttons[4]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(5,0)
		b5 = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0x05,str(b5))
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback14():
	sound()
	global b6
	if MCPpower == 1:
		mcp.output(3, 0)
		mcp.output(2, 1)
	if b6 == 0:
		msg = "Turn_on_" + buttons[5]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(6,1)
		b6 = 1
	else:
		msg = "Turn_off_" + buttons[5]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg  + ' ' + pushbulletkey)
		send(6,0)
		b6 = 0
	write_eeprom(1,ROM_ADDRESS,0x00,0x06,str(b6))
	if MCPpower == 1:
		mcp.output(3, 1)
		mcp.output(2, 0)
def callback15():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
	mylcd.lcd_clear()
	mylcd.backlight(0)
	from subprocess import call
	call(['shutdown', '-h', 'now'], shell=False)
def callback16():
	sound()
	if MCPpower == 1:
		mcp.output(3, 0)
	mylcd.lcd_clear()
	mylcd.backlight(0)
	from subprocess import call
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
	if LCDpower == 1:
		LCDpower = 0
		mylcd.lcd_clear()
		mylcd.backlight(0)
	else:
		LCDpower = 1
		mylcd.lcd_display_string("TGN Smart Home", 1, 1)
		mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
		mylcd.backlight(1)
def callback21():
	sound()
	global backlight
	if backlight == 1:
		backlight = 0
		mylcd.backlight(0)
	else:
		backlight = 1
		mylcd.backlight(1)
def callback22():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py install_rom"
	os.system(setn)
def callback23():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py cam"
	os.system(setn)
def callback24():
	subprocess.call('xset dpms force on', shell=True)
	sound()
def callback25():
	global su
	if su == 1:
		su = 0
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
	if LCDpower == 1:
		mylcd.backlight(0)
		time.sleep(1)
		mylcd.lcd_clear()
		time.sleep(1)
		mylcd.backlight(0)
	os.system('mpg321 /home/pi/tgn_smart_home/sounds/startup.mp3 &')
	root.quit()

def all_off():
	sound()
	subprocess.call('xset dpms force on', shell=True)
	global b1
	global b2
	global b3
	global b4
	global b5
	global b6
	b1=0
	b2=0
	b3=0
	b4=0
	b5=0
	b6=0
	send(6,0)
	time.sleep(1)
	send(5,0)
	time.sleep(1)
	send(4,0)
	time.sleep(1)
	send(3,0)
	time.sleep(1)
	send(2,0)
	time.sleep(1)
	send(1,0)
	time.sleep(1)
	print("exit")
	if MCPpower == 1:
		mcp.output(3, 0)
	if LCDpower == 1:
		mylcd.lcd_clear()
		mylcd.backlight(0)
	save_settings()
def all_on():
	sound()
	subprocess.call('xset dpms force on', shell=True)
	global b1
	global b2
	global b3
	global b4
	global b5
	global b6
	b1=1
	b2=1
	b3=1
	b4=1
	b5=1
	b6=1
	send(1,1)
	time.sleep(1)
	send(2,1)
	time.sleep(1)
	send(3,1)
	time.sleep(1)
	send(4,1)
	time.sleep(1)
	send(5,1)
	time.sleep(1)
	send(6,1)
	time.sleep(1)
	save_settings()
	time.sleep(1)
	os.system('mpg321 /home/pi/tgn_smart_home/sounds/startup.mp3 &')

def callback30():
	if ifI2C(NFC_ADDRESS) == "found device":
		pn532 = Pn532_i2c()
		pn532.SAMconfigure()
		print("waiting for card")
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
				print(cachC)
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
	sound()
	tex = SpeechToText("de","AIzaSyDDzPM2W74MU3NvWgRKG85b3-UWaNOAjQo")
	print(tex)
	#anschalten,ausschalten,exit,runterfahren
	if tex == "exit":
		exit()
	if tex == "runterfahren":
		if LCDpower == 1:
			mylcd.backlight(0)
			time.sleep(1)
			mylcd.lcd_clear()
			time.sleep(1)
			mylcd.backlight(0)
		call(['shutdown', '-h', 'now'], shell=False)
	if tex == "ausschalten":
		all_off()
	if tex == "anschalten":
		all_on()

def callback32():
	global speech
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

def callback35():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py thinkspeak"
	os.system(setn)

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
			global the_time
			global counterLCD
			newtime = time.time()
			if newtime != the_time:
				if MCPpower == 1:
					if mcp.input(7) >> 7 == 1:
						all_off()
					if mcp.input(4) >> 4 == 1:
						callback7()
					if mcp.input(5) >> 5 == 1:
						callback12()
					if mcp.input(6) >> 6 == 1:
						callback24()
				stats = 'Switch:'
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
				if counterLCD == 60 and LCDpower == 1:
					mylcd.lcd_clear()
					r = requests.get(api_url)
					dataPIhole = json.loads(r.text)
					DNSQUERIES = dataPIhole['dns_queries_today']
					ADSBLOCKED = dataPIhole['ads_blocked_today']
					CLIENTS = dataPIhole['unique_clients']
					mylcd.lcd_display_string("Ad Blocked:"+str(ADSBLOCKED), 1, 0)
					mylcd.lcd_display_string("Queries:"+str(DNSQUERIES), 2, 0)
					counterLCD = 0
				if backlight == 0 and LCDpower == 1:
					mylcd.backlight(0)
				the_time= pcf8563ReadTimeB()+"\nCPU:"+str(getCpuTemperature())+"°C\n"+stats
				self.display_time.config(text=the_time, font=('times', 20, 'bold'), bg=afbground, fg=fground)
			self.display_time.after(1000, change_value_the_time)
		change_value_the_time()
# updating window (Weather and PiHole)
class WindowB(Frame):
	def __init__(self,master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()
	def create_widgets(self):
		self.display_time=Label(self, text=the_time)
		self.display_time.grid(row=0, column=1)
		def change_value_the_time():
			global the_time
			newtime = time.time()
			if newtime != the_time:
				r = requests.get(api_url)
				dataPIhole = json.loads(r.text)
				DNSQUERIES = dataPIhole['dns_queries_today']
				ADSBLOCKED = dataPIhole['ads_blocked_today']
				CLIENTS = dataPIhole['unique_clients']
				temp_data = get_dht11()
				output = '---------------------------------------\n'
				if is_connected(REMOTE_SERVER)=="Online":
					if allowed_key(openweatherkey) == "yes":
						data = weather_info(zipcode,openweatherkey)
						m_symbol = '\xb0' + 'C'
						output = output+'Current weather in: '+data['city']+','+data['country']+'\n'
						output = output+str(data['temp'])+'°C  '+data['sky']+'\n'
						output = output+'Max:'+str(data['temp_max'])+'°C, Min:'+str(data['temp_min'])+'°C\n'
						output = output+'\n'
						output = output+'Wind Speed:'+str(data['wind'])+'km/h \n'
						output = output+'Humidity:'+str(data['humidity'])+'% \n'
						output = output+'Cloud:'+str(data['cloudiness'])+'% \n'
						output = output+'Pressure:'+str(data['pressure'])+'hpa \n'
						output = output+'Sunrise at:'+str(data['sunrise'])+'\n'
						output = output+'Sunset at:'+str(data['sunset'])+'\n'
						#output = output+'Icon ID:'+str(data['icon'])+'\n'
						output = output+'Last update from the server:'+str(data['dt'])+'\n'
						output = output+'---------------------------------------\n'
						output = output+temp_data+'\n'
						global weather_t
						global weather_c
						global weather_w
						weather_t = float(data['temp'])
						weather_c = int(data['cloudiness'])
						weather_w = float(data['wind'])
					else:
						output = output+'Please use a new key from openweathermap.org\n'
					output = output+'---------------------------------------\n'
				output = output+'Ad Blocked:'+str(ADSBLOCKED)+' Client:'+str(CLIENTS)+' DNS Queries:'+str(DNSQUERIES)
				channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
				global room_t
				global room_h
				global cpu_t
				rcach = temp_data.split(" / ")
				rcachB = rcach[1].split("%")
				rcachC = rcach[0].split(":")
				rcachD = rcachC[1].split("°C")
				room_t = float(rcachD[0])
				room_h = float(rcachB[0])
				cpu_t = getCpuTemperature()
				if Ts == 1:
					print(write_ts(channel,room_t,room_h,weather_t,weather_c,weather_w,cpu_t))
					output = output+'\n ThinkSpeak activate'
				self.display_time.config(text=output, font=('times', 17, 'bold'), bg=afbground, fg=fground)
				if is_connected(REMOTE_SERVER)=="Online":
					if allowed_key(openweatherkey) == "yes":
						phatI = phat+get_icon_name(str(data['icon']))
						load = Image.open(phatI)
						render = ImageTk.PhotoImage(load)
						img = Label(self, image=render)
						img.image = render
						img.config(bg=afbground)
						img.place(x=0, y=150)
			self.display_time.after(3600000, change_value_the_time)
		change_value_the_time()
def st1():
	global colorSet
	colorSet = 1
	write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st2():
	global colorSet
	colorSet = 2
	write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st3():
	global colorSet
	colorSet = 3
	write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st4():
	global colorSet
	colorSet = 4
	write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st5():
	global colorSet
	colorSet = 5
	write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st6():
	global colorSet
	colorSet = 6
	write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
#Main Prog
ini()
if LCDpower == 1:
	mylcd.lcd_display_string("TGN Smart Home", 1, 1)
	mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
if MCPpower == 1:
	mcp.output(3, 1)
os.system('mpg321 /home/pi/tgn_smart_home/sounds/startup.mp3 &')
print(">>Load GUI")
root = Tk()
#fullscreen mode
WMWIDTH, WMHEIGHT, WMLEFT, WMTOP = root.winfo_screenwidth(), root.winfo_screenheight(), 0, 0
root.overrideredirect(screen) 
root.geometry("%dx%d+%d+%d" % (WMWIDTH, WMHEIGHT, WMLEFT, WMTOP))

root.wm_title("TGN Smart Home "+version)
menu = Menu(root)
root.config(background = bground, menu=menu)

filemenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
filemenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Refresh Clock", command=callback8)
filemenu.add_command(label="Digi Cam", command=callback7)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=callback30)

setmenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
setmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
menu.add_cascade(label="Settings", menu=setmenu)
setmenu.add_command(label="Sound", command=callback25)
setmenu.add_command(label="Speech On/Off", command=callback32)
setmenu.add_command(label="ThinkSpeak On/Off", command=callback34)

stylemenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
stylemenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
setmenu.add_cascade(label="Screen", menu=stylemenu)
stylemenu.add_command(label="Fullscreen", command=callback19)

colmenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
colmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
stylemenu.add_cascade(label="Color", menu=colmenu)
colmenu.add_command(label="Dark/Green", command=st1)
colmenu.add_command(label="Gray", command=st2)
colmenu.add_command(label="White/Gray", command=st3)
colmenu.add_command(label="Gray/White", command=st4)
colmenu.add_command(label="Blue/White", command=st5)
colmenu.add_command(label="Blue/Green", command=st6)

rommenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
rommenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
setmenu.add_cascade(label="EEPROM", menu=rommenu)
rommenu.add_command(label="RTC Automatic", command=callback17)
rommenu.add_command(label="Remote Controll", command=callback18)
rommenu.add_command(label="Cam Settings", command=callback23)
rommenu.add_command(label="Weather Settings", command=callback26)
rommenu.add_command(label="Pushbullet Key", command=callback27)
rommenu.add_command(label="ThinkSpeak Settings", command=callback35)
rommenu.add_command(label="Reset eeprom", command=callback22)

nfcmenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
nfcmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
setmenu.add_cascade(label="NFC", menu=nfcmenu)
nfcmenu.add_command(label="Save Card", command=callback28)
nfcmenu.add_command(label="Remove Card", command=callback29)
nfcmenu.add_command(label="Show Crads", command=callback31)

helpmenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
helpmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

leftFrame = Frame(root, width=400, height = 400)
leftFrame.configure(background=bground)
leftFrame.grid(row=0, column=0, padx=10, pady=3)

infFrame1 = Frame(leftFrame)
infFrame1.configure(background=bground)
infFrame1.grid(row=0, column=0, padx=10, pady=3)
infLabel1 = Label(infFrame1, text="Weather Infos:")
infLabel1.configure(background=bground, foreground=fground)
infLabel1.grid(row=0, column=1, padx=10, pady=3)

rightFrame = Frame(root, width=400, height = 400)
rightFrame.configure(background=bground)
rightFrame.grid(row=0, column=1, padx=10, pady=3)

buttonFrame = Frame(rightFrame)
buttonFrame.configure(background=bground)
buttonFrame.grid(row=1, column=0, padx=10, pady=3)
buttonLabel1 = Label(buttonFrame, text="Camera Options")
buttonLabel1.configure(background=bground, foreground=fground)
buttonLabel1.grid(row=0, column=1, padx=10, pady=3)
buttonLabel2 = Label(buttonFrame, text="Record length:")
buttonLabel2.configure(background=bground, foreground=fground)
buttonLabel2.grid(row=1, column=0, padx=10, pady=3)
E1 = Entry(buttonFrame, width=18)
E1.grid(row=1, column=1, padx=10, pady=3)
B1 = Button(buttonFrame, text="Record", bg=buttona, fg=fground, width=15, command=callback1)
B1.grid(row=1, column=2, padx=10, pady=3)
B5 = Button(buttonFrame, text="Preview", bg=buttonb, fg=fground, width=15, command=callback5)
B5.grid(row=2, column=0, padx=10, pady=3) 
B2 = Button(buttonFrame, text="Capture", bg=buttonb, fg=fground, width=15, command=callback2)
B2.grid(row=2, column=1, padx=10, pady=3)
B3 = Button(buttonFrame, text="Timer Capture", bg=buttonb, fg=fground, width=15, command=callback3)
B3.grid(row=2, column=2, padx=10, pady=3)
B4 = Button(buttonFrame, text="Motion Detector", bg=buttonb, fg=fground, width=15, command=callback4)
B4.grid(row=3, column=0, padx=10, pady=3)
B7 = Button(buttonFrame, text="Digi Cam", bg=buttonb, fg=fground, width=15, command=callback7)
B7.grid(row=3, column=1, padx=10, pady=3)
B6 = Button(buttonFrame, text="Stream", bg=buttonb, fg=fground, width=15, command=callback6)
B6.grid(row=3, column=2, padx=10, pady=3)

seperatorFrame = Frame(rightFrame)
seperatorFrame.configure(background=bground)
seperatorFrame.grid(row=2, column=0, padx=5, pady=3)
seperatorLabel1 = Label(seperatorFrame, text="")
seperatorLabel1.configure(background=bground)
seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

buttonFrame1 = Frame(rightFrame)
buttonFrame1.configure(background=bground)
buttonFrame1.grid(row=3, column=0, padx=10, pady=3)
buttonLabel1 = Label(buttonFrame1, text="Home Control")
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
B7 = Button(buttonFrame1, text="All On", bg=buttonb, fg=fground, width=15, command=all_on)
B7.grid(row=3, column=0, padx=10, pady=3)
B8 = Button(buttonFrame1, text="All Off", bg=buttonb, fg=fground, width=15, command=all_off)
B8.grid(row=3, column=1, padx=10, pady=3)
if speech == 1:
	B9 = Button(buttonFrame1, text="Mic", bg=buttona, fg=fground, width=15, command=callback33)
	B9.grid(row=3, column=2, padx=10, pady=3)

infFrame1 = Frame(rightFrame)
infFrame1.configure(background=bground)
infFrame1.grid(row=5, column=0, padx=10, pady=3)
infLabel1 = Label(infFrame1, text="Timer Settings:")
infLabel1.configure(background=bground, foreground=fground)
infLabel1.grid(row=0, column=1, padx=10, pady=3)
oText1 = "Start:"+ontime
infLabel2 = Label(infFrame1, text=oText1)
infLabel2.configure(background=bground, foreground=fground)
infLabel2.grid(row=1, column=0, padx=10, pady=3)
oText2 = "End:"+offtime
infLabel3 = Label(infFrame1, text=oText2)
infLabel3.configure(background=bground, foreground=fground)
infLabel3.grid(row=1, column=2, padx=10, pady=3)
oText3 = "Automatic:"+s1+s2+s3+s4
infLabel4 = Label(infFrame1, text=oText3)
infLabel4.configure(background=bground, foreground=fground)
infLabel4.grid(row=1, column=1, padx=10, pady=3)

app=Window(rightFrame)

seperatorFrame2 = Frame(rightFrame)
seperatorFrame2.configure(background=bground)
seperatorFrame2.grid(row=7, column=0, padx=5, pady=3)
seperatorLabel1 = Label(seperatorFrame2, text="")
seperatorLabel1.configure(background=bground)
seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

buttonFrame2 = Frame(rightFrame)
buttonFrame2.configure(background=bground)
buttonFrame2.grid(row=8, column=0, padx=10, pady=3)
buttonLabel2 = Label(buttonFrame2, text="System Control")
buttonLabel2.configure(background=bground, foreground=fground)
buttonLabel2.grid(row=0, column=1, padx=10, pady=3)

B1 = Button(buttonFrame2, text="Shutdown", bg=buttonb, fg=fground, width=15, command=callback15)
B1.grid(row=1, column=0, padx=10, pady=3) 
B2 = Button(buttonFrame2, text="Reboot", bg=buttonb, fg=fground, width=15, command=callback16)
B2.grid(row=1, column=1, padx=10, pady=3)
if ifI2C(NFC_ADDRESS) == "found device":
	B3 = Button(buttonFrame2, text="Scan NFC", bg=buttona, fg=fground, width=15, command=callback30)
	B3.grid(row=1, column=2, padx=10, pady=3)

app=WindowB(leftFrame)

seperatorFrame3 = Frame(leftFrame)
seperatorFrame3.configure(background=bground)
seperatorFrame3.grid(row=2, column=0, padx=5, pady=3)
seperatorLabel1 = Label(seperatorFrame3, text="")
seperatorLabel1.configure(background=bground)
seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

buttonFrame3 = Frame(leftFrame)
buttonFrame3.configure(background=bground)
buttonFrame3.grid(row=3, column=0, padx=10, pady=3)

B1 = Button(buttonFrame3, text="LCD On/Off", bg=buttonb, fg=fground, width=15, command=callback20)
B1.grid(row=0, column=0, padx=10, pady=3) 
B2 = Button(buttonFrame3, text="LCD Backlight", bg=buttonb, fg=fground, width=15, command=callback21)
B2.grid(row=0, column=1, padx=10, pady=3)

root.mainloop()