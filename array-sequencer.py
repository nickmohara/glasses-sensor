# A script to program drum patterns on your solenoid based Raspberry Pi mechanical drum machine
# For the interactive step sequencer, @see https://github.com/mnkii/pibeat
# Instructable @see https://www.instructables.com/id/A-Raspberry-Pi-Powered-Junk-Drum-Machine/
# @see http://www.banjowise.com/post/automabeat/

import RPi.GPIO as GPIO
import time
import numpy as np

################ Tweak the variables in this section to configure your PI and create your drum pattern ################

# Set the BPM (speed) here
bpm = 120

# Create your drum pattern here. Each line represents a beat. Each 0 or 1 is a solenoid (1 = drum should be played,
# 0 = don't play). Add more arrays lines to add more beats. Add more 1's or 0's to each array to add more drums (also
# update gpio_map)
sequence = [
  [1, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
]

# List the BCM pin number of the GPIO pins you have connected each solenoid to here. You can leave this as is if you
# followed the numbering in the Instructable. Add more items to the array if you have more solenoids (and update
# sequence to match)
gpio_map = [2, 3, 4, 17, 27, 22, 10, 9]

# The Lenth of time each solenoid should be activated
active_duration = 0.01

############################################# The main script starts here #############################################

# Sets pin number to BCM mode
GPIO.setmode(GPIO.BCM)

# Calculate the time period between the solenoid being deactivated and the next beat starting
beat_gap = (float(60) / float(bpm)) - float(active_duration)


# Generator to infinitely loop around the sequence
def infinite_generator(n):
    i = 0
    while True:
        if i >= len(n):
            i = 0

        yield n[i]
        i = i + 1

# Loop through each pin and set the mode and state to 'low'
for i in gpio_map:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

# Run the infinite loop
try:
    for beat in infinite_generator(sequence):
        # Get active drum numbers
        active = np.where(beat)[0]
        # Get pin numbers for active drums
        pins = [gpio_map[i] for i in active]

        print('Activating Pins ', pins)
        GPIO.output(pins, GPIO.LOW)
        time.sleep(active_duration)
        GPIO.output(pins, GPIO.HIGH)
        print('Sleep ', beat_gap)
        time.sleep(beat_gap)

# End program cleanly
except KeyboardInterrupt:
    print ('Quit')
    # Reset GPIO settings
    GPIO.cleanup()
