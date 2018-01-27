#0x6e last add +1
from tgnLIB import *
import time

def rtc_settings():
	ontime = input("ontime example 17:10|4:31 ")
	offtime = input("offtime example 23:10|5:41 ")
	s1 = input("Switch 1 for off set 0 or on set 1: ")
	s2 = input("Switch 2 for off set 0 or on set 1: ")
	s3 = input("Switch 3 for off set 0 or on set 1: ")
	s4 = input("Switch 4 for off set 0 or on set 1: ")
	print("write eeprom, please wait.....")
	write_eeprom(1,0x54,0x00,0x08,s1)
	write_eeprom(1,0x54,0x00,0x09,s2)
	write_eeprom(1,0x54,0x00,0x0a,s3)
	write_eeprom(1,0x54,0x00,0x0b,s4)
	start_add_A = 0x0c
	index = 0 
	while index < 11:
		write_eeprom(1,0x54,0x00,start_add_A,"X")
		index = index + 1
		start_add_A = start_add_A + 1
	start_add_A = 0x0c
	index = 0 
	while index < len(ontime):
		letter = ontime[index]
		write_eeprom(1,0x54,0x00,start_add_A,letter) 
		index = index + 1
		start_add_A = start_add_A + 1
	start_add_B = 0x18
	index = 0 
	while index < 11:
		write_eeprom(1,0x54,0x00,start_add_B,"X")
		index = index + 1
		start_add_B = start_add_B + 1
	start_add_B = 0x18
	index = 0 
	while index < len(offtime):
		letter = offtime[index]
		write_eeprom(1,0x54,0x00,start_add_B,letter) 
		index = index + 1
		start_add_B = start_add_B + 1
	print("ready.......")
	time.sleep(3)

def funk_settings():
	key = input("Key example 10101 ")
	gpio = input("Gpio 26 ")
	b1 = input("Button name 1 ")
	b2 = input("Button name 2 ")
	b3 = input("Button name 3 ")
	b4 = input("Button name 4 ")
	b5 = input("Button name 5 ")
	b6 = input("Button name 6 ")
	print("write eeprom, please wait.....")
	start_add_A = 0x23
	index = 0 
	while index < len(key):
		letter = key[index]
		write_eeprom(1,0x54,0x00,start_add_A,letter) 
		index = index + 1
		start_add_A = start_add_A + 1
	start_add_B = 0x28
	index = 0 
	while index < len(gpio):
		letter = gpio[index]
		write_eeprom(1,0x54,0x00,start_add_B,letter) 
		index = index + 1
		start_add_B = start_add_B + 1
	start_add_C = 0x2a
	index = 0
	while index < 10:
		write_eeprom(1,0x54,0x00,start_add_C,"X")
		index = index + 1
		start_add_C = start_add_C + 1
	start_add_C = 0x2a
	index = 0 
	while index < len(b1):
		letter = b1[index]
		write_eeprom(1,0x54,0x00,start_add_C,letter) 
		index = index + 1
		start_add_C = start_add_C + 1
	start_add_D = 0x34
	index = 0
	while index < 10:
		write_eeprom(1,0x54,0x00,start_add_D,"X")
		index = index + 1
		start_add_D = start_add_D + 1
	start_add_D = 0x34
	index = 0 
	while index < len(b2):
		letter = b2[index]
		write_eeprom(1,0x54,0x00,start_add_D,letter) 
		index = index + 1
		start_add_D = start_add_D + 1
	start_add_E = 0x3e
	index = 0
	while index < 10:
		write_eeprom(1,0x54,0x00,start_add_E,"X")
		index = index + 1
		start_add_E = start_add_E + 1
	start_add_E = 0x3e
	index = 0 
	while index < len(b3):
		letter = b3[index]
		write_eeprom(1,0x54,0x00,start_add_E,letter) 
		index = index + 1
		start_add_E = start_add_E + 1
	start_add_F = 0x48
	index = 0
	while index < 10:
		write_eeprom(1,0x54,0x00,start_add_F,"X")
		index = index + 1
		start_add_F = start_add_F + 1
	start_add_F = 0x48
	index = 0 
	while index < len(b4):
		letter = b4[index]
		write_eeprom(1,0x54,0x00,start_add_F,letter) 
		index = index + 1
		start_add_F = start_add_F + 1
	start_add_G = 0x52
	index = 0
	while index < 10:
		write_eeprom(1,0x54,0x00,start_add_G,"X")
		index = index + 1
		start_add_G = start_add_G + 1
	start_add_G = 0x52
	index = 0 
	while index < len(b5):
		letter = b5[index]
		write_eeprom(1,0x54,0x00,start_add_G,letter) 
		index = index + 1
		start_add_G = start_add_G + 1
	start_add_H = 0x5c
	index = 0
	while index < 10:
		write_eeprom(1,0x54,0x00,start_add_H,"X")
		index = index + 1
		start_add_H = start_add_H + 1
	start_add_H = 0x5c
	index = 0 
	while index < len(b6):
		letter = b6[index]
		write_eeprom(1,0x54,0x00,start_add_H,letter) 
		index = index + 1
		start_add_H = start_add_H + 1

	print("ready.......")
	time.sleep(3)

version = "V.1.9"
start_add_I = 0x68
index = 0 
while index < 5:
	write_eeprom(1,0x54,0x00,start_add_I,"X")
	index = index + 1
	start_add_I = start_add_I + 1
start_add_I = 0x68
index = 0 
while index < len(version):
	letter = version[index]
	write_eeprom(1,0x54,0x00,start_add_I,letter) 
	index = index + 1
	start_add_I = start_add_I + 1
command = sys.argv[1]
if command == "rtc":
	rtc_settings()
if command == "funk":
	funk_settings()