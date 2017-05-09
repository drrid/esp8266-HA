import machine
import network
import time
from urequests import get
from umqtt.simple import MQTTClient
import ujson
from machine import Pin
from neopixel import NeoPixel

adc = machine.ADC(0)

room_pin = Pin(0, Pin.OUT)
room_pin.low()

neopixel_pin = Pin(12, Pin.OUT)
np5 = NeoPixel(neopixel_pin, 14)

pc_pin = Pin(5, Pin.OUT)
pc_pin.low()

c = MQTTClient("esp8266_desktop", "192.168.1.6", 1883, "drrid", "1543")


def setColor(r, g, b):
    for i in range(np5.n):
        np5[i] = (b, r, g)
    np5.write()


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect("Stealthy-Guy-2Ghz", "matingogenius")
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def callback(topic, msg):
    if topic == b"home/lights/desktop":
        if "color" in msg:
            r = ujson.loads(msg)["color"]["r"]
            g = ujson.loads(msg)["color"]["g"]
            b = ujson.loads(msg)["color"]["b"]
            setColor(r, g, b)
            # c.publish('lights/desktop', "ON")
        else:
            state = ujson.loads(msg)["state"]
            if state == "ON":
                setColor(220, 220, 220)
                # c.publish('lights/desktop', "ON")
            else:
                setColor(0, 0, 0)
                # c.publish('lights/desktop', "OFF")

    if topic == b"home/lights/room":
        adc_val_old = adc.read()
        room_switch()
        adc_val_new = adc.read()
        diff = adc_val_old - adc_val_new
        if diff < 0 :
            c.publish('home/lights/room/state', "ON")
        else:
            c.publish('home/lights/room/state', "OFF")


    if topic == b"home/pc":
        pc_switch()


def pc_switch():
    pc_pin.high()
    time.sleep(1)
    pc_pin.low()


def room_switch():
    room_pin.high()
    time.sleep(0.4)
    room_pin.low()
    time.sleep(0.4)


def mqtt_cli():

    c.set_callback(callback)
    c.connect()
    c.subscribe(b"home/lights/desktop")
    c.subscribe(b"home/lights/room")
    c.subscribe(b"home/pc")

    while True:
        if True:
            c.wait_msg()
        else:
            c.check_msg
            time.sleep(1)
    c.disconnect()


def main():
    do_connect()
    setColor(0, 0, 0)
    mqtt_cli()


if __name__ == '__main__':
    try:
        main()
    except:
        time.sleep(15)
        machine.reset()
