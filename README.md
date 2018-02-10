# tgn_smart_home
Project for a smarthome control with 433MHz transmitter and weather info and pi camera control

The setup installs all required libraries and programs.

Contain:
* python-matplotlib
* playsound
* gstreamer-1.0
* imagetk
* tgnLIB.py
* HA-Bridge
* PI-Hole
* xrdp
* Adafruit_Python_DHT
* ntp
* ntpdate


Required hardware:
* Raspberry Pi 3 with min. 16GB SD-Card with Debian Stretch Raspbian
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
* sudo bash Setup.sh

Start with /home/pi/start_main_gui.sh

add to autostart

sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart

after LXDE-pi add line:

@lxterminal -e /home/pi/start_main_gui.sh
