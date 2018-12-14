import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import base64
import csv
import datetime
import feedparser
import itertools
import json
import logging
import os
import os.path
import posix
import picamera
import RPi.GPIO as GPIO
import requests
import re
import speech_recognition as sr
import sys
import smbus
import socket
import string
import subprocess
import thingspeak
import time
import urllib.request
import zipfile
from ctypes import c_int, c_uint16, c_ushort, c_short, c_ubyte, c_char, POINTER, Structure, create_string_buffer, sizeof, byref, addressof, string_at
from contextlib import closing
from fcntl import ioctl
from gtts import gTTS
from threading import Thread
from time import gmtime, strftime
from time import sleep
from time import localtime

address = 0x51
register = 0x02
zone = 0
w  = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
bus = smbus.SMBus(1)

RPI_DEFAULT_I2C_NEW = 0x01
RPI_DEFAULT_I2C_OLD = 0x00
LOGGING_ENABLED = False
LOG_LEVEL = logging.DEBUG
DEFAULT_DELAY = 0.005

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

I2C_M_TEN = 0x0010
I2C_M_RD = 0x0001
I2C_M_NOSTART = 0x4000
I2C_M_REV_DIR_ADDR = 0x2000
I2C_M_IGNORE_NAK = 0x1000
I2C_M_NO_RD_ACK = 0x0800
I2C_M_RECV_LEN = 0x0400
I2C_FUNC_I2C = 0x00000001
I2C_FUNC_10BIT_ADDR = 0x00000002
I2C_FUNC_PROTOCOL_MANGLING = 0x00000004
I2C_SLAVE = 0x0703  
I2C_SLAVE_FORCE	= 0x0706			
I2C_TENBIT = 0x0704
I2C_FUNCS = 0x0705
I2C_RDWR = 0x0707

PN532_COMMAND_GETFIRMWAREVERSION = 0x02
PN532_COMMAND_SAMCONFIGURATION = 0x14
PN532_COMMAND_INLISTPASSIVETARGET = 0x4A
PN532_COMMAND_RFCONFIGURATION = 0x32
PN532_COMMAND_INDATAEXCHANGE = 0x40
PN532_COMMAND_INDESELECT = 0x44
PN532_IDENTIFIER_HOST_TO_PN532 = 0xD4
PN532_IDENTIFIER_PN532_TO_HOST = 0xD5
PN532_SAMCONFIGURATION_MODE_NORMAL = 0x01
PN532_SAMCONFIGURATION_MODE_VIRTUAL_CARD = 0x02
PN532_SAMCONFIGURATION_MODE_WIRED_CARD = 0x03
PN532_SAMCONFIGURATION_MODE_DUAL_CARD = 0X04
PN532_SAMCONFIGURATION_TIMEOUT_50MS = 0x01
PN532_SAMCONFIGURATION_IRQ_OFF = 0x00
PN532_SAMCONFIGURATION_IRQ_ON = 0x01
PN532_RFCONFIGURATION_CFGITEM_MAXRETRIES = 0x05
PN532_PREAMBLE = 0x00
PN532_START_CODE_1 = 0x00
PN532_START_CODE_2 = 0xFF
PN532_POSTAMBLE = 0x00
PN532_FRAME_POSITION_STATUS_CODE = 0
PN532_FRAME_POSITION_PREAMBLE = 1
PN532_FRAME_POSITION_START_CODE_1 = 2
PN532_FRAME_POSITION_START_CODE_2 = 3
PN532_FRAME_POSITION_LENGTH = 4
PN532_FRAME_POSITION_LENGTH_CHECKSUM = 5
PN532_FRAME_POSITION_FRAME_IDENTIFIER = 6
PN532_FRAME_POSITION_DATA_START = 7
PN532_FRAME_TYPE_DATA = 0
PN532_FRAME_TYPE_ACK = 1
PN532_FRAME_TYPE_NACK = 2
PN532_FRAME_TYPE_ERROR = 3

BH1750_POWER_DOWN = 0x00
BH1750_POWER_ON = 0x01
BH1750_RESET = 0x07
BH1750_CONTINUOUS_LOW_RES_MODE = 0x13
BH1750_CONTINUOUS_HIGH_RES_MODE_1 = 0x10
BH1750_CONTINUOUS_HIGH_RES_MODE_2 = 0x11
BH1750_ONE_TIME_HIGH_RES_MODE_1 = 0x20
BH1750_ONE_TIME_HIGH_RES_MODE_2 = 0x21
BH1750_ONE_TIME_LOW_RES_MODE = 0x23

ROM_ADDRESS = 0x53
PN532_I2C_SLAVE_ADDRESS = 0x24
BH1750_ADDRESS = 0x23

REMOTE_SERVER = "www.google.com"

phatC = "/home/pi/tgn_smart_home/config/rom.csv"

HexDigits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71]
ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_TYPICAL = 2
BRIGHT_HIGHEST = 7
OUTPUT = GPIO.OUT
INPUT = GPIO.IN
LOW = GPIO.LOW
HIGH = GPIO.HIGH

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
		if getMAC("eth0") == "b8:27:eb:46:45:02":
			allowed = "yes"
		else:
			allowed = "no"
	le=len(id)
	if le < 32:
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

def get_BMP085():
    sensor = BMP085.BMP085()
    databmp=(sensor.read_pressure() / 100.0)
    return databmp

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

def convertToNumber(data):
    return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=BH1750_ADDRESS):
    if ifI2C(addr) == "found device":
        data = bus.read_i2c_block_data(addr,BH1750_ONE_TIME_HIGH_RES_MODE_1)
        return round(convertToNumber(data),1)
    else:
        return "error "

def rss(url,num):
    feed = feedparser.parse(url)
    feed_title = feed['feed']['title']
    feed_entries = feed.entries
    out = ""
    x_num = 1
    for entry in feed_entries:
        if x_num <= num:
            article_title = entry.title
            article_link = entry.link
            article_published_at = entry.published # Unicode string
            article_published_at_parsed = entry.published_parsed # Time object
            #article_author = entry.author
            #print ("{}[{}]".format(article_title, article_link))
            #print ("Published at {}".format(article_published_at))
            #print ("\n")
            #print ("Published by {}".format(article_author))
            out = out + ("{}".format(article_title))+" - "
            x_num = x_num + 1
    return(out)

def write_eeprom(bus,add,block,reg,data):
    if ifI2C(add) == "found device":
        wr = []
        cach = hex(ord(data))
        wr.append(reg)
        wr.append(int(cach,16))
        bus = smbus.SMBus(bus)
        bus.write_i2c_block_data(add,block,wr)
        time.sleep(0.5)
    else:
        print ("Rom not found, save in CSV")
        file = open(phatC, newline='')
        reader = csv.reader(file)
        header = next(reader)
        dataB = [row for row in reader]
        nu = len(dataB)
        spA = []
        spB = []
        spC = []
        for i in range(nu):
            cach = dataB[i]
            spA.append(cach[0])
            spB.append(cach[1])
            spC.append(cach[2])
        nuB = len(spA)
        blockB = "0x"+format(block,"02x")
        regB = "0x"+format(reg,"02x")
        for x in range(nuB):
            if blockB == spA[x] and regB == spB[x]:
                cachB = hex(ord(data))
                spC[x] = cachB
        file = open(phatC,'w')
        writer = csv.writer(file)
        writer.writerow(["block", "address", "data"])
        for x in range(nuB):
            writer.writerow([spA[x], spB[x], spC[x]])

def read_eeprom(bus,add,block,reg):
    if ifI2C(add) == "found device":
        bus = smbus.SMBus(bus)
        bus.write_i2c_block_data(add, block, [reg])
        cach = hex(bus.read_byte(add))
        if cach != "0x0" and cach != "0xff" and cach != "0xef" and cach != "0xfb":
            cachB = cach.split("x")
            out = (bytes.fromhex(cachB[1]).decode('utf-8'))
        else:
            out = "?"
    else:
        print ("Rom not found, read CSV")
        out = "?"
        file = open(phatC, newline='')
        reader = csv.reader(file)
        header = next(reader)
        data = [row for row in reader]
        nu = len(data)
        for i in range(nu):
            cach = data[i]
            daz = cach[2].split("x")
            daa = (bytes.fromhex(daz[1]).decode('utf-8'))
            blockB = "0x"+format(block,"02x")
            regB = "0x"+format(reg,"02x")
            if cach[1] == regB and cach[0] == blockB:
                out = daa
    return out

def backup_rom(blocknum, phatB):
    print ("Backup EEPROM")
    time.sleep(3)
    file = open(phatB,'w')
    writer = csv.writer(file)
    writer.writerow(["block", "address", "data"])
    if blocknum >= 1:
        for i in range(255):
            nu = 0x01 + i
            cb = '0x'+hex(nu)[2:].rjust(2, '0')
            print (cb)
            cach = read_eeprom(1,ROM_ADDRESS,0x00,nu)
            cach = hex(ord(cach))
            print (cach)
            writer.writerow(["0x00", cb, cach])
    if blocknum >= 2:
        for i in range(255):
            nu = 0x01 + i
            cb = '0x'+hex(nu)[2:].rjust(2, '0')
            print (cb)
            cach = read_eeprom(1,ROM_ADDRESS,0x01,nu)
            cach = hex(ord(cach))
            print (cach)
            writer.writerow(["0x01", cb, cach])
    if blocknum >= 3:
        for i in range(255):
            nu = 0x01 + i
            cb = '0x'+hex(nu)[2:].rjust(2, '0')
            print (cb)
            cach = read_eeprom(1,ROM_ADDRESS,0x02,nu)
            cach = hex(ord(cach))
            print (cach)
            writer.writerow(["0x02", cb, cach])
    if blocknum >= 4:
        for i in range(255):
            nu = 0x01 + i
            cb = '0x'+hex(nu)[2:].rjust(2, '0')
            print (cb)
            cach = read_eeprom(1,ROM_ADDRESS,0x03,nu)
            cach = hex(ord(cach))
            print (cach)
            writer.writerow(["0x03", cb, cach])
    print("Done")

def restore_rom (blocknum, phatB):
    print("Restore EEPROM")
    blocknum = blocknum - 1
    time.sleep(3)
    file = open(phatB, newline='')
    reader = csv.reader(file)
    header = next(reader)
    data = [row for row in reader]
    nu = len(data)
    print ("lines in backup: "+str(nu))
    print ("Header:")
    print (header)
    time.sleep(3)
    bl = 0x00
    add = 0x01
    for i in range(nu):
        time.sleep(0.5)
        cach = data[i]
        print (cach)
        daz = cach[2].split("x")
        daa = (bytes.fromhex(daz[1]).decode('utf-8'))
        if bl <= blocknum:
            write_eeprom(1,ROM_ADDRESS,bl,add,daa)
        add = add + 1
        if add == 256:
            add = 0x01
            bl = bl + 1
    print ("Done")

out_zip = "searchig....."
def crack_zip(zip, pwd):
    try:
        global out_zip
        zip.extractall(pwd=str.encode(pwd))
        out_zip = "Password is " + pwd
    except:
        print(out_zip)
        pass
def get_zip_pwd(file):
    myLetters = string.ascii_letters + string.digits + string.punctuation
    zipFile = zipfile.ZipFile(file)
    for i in range(1, 15):
        for j in map(''.join, itertools.product(myLetters, repeat=i)):
            t = Thread(target=crack_zip, args=(zipFile, j))
            t.start()

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

def format_time(inputtime):
    timefo = inputtime
    cachfo = timefo.split(" ")
    cachfi = cachfo[3].split(":")
    timese = cachfi[2]
    timemi = cachfi[1]
    if int(timese) <= 9:
        timese = "0"+timese
    if int(timemi) <= 9:
        timemi = "0"+timemi
    timefo = cachfo[0]+"  "+cachfo[2]+" "+cachfi[0]+":"+timemi+":"+timese
    return timefo

def setRTC():
	var1 = strftime("%a-%Y-%m-%d-%H-%M-%S", localtime())
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

def write_ts(channel,a,b,c,d,e,f,g):
	try:
		response = channel.update({'field1': a, 'field2': b, 'field3': c, 'field4': d, 'field5': e, 'field6': f, 'field7': g})
		return("Done")
	except:
		return("connection failed")

def read_ts(channel):
	try:
		read = channel.get({})
		return("Read:", read)
	except:
		return("connection failed")

def get_dht11():
	humidity, temperature = Adafruit_DHT.read_retry(11, 18)
	if humidity is not None and temperature is not None:
   		return('Room:{0:0.1f}°C / {1:0.1f}%'.format(temperature, humidity))
	else:
		return('error')

def encode(text):
    encoded = base64.encodestring(text.encode('utf-8'))
    return encoded

def decode(text):
    decoded = base64.decodestring(text).decode('utf-8')
    return decoded

def TextToSpeech(text,ln):
	tts = gTTS(text=text, lang=ln, slow=False)
	tts.save("temp.mp3")
	os.system('mpg321 temp.mp3 &')
	time.sleep(1)
	os.system('rm temp.mp3 &')

def SpeechToText(la,api_key):
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
	try:
    		return(r.recognize_google(audio, language=la, key=api_key))
	except sr.UnknownValueError:
    		return("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
    		return("Could not request results from Google Speech Recognition service; {0}".format(e))

def revision():
    try:
        with open('/proc/cpuinfo','r') as f:
            for line in f:
                if line.startswith('Revision'):
                    return 1 if line.rstrip()[-1] in ['2','3'] else 2
            else:
                return 0
    except:
        return 0

def readPage(add,t):
    site = ""
    if(t == "ip"):
        site = "http://"+add
    else:
        site = add
    html_read = urllib.request.urlopen(site)
    html_read_out = str(html_read.read(), 'utf-8')
    return html_read_out

def html_to_text(data):        
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")
    data = " ".join(data.split())   
    p = re.compile(r'< script[^<>]*?>.*?< / script >')
    data = p.sub('', data)
    p = re.compile(r'< style[^<>]*?>.*?< / style >')
    data = p.sub('', data)
    p = re.compile(r'')
    data = p.sub('', data)
    p = re.compile(r'<[^<]*?>')
    data = p.sub('', data)
    return data.lower()

def remove_space(data):
    data = data.replace(" ", "")
    return data

def format_data(d_l, pos, sep):
    c_a = d_l[pos]
    c_b = c_a.split(sep)
    return c_b[1] 

def read_esp(add, com_typ):
    if is_connected(add) == "Online":
        data_html = readPage(add, com_typ)
        data_decode = html_to_text(data_html)
        data_clear = remove_space(data_decode)
        data_clear = data_clear.replace("data", "")
        return data_clear
    else:
        data_nf = "ESP not found"
        return data_nf

class i2c_msg(Structure):
    _fields_ = [
        ('addr', c_uint16),
        ('flags', c_ushort),
        ('len', c_short),
        ('buf', POINTER(c_char))]
    
    __slots__ = [name for name,type in _fields_]

class i2c_rdwr_ioctl_data(Structure):
    _fields_ = [
        ('msgs', POINTER(i2c_msg)),
        ('nmsgs', c_int)]

    __slots__ = [name for name,type in _fields_]

default_bus = 1 if revision() > 1 else 0

class I2CMaster(object):
    def __init__(self, n=default_bus, extra_open_flags=0):
        self.fd = posix.open("/dev/i2c-%i"%n, posix.O_RDWR|extra_open_flags)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    
    def close(self):
        posix.close(self.fd)
    
    def transaction(self, *msgs):
        msg_count = len(msgs)
        msg_array = (i2c_msg*msg_count)(*msgs)
        ioctl_arg = i2c_rdwr_ioctl_data(msgs=msg_array, nmsgs=msg_count)
        ioctl(self.fd, I2C_RDWR, ioctl_arg)
        return [i2c_msg_to_bytes(m) for m in msgs if (m.flags & I2C_M_RD)]

def reading(addr, n_bytes):
    return reading_into(addr, create_string_buffer(n_bytes))

def reading_into(addr, buf):
    return _new_i2c_msg(addr, I2C_M_RD, buf)

def writing_bytes(addr, *bytes):
    return writing(addr, bytes)

def writing(addr, byte_seq):
    buf = bytes(byte_seq)
    return _new_i2c_msg(addr, 0, create_string_buffer(buf, len(buf)))

def _new_i2c_msg(addr, flags, buf):
    return i2c_msg(addr=addr, flags=flags, len=sizeof(buf), buf=buf)

def i2c_msg_to_bytes(m):
    return string_at(m.buf, m.len)

class Pn532Frame:
    def __init__(
        self, frame_type=PN532_FRAME_TYPE_DATA,
        preamble=PN532_PREAMBLE,
        start_code_1=PN532_START_CODE_1,
        start_code_2=PN532_START_CODE_2,
        frame_identifier=0xD4,
        data=bytearray(),
            postamble=PN532_POSTAMBLE):
        self._frame_type = frame_type
        self._preamble = preamble
        self._startCode1 = start_code_1
        self._startCode2 = start_code_2
        self._frameIdentifier = frame_identifier
        self._data = data
        self._postamble = postamble

    def get_length(self):
        return len(self._data) + 1

    def get_length_checksum(self):
        return (~self.get_length() & 0xFF) + 0x01

    def get_data(self):
        return self._data

    def get_data_checksum(self):
        byte_array = bytearray()
        for byte in self._data:
            byte_array.append(byte)
        byte_array.append(self._frameIdentifier)
        inverse = (~sum(byte_array) & 0xFF) + 0x01
        if inverse > 255:
            inverse = inverse - 255
        return inverse

    def get_frame_type(self):
        return self._frame_type

    def to_tuple(self):
        byte_array = bytearray()
        if self._frame_type == PN532_FRAME_TYPE_ACK:
            byte_array.append(PN532_PREAMBLE)
            byte_array.append(PN532_START_CODE_1)
            byte_array.append(PN532_START_CODE_2)
            byte_array.append(PN532_START_CODE_1)
            byte_array.append(PN532_START_CODE_2)
            byte_array.append(PN532_POSTAMBLE)
            return (byte_array)
        byte_array.append(self._preamble)
        byte_array.append(self._startCode1)
        byte_array.append(self._startCode2)
        byte_array.append(self.get_length())
        byte_array.append(self.get_length_checksum())
        byte_array.append(self._frameIdentifier)
        for byte in self._data:
            byte_array.append(byte)
        byte_array.append(self.get_data_checksum())
        byte_array.append(self._postamble)
        return (byte_array)
    @staticmethod
    def from_response(response):
        if Pn532Frame.is_valid_response(response) is not True:
            raise RuntimeError("Invalid Response")
        if Pn532Frame.is_ack(response):
            return Pn532Frame(frame_type=PN532_FRAME_TYPE_ACK,
                              frame_identifier=0x00)
        if Pn532Frame.is_error(response):
            return Pn532Frame(frame_type=PN532_FRAME_TYPE_ERROR,
                             frame_identifier=0x7F,data=b'\x81')
        response_length = response[0][PN532_FRAME_POSITION_LENGTH] + 1
        data = bytearray(
            response[0][PN532_FRAME_POSITION_DATA_START:PN532_FRAME_POSITION_DATA_START + response_length - 2])
        return Pn532Frame(
            preamble=response[0][PN532_FRAME_POSITION_PREAMBLE],
            start_code_1=response[0][PN532_FRAME_POSITION_START_CODE_1],
            start_code_2=response[0][PN532_FRAME_POSITION_START_CODE_2],
            frame_identifier=response[0][
                PN532_FRAME_POSITION_FRAME_IDENTIFIER],
            data=data,
            postamble=response[0][PN532_FRAME_POSITION_DATA_START + response_length + 2])
    @staticmethod
    def is_valid_response(response):
        if (response[0][0] & 0x01) == 0x01:
            if response[0][PN532_FRAME_POSITION_PREAMBLE] == PN532_PREAMBLE:
                if response[0][PN532_FRAME_POSITION_START_CODE_1] == PN532_START_CODE_1:
                    if response[0][PN532_FRAME_POSITION_START_CODE_2] == PN532_START_CODE_2:
                        return True
        return False
    @staticmethod
    def is_ack(response):
        if response[0][PN532_FRAME_POSITION_LENGTH] == 0x00:
            if response[0][PN532_FRAME_POSITION_LENGTH_CHECKSUM] == 0xFF:
                if response[0][PN532_FRAME_POSITION_FRAME_IDENTIFIER] == 0x00:
                    return True
        return False
    @staticmethod
    def is_error(response):
        """ Checks if the response is an error frame."""
        if response[0][PN532_FRAME_POSITION_LENGTH] == 0x01:
            if response[0][PN532_FRAME_POSITION_LENGTH_CHECKSUM] == 0xFF:
                if response[0][PN532_FRAME_POSITION_FRAME_IDENTIFIER] == 0x7F:
                    if response[0][PN532_FRAME_POSITION_DATA_START] == 0x81:
                        return True
        return False

class Pn532_i2c:
    PN532 = None
    address = None
    i2c_channel = None
    logger = None
    def __init__(self, address=PN532_I2C_SLAVE_ADDRESS, i2c_channel=RPI_DEFAULT_I2C_NEW):
        self.logger = logging.getLogger()
        self.logger.propagate = LOGGING_ENABLED
        if self.logger.propagate:
            self.logger.setLevel("DEBUG")
        self.address = address
        self.i2c_channel = i2c_channel
        self.PN532 = I2CMaster(self.i2c_channel)

    def send_command_check_ack(self, frame):
        self.send_command(frame)
        if self.read_ack():
            return True
        else:
            return False

    def read_response(self):
        logging.debug("readResponse...")
        response = [b'\x00\x00\x00\x00\x00\x00\x00']
        while True:
            try:
                logging.debug("readResponse..............Reading.")

                sleep(DEFAULT_DELAY)
                response = self.PN532.transaction(
                    reading(self.address, 255))
                logging.debug(response)
                logging.debug("readResponse..............Read.")
            except Exception:
                pass
            else:
                try:
                    frame = Pn532Frame.from_response(response)

                    # Acknowledge Data frames coming from the PN532
                    if frame.get_frame_type() == PN532_FRAME_TYPE_DATA:
                        self.send_command(Pn532Frame(
                            frame_type=PN532_FRAME_TYPE_ACK))
                except Exception as ex:
                    logging.debug(ex)
                    logging.debug(ex.args)
                    pass
                else:
                    return frame

    def send_command(self, frame):
        logging.debug("send_command...")
        while True:
            try:
                logging.debug("send_command...........Sending.")
                sleep(DEFAULT_DELAY)
                self.PN532.transaction(
                    writing(self.address, frame.to_tuple()))
                logging.debug(frame.to_tuple())
                logging.debug("send_command...........Sent.")
            except Exception as ex:
                logging.debug(ex)
                self.reset_i2c()
                sleep(DEFAULT_DELAY)
            else:
                return True

    def read_ack(self):
        logging.debug("read_ack...")
        while True:
            sleep(DEFAULT_DELAY)
            response_frame = self.read_response()
            if response_frame.get_frame_type() == PN532_FRAME_TYPE_ACK:
                return True
            else:
                pass

    def read_mifare(self):
        frame = Pn532Frame(frame_type=PN532_FRAME_TYPE_DATA, data=bytearray([PN532_COMMAND_INLISTPASSIVETARGET, 0x01, 0x00]))
        self.send_command_check_ack(frame)
        return self.read_response()

    def reset_i2c(self):
        logging.debug("I2C Reset...")
        self.PN532.close()
        del self.PN532
        self.PN532 = I2CMaster(self.i2c_channel)
        logging.debug("I2C Reset............Created.")

    def SAMconfigure(self, frame=None):
        if frame is None:
            frame = Pn532Frame(frame_type=PN532_FRAME_TYPE_DATA,
                               data=bytearray(
                                   [PN532_COMMAND_SAMCONFIGURATION,
                                    PN532_SAMCONFIGURATION_MODE_NORMAL,
                                    PN532_SAMCONFIGURATION_TIMEOUT_50MS,
                                    PN532_SAMCONFIGURATION_IRQ_OFF]))

        self.send_command_check_ack(frame)

    def __exit__(self, type, value, traceback):
        self.PN532.close()
        del self.PN532

class TM1637:
    __doublePoint = False
    __Clkpin = 0
    __Datapin = 0
    __brightnes = BRIGHT_TYPICAL;
    __currentData = [0,0,0,0];
	
    def __init__( self, pinClock, pinData, brightnes ):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.__Clkpin = pinClock
        self.__Datapin = pinData
        self.__brightnes = brightnes;
        GPIO.setup(self.__Clkpin,OUTPUT)
        GPIO.setup(self.__Datapin,OUTPUT)

    def Clear(self):
        b = self.__brightnes;
        point = self.__doublePoint;
        self.__brightnes = 0;
        self.__doublePoint = False;
        data = [0x7F,0x7F,0x7F,0x7F];
        self.Show(data);
        self.__brightnes = b;
        self.__doublePoint = point;

    def Show( self, data ):
        for i in range(0,4):
            self.__currentData[i] = data[i];
        self.start();
        self.writeByte(ADDR_AUTO);
        self.stop();
        self.start();
        self.writeByte(STARTADDR);
        for i in range(0,4):
            self.writeByte(self.coding(data[i]));
        self.stop();
        self.start();
        self.writeByte(0x88 + self.__brightnes);
        self.stop();

    def Show1(self, DigitNumber, data):
        if( DigitNumber < 0 or DigitNumber > 3):
            return;
        self.__currentData[DigitNumber] = data;
        self.start();
        self.writeByte(ADDR_FIXED);
        self.stop();
        self.start();
        self.writeByte(STARTADDR | DigitNumber);
        self.writeByte(self.coding(data));
        self.stop();
        self.start();
        self.writeByte(0x88 + self.__brightnes);
        self.stop();
		
    def SetBrightnes(self, brightnes):
        if( brightnes > 7 ):
            brightnes = 7;
        elif( brightnes < 0 ):
            brightnes = 0;
        if( self.__brightnes != brightnes):
            self.__brightnes = brightnes;
            self.Show(self.__currentData);

    def ShowDoublepoint(self, on):
        if( self.__doublePoint != on):
            self.__doublePoint = on;
            self.Show(self.__currentData);
			
    def writeByte( self, data ):
        for i in range(0,8):
            GPIO.output( self.__Clkpin, LOW)
            if(data & 0x01):
                GPIO.output( self.__Datapin, HIGH)
            else:
                GPIO.output( self.__Datapin, LOW)
            data = data >> 1
            GPIO.output( self.__Clkpin, HIGH)
        GPIO.output( self.__Clkpin, LOW)
        GPIO.output( self.__Datapin, HIGH)
        GPIO.output( self.__Clkpin, HIGH)
        GPIO.setup(self.__Datapin, INPUT)
        while(GPIO.input(self.__Datapin)):
            time.sleep(0.001)
            if( GPIO.input(self.__Datapin)):
                GPIO.setup(self.__Datapin, OUTPUT)
                GPIO.output( self.__Datapin, LOW)
                GPIO.setup(self.__Datapin, INPUT)        
        GPIO.setup(self.__Datapin, OUTPUT)
    
    def start(self):
        GPIO.output( self.__Clkpin, HIGH)
        GPIO.output( self.__Datapin, HIGH)
        GPIO.output( self.__Datapin, LOW) 
        GPIO.output( self.__Clkpin, LOW)
	
    def stop(self):
        GPIO.output( self.__Clkpin, LOW) 
        GPIO.output( self.__Datapin, LOW) 
        GPIO.output( self.__Clkpin, HIGH)
        GPIO.output( self.__Datapin, HIGH)
	
    def coding(self, data):
        if( self.__doublePoint ):
            pointData = 0x80
        else:
            pointData = 0;
        if(data == 0x7F):
            data = 0
        else:
            data = HexDigits[data] + pointData;
        return data

class keypad_GPIO():
    def __init__(self, columnCount = 3):
        GPIO.setmode(GPIO.BOARD)
        if columnCount is 3:
            self.KEYPAD = [
                [1,2,3],
                [4,5,6],
                [7,8,9],
                ["*",0,"#"]
            ]
            self.ROW         = [26,24,23,22]
            self.COLUMN      = [21,19,10]
        elif columnCount is 4:
            self.KEYPAD = [
                [1,2,3,"A"],
                [4,5,6,"B"],
                [7,8,9,"C"],
                ["*",0,"#","D"]
            ]
            self.ROW         = [18,23,24,25]
            self.COLUMN      = [4,17,22,21]
        else:
            return
    def getKey(self):
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
        if rowVal <0 or rowVal >3:
            self.exit()
            return
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
        if colVal <0 or colVal >2:
            self.exit()
            return
        self.exit()
        return self.KEYPAD[rowVal][colVal]
    def exit(self):
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
