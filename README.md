# tgn_smart_home
Project for a smarthome control with 433MHz transmitter, weather info, pi camera control, optional NodeMCU and Android App

The setup installs all required libraries and programs.

Contain:
* xrdp
* python-matplotlib
* mpg321
* gir1.2-gstreamer-1.0
* gir1.2-gst-plugins-base-1.0
* python3-pil.imagetk
* thingspeak
* gTTS
* Adafruit_Python_DHT
* Adafruit_Python_BMP
* habridge
* routes
* pyopenssl
* simplejson
* cherrypy
* pushbullet
* pi-hole
* tgnLIB.py
* flac
* libportaudio
* SpeechRecognition
* ddclient
* libwebsockets3
* libssl1.0.0
* mosquitto server
* paho-mqtt


Required hardware:
* Raspberry Pi 3 with min. 16GB SD-Card installed Debian Stretch Raspbian 2017.09 and Python 3.5
* Speacker 3,5mm
* Pi Camera
* 7" HDMI Display
* DHT11 -- GPIO 18 (optional)
* 433Mhz RF Wireless Transmitter-Empfänger-Modul Link-Kit für ARM / MCU -- Transmitter on GPIO 17 /Reciver on GPIO 26
* PIR motion detector -- GPIO 24 (optional)
+ ON I2C Bus:     (all optional)
  * MCP23017 GPA0 - GPA3 = LED / GPA4 - GPA7 = button -- add: 0x20
  * 24LC256 EEPROM for saving settings -- add: 0x53 (recommended)
  * LCD 2x16 with PCF8574 -- add: 0x3f
  * PN532 NFC
  * BMP085
  * BH1750
 + optional:
   * NodeMcu with DHT22, Fotoresitor and Small Display
   * Android Phone for Smart Home App

Installation:
* open Terminal
* sudo su
* apt-get update
* apt-get upgrade
* raspi-config / Interfacing Options /P5 I2C  ---- yes
* raspi-config / Interfacing Options /P2 SSH  ---- yes  ---- Finished
* reboot
* open Terminal
* sudo su
* git clone https://github.com/cyber-Ahn/tgn_smart_home.git
* cd tgn_smart_home
* sudo bash setup.sh

GUI Start with /home/pi/start_main_gui.sh

WEB Interface Start with /home/pi/web_interface.sh

add to autostart

sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart

after LXDE-pi add line:

@lxterminal -e /home/pi/start_mqtt_broker.sh

@lxterminal -e /home/pi/start_main_gui.sh
