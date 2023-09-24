# tgn_smart_home

|Build Status|  |Python versions|

Project for a smarthome control with 433MHz transmitter, weather info, pi camera control, optional NodeMCU, Android App(sep. Project),
ha-bridge with web Interface and sinric-bridge for Alexa.

The setup installs all required libraries and programs.

Required min Hardware:

 * Raspberry Pi 3 with min. 16GB SD-Card installed 'Debian Stretch Raspbian 2017.09' and Python 3.5
 or
 
 * Raspberry Pi 4 with min. 16GB SD-Card installed '2019-09-26-raspbian-buster' and Python 3.7
 * 7" HDMI Display 
 -- Optional --
 
 * IR Reciver -- GPIO 18 (optional)
 * IR Transmitter -- GPIO 22 (optional)
 * Speacker 3,5mm (optional)
 * Pi Camera (optional)
 * PIR motion detector -- GPIO 24 (optional)

Plug / Socket / Modul Options:

 * 433Mhz RF Socket / Wireless Transmitter-Reciver-Modul Link-Kit für ARM / MCU -- Transmitter on GPIO 17 /Reciver on GPIO 26
 * Wlan-Socket Kasa HS100
 * Shelly (V. 1 / 2 / 2.5 / 4 / plug / bulb )

ON I2C Bus: (all Optional)
 
 * 24LC256 EEPROM for saving settings -- add: 0x53 (recommended) 
 * MCP23017 GPA0 - GPA3 = LED / GPA4 - GPA7 = button -- add: 0x20
 * LCD 2x16 with PCF8574 -- add: 0x3f
 * PN532 NFC
 * BMP085
 * BH1750
 * 5 x 4 Bit Digital Tube LED Display Modul I2C
  
Sensors optional:
   
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

API use

* ini API: 
    python3 /home/pi/tgn_smart_home/tgn-api/master_key.py

    save this Key (Master_key) !!!

* generate user_keys
    http://192.111.0.5:5555/genkey/Master_key

    save the user_key

* read API
    http://192.111.0.5:5555/api/read?key=USER-KEY

    example: http://192.111.0.5:5555/api/read?key=mmvdnQzWa06sJijOvfncQ6vrd

* set button
    http://192.111.0.5:5555/api?key=USER-KEY&opt=button&butnr=BUTTON-NUMBER&stat=STATUS

    example: http://192.111.0.5:5555?api/key=mmvdnQzWa06sJijOvfncQ6sswa&opt=button&butnr=3&stat=1

* Ir Air Conditioner
    http://192.111.0.5:5555/api?stat=0&key=USER-KEY&opt=IrAirConditioner&butnr=COMMAND

    example: http://192.111.0.5:5555/api?stat=0&key=mmvdnQzWa06sJijOvfncQtfzggu&opt=IrAirConditioner&butnr=power

    Commands:power | fan | cool | dry | up | down


    
|Bild_1|

|Bild_2|

|Bild_3|

|Bild_4|

|Bild_5|

.. ..

.. |Build Status| image:: https://caworks-sl.de/images/build.png
   :target: https://caworks-sl.de
.. |Python versions| image:: https://caworks-sl.de/images/python.png
   :target: https://caworks-sl.de

.. |Bild_1| image:: https://caworks-sl.de/Smart_Home_Images/IMG_20181101_174128.jpg
   :target: https://github.com/cyber-Ahn/tgn_smart_home
.. |Bild_2| image:: https://caworks-sl.de/Smart_Home_Images/IMG_20180602_215043.jpg
   :target: https://github.com/cyber-Ahn/tgn_smart_home
.. |Bild_3| image:: https://caworks-sl.de/Smart_Home_Images/Smart Home Comunications.jpg
   :target: https://github.com/cyber-Ahn/tgn_smart_home
.. |Bild_4| image:: https://caworks-sl.de/Smart_Home_Images/IMG_20180602_214845.jpg
   :target: https://github.com/cyber-Ahn/tgn_smart_home
.. |Bild_5| image:: https://caworks-sl.de/Smart_Home_Images/IMG_20180602_214958.jpg
   :target: https://github.com/cyber-Ahn/tgn_smart_home
