import RPi.GPIO as GPIO
from MCP23017 import *
from subprocess import call
import time
import socket
import os
mcp = MCP230XX(busnum = 1, address = 0x20, num_gpios = 16)
mcp.config(1, 0)
#var
shutdownPort = 26
command = "capture"
time_set = "0"
#read config
f = open("/home/pi/tgn_smart_home/config/cam.config","r")
data = []
for line in f:
	data.append(line)
shutdownPortB = data[9]
a,b = shutdownPortB.split("\n")
shutdownPort = int(a)
command = data[11]
a,b = command.split("\n")
command = a
time_set = data[13]
a,b = time_set.split("\n")
time_set = a
print(str(shutdownPort)+"-"+command+"-"+time_set) 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(shutdownPort, GPIO.IN)
def buttonStateChanged(pin):
	if not (GPIO.input(pin)):
		mcp.output(1, 1)
        	print"click"
		setn = "python /home/pi/tgn_smart_home/libs/auto_cam.py "+command+" "+time_set
		os.system(setn)
		time.sleep(30)
		mcp.output(1, 0)
		print("release")
GPIO.add_event_detect(shutdownPort, GPIO.BOTH, callback=buttonStateChanged)
while True:
	time.sleep(5)