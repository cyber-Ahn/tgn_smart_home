echo -e "#####################################################"
echo -e "####                                              ###"
echo -e "#### Alexa INSTALLATION FUER DEN RASPBERRY PI     ###"
echo -e "#### by www.caworks-sl.de/TGN                     ###"
echo -e "####                                              ###"
echo -e "#####################################################"


echo -e "\n>> Install Java"
sudo mkdir /usr/java
cd /usr/java
wget http://www.caworks-sl.de/data/download/jdk-8u144-linux-arm32-vfp-hflt.tar.gz
sudo tar xf jdk-8u144-linux-arm32-vfp-hflt.tar.gz
sudo update-alternatives --install /usr/bin/java java /usr/java/jdk1.8.0_144/bin/java 1000
sudo update-alternatives --install /usr/bin/javac javac /usr/java/jdk1.8.0_144/bin/javac 1000
java -version

echo -e "\n>> Einrichten von VLC"
cd /usr/lib/arm-linux-gnueabihf
sudo ln -s libvlc.so.5 libvlc.so
sudo ldconfig
cd /home/pi
sleep 5

wget http://www.caworks-sl.de/data/download/start_alexa.sh
sudo chmod +x start_alexa.sh

echo -e "\n>> Downlaod Alexa App"
git clone https://github.com/alexa/alexa-avs-sample-app.git
sleep 5

cd /home/pi/alexa-avs-sample-app

echo -e "\n>> Setup Api data"
sudo nano automated_install.sh

echo -e "\n>> Sarte Installation"
. automated_install.sh
sleep 5

echo -e "\n>> Ready"
