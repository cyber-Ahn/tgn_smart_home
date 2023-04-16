#0x03 0x81
from tgnLIB import *
import binascii

# NEW BUTTON

ROM_ADDRESS = 0x00
NFC_ADDRESS = 0x00
spr = "de"
spr_phat = ""
blocknum = 4 
phatrom = "/home/pi/tgn_smart_home/config/rom.csv"

try:
	f_d = open("/home/pi/tgn_smart_home/config/i2c.config","r")
	for line in f_d:
		if "ROM_ADDRESS" in line:
			ROM_ADDRESS = int(line.rstrip().split("*")[1],16)
		if "NFC_ADDRESS" in line:
			NFC_ADDRESS = int(line.rstrip().split("*")[1],16)
except IOError:
	print("cannot open i2c.config.... file not found")

if ifI2C(ROM_ADDRESS) == "found device":
	dataX = read_eeprom(1,ROM_ADDRESS,0x01,0x2a)
	dataX = "2"
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
spr_phat = "/home/pi/tgn_smart_home/language/"+spr+"/"
print(spr_phat)
try:
	f = open(spr_phat+"text.lang","r")
except IOError:
    	print("cannot open text.config.... file not found")
else:
	data = []
	for line in f:
		data.append(line)

def rtc_settings():
	ontime = input((data[70].rstrip()))
	offtime = input((data[71].rstrip()))
	s1 = input((data[72].rstrip()))
	s2 = input((data[73].rstrip()))
	s3 = input((data[74].rstrip()))
	s4 = input((data[75].rstrip()))
	print((data[103].rstrip()))
	write_eeprom(1,ROM_ADDRESS,0x00,0x08,s1)
	write_eeprom(1,ROM_ADDRESS,0x00,0x09,s2)
	write_eeprom(1,ROM_ADDRESS,0x00,0x0a,s3)
	write_eeprom(1,ROM_ADDRESS,0x00,0x0b,s4)
	start_add_A = 0x0c
	index = 0 
	while index < 11:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_A,"X")
		index = index + 1
		start_add_A = start_add_A + 1
	start_add_A = 0x0c
	index = 0 
	while index < len(ontime):
		letter = ontime[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_A,letter) 
		index = index + 1
		start_add_A = start_add_A + 1
	start_add_B = 0x18
	index = 0 
	while index < 11:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_B,"X")
		index = index + 1
		start_add_B = start_add_B + 1
	start_add_B = 0x18
	index = 0 
	while index < len(offtime):
		letter = offtime[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_B,letter) 
		index = index + 1
		start_add_B = start_add_B + 1
	print((data[104].rstrip()))
	time.sleep(3)

def funk_settings():
	key = input((data[76].rstrip()))
	gpio = input((data[77].rstrip()))
	b1 = input((data[78].rstrip()))
	b2 = input((data[79].rstrip()))
	b3 = input((data[80].rstrip()))
	b4 = input((data[81].rstrip()))
	b5 = input((data[82].rstrip()))
	b6 = input((data[83].rstrip()))
	b7 = input((data[136].rstrip()))
	b8 = input((data[137].rstrip()))
	b9 = input((data[138].rstrip()))
	esp2_button = input((data[144].rstrip()))
	print((data[103].rstrip()))
	write_eeprom(1,ROM_ADDRESS,0x01,0x5b,esp2_button)
	start_add_A = 0x23
	index = 0 
	while index < len(key):
		letter = key[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_A,letter) 
		index = index + 1
		start_add_A = start_add_A + 1
	start_add_B = 0x28
	index = 0 
	while index < len(gpio):
		letter = gpio[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_B,letter) 
		index = index + 1
		start_add_B = start_add_B + 1
	start_add_C = 0x2a
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_C,"X")
		index = index + 1
		start_add_C = start_add_C + 1
	start_add_C = 0x2a
	index = 0 
	while index < len(b1):
		letter = b1[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_C,letter) 
		index = index + 1
		start_add_C = start_add_C + 1
	start_add_D = 0x34
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_D,"X")
		index = index + 1
		start_add_D = start_add_D + 1
	start_add_D = 0x34
	index = 0 
	while index < len(b2):
		letter = b2[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_D,letter) 
		index = index + 1
		start_add_D = start_add_D + 1
	start_add_E = 0x3e
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_E,"X")
		index = index + 1
		start_add_E = start_add_E + 1
	start_add_E = 0x3e
	index = 0 
	while index < len(b3):
		letter = b3[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_E,letter) 
		index = index + 1
		start_add_E = start_add_E + 1
	start_add_F = 0x48
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_F,"X")
		index = index + 1
		start_add_F = start_add_F + 1
	start_add_F = 0x48
	index = 0 
	while index < len(b4):
		letter = b4[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_F,letter) 
		index = index + 1
		start_add_F = start_add_F + 1
	start_add_G = 0x52
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_G,"X")
		index = index + 1
		start_add_G = start_add_G + 1
	start_add_G = 0x52
	index = 0 
	while index < len(b5):
		letter = b5[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_G,letter) 
		index = index + 1
		start_add_G = start_add_G + 1
	start_add_H = 0x5c
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_H,"X")
		index = index + 1
		start_add_H = start_add_H + 1
	start_add_H = 0x5c
	index = 0 
	while index < len(b6):
		letter = b6[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_H,letter) 
		index = index + 1
		start_add_H = start_add_H + 1
	start_add_AAA = 0x6d
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAA,"X")
		index = index + 1
		start_add_AAA = start_add_AAA + 1
	start_add_AAA = 0x6d
	index = 0 
	while index < len(b7):
		letter = b7[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAA,letter) 
		index = index + 1
		start_add_AAA = start_add_AAA + 1
	start_add_AAB = 0x78
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAB,"X")
		index = index + 1
		start_add_AAB = start_add_AAB + 1
	start_add_AAB = 0x78
	index = 0 
	while index < len(b8):
		letter = b8[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAB,letter) 
		index = index + 1
		start_add_AAB = start_add_AAB + 1
	start_add_AAC = 0x83
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAC,"X")
		index = index + 1
		start_add_AAC = start_add_AAC + 1
	start_add_AAC = 0x83
	index = 0 
	while index < len(b9):
		letter = b9[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAC,letter) 
		index = index + 1
		start_add_AAC = start_add_AAC + 1
	print((data[104].rstrip()))
	time.sleep(3)

def cam_settings():
	sleep_t = input((data[84].rstrip()))
	start = input((data[85].rstrip()))
	end = input((data[86].rstrip()))
	sound = input((data[87].rstrip()))
	shutdownPort = input((data[88].rstrip()))
	time_set = input((data[89].rstrip()))
	command = input((data[90].rstrip()))
	path = input((data[91].rstrip()))
	print((data[103].rstrip()))
	start_add_K = 0x6f
	index = 0 
	while index < 3:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_K,"X")
		index = index + 1
		start_add_K = start_add_K + 1
	start_add_K = 0x6f
	index = 0 
	while index < len(sleep_t):
		letter = sleep_t[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_K,letter) 
		index = index + 1
		start_add_K = start_add_K + 1
	start_add_L = 0x72
	index = 0 
	while index < 5:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_L,"X")
		index = index + 1
		start_add_L = start_add_L + 1
	start_add_L = 0x72
	index = 0 
	while index < len(start):
		letter = start[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_L,letter) 
		index = index + 1
		start_add_L = start_add_L + 1
	start_add_M = 0x78
	index = 0 
	while index < 5:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_M,"X")
		index = index + 1
		start_add_M = start_add_M + 1
	start_add_M = 0x78
	index = 0 
	while index < len(end):
		letter = end[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_M,letter) 
		index = index + 1
		start_add_M = start_add_M + 1
	start_add_N = 0x7e
	index = 0 
	while index < 3:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_N,"X")
		index = index + 1
		start_add_N = start_add_N + 1
	start_add_N = 0x7e
	index = 0 
	while index < len(sound):
		letter = sound[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_N,letter) 
		index = index + 1
		start_add_N = start_add_N + 1
	start_add_O = 0x82
	index = 0 
	while index < 2:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_O,"X")
		index = index + 1
		start_add_O = start_add_O + 1
	start_add_O = 0x82
	index = 0 
	while index < len(shutdownPort):
		letter = shutdownPort[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_O,letter) 
		index = index + 1
		start_add_O = start_add_O + 1
	start_add_P = 0x85
	index = 0 
	while index < 3:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_P,"X")
		index = index + 1
		start_add_P = start_add_P + 1
	start_add_P = 0x85
	index = 0 
	while index < len(time_set):
		letter = time_set[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_P,letter) 
		index = index + 1
		start_add_P = start_add_P + 1
	start_add_Q = 0x89
	index = 0 
	while index < 7:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_Q,"X")
		index = index + 1
		start_add_Q = start_add_Q + 1
	start_add_Q = 0x89
	index = 0 
	while index < len(command):
		letter = command[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_Q,letter) 
		index = index + 1
		start_add_Q = start_add_Q + 1
	start_add_R = 0x91
	index = 0 
	while index < 20:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_R,"X")
		index = index + 1
		start_add_R = start_add_R + 1
	start_add_R = 0x91
	index = 0 
	while index < len(path):
		letter = path[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_R,letter) 
		index = index + 1
		start_add_R = start_add_R + 1
	print((data[104].rstrip()))
	time.sleep(3)

def waether_settings():
	region = input((data[92].rstrip()))
	wkey = input((data[93].rstrip()))
	print((data[103].rstrip()))
	start_add_S = 0xa7
	index = 0 
	while index < 7:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_S,"X")
		index = index + 1
		start_add_S = start_add_S + 1
	start_add_S = 0xa7
	index = 0 
	while index < len(region):
		letter = region[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_S,letter) 
		index = index + 1
		start_add_S = start_add_S + 1
	start_add_T = 0xaf
	index = 0 
	while index < 32:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_T,"X")
		index = index + 1
		start_add_T = start_add_T + 1
	start_add_T = 0xaf
	index = 0 
	while index < len(wkey):
		letter = wkey[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_T,letter) 
		index = index + 1
		start_add_T = start_add_T + 1
	print((data[104].rstrip()))

def pushbullet_settings():
	pkey = input((data[94].rstrip()))
	print((data[103].rstrip()))
	start_add_U = 0xcf
	index = 0 
	while index < 34:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_U,"X")
		index = index + 1
		start_add_U = start_add_U + 1
	start_add_U = 0xcf
	index = 0 
	while index < len(pkey):
		letter = pkey[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_U,letter) 
		index = index + 1
		start_add_U = start_add_U + 1
	print((data[104].rstrip()))

def webapp_settings():
	port_w = input((data[105].rstrip()))
	ip_w = input((data[106].rstrip()))
	pw_w = input((data[107].rstrip()))
	print((data[103].rstrip()))
	start_add_Y = 0x2b
	index = 0 
	while index < 4:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_Y,"X")
		index = index + 1
		start_add_Y = start_add_Y + 1
	start_add_Y = 0x2b
	index = 0 
	while index < len(port_w):
		letter = port_w[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_Y,letter) 
		index = index + 1
		start_add_Y = start_add_Y + 1
	start_add_Z = 0x30
	index = 0 
	while index < 15:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_Z,"X")
		index = index + 1
		start_add_Z = start_add_Z + 1
	start_add_Z = 0x30
	index = 0 
	while index < len(ip_w):
		letter = ip_w[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_Z,letter) 
		index = index + 1
		start_add_Z = start_add_Z + 1
	start_add_AA = 0x40
	index = 0 
	while index < 15:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AA,"X")
		index = index + 1
		start_add_AA = start_add_AA + 1
	start_add_AA = 0x40
	index = 0 
	while index < len(pw_w):
		letter = pw_w[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AA,letter) 
		index = index + 1
		start_add_AA = start_add_AA + 1
	print((data[104].rstrip()))

def thinkspeak_settings():
	chanl= input((data[95].rstrip()))
	wkey = input((data[96].rstrip()))
	rkey = input((data[97].rstrip()))
	print((data[103].rstrip()))
	start_add_V = 0x01
	index = 0 
	while index < 6:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_V,"X")
		index = index + 1
		start_add_V = start_add_V + 1
	start_add_V = 0x01
	index = 0 
	while index < len(chanl):
		letter = chanl[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_V,letter) 
		index = index + 1
		start_add_V = start_add_V + 1
	start_add_W= 0x07
	index = 0 
	while index < 16:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_W,"#")
		index = index + 1
		start_add_W = start_add_W + 1
	start_add_W = 0x07
	index = 0 
	while index < len(wkey):
		letter = wkey[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_W,letter) 
		index = index + 1
		start_add_W = start_add_W + 1
	start_add_X= 0x18
	index = 0 
	while index < 16:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_X,"#")
		index = index + 1
		start_add_X = start_add_X + 1
	start_add_X = 0x18
	index = 0 
	while index < len(rkey):
		letter = rkey[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_X,letter) 
		index = index + 1
		start_add_X = start_add_X + 1
	print((data[104].rstrip()))

def update_ver():
	version = "V.2.5"
	start_add_I = 0x68
	index = 0 
	while index < 5:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_I,"X")
		index = index + 1
		start_add_I = start_add_I + 1
		print("Write: "+str(start_add_I))
	start_add_I = 0x68
	index = 0 
	while index < len(version):
		letter = version[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_I,letter) 
		index = index + 1
		start_add_I = start_add_I + 1
		print("Write: "+str(start_add_I))

def prog_rom():
	version = "V.2.5"
	ontime = "23:10|4:31"
	offtime = "23:11|5:41"
	s1 = "0"
	s2 = "0"
	s3 = "0"
	s4 = "1"
	key = "10101"
	gpio = "26"
	b1 = "Main_Power"
	b2 = "NAS"
	b3 = "Computer"
	b4 = "WZ_Light"
	b5 = "Floor"
	b6 = "empty"
	b1A = 0
	b2A = 0
	b3A = 0
	b4A = 0
	b5A = 0
	b6A = 0
	screen = 1
	su = 1
	colorSet = 7
	sleep_t = "600"
	start = "22:0"
	end = "6:0"
	sound = "on"
	shutdownPort = "24"
	time_set = "120"
	command = "capture"
	path = "/home/pi/Pictures/"
	region = "6947479"
	wkey = "3aef357118b7ea5d700123785674b45"
	pkey = "o.luRM2iMEGKnns3pzkOUiEAGX3IxxVxZ"
	speech = 1
	Ts = 0
	chanl = "43245"
	wkey = "8WQB01T3F5JE0EZ"
	rkey = "PJGJDHMEUU1TAXQ"
	spr = 2
	port_w = "9090"
	ip_w = "192.168.0.94"
	pw_w = "1234"
	pw = "0"
	alarm_t = "17:55"
	alarm_s = "off"
	com_typ = "ip"
	esp_address = "100.100.100.100"
	esp2_button = "5"
	rssurl = "empty"
	rsslang = "de"
	b7 = "empty"
	b8 = "empty"
	b9 = "empty"
	b7A = 0
	b8A = 0
	b9A = 0
	keys = "210326d3-1gt2-tzd7-a321-5d288f"
	menu_on = "0"
	temp_key = "J6jxLVkL-Rh90ng-Ab1e3z5zWWr5guz"
	temp_url = "https://test_url.de"
	start_add_AAD = 0x2d
	index = 0 
	while index < 32:
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,"X")
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	start_add_AAD = 0x2d
	index = 0
	while index < len(temp_key):
		letter = temp_key[index]
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,letter) 
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	start_add_AAD = 0x4e
	index = 0 
	while index < 50:
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,"X")
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	start_add_AAD = 0x4e
	index = 0
	while index < len(temp_url):
		letter = temp_url[index]
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,letter) 
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	start_add_AAD = 0x01
	index = 0
	while index < 40:
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,"X")
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	start_add_AAD = 0x01
	index = 0 
	while index < len(keys):
		letter = keys[index]
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,letter) 
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	write_eeprom(1,ROM_ADDRESS,0x02,0x6a,str(b7A))
	write_eeprom(1,ROM_ADDRESS,0x02,0x6b,str(b8A))
	write_eeprom(1,ROM_ADDRESS,0x02,0x6c,str(b9A))
	start_add_AAA = 0x6d
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAA,"X")
		index = index + 1
		start_add_AAA = start_add_AAA + 1
		print("Write: "+str(start_add_AAA))
	start_add_AAA = 0x6d
	index = 0 
	while index < len(b7):
		letter = b7[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAA,letter) 
		index = index + 1
		start_add_AAA = start_add_AAA + 1
		print("Write: "+str(start_add_AAA))
	start_add_AAB = 0x78
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAB,"X")
		index = index + 1
		start_add_AAB = start_add_AAB + 1
		print("Write: "+str(start_add_AAB))
	start_add_AAB = 0x78
	index = 0 
	while index < len(b8):
		letter = b8[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAB,letter) 
		index = index + 1
		start_add_AAB = start_add_AAB + 1
		print("Write: "+str(start_add_AAB))
	start_add_AAC = 0x83
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAC,"X")
		index = index + 1
		start_add_AAC = start_add_AAC + 1
		print("Write: "+str(start_add_AAC))
	start_add_AAC = 0x83
	index = 0 
	while index < len(b9):
		letter = b9[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AAC,letter) 
		index = index + 1
		start_add_AAC = start_add_AAC + 1
		print("Write: "+str(start_add_AAC))
	print((data[103].rstrip()))
	write_eeprom(1,ROM_ADDRESS,0x01,0x2a,str(spr))
	write_eeprom(1,ROM_ADDRESS,0x00,0xa6,str(su))
	write_eeprom(1,ROM_ADDRESS,0x00,0x01,str(b1A))
	write_eeprom(1,ROM_ADDRESS,0x00,0x02,str(b2A))
	write_eeprom(1,ROM_ADDRESS,0x00,0x03,str(b3A))
	write_eeprom(1,ROM_ADDRESS,0x00,0x04,str(b4A))
	write_eeprom(1,ROM_ADDRESS,0x00,0x05,str(b5A))
	write_eeprom(1,ROM_ADDRESS,0x00,0x06,str(b6A))
	write_eeprom(1,ROM_ADDRESS,0x00,0x67,str(screen))
	write_eeprom(1,ROM_ADDRESS,0x00,0x07,str(colorSet))
	write_eeprom(1,ROM_ADDRESS,0x00,0xf2,str(speech))
	write_eeprom(1,ROM_ADDRESS,0x00,0xf3,str(Ts))
	write_eeprom(1,ROM_ADDRESS,0x01,0x50,pw)
	write_eeprom(1,ROM_ADDRESS,0x01,0x5b,esp2_button)
	start_add_AF = 0x01
	index = 0 
	while index < 2:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AF,"#")
		index = index + 1
		start_add_AF = start_add_AF + 1
		print("Write: "+str(start_add_AF))
	start_add_AF = 0x01
	index = 0 
	while index < len(rsslang):
		letter = rsslang[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AF,letter)
		index = index + 1
		start_add_AF = start_add_AF + 1
		print("Write: "+str(start_add_AF))
	start_add_AG = 0x04
	index = 0 
	while index < 60:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AG,"#")
		index = index + 1
		start_add_AG = start_add_AG + 1
		print("Write: "+str(start_add_AG))
	start_add_AG = 0x04
	index = 0 
	while index < len(rssurl):
		letter = rssurl[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AG,letter)
		index = index + 1
		start_add_AG = start_add_AG + 1
		print("Write: "+str(start_add_AG))
	start_add_Y = 0x2b
	index = 0 
	while index < 4:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_Y,"X")
		index = index + 1
		start_add_Y = start_add_Y + 1
		print("Write: "+str(start_add_Y))
	start_add_Y = 0x2b
	index = 0 
	while index < len(port_w):
		letter = port_w[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_Y,letter) 
		index = index + 1
		start_add_Y = start_add_Y + 1
		print("Write: "+str(start_add_Y))
	start_add_Z = 0x30
	index = 0 
	while index < 15:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_Z,"X")
		index = index + 1
		start_add_Z = start_add_Z + 1
		print("Write: "+str(start_add_Z))
	start_add_Z = 0x30
	index = 0 
	while index < len(ip_w):
		letter = ip_w[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_Z,letter) 
		index = index + 1
		start_add_Z = start_add_Z + 1
		print("Write: "+str(start_add_Z))
	start_add_I = 0x68
	index = 0 
	while index < 5:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_I,"X")
		index = index + 1
		start_add_I = start_add_I + 1
		print("Write: "+str(start_add_I))
	start_add_I = 0x68
	index = 0 
	while index < len(version):
		letter = version[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_I,letter) 
		index = index + 1
		start_add_I = start_add_I + 1
		print("Write: "+str(start_add_I))
	write_eeprom(1,ROM_ADDRESS,0x00,0x08,s1)
	write_eeprom(1,ROM_ADDRESS,0x00,0x09,s2)
	write_eeprom(1,ROM_ADDRESS,0x00,0x0a,s3)
	write_eeprom(1,ROM_ADDRESS,0x00,0x0b,s4)
	start_add_J = 0x0c
	index = 0 
	while index < 11:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_J,"X")
		index = index + 1
		start_add_J = start_add_J + 1
		print("Write: "+str(start_add_J))
	start_add_J = 0x0c
	index = 0 
	while index < len(ontime):
		letter = ontime[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_J,letter) 
		index = index + 1
		start_add_J = start_add_J + 1
		print("Write: "+str(start_add_J))
	start_add_K = 0x18
	index = 0 
	while index < 11:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_K,"X")
		index = index + 1
		start_add_K = start_add_K + 1
		print("Write: "+str(start_add_K))
	start_add_K = 0x18
	index = 0 
	while index < len(offtime):
		letter = offtime[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_K,letter) 
		index = index + 1
		start_add_K = start_add_K + 1
		print("Write: "+str(start_add_K))
	start_add_A = 0x23
	index = 0 
	while index < len(key):
		letter = key[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_A,letter) 
		index = index + 1
		start_add_A = start_add_A + 1
		print("Write: "+str(start_add_A))
	start_add_B = 0x28
	index = 0 
	while index < len(gpio):
		letter = gpio[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_B,letter) 
		index = index + 1
		start_add_B = start_add_B + 1
		print("Write: "+str(start_add_B))
	start_add_C = 0x2a
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_C,"X")
		index = index + 1
		start_add_C = start_add_C + 1
		print("Write: "+str(start_add_C))
	start_add_C = 0x2a
	index = 0 
	while index < len(b1):
		letter = b1[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_C,letter) 
		index = index + 1
		start_add_C = start_add_C + 1
		print("Write: "+str(start_add_C))
	start_add_D = 0x34
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_D,"X")
		index = index + 1
		start_add_D = start_add_D + 1
		print("Write: "+str(start_add_D))
	start_add_D = 0x34
	index = 0 
	while index < len(b2):
		letter = b2[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_D,letter) 
		index = index + 1
		start_add_D = start_add_D + 1
		print("Write: "+str(start_add_D))
	start_add_E = 0x3e
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_E,"X")
		index = index + 1
		start_add_E = start_add_E + 1
		print("Write: "+str(start_add_E))
	start_add_E = 0x3e
	index = 0 
	while index < len(b3):
		letter = b3[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_E,letter) 
		index = index + 1
		start_add_E = start_add_E + 1
		print("Write: "+str(start_add_E))
	start_add_F = 0x48
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_F,"X")
		index = index + 1
		start_add_F = start_add_F + 1
		print("Write: "+str(start_add_F))
	start_add_F = 0x48
	index = 0 
	while index < len(b4):
		letter = b4[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_F,letter) 
		index = index + 1
		start_add_F = start_add_F + 1
		print("Write: "+str(start_add_F))
	start_add_G = 0x52
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_G,"X")
		index = index + 1
		start_add_G = start_add_G + 1
		print("Write: "+str(start_add_G))
	start_add_G = 0x52
	index = 0 
	while index < len(b5):
		letter = b5[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_G,letter) 
		index = index + 1
		start_add_G = start_add_G + 1
		print("Write: "+str(start_add_G))
	start_add_H = 0x5c
	index = 0
	while index < 10:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_H,"X")
		index = index + 1
		start_add_H = start_add_H + 1
		print("Write: "+str(start_add_H))
	start_add_H = 0x5c
	index = 0 
	while index < len(b6):
		letter = b6[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_H,letter) 
		index = index + 1
		start_add_H = start_add_H + 1
		print("Write: "+str(start_add_H))
	start_add_K = 0x6f
	index = 0 
	while index < 3:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_K,"X")
		index = index + 1
		start_add_K = start_add_K + 1
		print("Write: "+str(start_add_K))
	start_add_K = 0x6f
	index = 0 
	while index < len(sleep_t):
		letter = sleep_t[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_K,letter) 
		index = index + 1
		start_add_K = start_add_K + 1
		print("Write: "+str(start_add_K))
	start_add_L = 0x72
	index = 0 
	while index < 5:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_L,"X")
		index = index + 1
		start_add_L = start_add_L + 1
		print("Write: "+str(start_add_L))
	start_add_L = 0x72
	index = 0 
	while index < len(start):
		letter = start[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_L,letter) 
		index = index + 1
		start_add_L = start_add_L + 1
		print("Write: "+str(start_add_L))
	start_add_M = 0x78
	index = 0 
	while index < 5:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_M,"X")
		index = index + 1
		start_add_M = start_add_M + 1
		print("Write: "+str(start_add_M))
	start_add_M = 0x78
	index = 0 
	while index < len(end):
		letter = end[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_M,letter) 
		index = index + 1
		start_add_M = start_add_M + 1
		print("Write: "+str(start_add_M))
	start_add_N = 0x7e
	index = 0 
	while index < 3:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_N,"X")
		index = index + 1
		start_add_N = start_add_N + 1
		print("Write: "+str(start_add_N))
	start_add_N = 0x7e
	index = 0 
	while index < len(sound):
		letter = sound[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_N,letter) 
		index = index + 1
		start_add_N = start_add_N + 1
		print("Write: "+str(start_add_N))
	start_add_O = 0x82
	index = 0 
	while index < 2:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_O,"X")
		index = index + 1
		start_add_O = start_add_O + 1
		print("Write: "+str(start_add_O))
	start_add_O = 0x82
	index = 0 
	while index < len(shutdownPort):
		letter = shutdownPort[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_O,letter) 
		index = index + 1
		start_add_O = start_add_O + 1
		print("Write: "+str(start_add_O))
	start_add_P = 0x85
	index = 0 
	while index < 3:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_P,"X")
		index = index + 1
		start_add_P = start_add_P + 1
		print("Write: "+str(start_add_P))
	start_add_P = 0x85
	index = 0 
	while index < len(time_set):
		letter = time_set[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_P,letter) 
		index = index + 1
		start_add_P = start_add_P + 1
		print("Write: "+str(start_add_P))
	start_add_Q = 0x89
	index = 0 
	while index < 7:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_Q,"X")
		index = index + 1
		start_add_Q = start_add_Q + 1
		print("Write: "+str(start_add_Q))
	start_add_Q = 0x89
	index = 0 
	while index < len(command):
		letter = command[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_Q,letter) 
		index = index + 1
		start_add_Q = start_add_Q + 1
		print("Write: "+str(start_add_Q))
	start_add_R = 0x91
	index = 0 
	while index < 20:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_R,"X")
		index = index + 1
		start_add_R = start_add_R + 1
		print("Write: "+str(start_add_R))
	start_add_R = 0x91
	index = 0 
	while index < len(path):
		letter = path[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_R,letter) 
		index = index + 1
		start_add_R = start_add_R + 1
		print("Write: "+str(start_add_R))
	start_add_S = 0xa7
	index = 0 
	while index < 7:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_S,"X")
		index = index + 1
		start_add_S = start_add_S + 1
		print("Write: "+str(start_add_S))
	start_add_S = 0xa7
	index = 0 
	while index < len(region):
		letter = region[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_S,letter) 
		index = index + 1
		start_add_S = start_add_S + 1
		print("Write: "+str(start_add_S))
	start_add_T = 0xaf
	index = 0 
	while index < 32:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_T,"X")
		index = index + 1
		start_add_T = start_add_T + 1
		print("Write: "+str(start_add_T))
	start_add_T = 0xaf
	index = 0 
	while index < len(wkey):
		letter = wkey[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_T,letter) 
		index = index + 1
		start_add_T = start_add_T + 1
		print("Write: "+str(start_add_T))
	start_add_U = 0xcf
	index = 0 
	while index < 34:
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_U,"X")
		index = index + 1
		start_add_U = start_add_U + 1
		print("Write: "+str(start_add_U))
	start_add_U = 0xcf
	index = 0 
	while index < len(pkey):
		letter = pkey[index]
		write_eeprom(1,ROM_ADDRESS,0x00,start_add_U,letter) 
		index = index + 1
		start_add_U = start_add_U + 1
		print("Write: "+str(start_add_U))
	start_add_V = 0x01
	index = 0 
	while index < 6:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_V,"X")
		index = index + 1
		start_add_V = start_add_V + 1
		print("Write: "+str(start_add_V))
	start_add_V = 0x01
	index = 0 
	while index < len(chanl):
		letter = chanl[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_V,letter) 
		index = index + 1
		start_add_V = start_add_V + 1
		print("Write: "+str(start_add_V))
	start_add_W= 0x07
	index = 0 
	while index < 16:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_W,"#")
		index = index + 1
		start_add_W = start_add_W + 1
		print("Write: "+str(start_add_W))
	start_add_W = 0x07
	index = 0 
	while index < len(wkey):
		letter = wkey[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_W,letter) 
		index = index + 1
		start_add_W = start_add_W + 1
		print("Write: "+str(start_add_W))
	start_add_X= 0x18
	index = 0 
	while index < 16:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_X,"#")
		index = index + 1
		start_add_X = start_add_X + 1
		print("Write: "+str(start_add_X))
	start_add_X = 0x18
	index = 0 
	while index < len(rkey):
		letter = rkey[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_X,letter) 
		index = index + 1
		start_add_X = start_add_X + 1
		print("Write: "+str(start_add_X))
	start_add_AA = 0x40
	index = 0 
	while index < 15:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AA,"X")
		index = index + 1
		start_add_AA = start_add_AA + 1
		print("Write: "+str(start_add_AA))
	start_add_AA = 0x40
	index = 0 
	while index < len(pw_w):
		letter = pw_w[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AA,letter)
		index = index + 1
		start_add_AA = start_add_AA + 1
		print("Write: "+str(start_add_AA))
	start_add_AB = 0x51
	index = 0 
	while index < 5:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AB,"X")
		index = index + 1
		start_add_AB = start_add_AB + 1
		print("Write: "+str(start_add_AB))
	start_add_AB = 0x51
	index = 0 
	while index < len(alarm_t):
		letter = alarm_t[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AB,letter)
		index = index + 1
		start_add_AB = start_add_AB + 1
		print("Write: "+str(start_add_AB))
	start_add_AC = 0x57
	index = 0 
	while index < 3:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AC,"X")
		index = index + 1
		start_add_AC = start_add_AC + 1
		print("Write: "+str(start_add_AC))
	start_add_AC = 0x57
	index = 0 
	while index < len(alarm_s):
		letter = alarm_s[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AC,letter)
		index = index + 1
		start_add_AC = start_add_AC + 1
		print("Write: "+str(start_add_AC))
	start_add_AD = 0x5b
	index = 0
	while index < 3:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AD,"X")
		index = index + 1
		start_add_AD = start_add_AD + 1
		print("Write: "+str(start_add_AD))
	start_add_AD = 0x5b
	index = 0
	while index < len(com_typ):
		letter = com_typ[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AD,letter)
		index = index + 1
		start_add_AD = start_add_AD + 1
		print("Write: "+str(start_add_AD))
	start_add_AE = 0x5f
	index = 0
	while index < 30:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AE,"#")
		index = index + 1
		start_add_AE = start_add_AE + 1
		print("Write: "+str(start_add_AE))
	start_add_AE = 0x5f
	index = 0
	while index < len(esp_address):
		letter = esp_address[index] 
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AE,letter)
		index = index + 1
		start_add_AE = start_add_AE + 1
		print("Write: "+str(start_add_AE))
	write_eeprom(1,ROM_ADDRESS,0x03,0x2b,str(menu_on))

	print((data[104].rstrip()))
	time.sleep(3)

def alarm_settings():
	alarm_t = input((data[116].rstrip()))
	alarm_s = input((data[117].rstrip()))
	print((data[103].rstrip()))
	start_add_AB = 0x51
	index = 0 
	while index < 5:
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AB,"X")
		index = index + 1
		start_add_AB = start_add_AB + 1
	start_add_AB = 0x51
	index = 0 
	while index < len(alarm_t):
		letter = alarm_t[index]
		write_eeprom(1,ROM_ADDRESS,0x01,start_add_AB,letter)
		index = index + 1
		start_add_AB = start_add_AB + 1
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
	print((data[104].rstrip()))
	time.sleep(3)

def rss_settings():
	rssurl = input((data[120].rstrip()))
	rsslang = input((data[121].rstrip()))
	print((data[103].rstrip()))
	start_add_AF = 0x01
	index = 0 
	while index < 2:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AF,"#")
		index = index + 1
		start_add_AF = start_add_AF + 1
	start_add_AF = 0x01
	index = 0 
	while index < len(rsslang):
		letter = rsslang[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AF,letter)
		index = index + 1
		start_add_AF = start_add_AF + 1
	start_add_AG = 0x04
	index = 0 
	while index < 60:
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AG,"#")
		index = index + 1
		start_add_AG = start_add_AG + 1
	start_add_AG = 0x04
	index = 0 
	while index < len(rssurl):
		letter = rssurl[index]
		write_eeprom(1,ROM_ADDRESS,0x02,start_add_AG,letter)
		index = index + 1
		start_add_AG = start_add_AG + 1
	print((data[104].rstrip()))
	time.sleep(3)

def save_nfc():
	pn532 = Pn532_i2c()
	pn532.SAMconfigure()
	print((data[98].rstrip()))
	card_data = pn532.read_mifare().get_data()
	name = encode(input((data[99].rstrip())))
	function = encode(input((data[100].rstrip())))
	card_data = str(binascii.hexlify(card_data))
	card_data=card_data+"|"+str(binascii.hexlify(name))+"|"+str(binascii.hexlify(function))+"\n"
	file = open("/home/pi/tgn_smart_home/config/logfile.log","a")
	file.write(card_data)
	file.close()
	print(card_data)
	time.sleep(4)

def remove_nfc():
	pn532 = Pn532_i2c()
	pn532.SAMconfigure()
	print((data[101].rstrip()))
	card_data = pn532.read_mifare().get_data()
	card_data = str(binascii.hexlify(card_data))
	file = open("/home/pi/tgn_smart_home/config/logfile.log","r")
	lines = file.readlines()
	file.close()
	file = open("/home/pi/tgn_smart_home/config/logfile.log","w")
	for line in lines:
		cach = line
		cachB=cach.split("|")
		if cachB[0]!=card_data:
			file.write(line)
		else:
			print((data[102].rstrip())+cachB[0])
	file.close()
	time.sleep(4)

def show_nfc():
	file = open("/home/pi/tgn_smart_home/config/logfile.log","r")
	lines = file.readlines()
	file.close()
	for line in lines:
		print(line)

def sinric():
	keys = input("ApiKey:")
	print("add Devices in /config/system.comfig at line 13")
	time.sleep(10)
	start_add_AAD = 0x01
	index = 0
	while index < 40:
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,"X")
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	start_add_AAD = 0x01
	index = 0 
	while index < len(keys):
		letter = keys[index]
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,letter) 
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))

def test():
	print("nothing")

def webinterface_set():
	temp_key = input("User_Key:")
	temp_url = input("Url:")
	start_add_AAD = 0x2d
	index = 0 
	while index < 32:
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,"X")
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	start_add_AAD = 0x2d
	index = 0
	while index < len(temp_key):
		letter = temp_key[index]
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,letter) 
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	start_add_AAD = 0x4e
	index = 0 
	while index < 50:
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,"X")
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))
	start_add_AAD = 0x4e
	index = 0
	while index < len(temp_url):
		letter = temp_url[index]
		write_eeprom(1,ROM_ADDRESS,0x03,start_add_AAD,letter) 
		index = index + 1
		start_add_AAD = start_add_AAD + 1
		print("Write: "+str(start_add_AAD))

def clear_mqtt():
	os.system('sudo systemctl stop mosquitto.service')
	os.system('sudo rm /var/lib/mosquitto/mosquitto.db')
	os.system('sudo systemctl start mosquitto.service')
	os.system('sudo systemctl status mosquitto.service')
	time.sleep(10)
	os.system('sudo reboot')

def base64_set():
	data = input("Data:")
	cach = encode(data)
	print(cach)
	cach_b = decode(cach)
	print(cach_b)

if __name__ == "__main__":
	#setRTC()
	print("python3 settings.py command")
	print("commands: rtc / funk / install_rom / cam / weather / pushb / save_nfc / remove_nfc / show_nfc / thinkspeak / alarm / rss / update / backup / restore / sinric / clear_mqtt / webinterface / base64")

command = sys.argv[1]
if command == "rtc":
	rtc_settings()
if command == "sinric":
    sinric()
if command == "funk":
	funk_settings()
if command == "install_rom":
	print("Loading")
	prog_rom()
if command == "cam":
	cam_settings()
if command == "weather":
	waether_settings()
if command == "pushb":
	pushbullet_settings()
if command == "save_nfc":
	save_nfc()
if command == "remove_nfc":
	remove_nfc()
if command == "show_nfc":
	show_nfc()
if command == "thinkspeak":
	thinkspeak_settings()
if command == "webapp":
	webapp_settings()
if command == "alarm":
	alarm_settings()
if command == "rss":
	rss_settings()
if command == "update":
	update_ver()
if command == "backup":
	backup_rom(blocknum, phatrom)
if command == "restore":
	restore_rom(blocknum, phatrom)
if command == "test":
	test()
if command == "clear_mqtt":
	clear_mqtt()
if command == "webinterface":
	webinterface_set()
if command == "base64":
	base64_set()
