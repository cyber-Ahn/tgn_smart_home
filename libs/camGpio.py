import RPi.GPIO as GPIO
from tgnLIB import *
from subprocess import call
import time
import socket
import os

#var
ROM_ADDRESS = 0x53
MCP_ADDRESS = 0x20
shutdownPort = 26
command = "capture"
time_set = "0"
MCPpower = 0

if ifI2C(MCP_ADDRESS) == "found device":
	global MCPpower
	MCPpower = 1
	mcp = MCP230XX(busnum = 1, address = 0x20, num_gpios = 16)
	mcp.config(1, 0)

#read config
if ifI2C(ROM_ADDRESS) == "found device":
	start_add_O = 0x82
	index = 0 
	shutdownPortA = ""
	while index < 2:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_O)
		if cach != "X":
			shutdownPortA = shutdownPortA + cach
		index = index + 1
		start_add_O = start_add_O + 1
	shutdownPort = int(shutdownPortA)
	start_add_Q = 0x89
	index = 0 
	command = ""
	while index < 7:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_Q)
		if cach != "X":
			command = command + cach
		index = index + 1
		start_add_Q = start_add_Q + 1
	start_add_P = 0x85
	index = 0 
	time_setA = ""
	while index < 3:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_P)
		if cach != "X":
			time_set = time_set + cach
		index = index + 1
		start_add_P = start_add_P + 1
print(str(shutdownPort)+"-"+command+"-"+time_set) 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(shutdownPort, GPIO.IN)
def buttonStateChanged(pin):
	if not (GPIO.input(pin)):
		if MCPpower == 1:
			mcp.output(1, 1)
		print("click")
		setn = "python3 /home/pi/tgn_smart_home/libs/auto_cam.py "+command+" "+time_set
		os.system(setn)
		time.sleep(30)
		if MCPpower == 1:
			mcp.output(1, 0)
		print("release")
GPIO.add_event_detect(shutdownPort, GPIO.BOTH, callback=buttonStateChanged)
while True:
	time.sleep(5)