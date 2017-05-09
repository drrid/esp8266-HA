def mqtt_cli():
	# c = MQTTClient("esp8266_bed", "m12.cloudmqtt.com", 16883, "drrid", "210628")
	c = MQTTClient("esp8266_bed", "192.168.1.101", 1883, "homeassistant", "210628")
	c.connect()
	c.publish(b"foo_topic", b"hello")
	c.disconnect()


do_connect()
mqtt_cli()


def get_data():
	url = URL.format('sun.sun')
	resp = get(url)
	return resp.json()['state']

def main():
	do_connect()
	while True:
		try:
			data = get_data()
			print(data)
		except TypeError:
			pass
		time.sleep(TIMEOUT)