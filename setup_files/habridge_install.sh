#!/bin/bash
#title:          habridge_install.sh
#description:    Automated HA-Bridge Installation Version 4.1.4
#author:         O. Splitt
#date:           20170206
#version:        1.01    
#usage:          sudo bash habridge_install.sh
#notes:          Install oracle-java8-jdk to use HA-Bridge. Needs root to install...
#Support:        https://wp.me/p5xMu5-gl
#==============================================================================

INSTALLATION_PATH=/home/pi/habridge
WEBSERVER_PORT=81
IP_ADRESS=`ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'`
DOWNLOAD_HABRIDGE=https://github.com/bwssytems/ha-bridge/releases/download/v4.5.1/ha-bridge-4.5.1.jar
DOWNLOAD_FILENAME=ha-bridge-4.5.1.jar


echo -e "#####################################################"
echo -e "####                                              ###"
echo -e "#### HA-BRIDGE INSTALLATION FUER DEN RASPBERRY PI ###"
echo -e "#### by www.splittscheid.de                       ###"
echo -e "####                                              ###"
echo -e "#####################################################"
echo -e "\n>> Erstelle Verzeichnis"
mkdir ${INSTALLATION_PATH} >/dev/null 2>&1
mkdir ${INSTALLATION_PATH}/data >/dev/null 2>&1
touch ${INSTALLATION_PATH}/data/habridge.config
echo -e "{\"upnpconfigaddress\":\"${IP_ADRESS}\",\"serverport\":${WEBSERVER_PORT},\"upnpresponseport\":50000,\"upnpdevicedb\":\"${INSTALLATION_PATH}/data/device.db\",\"buttonsleep\":100,\"upnpstrict\":true,\"traceupnp\":false,\"veraconfigured\":false,\"harmonyconfigured\":false,\"nestconfigured\":false,\"farenheit\":true,\"configfile\":\"${INSTALLATION_PATH}/data/habridge.config\",\"numberoflogmessages\":512,\"hueconfigured\":false,\"halconfigured\":false,\"settingsChanged\":false,\"myechourl\":\"echo.amazon.com/#cards\",\"webaddress\":\"0.0.0.0\",\"mqttconfigured\":false,\"hassconfigured\":false,\"domoticzconfigured\":false}" > ${INSTALLATION_PATH}/data/habridge.config

echo -e ">> Download HA-Bridge"
wget ${DOWNLOAD_HABRIDGE} >/dev/null 2>&1
mv  ${DOWNLOAD_FILENAME} ${INSTALLATION_PATH}

echo -e ">> Verlinke HA-Bridge"
ln -s ${INSTALLATION_PATH}/${DOWNLOAD_FILENAME} ${INSTALLATION_PATH}/ha-bridge.jar >/dev/null 2>&1

echo -e ">> Korrigiere Berechtigungen"
sudo chown -R pi:pi ${INSTALLATION_PATH}

echo -e ">> Erstelle HA-Bridge Service"
touch /etc/systemd/system/habridge.service >/dev/null 2>&1
echo -e "[Unit]\nDescription=HA Bridge\nWants=network.target\nAfter=network.target\n\n[Service]\nType=simple\n\nExecStart=/usr/bin/java -jar -Dserver.port=${WEBSERVER_PORT} -Dconfig.file=${INSTALLATION_PATH}/data/habridge.config ${INSTALLATION_PATH}/ha-bridge.jar\n\n[Install]\nWantedBy=multi-user.target" > /etc/systemd/system/habridge.service
systemctl daemon-reload >/dev/null 2>&1
systemctl enable habridge.service >/dev/null 2>&1
systemctl start habridge.service >/dev/null 2>&1

sleep 1
HB_PID=`ps -ef | grep habridge | grep java | grep -v grep | awk '{print $2}'`
if [ ! ${HB_PID} ]
then
        echo -e "\n>> Dienst HA-Bridge wurde nicht gestartet... Bitte Log prüfen: /var/log/syslog"
else
        echo -e "\n>> Dienst HA-Bridge mit Prozess ID >>  ${HB_PID}  << gestartet und im Browser wie folgt erreichbar:\n   http://${IP_ADRESS}:${WEBSERVER_PORT}\n\n   INSTALLATION ERFOLGREICH ABGESCHLOSSEN"
fi
