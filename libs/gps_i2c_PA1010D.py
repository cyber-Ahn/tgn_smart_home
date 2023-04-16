import time
import board
import adafruit_gps
from tgnLIB import ifI2C, get_ip
import paho.mqtt.client as mqtt

gps_address = 0x00

num_count = 0
wait_for_fix = 7200 #2 hours
client = mqtt.Client("kasa_bridge")
client.connect(get_ip())

try:
    f_d = open("/home/pi/tgn_smart_home/config/i2c.config","r")
    for line in f_d:
        if "gps_address" in line:
            gps_address = int(line.rstrip().split("*")[1],16)
except IOError:
	print("cannot open i2c.config.... file not found")

if ifI2C(gps_address) == "found device":
    print("GPS found $d{}".format(gps_address))
    print("=" * 40)
    client.publish("tgn/gps/found","GPS found $d{}".format(gps_address),qos=0,retain=True)
    i2c = board.I2C()
    gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")  # Turn on the basic GGA and RMC info
    gps.send_command(b"PMTK220,1000")                                   # Set update rate to once a second (1hz)
    last_print = time.monotonic()
    client.publish("tgn/gps/status","Offline ... search GPS",qos=0,retain=True)
    while True:
        gps.update()
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            if not gps.has_fix:
                num_count = num_count + 1                                            # wait for GPS Signal
                print("Waiting for fix..."+str(num_count))
                if num_count == wait_for_fix:
                    break
                continue
            client.publish("tgn/gps/status","Online",qos=0,retain=True)
            print("=" * 40)
            print("Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(gps.timestamp_utc.tm_mon,gps.timestamp_utc.tm_mday,gps.timestamp_utc.tm_year,gps.timestamp_utc.tm_hour,gps.timestamp_utc.tm_min,gps.timestamp_utc.tm_sec))
            client.publish("tgn/gps/timestamp","Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(gps.timestamp_utc.tm_mon,gps.timestamp_utc.tm_mday,gps.timestamp_utc.tm_year,gps.timestamp_utc.tm_hour,gps.timestamp_utc.tm_min,gps.timestamp_utc.tm_sec),qos=0,retain=True)
            print("Latitude: {0:.6f} degrees".format(gps.latitude))
            client.publish("tgn/gps/latitude","Latitude: {0:.6f} degrees".format(gps.latitude),qos=0,retain=True)
            print("Longitude: {0:.6f} degrees".format(gps.longitude))
            client.publish("tgn/gps/longitude","Longitude: {0:.6f} degrees".format(gps.longitude),qos=0,retain=True)
            print("Fix quality: {}".format(gps.fix_quality))
            client.publish("tgn/gps/quality",gps.fix_quality,qos=0,retain=True)
            if gps.satellites is not None:
                print("# satellites: {}".format(gps.satellites))
                client.publish("tgn/gps/satellites",gps.satellites,qos=0,retain=True)
            if gps.altitude_m is not None:
                print("Altitude: {} meters".format(gps.altitude_m))
                client.publish("tgn/gps/altitude",gps.altitude_m,qos=0,retain=True)
            if gps.speed_knots is not None:
                print("Speed: {} knots".format(gps.speed_knots))
                client.publish("tgn/gps/speed",gps.speed_knots,qos=0,retain=True)
            if gps.track_angle_deg is not None:
                print("Track angle: {} degrees".format(gps.track_angle_deg))
                client.publish("tgn/gps/angle",gps.track_angle_deg,qos=0,retain=True)
            if gps.horizontal_dilution is not None:
                print("Horizontal dilution: {}".format(gps.horizontal_dilution))
                client.publish("tgn/gps/dilution",gps.horizontal_dilution,qos=0,retain=True)
            if gps.height_geoid is not None:
                print("Height geoid: {} meters".format(gps.height_geoid))
                client.publish("tgn/gps/height",gps.height_geoid,qos=0,retain=True)
            break
else:
    print("GPS not found")
    client.publish("tgn/gps/found","GPS not found $d{}".format(gps_address),qos=0,retain=True)