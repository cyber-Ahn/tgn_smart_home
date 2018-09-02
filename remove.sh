#!/bin/bash
#title:          tgn_smart_home
#description:    Automated TGN Smart Home Deinstallation
#author:         cyber Ahn
#date:           20180315
#version:        1.9
#usage:          sudo bash Setup.sh
#Support:        https:caworks-sl.de/TGN
#OS:             Debian_Stretch_Raspbian_2017.09 / Python3.5 !!!
#==============================================================================

echo -e "##########################################################"
echo -e "####      tgn_smart_home DEINSTALLATION FOR              ###"
echo -e "####           RASPBERRY PI 3 & PI 3 B+                ###"
echo -e "####               by cyber Ahn                        ###"
echo -e "####           http://caworks-sl.de                    ###"
echo -e "##########################################################"

echo -e "\n>> remove Clock"
apt-get remove ntp
apt-get remove ntpdate
sleep 3

clear

echo -e ">> deinstall Remote Desktop"
apt-get remove xrdp
sleep 5

clear

echo -e ">> remove Libs"
apt-get remove python-matplotlib
apt-get remove mpg321
apt-get remove gir1.2-gstreamer-1.0
apt-get remove gir1.2-gst-plugins-base-1.0
apt-get remove python3-pil.imagetk
sudo pip3 uninstall thingspeak
sudo pip3 uninstall gTTS
sudo pip3 uninstall feedparser
sudo pip3 uninstall gitpython
apt-get remove lirc
sleep 5

clear

echo -e ">> denstall Adafruit_Python_DHT"
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python3 setup.py remove
sleep 3
cd ..
rm -fr Adafruit_Python_DHT/

clear

echo -e ">> Install Adafruit_Python_BMP"
git clone https://github.com/adafruit/Adafruit_Python_BMP 
cd Adafruit_Python_BMP
sudo python3 setup.py remove
cd ..
sleep 3
rm -fr Adafruit_Python_BMP/


clear

echo -e ">> deinstall Web Interface Libs"
pip3 uninstall routes
pip3 unintsall pyopenssl
git clone https://github.com/simplejson/simplejson.git
cd simplejson
python3 setup.py remove
cd ..
rm -fr simplejson 
pip3 uninstall cherrypy
sleep 3

clear

echo -e ">> Install PiHole"
curl -sSL https://install.pi-hole.net | bash
sleep 5

clear

echo -e ">> Move backup files"
rm /usr/local/lib/python3.5/dist-packages/tgnLIB.py
rm /home/pi/.asoundrc
rm /home/pi/start_main_gui.sh
rm /home/pi/web_interface.sh
rm /home/pi/start_main_gui.sh
rm /home/pi/start_mqtt_broker.sh
cd ..
clear

echo -e ">> deinstall SpeechRecognition and LIB's"
sudo apt-get remove flac
sudo apt-get remove libportaudio-dev
sudo apt-get remove python-dev
sudo apt-get remove libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
sleep 3
cd /home/pi/tgn_smart_home
sudo pip3 uninstall SpeechRecognition

clear
echo -e ">> deinstall ddclient (ignore setup infos and click ok)"
sleep 2
sudo apt-get remove ddclient 
sleep 3

clear

echo -e ">> deinstall MQTT-Server"
apt-get remove libwebsockets3
apt-get remove libssl1.0.0
sudo apt-get remove mosquitto
sudo apt remove mosquitto mosquitto-clients
pip3 uninstall paho-mqtt
sleep 3

clear

sudo rm -fr /home/pi/tgn_smart_home

echo -e ">> deinstall Code-OSS"
sudo apt-get remove code-oss
sleep 3

clear

echo -e ">> Reboot System in 10 sec"
sleep 10
reboot
