from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import platform
import sys
import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

print("loading..")

# Example: https://github.com/mbientlab/MetaWear-SDK-Python/blob/master/examples/stream_acc_gyro.py
# Run with python3 metawear.py C4:89:ED:7D:03:ED

def press_button():
    GPIO.output([2], GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output([2], GPIO.LOW)

class State:
    def __init__(self, device):
        self.isLookingDown = False
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)

    def data_handler(self, ctx, data):
        parsedData = parse_value(data)
        leftToRight = parsedData.x
        upAndDown = parsedData.z # -100 is looked down; 100 is looked back up (assuming starting looking straight)
        # print(upAndDown)

        if (self.isLookingDown is False):
            if (upAndDown <= -80):
                self.isLookingDown = True
                print('isLookingDown: ', self.isLookingDown)
                press_button()

        if (self.isLookingDown is True):
            if (upAndDown >= 80):
                self.isLookingDown = False
                print('isLookingDown: ', self.isLookingDown)
                press_button()

        # print("%s -> %s" % (self.device.address, parse_value(data)))
        self.samples+= 1


states = []
for i in range(len(sys.argv) - 1):
    d = MetaWear(sys.argv[i + 1])
    d.connect()
    print("Connected to " + d.address)
    states.append(State(d))

for s in states:
    print("Configuring device")
    libmetawear.mbl_mw_settings_set_connection_parameters(s.device.board, 7.5, 7.5, 0, 6000)
    sleep(1.5)

    #libmetawear.mbl_mw_acc_set_odr(s.device.board, 100.0)
    #libmetawear.mbl_mw_acc_set_range(s.device.board, 16.0)
    #libmetawear.mbl_mw_acc_write_acceleration_config(s.device.board)

    #libmetawear.mbl_mw_gyro_bmi160_set_range(s.device.board, 2000.0);
    #libmetawear.mbl_mw_gyro_bmi160_set_odr(s.device.board, 25.0);
    #libmetawear.mbl_mw_gyro_bmi160_write_config(s.device.board);

    #acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(s.device.board)
    #libmetawear.mbl_mw_datasignal_subscribe(acc, None, s.callback)

    gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(s.device.board)
    libmetawear.mbl_mw_datasignal_subscribe(gyro, None, s.callback)

    #libmetawear.mbl_mw_acc_enable_acceleration_sampling(s.device.board)
    #libmetawear.mbl_mw_acc_start(s.device.board)

    libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(s.device.board)
    libmetawear.mbl_mw_gyro_bmi160_start(s.device.board)

try:
    while True:
        # do nothing and let the script run
        x = 1
except KeyboardInterrupt:
    GPIO.output([2], GPIO.LOW)
    for s in states:
        libmetawear.mbl_mw_acc_stop(s.device.board)
        libmetawear.mbl_mw_acc_disable_acceleration_sampling(s.device.board)

        libmetawear.mbl_mw_gyro_bmi160_stop(s.device.board)
        libmetawear.mbl_mw_gyro_bmi160_disable_rotation_sampling(s.device.board)

        acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(s.device.board)
        libmetawear.mbl_mw_datasignal_unsubscribe(acc)

        gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(s.device.board)
        libmetawear.mbl_mw_datasignal_unsubscribe(gyro)

        libmetawear.mbl_mw_debug_disconnect(s.device.board)

    print("Total Samples Received")
    for s in states:
        print("%s -> %d" % (s.device.address, s.samples))


