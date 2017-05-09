import machine
import network
import time
from urequests import get
from umqtt.simple import MQTTClient
import ujson
from machine import Pin
from neopixel import NeoPixel


pin = Pin(13, Pin.OUT)
np = NeoPixel(pin, 20)


def setColor(r, g, b):
	for i in range(np.n):
		np[i] = (b, r, g)
	np.write()


def do_connect():
	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		sta_if.active(True)
		sta_if.connect("Don't Mess With Me", "matingogenius")
		while not sta_if.isconnected():
			pass
	print('network config:', sta_if.ifconfig())


def callback(topic, msg):
	if topic == b"home/lights/bed":
		if "color" in msg:
			r = ujson.loads(msg)["color"]["r"]
			g = ujson.loads(msg)["color"]["g"]
			b = ujson.loads(msg)["color"]["b"]
			setColor(r, g, b)
		else:
			state = ujson.loads(msg)["state"]
			if state == "ON":
				setColor(220, 220, 220)
			else:
				setColor(0, 0, 0)


def mqtt_cli():
	c = MQTTClient("esp8266_bed", "192.168.1.111", 1883, "drrid", "1543")
	c.set_callback(callback)
	c.connect()
	c.subscribe(b"home/lights/bed")

	while True:
		if True:
			c.wait_msg()
		else:
			c.check_msg
			time.sleep(1)
	c.disconnect()

do_connect()
mqtt_cli()


#
#
# if __name__ == '__main__':
#     main()