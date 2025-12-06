#!/bin/bash
sudo chmod +x /home/pi/tgn_smart_home/tasmota-NSPanel/nspanel.sh
sudo cp /home/pi/tgn_smart_home/tasmota-NSPanel/panel.service /etc/systemd/system
systemctl daemon-reload >/dev/null 2>&1
systemctl enable panel.service >/dev/null 2>&1
systemctl start panel.service >/dev/null 2>&1