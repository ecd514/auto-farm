import RPI.gpio as gpio
from hardware import PUMP_PIN, LIGHT_PIN


def gpioSetup():
    gpio.setmode(gpio.BOARD)

    gpio.setup(PUMP_PIN, gpio.OUT, initial=gpio.LOW)
    gpio.setup(LIGHT_PIN, gpio.OUT, initial=gpio.HIGH)
