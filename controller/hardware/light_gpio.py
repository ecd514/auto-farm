import RPi.GPIO as gpio
from hardware import LIGHT_PIN


def turnLightOn():
    if not gpio.input(LIGHT_PIN):
        gpio.output(LIGHT_PIN, 1)
    else:
        print("Light is already active")


def turnLightOff():
    if gpio.input(LIGHT_PIN):
        gpio.output(LIGHT_PIN, 0)
    else:
        print("Light is already off")
