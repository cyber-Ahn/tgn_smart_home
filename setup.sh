#!/bin/bash
#title:          tgn_smart_home
#description:    Automated TGN Smart Home Installation
#author:         cyber Ahn
#date:           20181112
#version:        2.0
#usage:          sudo bash setup.sh
#Support:        http:caworks-sl.de
#OS:             Debian_Stretch_Raspbian_2018.07 / Python3.5 !!!
#==============================================================================

if [ "$(id -u)" != "0" ]; then
   echo "The script must be executed as root!"
   exit 1
fi
echo -e "\e[32m#######################################################"
echo -e "\e[32m####      \e[31mtgn_smart_home INSTALLATION FOR           \e[32m###"
echo -e "\e[32m####           \e[31mRASPBERRY PI 3 & PI 3 B+             \e[32m###"
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
clear
echo -e "\e[33m>> \e[31mCopy tgn NeuralNetwork (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
git clone https://github.com/cyber-Ahn/tgn_neural_network.git
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
echo -e "\n\e[33m>> \e[31mEnter Your Python Version '3.5'?\e[32m"
read ver
sudo mv /home/pi/tgn_smart_home/setup_files/tgnLIB.py /usr/local/lib/python"$ver"/dist-packages/
sudo mv /home/pi/tgn_smart_home/setup_files/tgn_file_crypt.py /usr/local/lib/python"$ver"/dist-packages/
sudo python3 /usr/local/lib/python"$ver"/dist-packages/tgn_file_crypt.py
sudo cp /home/pi/tgn_smart_home/setup_files/adlists.list /etc/.pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/adlists.list /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/black.list /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/blacklist.txt /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/.asoundrc /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/start_main_gui.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/mosquitto.conf /etc/mosquitto/
sudo mv /home/pi/tgn_smart_home/setup_files/start_sinric.sh /home/pi
sudo chmod +x /home/pi/start_sinric.sh
sudo chmod +x /home/pi/start_main_gui.sh
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
sudo echo "@lxterminal -e /home/pi/start_main_gui.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
sudo echo "@lxterminal -e /home/pi/start_main_gui.sh" >>  /home/pi/.config/lxsession/LXDE-pi/autostart
sudo echo "@lxterminal -e /home/pi/start_sinric.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
sudo echo "@lxterminal -e /home/pi/start_sinric.sh" >>  /home/pi/.config/lxsession/LXDE-pi/autostart
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
echo -e "\e[33m>> \e[31mInstall Code-OSS PI3 (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sleep 2
git clone https://github.com/cyber-Ahn/VSCode-Raspberry-Pi.git
cd VSCode-Raspberry-Pi
sudo sh install.sh
rm -fr VSCode-Raspberry-Pi
sleep 3
clear
fi
echo -e "\e[33m>> \e[31mSet Terminal File Menu (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo mv /home/pi/tgn_smart_home/setup_files/boot_smh.sh /home/pi
echo "bash boot_smh.sh" >> .bashrc
sleep 5
clear
fi
clear
echo -e "\e[31m\e[7m>>\e[0m \e[33mReboot System in 10 sec \e[31m\e[7m<<\e[0m"
sudo rm -fr /home/pi/tgn_smart_home/setup_files
sudo rm -fr /home/pi/tgn_smart_home/setup.sh
sudo rm -fr /home/pi/tgn_smart_home/setup_4.sh
sudo rm -fr /home/pi/tgn_smart_home/requirements.txt
sudo rm -fr /home/pi/tgn_smart_home/requirements_apt.txt
sudo chmod +x /home/pi/tgn_smart_home/tgn-api/api.sh
sudo chmod +x /home/pi/tgn_smart_home/tgn-api/synric.sh
sudo cp /home/pi/tgn_smart_home/tgn-api/tgnapi.service /etc/systemd/system
sudo cp /home/pi/tgn_smart_home/tgn-api/tgnsynric.service /etc/systemd/system
systemctl daemon-reload >/dev/null 2>&1
systemctl enable tgnapi.service >/dev/null 2>&1
systemctl start tgnapi.service >/dev/null 2>&1
systemctl enable tgnsynric.service >/dev/null 2>&1
systemctl start tgnsynric.service >/dev/null 2>&1
sleep 10
reboot
