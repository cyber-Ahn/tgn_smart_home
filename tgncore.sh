#!/bin/bash
pkill firefox
pkill chromium
pkill xterm
sleep 5
DISPLAY=:0 xterm -hold -e python3 /home/pi/tgn_smart_home/core.py