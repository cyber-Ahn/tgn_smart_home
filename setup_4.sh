#!/bin/bash
#title:          tgn_smart_home
#description:    Automated TGN Smart Home Installation
#author:         cyber Ahn
#date:           20190720
#version:        2.1
#usage:          sudo bash setup_4.sh
#Support:        http:caworks-sl.de
#OS:             2019-07-10-raspbian-buster / Python3.7 !!!
#==============================================================================

echo -e "\e[32m#######################################################"
echo -e "\e[32m####      \e[31mtgn_smart_home INSTALLATION FOR           \e[32m###"
echo -e "\e[32m####           \e[31mRASPBERRY PI 4                       \e[32m###"
echo -e "\e[32m####               \e[33mby cyber Ahn                     \e[32m###"
echo -e "\e[32m####           \e[34mhttp://caworks-sl.de                 \e[32m###"
echo -e "\e[32m#######################################################"

sudo apt-get update
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
clear
echo -e "\n\e[33m>> \e[31mUpgrade Linux (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo apt-get update
sudo apt-get upgrade
fi
clear
echo -e "\e[33m>> \e[31mInstall Remote Desktop (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo apt-get -y install xrdp
sleep 5
clear
fi
clear
echo -e "\e[33m>> \e[31mDownload Libs\e[32m"
xargs apt-get -y install < requirements_apt.txt
p7zip -d setup_files.7z
sudo pip3 uninstall numpy
sudo pip3 uninstall gitdb2
sudo pip3 install -r requirements.txt
sudo mkdir /home/pi/Pictures
sudo chmod +777 /home/pi/Pictures/
cd /home/pi/tgn_smart_home/setup_files/PyAudio
python3 setup.py install
cd ..
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
chmod +x start_gui.sh
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
sudo mv /home/pi/tgn_smart_home/setup_files/tgnLIB.py /usr/local/lib/python3.7/dist-packages/
sudo mv /home/pi/tgn_smart_home/setup_files/haset1.bk /home/pi/habridge/data
sudo cp /home/pi/tgn_smart_home/setup_files/adlists.list /etc/.pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/adlists.list /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/black.list /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/blacklist.txt /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/.asoundrc /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/start_main_gui.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/web_interface.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/start_mqtt_broker.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/mosquitto.conf /etc/mosquitto/
sudo chmod +x /home/pi/start_main_gui.sh
sudo chmod +x /home/pi/start_mqtt_broker.sh
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
echo -e "\e[33m>> \e[31mInstall Code-OSSm PI4 (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
wget https://packagecloud.io/headmelted/codebuilds/gpgkey -O - | sudo apt-key add -
curl -L https://code.headmelted.com/installers/apt.sh | sudo bash
sleep 3
sudo apt-get purge code-oss
sudo apt-get install code-oss=1.29.0-1539702286
sudo apt-mark hold code-oss
clear
fi
clear
echo -e "\e[31m\e[7m>>\e[0m \e[33mReboot System in 10 sec \e[31m\e[7m<<\e[0m"
sudo rm -fr /home/pi/tgn_smart_home/setup_files
sudo rm -fr /home/pi/tgn_smart_home/setup.sh
sudo rm -fr /home/pi/tgn_smart_home/setup_4.sh
sleep 10
reboot
