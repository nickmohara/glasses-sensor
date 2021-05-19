import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

# Run the infinite loop
try:
    while True:
        GPIO.output([2], GPIO.LOW)
        time.sleep(2)
        GPIO.output([2], GPIO.HIGH)
        time.sleep(2)

# End program cleanly
except KeyboardInterrupt:
    print ('Quit')
    # Reset GPIO settings
    GPIO.output([2], GPIO.LOW)

