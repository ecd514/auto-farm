try:
    import RPI.gpio as gpio
    gpioAvailable = True
except Exception as PiImportFail:
    print(PiImportFail)
    gpioAvailable = False

from .constants import LIGHT_PIN


def turnLightOn():
    if gpioAvailable:
        if not gpio.input(LIGHT_PIN):
            gpio.output(LIGHT_PIN, 1)
        else:
            print("Light is already active")
    else:
        print("Light activated!")


def turnLightOff():
    if gpioAvailable:
        if gpio.input(LIGHT_PIN):
            gpio.output(LIGHT_PIN, 0)
        else:
            print("Light is already off")
    else:
        print("Light turned off.")
