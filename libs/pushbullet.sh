#!/bin/bash
MSG="$1"
API="$2"
curl -u $API: https://api.pushbullet.com/v2/pushes -d type=note -d title="Raspberry PI" -d body="$MSG"