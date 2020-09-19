#!/bin/bash
#title:          tgn_setup_lib
#description:    Automated Lib Installation for TGN-Software
#author:         cyber Ahn
#date:           20193011
#version:        2.3
#usage:          sudo bash setup_4.sh
#Support:        http:caworks-sl.de
#OS:             2019-09-26-raspbian-buster / Python3.7 !!!
#==============================================================================

echo -e "\e[32m#######################################################"
echo -e "\e[32m####      \e[31mtgn_setup_lib INSTALLATION FOR           \e[32m###"
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
echo -e "\e[33m>> \e[31mDownload Adafruit Libs(y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
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
echo -e "\e[33m>> \e[31mInstall lib's\e[32m"
xargs apt-get -y install < requirements_apt.txt
sudo mkdir /home/pi/Pictures
sudo chmod +777 /home/pi/Pictures/
clear
sleep 3
echo -e "\e[33m>> \e[31mInstall pip3 lib's\e[32m"
sudo pip3 uninstall numpy
sudo pip3 uninstall gitdb2
sudo pip3 install -r requirements.txt
clear
sleep 3
echo -e "\e[33m>> \e[31mCopy backupfiles\e[32m"
sudo mv /home/pi/tgn_setup_lib/setup_files/geckodriver /usr/local/bin
sudo mv /home/pi/tgn_setup_lib/setup_files/tgnLIB.py /usr/local/lib/python3.7/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/tw_auth.py /usr/local/lib/python3.7/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/.asoundrc /home/pi
sudo mv /home/pi/tgn_setup_lib/setup_files/fabfile.py /home/pi
echo -e "\e[33m>> \e[31mInstall PyAudio\e[32m"
cd /home/pi/tgn_setup_lib/setup_files/PyAudio
sleep 1
python3 setup.py install
sleep 3
cd /home/pi/tgn_setup_lib
sudo pip3 install SpeechRecognition
clear
sleep 5
clear
fi
echo -e "\e[33m>> \e[31mInstall habridge (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo mv /home/pi/tgn_setup_lib/setup_files/habridge_install.sh /home/pi/tgn_setup_lib
chmod +x habridge_install.sh
sudo bash habridge_install.sh
sleep 1
sudo rm -r habridge_install.sh
sudo mv /home/pi/tgn_setup_lib/setup_files/haset1.bk /home/pi/habridge/data
sleep 5
clear
fi
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
cd /home/pi/tgn_setup_lib
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
echo -e "\e[33m>> \e[31mInstall MQTT-Server (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo apt-get -y install libwebsockets3
sudo apt-get -y install mosquitto
sudo apt install mosquitto mosquitto-clients
sleep 3
sudo mv /home/pi/tgn_setup_lib/setup_files/mosquitto.conf /etc/mosquitto/
sudo mv /home/pi/tgn_setup_lib/setup_files/start_mqtt_broker.sh /home/pi
chmod +x /home/pi/start_mqtt_broker.sh
clear
fi
echo -e "\e[33m>> \e[31mCopy tgn_smart_home (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
git clone https://github.com/cyber-Ahn/tgn_smart_home.git
sudo mv /home/pi/tgn_setup_lib/tgn_smart_home /home/pi/
chmod +x /home/pi/tgn_smart_home/start_gui.sh
chmod +x /home/pi/tgn_smart_home/start_mqtt_broker.sh
chmod +x /home/pi/tgn_smart_home/start_gesture.sh
sudo mv /home/pi/tgn_smart_home/setup_files/start_main_gui.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/start_mqtt_broker.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/start_gesture.sh /home/pi
sudo chmod +x /home/pi/start_main_gui.sh
sudo chmod +x /home/pi/start_mqtt_broker.sh
sudo chmod +x /home/pi/start_gesture.sh.sh
sudo mv /home/pi/tgn_setup_lib/setup_files/rom.csv /home/pi/tgn_smart_home/config/
sudo mv /home/pi/tgn_setup_lib/setup_files/motd /etc/
clear
sudo python3 /home/pi/tgn_smart_home/libs/settings.py restore
sudo rm -fr /home/pi/tgn_smart_home/setup.sh
sudo rm -fr /home/pi/tgn_smart_home/setup_4.sh
sudo rm -fr /home/pi/tgn_smart_home/remove.sh
sudo rm -fr /home/pi/tgn_smart_home/setup_files
sudo rm -fr /home/pi/tgn_smart_home/update.py
echo -e "\e[33m>> \e[31madd tgn_smart_home to autostart (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo echo "@lxterminal -e /home/pi/start_mqtt_broker.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
sudo echo "@lxterminal -e /home/pi/start_main_gui.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
#sudo echo "@lxterminal -e /home/pi/start_gesture.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
sudo echo "@lxterminal -e /home/pi/start_mqtt_broker.sh" >>  /home/pi/.config/lxsession/LXDE-pi/autostart
sudo echo "@lxterminal -e /home/pi/start_main_gui.sh" >>  /home/pi/.config/lxsession/LXDE-pi/autostart
#sudo echo "@lxterminal -e /home/pi/start_gesture.sh" >>  /home/pi/.config/lxsession/LXDE-pi/autostart
fi
echo -e "\e[33m>> \e[31mcopy working files (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo mv /home/pi/tgn_smart_home/setup_files/working_gesture.sh /home/pi/Desktop
sudo mv /home/pi/tgn_smart_home/setup_files/working_main_gui.sh /home/pi/Desktop
fi
clear
fi
echo -e "\e[33m>> \e[31mCopy tgn_discord_bot (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
git clone https://github.com/cyber-Ahn/tgn_discord_bot.git
sudo mv /home/pi/tgn_setup_lib/tgn_discord_bot /home/pi/
sudo chmod +x /home/pi/tgn_discord_bot/start_bot.sh
sudo rm -fr /home/pi/tgn_discord_bot/SETTINGS
sudo rm -fr /home/pi/tgn_discord_bot/playlist
sudo mv /home/pi/tgn_setup_lib/setup_files/SETTINGS /home/pi/tgn_discord_bot/
sudo mv /home/pi/tgn_setup_lib/setup_files/playlist /home/pi/tgn_discord_bot/
sudo mv /home/pi/tgn_setup_lib/setup_files/bot.py /home/pi/tgn_discord_bot/
sudo mv /home/pi/tgn_setup_lib/setup_files/mqtt.py /home/pi/tgn_discord_bot/
sudo mv /home/pi/tgn_setup_lib/setup_files/splashScreen.gif /home/pi/tgn_discord_bot/
echo -e "\e[33m>> \e[31madd tgn_discord_bot to autostart (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo echo "@lxterminal -e /home/pi/tgn_discord_bot/start_bot.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
sudo echo "@lxterminal -e /home/pi/tgn_discord_bot/start_bot.sh" >>  /home/pi/.config/lxsession/LXDE-pi/autostart
fi
clear
fi
echo -e "\e[33m>> \e[31mCopy tgn NeuralNetwork (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
git clone https://github.com/cyber-Ahn/tgn_neural_network.git
cd tgn_neural_network
sudo p7zip -d NeuralNetwork.7z
sudo mv /home/pi/tgn_setup_lib/tgn_neural_network/ /home/pi/
cd /home/pi/tgn_setup_lib/
sudo rm -fr /home/pi/tgn_setup_lib/tgn_neural_network
clear
fi
echo -e "\e[33m>> \e[31Copy Retropie-Setup mod fpr PI 4 (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo mv /home/pi/tgn_setup_lib/setup_files/RetroPie-Setup.7z /home/pi/tgn_setup_lib/
sudo p7zip -d RetroPie-Setup.7z
sudo chmod -R +777 RetroPie-Setup/
sudo rm -fr RetroPie-Setup.7z
sudo mv /home/pi/tgn_setup_lib/RetroPie-Setup /home/pi/
sudo mv /home/pi/tgn_setup_lib/setup_files/start_retropie.sh /home/pi/Desktop/
echo -e "\e[33m>> \e[31mStart Installation with 'sudo bash retropie_setup.sh'     Satrt with 'emulationstation'\e[32m"
clear
fi
echo -e "\e[33m>> \e[31mCopy Kalli Tools (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo mkdir /home/pi/kalli
cd /home/pi/kalli
git clone https://github.com/samyoyo/weeman
sleep 3
git clone https://github.com/UndeadSec/SocialFish.git
sleep 3
git clone https://github.com/thelinuxchoice/blackeye
sleep 3
git clone https://github.com/thelinuxchoice/shellphish
sleep 3
git clone https://github.com/Cabdulahi/pish
sleep 3
git clone https://github.com/UndeadSec/EvilURL.git
sleep 3
git clone -b Termux-Support-Branch https://github.com/DarkSecDevelopers/HiddenEye.git
sleep3
ln -s /home/pi/kalli /home/pi/Desktop/
clear
fi
echo -e "\e[33m>> \e[31mInstall Apache 2 (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo apt-get -y install apache2
sudo apt-get install php php-mbstring
sudo apt-get install mysql-server php-mysql
sudo apt install phpmyadmin
sudo apt-get remove --purge *mysql\*
sudo apt-get autoremove
sudo apt-get autoclean
sudo apt-get install -y php7.0 libapache2-mod-php7.0 php7.0-cli php7.0-common php7.0-mbstring php7.0-gd php7.0-intl php7.0-xml php7.0-mysql php7.0-mcrypt php7.0-zip
apt-get install mysql-server
service mysql start
sleep 3
clear
fi
echo -e "\e[33m>> \e[31mCopy tgn Website (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo mv /home/pi/tgn_setup_lib/setup_files/html.7z /home/pi/tgn_setup_lib/
sudo p7zip -d html.7z
sudo chmod -R +777 html/
sudo rm -fr html.7z
sudo rm -fr /var/www/html
sudo mv /home/pi/tgn_setup_lib/html /var/www/
sudo chmod -R +777 /var/www/html/*
sudo chmod -R +777 /var/www/html/images/*
clear
fi
echo -e "\e[33m>> \e[31mInstall PiHole (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo rm -fr /var/www/html/admin
curl -sSL https://install.pi-hole.net | bash
sleep 2
pihole -a -p Kevin2711
sudo cp /home/pi/tgn_setup_lib/setup_files/adlists.list /etc/.pihole/
sudo mv /home/pi/tgn_setup_lib/setup_files/adlists.list /etc/pihole/
sudo mv /home/pi/tgn_setup_lib/setup_files/black.list /etc/pihole/
sudo mv /home/pi/tgn_setup_lib/setup_files/blacklist.txt /etc/pihole/
sudo mv /home/pi/tgn_setup_lib/setup_files/piHolelist /etc/pihole/
sudo mv /home/pi/tgn_setup_lib/setup_files/domains /etc/pihole/
sudo mv /home/pi/tgn_setup_lib/setup_files/regex.list /etc/pihole/
sudo chmod -R +777 html/
sleep 5
clear
fi
echo -e "\e[33m>> \e[31mInstall I2C LCD Driver (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo mv /home/pi/tgn_setup_lib/setup_files/LCD-show-170703.tar.gz /home/pi/
cd /home/pi
sudo tar xvf LCD-show-170703.tar.gz
sudo rm -fr LCD-show-170703.tar.gz
cd LCD-show
sudo rm -fr /home/pi/tgn_setup_lib
sudo chmod +x LCD35-show
sudo ./LCD35-show
fi
echo -e "\e[31m\e[7m>>\e[0m \e[33mReboot System in 10 sec \e[31m\e[7m<<\e[0m"
sudo rm -fr /home/pi/tgn_setup_lib
sleep 10
reboot
