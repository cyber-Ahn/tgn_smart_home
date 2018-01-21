#!/bin/bash

#Start companion service
cd /home/pi/alexa-avs-sample-app/samples
cd companionService && sudo npm start&

#Run the sample app
echo "Starting sample app."
cd /home/pi/alexa-avs-sample-app/samples
cd javaclient && sudo mvn exec:exec&
echo "When finished "
read -n1 -r -p "Press space to continue..." key

#Run the Wake Word Engine
cd /home/pi/alexa-avs-sample-app/samples
cd wakeWordAgent/src && sudo ./wakeWordAgent -e sensory &
