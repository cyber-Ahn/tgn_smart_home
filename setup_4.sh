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

if [ "$(id -u)" != "0" ]; then
   echo "The script must be executed as root!"
   exit 1
fi

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
sudo apt-get -y install xfce4 xfce4-goodies xorg dbus-x11 x11-xserver-utils
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
clear
echo -e "\e[33m>> \e[31mCopy tgn NeuralNetwork (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
git clone https://github.com/cyber-Ahn/tgn_neural_network.git
clear
fi
echo -e "\e[33m>> \e[31mset authority\e[32m"
chmod +x start_gui.sh
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
echo -e "\e[33m>> \e[31mMove backup files\e[32m"
echo -e "\n\e[33m>> \e[31mEnter Your Python Version '3.5'?\e[32m"
read ver
sudo mv /home/pi/tgn_smart_home/setup_files/xorg.conf /etc/X11/xrdp/
sudo mv /home/pi/tgn_smart_home/setup_files/tgnLIB.py /usr/local/lib/python"$ver"/dist-packages/
sudo mv /home/pi/tgn_smart_home/setup_files/tgn_file_crypt.py /usr/local/lib/python"$ver"/dist-packages/
sudo python3 /usr/local/lib/python"$ver"/dist-packages/tgn_file_crypt.py
sudo mv /home/pi/tgn_setup_lib/setup_files/habridge.config /home/pi/habridge/data
sudo mv /home/pi/tgn_setup_lib/setup_files/device.db /home/pi/habridge/data
sudo cp /home/pi/tgn_smart_home/setup_files/adlists.list /etc/.pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/adlists.list /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/black.list /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/blacklist.txt /etc/pihole/
sudo mv /home/pi/tgn_smart_home/setup_files/.asoundrc /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/start_main_gui.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/mosquitto.conf /etc/mosquitto/
sudo chmod +x /home/pi/start_main_gui.sh
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
sudo echo "@lxterminal -e /home/pi/start_main_gui.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
sudo echo "@lxterminal -e /home/pi/start_main_gui.sh" >>  /home/pi/.config/lxsession/LXDE-pi/autostart
fi
echo -e "\e[33m>> \e[31mInstall Code-OSSm PI4 (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
cd setup_files
sudo apt install ./code-oss_arm64.deb
cd ..
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
sleep 10
reboot
