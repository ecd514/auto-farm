import RPI.gpio as gpio
from hardware import PUMP_PIN


def turnPumpOn():
    if not gpio.input(PUMP_PIN):
        gpio.output(PUMP_PIN, 1)
    else:
        print("Pump is already active")


def turnPumpOff():
    if gpio.input(PUMP_PIN):
        gpio.output(PUMP_PIN, 0)
    else:
        print("Pump is already off")
