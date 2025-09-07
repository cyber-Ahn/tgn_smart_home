#!/bin/bash
#---- install
echo -e "\e[33m>> \e[31mInstall Zigbee2Mqtt\e[32m"
sudo curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs git make g++ gcc libsystemd-dev
corepack enable
node --version
sudo mkdir /opt/zigbee2mqtt
sudo chown -R pi: /opt/zigbee2mqtt
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
cd /opt/zigbee2mqtt
pnpm install --frozen-lockfile
sudo rm -fr /opt/zigbee2mqtt/data/configuration.yaml
#---- autostart
systemctl stop pihole-FTL
pnpm start
xdg-open 'http://192.168.0.98:8080'
read answer
echo -e "\e[33m>> \e[31mSettings Saved (y/n)?\e[32m"
if [ "$answer" != "${answer#[Yy]}" ] ;then
systemctl start pihole-FTL
fi
sudo cp /home/pi/tgn_smart_home/zigbee/zigbee2mqtt.service /etc/systemd/system
systemctl daemon-reload >/dev/null 2>&1
systemctl enable zigbee2mqtt.service >/dev/null 2>&1
chmod -R 777 /opt/zigbee2mqtt/
systemctl start zigbee2mqtt.service >/dev/null 2>&1
#-----
sudo cp /home/pi/tgn_smart_home/zigbee/zigbee2tgn.service /etc/systemd/system
systemctl daemon-reload >/dev/null 2>&1
systemctl enable zigbee2tgn.service >/dev/null 2>&1
systemctl start zigbee2tgn.service >/dev/null 2>&1