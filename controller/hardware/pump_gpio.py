try:
    import RPI.gpio as gpio
    gpioAvailable = True
except Exception as PiImportFail:
    print(PiImportFail)
    gpioAvailable = False

from .constants import PUMP_PIN


def turnPumpOn():
    if gpioAvailable:
        if not gpio.input(PUMP_PIN):
            gpio.output(PUMP_PIN, 1)
        else:
            print("Pump is already active")
    else:
        print("Pump has been turned on!")


def turnPumpOff():
    if gpioAvailable:
        if gpio.input(PUMP_PIN):
            gpio.output(PUMP_PIN, 0)
        else:
            print("Pump is already off")
    else:
        print("Pump turned off.")
