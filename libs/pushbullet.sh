#!/bin/bash
API="o.luRM2iMEGKnns3pzkOUiEAGX3IxxVxZS"
MSG="$1"
curl -u $API: https://api.pushbullet.com/v2/pushes -d type=note -d title="Raspberry PI" -d body="$MSG"