#!/bin/bash
#title:          tgn_setup_lib
#description:    Automated Lib Installation for TGN-Software
#author:         cyber Ahn
#date:           20192104
#version:        1.1
#usage:          sudo bash setup.sh
#Support:        http:caworks-sl.de/TGN
#OS:             Debian_Stretch_Raspbian_2018.07 / Python3.5 !!!
#==============================================================================

echo -e "\e[32m#######################################################"
echo -e "\e[32m####      \e[31mtgn_setup_lib INSTALLATION FOR           \e[32m###"
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

echo -e "\e[33m>> \e[31mDownload Libs(y/n)?\e[32m"
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
sudo apt-get -y install firefox-esr
sudo apt-get -y install python-matplotlib
sudo apt-get -y install mpg321
sudo apt-get -y install gir1.2-gstreamer-1.0
sudo apt-get -y install gir1.2-gst-plugins-base-1.0
sudo apt-get -y install python3-pil.imagetk
sudo apt-get -y install p7zip
echo -e "\e[33m>> \e[31mInstall thingspeak\e[32m"
sudo pip3 install thingspeak
sleep 3
echo -e "\e[33m>> \e[31mInstall gtts\e[32m"
sudo pip3 install gTTS
sleep 3
echo -e "\e[33m>> \e[31mInstall feedparser\e[32m"
sudo pip3 install feedparser
sleep 3
echo -e "\e[33m>> \e[31mInstall gitpython\e[32m"
sudo pip3 install gitpython
sleep 3
echo -e "\e[33m>> \e[31mInstall fabric3\e[32m"
sudo pip3 install fabric3
sleep 3
echo -e "\e[33m>> \e[31mInstall lirc\e[32m"
sudo apt-get -y install lirc
sleep 3
echo -e "\e[33m>> \e[31mInstall youtube_dl\e[32m"
sudo python3 -m pip install -U youtube_dl
sleep 3
echo -e "\e[33m>> \e[31mInstall spotipy\e[32m"
sudo pip3 install spotipy
sleep 3
echo -e "\e[33m>> \e[31mInstall FFmpeg\e[32m"
sudo pip3 install FFmpeg
sleep 3
echo -e "\e[33m>> \e[31mInstall websockets\e[32m"
sudo pip3 install websockets
sleep 3
echo -e "\e[33m>> \e[31mInstall aiohttp\e[32m"
sudo pip3 install aiohttp
sleep 3
echo -e "\e[33m>> \e[31mInstall python-dateutil\e[32m"
sudo pip3 install python-dateutil
sleep 3
echo -e "\e[33m>> \e[31mInstall selenium\e[32m"
sudo pip3 install selenium
sleep 3
echo -e "\e[33m>> \e[31mInstall paho-mqtt client\e[32m"
sudo pip3 install paho-mqtt
sleep 3
sudo mv /home/pi/tgn_setup_lib/setup_files/geckodriver /usr/local/bin
sudo mv /home/pi/tgn_setup_lib/setup_files/tgnLIB.py /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/chatterbot /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/ChatterBot-0.8.7.dist-info /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/chatterbot_corpus /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/chatterbot_corpus-1.1.4.dist-info /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/discord /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/discord.py-0.16.12.dist-info /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/sqlalchemy /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/SQLAlchemy-1.2.15.dist-info /usr/local/lib/python3.5/dist-packages/
sudo mv /home/pi/tgn_setup_lib/setup_files/.asoundrc /home/pi
sudo mv /home/pi/tgn_setup_lib/setup_files/fabfile.py /home/pi
sudo mv /home/pi/tgn_setup_lib/setup_files/lircd.conf /etc/lirc
sudo mv /home/pi/tgn_setup_lib/setup_files/lirc_options.conf /etc/lirc
sudo mv /home/pi/tgn_setup_lib/setup_files/hardware.conf /etc/lirc
sudo mv /home/pi/tgn_setup_lib/setup_files/unitymedia_samsung.lircd.conf /etc/lirc/lircd.conf.d
echo "dtoverlay=lirc-rpi,gpio_in_pin=18,gpio_out_pin=23" >> /boot/config.txt
echo "lirc_rpi" >> /etc/modules
echo "lirc_dev" >> /etc/modules
echo -e "\e[33m>> \e[31mInstall SpeechRecognition and LIB's\e[32m"
sudo apt-get -y install flac
sudo apt-get -y install libportaudio-dev
sudo apt-get -y install python-dev
sudo apt-get -y install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
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

echo -e "\e[33m>> \e[31mInstall PiHole (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
curl -sSL https://install.pi-hole.net | bash
sleep 2
pihole -a -p Kevin2711
sudo cp /home/pi/tgn_setup_lib/setup_files/adlists.list /etc/.pihole/
sudo mv /home/pi/tgn_setup_lib/setup_files/adlists.list /etc/pihole/
sudo mv /home/pi/tgn_setup_lib/setup_files/black.list /etc/pihole/
sudo mv /home/pi/tgn_setup_lib/setup_files/blacklist.txt /etc/pihole/
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

echo -e "\e[33m>> \e[31mInstall Code-OSS (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo echo "deb http://mirrordirector.raspbian.org/raspbian/ jessie main contrib non-free rpi" >> /etc/apt/sources.list
sudo echo "deb http://archive.raspbian.org/raspbian jessie main contrib non-free rpi" >> /etc/apt/sources.list
sudo echo "deb https://packagecloud.io/headmelted/codebuilds/raspbian/ jessie main" >> /etc/apt/sources.list
sleep 2
sudo apt-get update
sudo apt-get install code-oss
sleep 3
clear
fi

echo -e "\e[33m>> \e[31mInstall MQTT-Server (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo apt-get -y install libwebsockets3
sudo apt-get -y install libssl1.0.0
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
chmod +x /home/pi/tgn_smart_home/libs/pushbullet.sh
chmod +x /home/pi/tgn_smart_home/start_gui.sh
sudo mv /home/pi/tgn_smart_home/setup_files/start_main_gui.sh /home/pi
sudo mv /home/pi/tgn_smart_home/setup_files/start_mqtt_broker.sh /home/pi
sudo chmod +x /home/pi/start_main_gui.sh
sudo chmod +x /home/pi/start_mqtt_broker.sh
sudo mv /home/pi/tgn_setup_lib/setup_files/rom.csv /home/pi/tgn_smart_home/config/
clear
sudo python3 /home/pi/tgn_smart_home/libs/settings.py restore
sudo rm -fr /home/pi/tgn_smart_home/setup.sh
sudo rm -fr /home/pi/tgn_smart_home/remove.sh
sudo rm -fr /home/pi/tgn_smart_home/setup_files
echo -e "\e[33m>> \e[31madd tgn_smart_home to autostart (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo echo "@lxterminal -e /home/pi/start_mqtt_broker.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
sudo echo "@lxterminal -e /home/pi/start_main_gui.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
fi
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
echo -e "\e[33m>> \e[31madd tgn_discord_bot to autostart (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo echo "@lxterminal -e /home/pi/tgn_discord_bot/start_bot.sh" >>  /etc/xdg/lxsession/LXDE-pi/autostart
fi
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

echo -e "\e[33m>> \e[31mInstall Apache 2 (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo apt-get -y install apache2
sudo apt-get install php php-mbstring
sudo apt-get install mysql-server php-mysql
sudo apt install phpmyadmin
sleep 3
clear
fi

echo -e "\e[33m>> \e[31mCopy tgn Website (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo mv /home/pi/tgn_setup_lib/setup_files/html.7z /home/pi/tgn_setup_lib/
sudo p7zip -d html.7z
sudo chmod +777 html/
sudo rm -fr html.7z
sudo rm -fr /var/www/html
sudo mv /home/pi/tgn_setup_lib/html /var/www/
sudo chmod +777 /var/www/html/*
sudo chmod +777 /var/www/html/images/*
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
