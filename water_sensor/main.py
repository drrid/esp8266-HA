import machine
import network
import time
from umqtt.simple import MQTTClient
import ujson
from machine import Pin

pin = Pin(0, Pin.IN)


def do_connect():
	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		sta_if.active(True)
		sta_if.connect("Stealthy-Guy-2Ghz", "matingogenius")
		while not sta_if.isconnected():
			pass
	print('network config:', sta_if.ifconfig())


def get_percentage(duration):
	fromLow = 895
	fromHigh = 1074
	toLow = 65
	toHigh = 97 #84

	percentage = (((duration - fromLow) * (toHigh - toLow)) / (fromHigh - fromLow)) + toLow
	return(percentage)


def get_cap():
	count = 0
	count2 = 0
	f = 0
	f2 = 0

	while count < 500:
		f+=machine.time_pulse_us(pin, 0)
		count+=1
	f = f/500
	p = get_percentage(f)

	while count2 < 500:
		f2+=machine.time_pulse_us(pin, 1)
		count2+=1
	f2 = f2/500
	f3 = (f+f2)/2
	p2 = get_percentage(f3)

	return(f3, p2)


def mqtt_cli():

	c = MQTTClient("esp8266_water", "192.168.1.6", 1883, "drrid", "1543")
	c.connect()
	while True:
		duration, percentage = get_cap()
		c.publish("home/sensors/water", ujson.dumps({"percentage": round(percentage, 2)}))
		time.sleep(0.1)
	c.disconnect()


def main():
	do_connect()
	mqtt_cli()


if __name__ == '__main__':
	try:
		main()
	except:
		time.sleep(15)
		machine.reset()