#!/bin/bash
#title:          tgn_smart_home
#description:    Automated TGN Smart Home Installation
#author:         cyber Ahn
#date:           20180315
#version:        1.9
#usage:          sudo bash Setup.sh
#Support:        https:caworks-sl.de/TGN
#OS:             Debian_Stretch_Raspbian_2017.09 / Python3.5 !!!
#==============================================================================

echo -e "##########################################################"
echo -e "####      tgn_smart_home INSTALLATION FOR              ###"
echo -e "####           RASPBERRY PI 3 & PI 3 B+                ###"
echo -e "####               by cyber Ahn                        ###"
echo -e "####           http://caworks-sl.de                    ###"
echo -e "##########################################################"

echo -e "\n>> Setup Clock"
dpkg-reconfigure tzdata
cat /etc/localtime
apt-get install ntp
apt-get install ntpdate
ntpd -qg
sleep 3

apt-get update

clear

echo -e ">> Install Remote Desktop"
apt-get install xrdp
sleep 5

clear

echo -e ">> Download Libs"
apt-get install python-matplotlib
apt-get install mpg321
apt-get install gir1.2-gstreamer-1.0
apt-get install gir1.2-gst-plugins-base-1.0
apt-get install python3-pil.imagetk
sudo pip3 install thingspeak
sudo pip3 install gTTS
sudo pip3 install feedparser
sudo pip3 install gitpython
apt-get install lirc -y
sleep 5

clear

echo -e ">> Install Adafruit_Python_DHT"
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get install build-essential python-dev
sudo python3 setup.py install
sleep 3
cd ..
rm -fr Adafruit_Python_DHT/

clear

echo -e ">> Install Adafruit_Python_BMP"
git clone https://github.com/adafruit/Adafruit_Python_BMP 
cd Adafruit_Python_BMP
sudo python3 setup.py install
cd ..
sleep 3
rm -fr Adafruit_Python_BMP/

sudo mv /home/pi/tgn_smart_home/setup_files/habridge_install.sh /home/pi/tgn_smart_home

clear

echo -e ">> Install tgn NeuralNetwork"
git clone https://github.com/cyber-Ahn/tgn_neural_network.git

clear

echo -e ">> Install Web Interface Libs"
pip3 install routes
pip3 install pyopenssl
git clone https://github.com/simplejson/simplejson.git
cd simplejson
python3 setup.py install
cd ..
rm -fr simplejson 
pip3 install cherrypy
sleep 3

clear

echo -e ">> set authority"
chmod +x /home/pi/tgn_smart_home/libs/pushbullet.sh
chmod +x start_gui.sh
chmod +x web_interface.sh
chmod +x start_mqtt_broker.sh
chmod +x habridge_install.sh
sleep 5

echo -e ">> Install habridge"
sudo bash habridge_install.sh
sleep 1
sudo rm -r habridge_install.sh
sleep 5

clear

echo -e ">> Install PiHole"
curl -sSL https://install.pi-hole.net | bash
sleep 2
pihole -a -p Kevin2711
sleep 5

clear

echo -e ">> Move backup files"
sudo mv /home/pi/tgn_smart_home/setup_files/tgnLIB.py /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_smart_home/setup_files/haset1.bk /home/pi/habridge/data
sudo cp /home/pi/tgn_smart_home/setup_files/adlists.list /etc/.pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/adlists.list /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/black.list /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/blacklist.txt /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/.asoundrc /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/start_main_gui.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/web_interface.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/start_mqtt_broker.sh /home/pi

sudo mv /home/pi/tgn_smart_home/setup_files/lircd.conf /etc/lirc
sudo mv /home/pi/tgn_smart_home/setup_files/lirc_options.conf /etc/lirc
sudo mv /home/pi/tgn_smart_home/setup_files/hardware.conf /etc/lirc
sudo mv /home/pi/tgn_smart_home/setup_files/unitymedia_samsung.lircd.conf /etc/lirc/lircd.conf.d
echo "dtoverlay=lirc-rpi,gpio_in_pin=18,gpio_out_pin=23" >> /boot/config.txt
echo "lirc_rpi" >> /etc/modules
echo "lirc_dev" >> /etc/modules

cd ..
sudo chmod +x /home/pi/start_main_gui.sh
sudo chmod +x /home/pi/web_interface.sh
sudo chmod +x /home/pi/start_mqtt_broker.sh
clear

echo -e ">> Install SpeechRecognition and LIB's"
sudo apt-get install flac
sudo apt-get install libportaudio-dev
sudo apt-get install python-dev
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
cd /home/pi/tgn_smart_home/setup_files/PyAudio
sleep 1
python3 setup.py install
sleep 3
cd /home/pi/tgn_smart_home
sudo pip3 install SpeechRecognition

clear
echo -e ">> Install ddclient (ignore setup infos and click ok)"
sleep 2
sudo apt-get install ddclient -y
sudo nano /etc/ddclient.conf
ddclient -daemon=0 -debug -verbose -noquiet 2 /etc/ddclient.conf
sudo /etc/init.d/ddclient restart
sleep 3

clear

sudo python3 /home/pi/tgn_smart_home/libs/settings.py install_rom
sleep 5

clear

sudo python3 /home/pi/tgn_smart_home/libs/settings.py weather

clear

sudo python3 /home/pi/tgn_smart_home/libs/settings.py pushb

clear

sudo python3 /home/pi/tgn_smart_home/libs/settings.py thinkspeak

clear

sudo python3 /home/pi/tgn_smart_home/libs/settings.py webapp

clear

sudo python3 /home/pi/tgn_smart_home/libs/settings.py esp

clear

echo -e ">> Install Java"
sudo mkdir /usr/java
cd /usr/java
wget http://www.caworks-sl.de/data/download/jdk-8u162-linux-arm32-vfp-hflt.tar.gz
sudo tar xf jdk-8u162-linux-arm32-vfp-hflt.tar.gz
sudo update-alternatives --install /usr/bin/java java /usr/java/jdk1.8.0_162/bin/java 1000
sudo update-alternatives --install /usr/bin/javac javac /usr/java/jdk1.8.0_162/bin/javac 1000
java -version
sleep 3

clear

echo -e ">> addd sources"
echo "deb http://mirrordirector.raspbian.org/raspbian/ jessie main contrib non-free rpi" >> /etc/apt/sources.list
echo "deb http://archive.raspbian.org/raspbian jessie main contrib non-free rpi" >> /etc/apt/sources.list
echo "deb https://packagecloud.io/headmelted/codebuilds/raspbian/ jessie main" >> /etc/apt/sources.list
sleep 2
sudo apt-get update
sleep 3

clear

echo -e ">> Install MQTT-Server"
apt-get install libwebsockets3
apt-get install libssl1.0.0
sudo apt-get install mosquitto -y
sudo apt install mosquitto mosquitto-clients
pip3 install paho-mqtt
sleep 3
sudo mv /home/pi/tgn_smart_home/setup_files/mosquitto.conf /etc/mosquitto/

clear

sudo rm -fr /home/pi/tgn_smart_home/setup_files

echo -e ">> Install Code-OSS"
sudo apt-get install code-oss
sleep 3

clear

echo -e ">> Reboot System in 10 sec"
sleep 10
reboot
