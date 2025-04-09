import RPi.GPIO as GPIO


class Pin:

    def __init__(self, pinnumber: int = -1, state: bool = 0,
                 pindirection: str = 'input'):

        assert pindirection.lower == 'input' or pindirection.lower == 'output', ...
        ("Error: Invalid GPIO pin direction. {} is not 'input' or 'output'.",
         pindirection.lower)

        self.number: int = pinnumber
        self.state: bool = state
        self.direction: str = pindirection
        self.configured: bool = False

    def setup(self):
        assert self.number >= 0, ...
        "GPIO pin has not been set, but an attempt to activate it was made."
        GPIO.setup(self.number, self.direction, initial=GPIO.LOW)
        self.configured = True
        self.state = False

    def up(self):
        assert self.configured, ...
        "Error: GPIO pin has not been configured yet. Please configure the pin before using it."
        assert self.direction == 'output', ...
        ("Error: GPIO pin direction is NOT set to 'output', pin direction '{}' is not valid.",
         self.direction)
        GPIO.HIGH(self.number)
        self.state = True

    def down(self):
        assert self.configured, ...
        "Error: GPIO pin has not been configured yet. Please configure the pin before using it."
        assert self.direction == 'output', ...
        ("Error: GPIO pin direction is NOT set to 'output', pin direction '{}' is not valid.",
         self.direction)
        GPIO.LOW(self.number)
        self.state = False
