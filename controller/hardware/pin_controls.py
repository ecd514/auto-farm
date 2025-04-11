try:
    import RPI.gpio as gpio
    gpioAvailable = True
except Exception as PiImportFail:
    print(PiImportFail)
    gpioAvailable = False

from .constants import PUMP_PIN, LIGHT_PIN


def gpioSetup():
    gpio.setmode(gpio.BOARD)

    gpio.setup(PUMP_PIN, gpio.OUT, initial=gpio.LOW)
    gpio.setup(LIGHT_PIN, gpio.OUT, initial=gpio.HIGH)
