#!/bin/bash
#title:          tgn_smart_home
#description:    Automated TGN Smart Home Installation
#author:         cyber Ahn
#date:           20180121
#version:        1.8
#usage:          sudo bash Setup.sh
#Support:        https:caworks-sl.de/TGN
#==============================================================================

echo -e "##########################################################"
echo -e "####                                                   ###"
echo -e "#### tgn_smart_home INSTALLATION FOR RASPBERRY PI 3    ###"
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

echo -e ">> set authority"
chmod +x /home/pi/tgn_smart_home/libs/pushbullet.sh
chmod +x start_gui.sh
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
cd ..
sudo chmod +x /home/pi/start_main_gui.sh
clear

echo -e ">> Install SpeechRecognition and LIB's"
sudo apt-get install flac
cd /home/pi/tgn_smart_home/setup_files/PyAudio
python3 setup.py install --skip-build
cd /home/pi/tgn_smart_home
sudo apt-get installl libportaudio-dev
sudo apt-get install python-dev
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
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

sudo rm -fr /home/pi/tgn_smart_home/setup_files
sleep 5

sudo python3 /home/pi/tgn_smart_home/libs/settings.py install_rom
sleep 5

clear

sudo python3 /home/pi/tgn_smart_home/libs/settings.py weather

clear

sudo python3 /home/pi/tgn_smart_home/libs/settings.py pushb

clear

sudo python3 /home/pi/tgn_smart_home/libs/settings.py thinkspeak

clear

echo -e "\n>> Install Java"
sudo mkdir /usr/java
cd /usr/java
wget http://www.caworks-sl.de/data/download/jdk-8u144-linux-arm32-vfp-hflt.tar.gz
sudo tar xf jdk-8u144-linux-arm32-vfp-hflt.tar.gz
sudo update-alternatives --install /usr/bin/java java /usr/java/jdk1.8.0_144/bin/java 1000
sudo update-alternatives --install /usr/bin/javac javac /usr/java/jdk1.8.0_144/bin/javac 1000
java -version
sleep 3

clear

echo -e ">> Reboot System"
sleep 3
reboot
