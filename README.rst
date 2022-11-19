# tgn_smart_home

|Build Status| |Code Health|

Project for a smarthome control with 433MHz transmitter, weather info, pi camera control, optional NodeMCU, Android App(sep. Project),
ha-bridge with web Interface and sinric-bridge for Alexa.

The setup installs all required libraries and programs.

Required hardware:
* Raspberry Pi 3 with min. 16GB SD-Card installed 'Debian Stretch Raspbian 2017.09' and Python 3.5
or
* Raspberry Pi 4 with min. 16GB SD-Card installed '2019-09-26-raspbian-buster' and Python 3.7
* Speacker 3,5mm
* Pi Camera
* 7" HDMI Display
* IR Reciver -- GPIO 18 (optional)
* IR Transmitter -- GPIO 22 (optional)
* 433Mhz RF Socket / Wireless Transmitter-Reciver-Modul Link-Kit für ARM / MCU -- Transmitter on GPIO 17 /Reciver on GPIO 26
  
  or
  
  Wlan-Socket Kasa HS100 / Shelly (V. 1 / 2 / 2.5 / 4 / plug / bulb ) 
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
* apt-get dist-upgrade
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

Button Name Configuration for set System
 * buttonname   = 423MHZ
 * s_buttonname = Sonoff
 * p_buttonname = Kasa HS100
 * y_buttonname = Shelly

Commands for HA Bridge or Google Assistant(need Auto Voice and Tasker):
 * Pi Commands
 
   - sudo python3 /home/pi/tgn_smart_home/libs/ha_bridge_com.py reboot 1
   - sudo python3 /home/pi/tgn_smart_home/libs/ha_bridge_com.py shutdown 1
  
 * wireless socket
 
   - sudo python3 /home/pi/tgn_smart_home/libs/ha_bridge_com.py [wireless socket number] [1 = on 0 = off]
   - example:
    - sudo python3 /home/pi/tgn_smart_home/libs/ha_bridge_com.py 4 1
    
<img src="http://caworks-sl.de/Smart_Home_Images/IMG_20181101_174128.jpg" alt="1" style="width:600px;height:500px;">

<img src="http://caworks-sl.de/Smart_Home_Images/IMG_20180602_215043.jpg" alt="1" style="width:600px;height:500px;">

<img src="http://caworks-sl.de/Smart_Home_Images/Smart Home Comunications.jpg" alt="1" style="width:600px;height:500px;">

<img src="http://caworks-sl.de/Smart_Home_Images/IMG_20180602_214845.jpg" alt="1" style="width:600px;height:500px;">

<img src="http://caworks-sl.de/Smart_Home_Images/IMG_20180602_214958.jpg" alt="1" style="width:600px;height:500px;">

.. ..

.. |Build Status| image:: https://img.shields.io/travis/marcogazzola/shelly-python/master.svg
   :target: https://travis-ci.org/marcogazzola/shelly-python
.. |Code Health| image:: https://landscape.io/github/marcogazzola/shelly-python/landscape.svg?style=flat
   :target: https://landscape.io/github/marcogazzola/shelly-python/master
