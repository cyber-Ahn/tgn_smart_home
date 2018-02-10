import picamera
import re
import smbus
import time
import socket
import os
import sys
import os, sys
import os.path
import Adafruit_DHT
import datetime
import json
import urllib.request
import requests
import subprocess
import RPi.GPIO as GPIO
from time import gmtime, strftime
from time import sleep

address = 0x51
register = 0x02
zone = 1
w  = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
bus = smbus.SMBus(1)

MCP23017_IODIRA = 0x00
MCP23017_IODIRB = 0x01
MCP23017_GPIOA  = 0x12
MCP23017_GPIOB  = 0x13
MCP23017_GPPUA  = 0x0C
MCP23017_GPPUB  = 0x0D
MCP23017_OLATA  = 0x14
MCP23017_OLATB  = 0x15
MCP23008_GPIOA  = 0x09
MCP23008_GPPUA  = 0x06
MCP23008_OLATA  = 0x0A

I2CBUS = 1
LCD_ADDRESS = 0x3f
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00
En = 0b00000100
Rw = 0b00000010
Rs = 0b00000001

ROM_ADDRESS = 0x53

REMOTE_SERVER = "www.google.com"

class MCP230XX(object):
    OUTPUT = 0
    INPUT = 1

    def __init__(self, address, num_gpios, busnum=-1):
        assert num_gpios >= 0 and num_gpios <= 16, "Number of GPIOs must be between 0 and 16"
        self.i2c = I2C(address=address, busnum=busnum)
        self.address = address
        self.num_gpios = num_gpios

        # set defaults
        if num_gpios <= 8:
            self.i2c.write8(MCP23017_IODIRA, 0xFF)  # all inputs on port A
            self.direction = self.i2c.readU8(MCP23017_IODIRA)
            self.i2c.write8(MCP23008_GPPUA, 0x00)
        elif num_gpios > 8 and num_gpios <= 16:
            self.i2c.write8(MCP23017_IODIRA, 0xFF)  # all inputs on port A
            self.i2c.write8(MCP23017_IODIRB, 0xFF)  # all inputs on port B
            self.direction = self.i2c.readU8(MCP23017_IODIRA)
            self.direction |= self.i2c.readU8(MCP23017_IODIRB) << 8
            self.i2c.write8(MCP23017_GPPUA, 0x00)
            self.i2c.write8(MCP23017_GPPUB, 0x00)

    def _changebit(self, bitmap, bit, value):
        assert value == 1 or value == 0, "Value is %s must be 1 or 0" % value
        if value == 0:
            return bitmap & ~(1 << bit)
        elif value == 1:
            return bitmap | (1 << bit)

    def _readandchangepin(self, port, pin, value, currvalue = None):
        assert pin >= 0 and pin < self.num_gpios, "Pin number %s is invalid, only 0-%s are valid" % (pin, self.num_gpios)
        #assert self.direction & (1 << pin) == 0, "Pin %s not set to output" % pin
        if not currvalue:
             currvalue = self.i2c.readU8(port)
        newvalue = self._changebit(currvalue, pin, value)
        self.i2c.write8(port, newvalue)
        return newvalue


    def pullup(self, pin, value):
        if self.num_gpios <= 8:
            return self._readandchangepin(MCP23008_GPPUA, pin, value)
        if self.num_gpios <= 16:
            lvalue = self._readandchangepin(MCP23017_GPPUA, pin, value)
            if (pin < 8):
                return
            else:
                return self._readandchangepin(MCP23017_GPPUB, pin-8, value) << 8

    # Set pin to either input or output mode
    def config(self, pin, mode):
        if self.num_gpios <= 8:
            self.direction = self._readandchangepin(MCP23017_IODIRA, pin, mode)
        if self.num_gpios <= 16:
            if (pin < 8):
                self.direction = self._readandchangepin(MCP23017_IODIRA, pin, mode)
            else:
                self.direction |= self._readandchangepin(MCP23017_IODIRB, pin-8, mode) << 8

        return self.direction

    def output(self, pin, value):
        # assert self.direction & (1 << pin) == 0, "Pin %s not set to output" % pin
        if self.num_gpios <= 8:
            self.outputvalue = self._readandchangepin(MCP23008_GPIOA, pin, value, self.i2c.readU8(MCP23008_OLATA))
        if self.num_gpios <= 16:
            if (pin < 8):
                self.outputvalue = self._readandchangepin(MCP23017_GPIOA, pin, value, self.i2c.readU8(MCP23017_OLATA))
            else:
                self.outputvalue = self._readandchangepin(MCP23017_GPIOB, pin-8, value, self.i2c.readU8(MCP23017_OLATB)) << 8

        return self.outputvalue


        self.outputvalue = self._readandchangepin(MCP23017_IODIRA, pin, value, self.outputvalue)
        return self.outputvalue

    def input(self, pin):
        assert pin >= 0 and pin < self.num_gpios, "Pin number %s is invalid, only 0-%s are valid" % (pin, self.num_gpios)
        assert self.direction & (1 << pin) != 0, "Pin %s not set to input" % pin
        if self.num_gpios <= 8:
            value = self.i2c.readU8(MCP23008_GPIOA)
        elif self.num_gpios > 8 and self.num_gpios <= 16:
            value = self.i2c.readU8(MCP23017_GPIOA)
            value |= self.i2c.readU8(MCP23017_GPIOB) << 8
        return value & (1 << pin)

    def readU8(self):
        result = self.i2c.readU8(MCP23008_OLATA)
        return(result)

    def readS8(self):
        result = self.i2c.readU8(MCP23008_OLATA)
        if (result > 127): result -= 256
        return result

    def readU16(self):
        assert self.num_gpios >= 16, "16bits required"
        lo = self.i2c.readU8(MCP23017_OLATA)
        hi = self.i2c.readU8(MCP23017_OLATB)
        return((hi << 8) | lo)

    def readS16(self):
        assert self.num_gpios >= 16, "16bits required"
        lo = self.i2c.readU8(MCP23017_OLATA)
        hi = self.i2c.readU8(MCP23017_OLATB)
        if (hi > 127): hi -= 256
        return((hi << 8) | lo)

    def write8(self, value):
        self.i2c.write8(MCP23008_OLATA, value)

    def write16(self, value):
        assert self.num_gpios >= 16, "16bits required"
        self.i2c.write8(MCP23017_OLATA, value & 0xFF)
        self.i2c.write8(MCP23017_OLATB, (value >> 8) & 0xFF)

class MCP230XX_GPIO(object):
    OUT = 0
    IN = 1
    BCM = 0
    BOARD = 0
    def __init__(self, busnum, address, num_gpios):
        self.chip = Adafruit_MCP230XX(address, num_gpios, busnum)
    def setmode(self, mode):
        # do nothing
        pass
    def setup(self, pin, mode):
        self.chip.config(pin, mode)
    def input(self, pin):
        return self.chip.input(pin)
    def output(self, pin, value):
        self.chip.output(pin, value)
    def pullup(self, pin, value):
        self.chip.pullup(pin, value)

class I2C(object):

  @staticmethod
  def getPiRevision():
    "Gets the version number of the Raspberry Pi board"
    # Revision list available at: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
    try:
      with open('/proc/cpuinfo', 'r') as infile:
        for line in infile:
          # Match a line of the form "Revision : 0002" while ignoring extra
          # info in front of the revsion (like 1000 when the Pi was over-volted).
          match = re.match('Revision\s+:\s+.*(\w{4})$', line)
          if match and match.group(1) in ['0000', '0002', '0003']:
            # Return revision 1 if revision ends with 0000, 0002 or 0003.
            return 1
          elif match:
            # Assume revision 2 if revision ends with any other 4 chars.
            return 2
        # Couldn't find the revision, assume revision 0 like older code for compatibility.
        return 0
    except:
      return 0

  @staticmethod
  def getPiI2CBusNumber():
    # Gets the I2C bus number /dev/i2c#
    return 1 if Adafruit_I2C.getPiRevision() > 1 else 0

  def __init__(self, address, busnum=-1, debug=False):
    self.address = address
    # By default, the correct I2C bus is auto-detected using /proc/cpuinfo
    # Alternatively, you can hard-code the bus version below:
    # self.bus = smbus.SMBus(0); # Force I2C0 (early 256MB Pi's)
    # self.bus = smbus.SMBus(1); # Force I2C1 (512MB Pi's)
    self.bus = smbus.SMBus(busnum if busnum >= 0 else Adafruit_I2C.getPiI2CBusNumber())
    self.debug = debug

  def reverseByteOrder(self, data):
    "Reverses the byte order of an int (16-bit) or long (32-bit) value"
    # Courtesy Vishal Sapre
    byteCount = len(hex(data)[2:].replace('L','')[::2])
    val       = 0
    for i in range(byteCount):
      val    = (val << 8) | (data & 0xff)
      data >>= 8
    return val

  def errMsg(self):
    print("Error accessing 0x%02X: Check your I2C address" % self.address)
    return -1

  def write8(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    try:
      self.bus.write_byte_data(self.address, reg, value)
      if self.debug:
        print("I2C: Wrote 0x%02X to register 0x%02X" % (value, reg))
    except IOError:
      return self.errMsg()

  def write16(self, reg, value):
    "Writes a 16-bit value to the specified register/address pair"
    try:
      self.bus.write_word_data(self.address, reg, value)
      if self.debug:
        print ("I2C: Wrote 0x%02X to register pair 0x%02X,0x%02X" %
         (value, reg, reg+1))
    except IOError:
      return self.errMsg()

  def writeRaw8(self, value):
    "Writes an 8-bit value on the bus"
    try:
      self.bus.write_byte(self.address, value)
      if self.debug:
        print("I2C: Wrote 0x%02X" % value)
    except IOError:
      return self.errMsg()

  def writeList(self, reg, list):
    "Writes an array of bytes using I2C format"
    try:
      if self.debug:
        print("I2C: Writing list to register 0x%02X:" % reg)
        print(list)
      self.bus.write_i2c_block_data(self.address, reg, list)
    except IOError:
      return self.errMsg()

  def readList(self, reg, length):
    "Read a list of bytes from the I2C device"
    try:
      results = self.bus.read_i2c_block_data(self.address, reg, length)
      if self.debug:
        print ("I2C: Device 0x%02X returned the following from reg 0x%02X" %
         (self.address, reg))
        print(results)
      return results
    except IOError:
      return self.errMsg()

  def readU8(self, reg):
    "Read an unsigned byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if self.debug:
        print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
         (self.address, result & 0xFF, reg))
      return result
    except IOError:
      return self.errMsg()

  def readS8(self, reg):
    "Reads a signed byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if result > 127: result -= 256
      if self.debug:
        print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
         (self.address, result & 0xFF, reg))
      return result
    except IOError:
      return self.errMsg()

  def readU16(self, reg, little_endian=True):
    "Reads an unsigned 16-bit value from the I2C device"
    try:
      result = self.bus.read_word_data(self.address,reg)
      # Swap bytes if using big endian because read_word_data assumes little 
      # endian on ARM (little endian) systems.
      if not little_endian:
        result = ((result << 8) & 0xFF00) + (result >> 8)
      if (self.debug):
        print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
      return result
    except IOError:
      return self.errMsg()

  def readS16(self, reg, little_endian=True):
    "Reads a signed 16-bit value from the I2C device"
    try:
      result = self.readU16(reg,little_endian)
      if result > 32767: result -= 65536
      return result
    except IOError:
      return self.errMsg()

class RemoteSwitch(object):
        repeat = 10 # Number of transmissions
        pulselength = 300 # microseconds
        GPIOMode = GPIO.BCM
       
        def __init__(self, device, key=[1,1,1,1,1], pin=4):            
                self.pin = pin
                self.key = key
                self.device = device
                GPIO.setmode(self.GPIOMode)
                GPIO.setup(self.pin, GPIO.OUT)
               
        def switchOn(self):
                self._switch(GPIO.HIGH)
 
        def switchOff(self):
                self._switch(GPIO.LOW)
 
        def _switch(self, switch):
                self.bit = [142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 136, 128, 0, 0, 0]          
 
                for t in range(5):
                        if self.key[t]:
                                self.bit[t]=136
                x=1
                for i in range(1,6):
                        if self.device & x > 0:
                                self.bit[4+i] = 136
                        x = x<<1
 
                if switch == GPIO.HIGH:
                        self.bit[10] = 136
                        self.bit[11] = 142
                               
                bangs = []
                for y in range(16):
                        x = 128
                        for i in range(1,9):
                                b = (self.bit[y] & x > 0) and GPIO.HIGH or GPIO.LOW
                                bangs.append(b)
                                x = x>>1
                               
                GPIO.output(self.pin, GPIO.LOW)
                for z in range(self.repeat):
                        for b in bangs:
                                GPIO.output(self.pin, b)
                                time.sleep(self.pulselength/1000000.)

class i2c_device:
   def __init__(self, addr, port=I2CBUS):
      self.addr = addr
      self.bus = smbus.SMBus(port)
   def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      sleep(0.0001)
   def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self.addr, cmd, data)
      sleep(0.0001)
   def write_block_data(self, cmd, data):
      self.bus.write_block_data(self.addr, cmd, data)
      sleep(0.0001)
   def read(self):
      return self.bus.read_byte(self.addr)
   def read_data(self, cmd):
      return self.bus.read_byte_data(self.addr, cmd)
   def read_block_data(self, cmd):
      return self.bus.read_block_data(self.addr, cmd)

class lcd:
   #initializes objects and lcd
   def __init__(self):
      self.lcd_device = i2c_device(LCD_ADDRESS)
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x02)
      self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
      sleep(0.2)
   def lcd_strobe(self, data):
      self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)
   def lcd_write_four_bits(self, data):
      self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
      self.lcd_strobe(data)
   def lcd_write(self, cmd, mode=0):
      self.lcd_write_four_bits(mode | (cmd & 0xF0))
      self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))
   def lcd_write_char(self, charvalue, mode=1):
      self.lcd_write_four_bits(mode | (charvalue & 0xF0))
      self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))
   def lcd_display_string(self, string, line=1, pos=0):
    if line == 1:
      pos_new = pos
    elif line == 2:
      pos_new = 0x40 + pos
    elif line == 3:
      pos_new = 0x14 + pos
    elif line == 4:
      pos_new = 0x54 + pos
    self.lcd_write(0x80 + pos_new)
    for char in string:
      self.lcd_write(ord(char), Rs)
   def lcd_clear(self):
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_RETURNHOME)
   def backlight(self, state): # for state, 1 = on, 0 = off
      if state == 1:
         self.lcd_device.write_cmd(LCD_BACKLIGHT)
      elif state == 0:
         self.lcd_device.write_cmd(LCD_NOBACKLIGHT)
   def lcd_load_custom_chars(self, fontdata):
      self.lcd_write(0x40);
      for char in fontdata:
         for line in char:
            self.lcd_write_char(line)

def ifI2C(add):
	add = hex(add)
	p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
	out = "not found"
	for i in range(0,9):
		line = str(p.stdout.readline()).rstrip()
		if i >> 0:
			cach=line.split(": ")
			cachB=cach[1].split(" ")
			for x in range(len(cachB)):
				if cachB[x]!="" and cachB[x]!="--":
					if add==("0x"+cachB[x]):
						out="found device"
	return out

def getMAC(interface):
	try:
		str = open('/sys/class/net/%s/address' %interface).read()
	except:
		str = "00:00:00:00:00:00"
	return str[0:17]

def allowed_key(id):
	allowed = "yes"
	if id == "3aef357118b7ea5d700123785674b45e":
		if getMAC("eth0") == "b8:27:eb:76:2e:10":
			allowed = "yes"
		else:
			allowed = "no"
	return allowed

def is_connected(hostname):
  try:
    host = socket.gethostbyname(hostname)
    s = socket.create_connection((host, 80), 2)
    return "Online"
  except:
     pass
  return "Offline"

def toHex(s):
	lst = []
	for ch in s:
		hv = hex(ord(ch)).replace('0x', '')
		if len(hv) == 1:
			hv = '0'+hv
		lst.append("0x"+hv)
	return lst

def stream():
	setn = "raspivid -o - -t 0 -hf -w 800 -h 400 -fps 24 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264"
	os.system(setn)

def toStr(s):
	cachA = ""
	for x in range(len(s)):
		cachB = s[x].split("x")
		cachA=cachA+(bytes.fromhex(cachB[1]).decode('utf-8'))
	return cachA
	
def write_eeprom(bus,add,block,reg,data):
	if ifI2C(add) == "found device":
		wr = []
		cach = hex(ord(data))
		wr.append(reg)
		wr.append(int(cach,16))
		bus = smbus.SMBus(bus)
		bus.write_i2c_block_data(add,block,wr)
		time.sleep(0.5)

def read_eeprom(bus,add,block,reg):
	if ifI2C(add) == "found device":
		bus = smbus.SMBus(bus)
		bus.write_i2c_block_data(add, block, [reg])
		cach = hex(bus.read_byte(add))
		cachB = cach.split("x")
		out = (bytes.fromhex(cachB[1]).decode('utf-8'))
		return out
		time.sleep(0.5)

default_key = [1,0,0,0,1]
default_pin = 12
start_add_A = 0x23
index = 0 
keyA = ""
if ifI2C(ROM_ADDRESS) == "found device":
	while index < 5:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_A)
		if cach != "X":
			keyA = keyA + cach
		index = index + 1
		start_add_A = start_add_A + 1
	index = 0 
	cachKey=[]
	while index < len(keyA):
		letter = int(keyA[index])
		cachKey.append(letter)
		index = index + 1
	default_key=cachKey
	start_add_B = 0x28
	index = 0 
	gpioA = ""
	while index < 2:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_B)
		if cach != "X":
			gpioA = gpioA + cach
		index = index + 1
		start_add_B = start_add_B + 1
	default_pin=int(gpioA)

def send(chan,stat):
	GPIO.setwarnings(False)
	device = RemoteSwitch(device= chan,key=default_key,pin=default_pin)
	if stat == 1:
		device.switchOn()
	else:
		device.switchOff()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def getCpuTemperature():
	tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
	cpu_temp = tempFile.read()
	tempFile.close()
	return float(cpu_temp)/1000

def pcf8563ReadTime():
	t = bus.read_i2c_block_data(address,register,7);
	t[0] = t[0]&0x7F  #sec
	t[1] = t[1]&0x7F  #min
	t[2] = t[2]&0x3F  #hour
	t[3] = t[3]&0x3F  #day
	t[4] = t[4]&0x07  #month   -> dayname
	t[5] = t[5]&0x1F  #dayname -> month
	return("%s  20%x/%x/%x %x:%x:%x" %(w[t[4]],t[6],t[5],t[3],t[2],t[1],t[0]))

def setRTC():
	var1 = strftime("%a-%Y-%m-%d-%H-%M-%S", gmtime())
	var2 = var1.split("-")
	year_s = "0x"+str(int(var2[1]) - 2000)
	year = int(year_s,16)
	day_s = "0x"+str(int(var2[3]))
	day = int(day_s,16)
	h_s = "0x"+str(int(var2[4])+zone)
	h = int(h_s,16)
	min_s = "0x"+str(int(var2[5]))
	min = int(min_s,16)
	sec_s = "0x"+str(int(var2[6]))
	sec = int(sec_s,16)
	day_n_s = "0x"+str(w.index(var2[0]))
	day_n = int(day_n_s,16)
	mon_s = "0x"+str(int(var2[2]))
	mon = int(mon_s,16)
	NowTime = [sec,min,h,day,day_n,mon,year]
	bus.write_i2c_block_data(address,register,NowTime)
	print("RTC set to:" + strftime("%a-%Y-%m-%d-%H-%M-%S", gmtime()) + " +" + str(zone) + "h")

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time

def get_icon_name(data):
	icon = "na.png"
	if data == "200" or data == "211" or data == "212" or data == "221" or data == "905" or data == "960" or data == "961":
		icon = "thunderstorms.png"
	if data == "201" or data == "202" or data == "210":
		icon = "thundery_showers.png"
	if data == "230" or data == "231" or data == "232":
		icon = "cloudy_with_light_rain.png"
	if data == "300" or data == "301" or data == "302" or data == "310" or data == "311" or data == "312" or data == "313" or data == "314" or data == "321":
		icon = "cloudy_with_heavy_hail.png"
	if data == "500" or data == "501" or data == "502" or data == "503" or data == "504":
		icon = "heavy_rain_showers.png"
	if data == "511":
		icon = "cloudy_with_sleet.png"
	if data == "520" or data == "521" or data == "522" or data == "531":
		icon = "cloudy_with_light_hail_night.png"
	if data == "600" or data == "601" or data == "602":
		icon = "cloudy_with_light_snow.png"
	if data == "611" or data == "612":
		icon = "heavy_snow_showers.png"
	if data == "615" or data == "616" or data == "620" or data == "621" or data == "622":
		icon = "cloudy_with_sleet.png"
	if data == "701":
		icon = "light_rain_showers.png"
	if data == "711" or data == "741" or data == "721" or data == "761" or data == "762":
		icon = "mist.png"
	if data == "731" or data == "751" or data == "771":
		icon = "black_low_cloud.png"
	if data == "781" or data == "900" or data == "901" or data == "902" or data == "952" or data == "953" or data == "954" or data == "955" or data == "956" or data == "957" or data == "958" or data == "959" or data == "962":
		icon = "thundery_showers_night.png"
	if data == "800" or data == "951":
		icon = "sunny.png"
	if data == "801":
		icon = "sunny2.png"
	if data == "803" or data == "804" or data == "802":
		icon = "white_cloud.png"
	if data == "904":
		icon = "hazy_sun.png"
	if data == "903":
		icon = "light_snow_showers.png"
	if data == "906":
		icon = "heavy_hail_showers_night.png"  
	return icon

def weather_info(city_id,apikey):
    user_api = apikey
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/weather?id='
    full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
	icon=raw_api_dict['weather'][0]['id'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=raw_api_dict.get('deg'),
        dt=time_converter(raw_api_dict.get('dt')),
        cloudiness=raw_api_dict.get('clouds').get('all')
    )
    return data

def get_dht11():
	humidity, temperature = Adafruit_DHT.read_retry(11, 18)
	if humidity is not None and temperature is not None:
   		return('Room:{0:0.1f}°C / {1:0.1f}%'.format(temperature, humidity))
	else:
		return('error')