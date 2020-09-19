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
sudo apt-get -y install firefox-esr
sudo apt-get -y install python-matplotlib
sudo apt-get -y install mpg321
sudo apt-get -y install gir1.2-gstreamer-1.0
sudo apt-get -y install gir1.2-gst-plugins-base-1.0
sudo apt-get -y install python3-pil.imagetk
sudo apt-get -y install p7zip
sudo pip3 install thingspeak==0.4.1
sudo pip3 install gTTS==2.0.3
sudo pip3 install feedparser==5.2.1
sudo pip3 install gitpython==2.1.11
sudo pip3 install fabric3==1.14.post1
sudo pip3 install youtube_dl==2019.7.16
sudo pip3 install spotipy==2.4.4
sudo pip3 install FFmpeg==1.4
sudo pip3 install websockets==7.0
sudo pip3 install aiohttp==3.5.4
sudo pip3 install python-dateutil==2.8.0
sudo pip3 install selenium==3.141.0
sudo pip3 install paho-mqtt==1.4.0
sudo pip3 install pexpect==4.7.0
sudo pip3 install py-enigma==0.1
sudo pip3 install discord.py==0.16.12
sudo pip3 install SQLAlchemy==1.2.15
sudo pip3 install ChatterBot==0.8.7
sudo pip3 install chatterbot-corpus==1.1.4
sudo pip3 install opencv-python==3.4.4.19
sudo pip3 install pushbullet.py==0.11.0
sudo pip3 install twython==3.7.0
sudo pip3 install mcstatus==2.3.0
sudo pip3 uninstall numpy
sudo pip3 install numpy==1.12.1
sudo apt-get install -y libcblas-dev
sudo apt-get install -y libhdf5-dev
sudo apt-get install -y libhdf5-serial-dev
sudo apt-get install -y libatlas-base-dev
sudo apt-get install -y libjasper-dev
sudo apt-get install -y libqtgui4
sudo apt-get install -y libqt4-test
sudo mkdir /home/pi/Pictures
sudo chmod +777 /home/pi/Pictures/
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

cd ..
sudo chmod +x /home/pi/start_main_gui.sh
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

echo -e "\e[33m>> \e[31mInstall MQTT-Server (y/n)?\e[32m"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
sudo apt-get -y install libwebsockets3
sudo apt-get -y install mosquitto
sudo apt install mosquitto mosquitto-clients
pip3 install paho-mqtt
sleep 3
sudo mv /home/pi/tgn_smart_home/setup_files/mosquitto.conf /etc/mosquitto/
sudo rm -fr /home/pi/tgn_smart_home/setup_files
fi

clear

echo -e "\e[31m\e[7m>>\e[0m \e[33mReboot System in 10 sec \e[31m\e[7m<<\e[0m"
sudo rm -fr /home/pi/tgn_smart_home/setup.sh
sudo rm -fr /home/pi/tgn_smart_home/setup_4.sh
sleep 10
reboot
