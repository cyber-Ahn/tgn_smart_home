
from tgnLIB import PAJ7620U2, ifI2C, get_ip
import paho.mqtt.client as mqtt
import time

count_pos = 1
count_max = 6

client = mqtt.Client("PAJ_Gesture")
client.connect(get_ip())
client.publish("tgn/gesture/touch","0",qos=0,retain=True)
client.publish("tgn/gesture/btn_ni_li","1",qos=0,retain=True)

if ifI2C(0x73) == "found device":
	print("Gesture Sensor Program ...")
	paj7620u2=PAJ7620U2()
	while True:
		time.sleep(0.05)
		gesture_name = paj7620u2.check_gesture()
		if gesture_name != "x":
			#print(gesture_name)
			if gesture_name == "Right":
				count_pos = count_pos - 1
				if count_pos < 1:
					count_pos = 1
				client.publish("tgn/gesture/btn_ni_li",str(count_pos),qos=0,retain=True)
			if gesture_name == "Left":
				count_pos = count_pos + 1
				if count_pos > count_max:
					count_pos = count_max
				client.publish("tgn/gesture/btn_ni_li",str(count_pos),qos=0,retain=True)
			print(str(count_pos))
			if gesture_name == "Forward":
				client.publish("tgn/gesture/touch","1",qos=0,retain=True)
				time.sleep(8)
				client.publish("tgn/gesture/touch","0",qos=0,retain=True)

else:
	print("Gesture Sensor not found ...")