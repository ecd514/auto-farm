import RPi.GPIO as pin
import time

pin.setwarnings(False)
pin.setmode(pin.BCM)
pin.setup(17, pin.OUT)

toggle_var: bool = False

try:
    while True:
        pin.output(17, pin.HIGH)
        time.sleep(1)

except KeyboardInterrupt:
    pin.cleanup()
    print("Done")
