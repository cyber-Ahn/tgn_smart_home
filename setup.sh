#!/bin/bash
#title:          tgn_smart_home
#description:    Automated TGN Smart Home Installation
#author:         cyber Ahn
#date:           20181112
#version:        2.0
#usage:          sudo bash setup.sh
#Support:        http:caworks-sl.de/TGN
#OS:             Debian_Stretch_Raspbian_2018.07 / Python3.5 !!!
#==============================================================================

echo -e "\e[32m#######################################################"
echo -e "\e[32m####      \e[31mtgn_smart_home INSTALLATION FOR           \e[32m###"
echo -e "\e[32m####           \e[31mRASPBERRY PI 3 & PI 3 B+             \e[32m###"
echo -e "\e[32m####               \e[33mby cyber Ahn                     \e[32m###"
echo -e "\e[32m####           \e[34mhttp://caworks-sl.de                 \e[32m###"
echo -e "\e[32m#######################################################"

echo -e "\n\e[33m>> \e[31mSetup Clock (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
dpkg-reconfigure tzdata
cat /etc/localtime
sudo apt-get -y install ntp
sudo apt-get -y install ntpdate
ntpd -qg
sleep 3
fi

sudo apt-get update

clear

echo -e "\e[33m>> \e[31mInstall Remote Desktop (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo apt-get -y install xrdp
sleep 5
clear
fi

echo -e "\e[33m>> \e[31mDownload Libs\e[32m"
sudo apt-get -y install python-matplotlib
sudo apt-get -y install mpg321
sudo apt-get -y install gir1.2-gstreamer-1.0
sudo apt-get -y install gir1.2-gst-plugins-base-1.0
sudo apt-get -y install python3-pil.imagetk
sudo pip3 install thingspeak
sudo pip3 install gTTS
sudo pip3 install feedparser
sudo pip3 install gitpython
sudo apt-get -y install lirc
sleep 5

clear

echo -e "\e[33m>> \e[31mInstall Adafruit_Python_DHT\e[32m"
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get -y install build-essential python-dev
sudo python3 setup.py install
sleep 3
cd ..
rm -fr Adafruit_Python_DHT/

clear

echo -e "\e[33m>> \e[31mInstall Adafruit_Python_BMP\e[32m"
git clone https://github.com/adafruit/Adafruit_Python_BMP 
cd Adafruit_Python_BMP
sudo python3 setup.py install
cd ..
sleep 3
rm -fr Adafruit_Python_BMP/

sudo mv /home/pi/tgn_smart_home/setup_files/habridge_install.sh /home/pi/tgn_smart_home
sudo mv /home/pi/tgn_smart_home/setup_files/AlexaInstaller.sh /home/pi/tgn_smart_home

clear

echo -e "\e[33m>> \e[31mCopy tgn NeuralNetwork (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
git clone https://github.com/cyber-Ahn/tgn_neural_network.git
clear
fi

echo -e "\e[33m>> \e[31mset authority\e[32m"
chmod +x /home/pi/tgn_smart_home/libs/pushbullet.sh
chmod +x start_gui.sh
chmod +x web_interface.sh
chmod +x start_mqtt_broker.sh
chmod +x habridge_install.sh
sleep 5

echo -e "\e[33m>> \e[31mInstall habridge (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo bash habridge_install.sh
sleep 1
sudo rm -r habridge_install.sh
sleep 5
clear
fi

echo -e "\e[33m>> \e[31mInstall PiHole (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
curl -sSL https://install.pi-hole.net | bash
sleep 2
pihole -a -p Kevin2711
sleep 5
clear
fi

echo -e "\e[33m>> \e[31mMove backup files\e[32m"
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

echo -e "\e[33m>> \e[31mInstall SpeechRecognition and LIB's\e[32m"
sudo apt-get -y install flac
sudo apt-get -y install libportaudio-dev
sudo apt-get -y install python-dev
sudo apt-get -y install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
cd /home/pi/tgn_smart_home/setup_files/PyAudio
sleep 1
python3 setup.py install
sleep 3
cd /home/pi/tgn_smart_home
sudo pip3 install SpeechRecognition

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

sudo python3 /home/pi/tgn_smart_home/libs/settings.py rss

clear

echo -e "\e[33m>> \e[31mInstall Java (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo mkdir /usr/java
cd /usr/java
wget http://www.caworks-sl.de/data/download/jdk-8u162-linux-arm32-vfp-hflt.tar.gz
sudo tar xf jdk-8u162-linux-arm32-vfp-hflt.tar.gz
sudo update-alternatives --install /usr/bin/java java /usr/java/jdk1.8.0_162/bin/java 1000
sudo update-alternatives --install /usr/bin/javac javac /usr/java/jdk1.8.0_162/bin/javac 1000
java -version
sleep 3
clear
fi


echo -e "\e[33m>> \e[31mInstall Code-OSS (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
echo "deb http://mirrordirector.raspbian.org/raspbian/ jessie main contrib non-free rpi" >> /etc/apt/sources.list
echo "deb http://archive.raspbian.org/raspbian jessie main contrib non-free rpi" >> /etc/apt/sources.list
echo "deb https://packagecloud.io/headmelted/codebuilds/raspbian/ jessie main" >> /etc/apt/sources.list
sleep 2
sudo apt-get update
sudo apt-get install code-oss
sleep 3
clear
fi

echo -e "\e[33m>> \e[31mInstall MQTT-Server\e[32m"
sudo apt-get -y install libwebsockets3
sudo apt-get -y install libssl1.0.0
sudo apt-get -y install mosquitto
sudo apt install mosquitto mosquitto-clients
pip3 install paho-mqtt
sleep 3
sudo mv /home/pi/tgn_smart_home/setup_files/mosquitto.conf /etc/mosquitto/
sudo rm -fr /home/pi/tgn_smart_home/setup_files

clear

echo -e "\e[31m\e[7m>>\e[0m \e[33mReboot System in 10 sec \e[31m\e[7m<<\e[0m"
sleep 10
reboot
