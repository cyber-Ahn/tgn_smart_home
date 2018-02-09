import picamera
import time
import os
from time import gmtime, strftime
from tgnLIB import *

#var
ROM_ADDRESS = 0x53
sleep_t = "300"
start = "14:00"
end = "22:00"
sound = "off"
path = "/home/pi/test/"
num = 1
auto_capture = 0
count = 0

camera = picamera.PiCamera()
camera.vflip = True

def ini():
	global sleep_t
	global start
	global end
	global sound
	global path
	if ifI2C(ROM_ADDRESS) == "found device":
		start_add_K = 0x6f
		index = 0 
		sleep_t = ""
		while index < 3:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_K)
			if cach != "X":
				sleep_t = sleep_t + cach
			index = index + 1
			start_add_K = start_add_K + 1
		start_add_L = 0x72
		index = 0 
		start = ""
		while index < 5:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_L)
			if cach != "X":
				start = start + cach
			index = index + 1
			start_add_L = start_add_L + 1
		start_add_M = 0x78
		index = 0 
		end = ""
		while index < 5:
			cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_M)
			if cach != "X":
				end = end + cach
			index = index + 1
			start_add_M = start_add_M + 1
		start_add_N = 0x7e
		index = 0 
		sound = ""
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
	camera.start_preview()
	print("click")
	global num
	file = path+"capture"+str(num)+".jpg"
	check_1(file)
	time.sleep(5)
	camera.capture(path+"capture"+str(num)+".jpg")
	if sound == "on":
		os.system('mpg321 /home/pi/tgn_smart_home/sounds/flash.mp3 &')
	camera.stop_preview()
def preview():
	camera.start_preview()
	time.sleep(30)
	camera.stop_preview()
def make_video(t):
	print("recording")
	camera.start_preview()
	if sound == "on":
		os.system('mpg321 /home/pi/tgn_smart_home/sounds/button.mp3 &')
	global num
	file = path+"video"+str(num)+".h264"
	check_2(file)
	camera.start_recording(path+"video"+str(num)+".h264")
	time.sleep(t)
	camera.stop_recording
	camera.stop_preview()
	if sound == "on":
		os.system('mpg321 /home/pi/tgn_smart_home/sounds/button.mp3 &')
def capture_time():
	global auto_capture
	global count
	var1 = strftime("%H:%M", gmtime())
	if auto_capture == 1:
		count = count + 10
		if count == int(sleep_t):
			make_image()
			count = 0
	if var1 == start:
		if auto_capture == 0:
			print("start")
			auto_capture = 1
			make_image()
		time.sleep(10)
		capture_time()
	elif var1 == end:
		print("stop")
		count = 0
		auto_capture = 0
	else:
		time.sleep(10)
		capture_time()
ini()
command = sys.argv[1]
timer = int(sys.argv[2])
if command == "capture":
	make_image()
if command == "video":
	make_video(timer)
if command == "timer":
	capture_time()
if command == "preview":
	preview()