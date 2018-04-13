import paho.mqtt.client as mqtt

mqtt_topic = "esp"
mqtt_broker_ip = "192.168.0.98"
temp_target = "/home/pi/tgn_smart_home/config/"
temp_file = "mqtt.temp"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected!", str(rc))
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):
    topic = msg.topic
    message = str(msg.payload)
    message = message.replace("b'", " ")
    message = message.replace("'", " ")
    message = message.replace(" ", "")
    if topic == mqtt_topic:
        print(message)
        file = open(temp_target+temp_file,"w")
        file.write(message)
        file.close()

client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
