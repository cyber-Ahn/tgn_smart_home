#!/bin/bash
#title:          tgn_smart_home.sh
#description:    Automated TGN Scripts Installation Version 1.6
#author:         cyber Ahn
#date:           20180121
#version:        1.6   
#usage:          sudo bash tgnPythoninstaller.sh
#Support:        https:caworks-sl.de/TGN
#==============================================================================

echo -e "##########################################################"
echo -e "####                                                   ###"
echo -e "#### tgn_smart_home INSTALLATION FOR RASPBERRY PI 3    ###"
echo -e "#### by www.caworks-sl.de/TGN                          ###"
echo -e "####                                                   ###"
echo -e "##########################################################"

echo -e "\n>> Setup Clock"
dpkg-reconfigure tzdata
cat /etc/localtime
apt-get install ntp
apt-get install ntpdate
ntpd -qg
sleep 3

echo -e ">> Install Remote Desktop"
apt-get install xrdp
sleep 5

echo -e ">> Download Libs"
apt-get install python-matplotlib
apt-get install mpg321
apt-get install gir1.2-gstreamer-1.0
apt-get install gir1.2-gst-plugins-base-1.0
apt-get install python-mysqldb
apt-get install python3-pil.imagetk
apt-get install mysql-server
sleep 5

echo -e ">> Install Adafruit_Python_DHT"
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get install build-essential python-dev
sudo python3 setup.py install
sleep 3
cd ..
rm -fr Adafruit_Python_DHT/

sudo mv /home/pi/tgn_smart_home/setup_files/habridge_install.sh /home/pi/tgn_smart_home

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

echo -e ">> Install PiHole"
curl -sSL https://install.pi-hole.net | bash
sleep 2
pihole -a -p Kevin2711
sleep 5

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
sudo chmod +x start_main_gui.sh
sudo rmdir /home/pi/tgn_smart_home/setup_files
sleep 5

sudo python3 /home/pi/tgn_smart_home/libs/settings.py intsall_rom
sleep 5

echo -e ">> Please Reboot System"
