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
* lirc


Required hardware:
* Raspberry Pi 3 with min. 16GB SD-Card installed Debian Stretch Raspbian 2017.09 and Python 3.5
* Speacker 3,5mm
* Pi Camera
* 7" HDMI Display
* IR Reciver -- GPIO 18 (optional)
* IR Transmitter -- GPIO 22 (optional)
* 433Mhz RF Wireless Transmitter-Empfänger-Modul Link-Kit für ARM / MCU -- Transmitter on GPIO 17 /Reciver on GPIO 26
* PIR motion detector -- GPIO 24 (optional)
+ ON I2C Bus:     (all optional)
  * MCP23017 GPA0 - GPA3 = LED / GPA4 - GPA7 = button -- add: 0x20
  * 24LC256 EEPROM for saving settings -- add: 0x53 (recommended)
  * LCD 2x16 with PCF8574 -- add: 0x3f
  * PN532 NFC
  * BMP085
  * BH1750
  * 5 x 4 Bit Digital Tube LED Display Modul I2C
 + optional:
   * NodeMcu with DHT22, Fotoresitor and Small Display
   * Android Phone for Smart Home App
   * NodeMcu with DHT22, Fotoresistor and PIR Sensor
   * NodeMcu with NeoPixel Light (ws2812b)
   
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
* PI 3 sudo bash setup.sh
* PI 4 sudo bash setup_4.sh

GUI Start with /home/pi/start_main_gui.sh

WEB Interface Start with /home/pi/web_interface.sh

add to autostart:

sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart

or

sudo nano  /etc/xdg/lxsession/LXDE-pi/autostart

after LXDE-pi add line:

@lxterminal -e /home/pi/start_mqtt_broker.sh

@lxterminal -e /home/pi/start_main_gui.sh

Commands for HA Bridge or Google Assistant(need Auto Voice and Tasker):
 * Pi Commands
 
   - sudo python3 /home/pi/tgn_smart_home/libs/ha_bridge_com.py reboot 1
   - sudo python3 /home/pi/tgn_smart_home/libs/ha_bridge_com.py shutdown 1
  
 * wireless socket
 
   - sudo python3 /home/pi/tgn_smart_home/libs/ha_bridge_com.py [wireless socket number] [1 = on 0 = off]
   - example:
    - sudo python3 /home/pi/tgn_smart_home/libs/ha_bridge_com.py 4 1
    
<img src="http://caworks-sl.de/Smart_Home_Images/IMG_20181101_174128.jpg" alt="1" style="width:600px;height:500px;">

<img src="http://caworks-sl.de/Smart_Home_Images/IMG_20181101_174155.jpg" alt="1" style="width:600px;height:500px;">

<img src="http://caworks-sl.de/Smart_Home_Images/IMG_20180602_215043.jpg" alt="1" style="width:600px;height:500px;">

<img src="http://caworks-sl.de/Smart_Home_Images/Smart Home Comunication.jpg" alt="1" style="width:600px;height:500px;">

<img src="http://caworks-sl.de/Smart_Home_Images/IMG_20180602_214845.jpg" alt="1" style="width:600px;height:500px;">

<img src="http://caworks-sl.de/Smart_Home_Images/IMG_20180602_214958.jpg" alt="1" style="width:600px;height:500px;">

