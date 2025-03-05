import RPi.GPIO as GPIO
import enum as Enum


class GPIOPinDirection(Enum):
    INPUT = 'input'
    OUTPUT = 'output'


class Pin:

    def __init__(self, pinnumber: int = -1, state: bool = 0, pindirection: GPIOPinDirection):
        self.pinnumber = pinnumber
        self.state = state
        self.pindirection = pindirection
        self.configured: bool = False

    def pinsetup(self):
        GPIO.setmode

    def on(self):
        assert self.pinnumber >= 0, "GPIO pin has not been set, but an attempt to activate it was made."
        GPIO.
