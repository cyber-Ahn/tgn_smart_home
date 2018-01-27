import picamera
import time
import os
from time import gmtime, strftime
from tgnLIB import *

#var
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
	f = open("/home/pi/tgn_smart_home/config/cam.config","r")
	data = []
	for line in f:
		data.append(line)
	global sleep_t
	sleep_t = data[1]
	a,b = sleep_t.split("\n")
	sleep_t = a
	global start
	start = data[3]
	a,b = start.split("\n")
	start = a
	global end
	end = data[5]
	a,b = end.split("\n")
	end = a
	global sound
	sound = data[7]
	a,b = sound.split("\n")
	sound = a
	global path
	path = data[17]
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