import picamera
import time
import os
import smbus
from tgnLIB import *

ROM_ADDRESS = 0x53
MCP_ADDRESS = 0x20

sound = "off"
path = "/home/pi/test/"
num = 1
auto_capture = 0
count = 0
MCPpower = 0

if ifI2C(MCP_ADDRESS) == "found device":
	global MCPpower
	MCPpower = 1
	mcp = MCP230XX(busnum = 1, address = MCP_ADDRESS, num_gpios = 16)
	mcp.config(1, 0)
	mcp.pullup(4, 1)
	mcp.pullup(5, 1)
	mcp.pullup(6, 1)
	mcp.pullup(7, 1)

address = 0x51
register = 0x02
w  = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
bus = smbus.SMBus(1)

camera = picamera.PiCamera()
camera.vflip = True

def ini():
	global sound
	global path
	if ifI2C(ROM_ADDRESS) == "found device":
		start_add_N = 0x7e
		index = 0 
		sound= ""
		while index < 3:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_N)
			if cach != "X":
				sound = sound + cach
			index = index + 1
			start_add_N = start_add_N + 1
		start_add_Q = 0x91
		index = 0 
		path = ""
		while index < 20:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_Q)
			if cach != "X":
				path = path + cach
			index = index + 1
			start_add_Q = start_add_Q + 1	
def check_1(file):
	global num
	if os.path.exists(file):
		num = num + 1
		file = path+"capture"+str(num)+".jpg"
		check_1(file)
def check_2(file):
	global num
	if os.path.exists(file):
		num = num + 1
		file = path+"video"+str(num)+".h264"
		check_2(file)
def make_image():
	#camera.start_preview()
	print("click")
	global num
	file = path+"capture"+str(num)+".jpg"
	check_1(file)
	time.sleep(5)
	camera.capture(path+"capture"+str(num)+".jpg")
	if sound == "on":
		os.system('mpg321 /home/pi/tgn_smart_home/sounds/flash.mp3 &')
	#camera.stop_preview()
def pcf8563ReadTime():
	t = bus.read_i2c_block_data(address,register,7);
	t[0] = t[0]&0x7F  #sec
	t[1] = t[1]&0x7F  #min
	t[2] = t[2]&0x3F  #hour
	t[3] = t[3]&0x3F  #day
	t[4] = t[4]&0x07  #month   -> dayname
	t[5] = t[5]&0x1F  #dayname -> month
	return("20%x/%x/%x %x:%x:%x  %s" %(t[6],t[5],t[3],t[2],t[1],t[0],w[t[4]]))
ini()
camera.start_preview()
camera.led = False
x = True
while x == True:
	
	var1 = pcf8563ReadTime()
	camera.annotate_text = var1
	if MCPpower == 1:
		if mcp.input(7) >> 7 == 1:
			camera.led = True
			mcp.output(1, 1)
			make_image()
			time.sleep(4)
			camera.led = Fals
			mcp.output(1, 0)
		if mcp.input(6) >> 6 == 1:
			print("recording")
			mcp.output(1, 1)
			camera.led = True
			if sound == "on":
				os.system('mpg321 /home/pi/tgn_smart_home/sounds/button.mp3 &')
			global num
			file = path+"video"+str(num)+".h264"
			check_2(file)
			camera.start_recording(path+"video"+str(num)+".h264")
			time.sleep(4)
		if mcp.input(5) >> 5 == 1:
			mcp.output(1, 0)
			camera.stop_recording
			print("stop recording")
			camera.led = False
			if sound == "on":
				os.system('mpg321 /home/pi/tgn_smart_home/sounds/button.mp3 &')
			time.sleep(4)
		if mcp.input(4) >> 4 == 1:
			mcp.output(1, 1)
			print("Close Program.....")
			x = False
		time.sleep(0.05)
time.sleep(5)
camera.stop_preview()
if MCPpower == 1:
	mcp.output(1, 0)