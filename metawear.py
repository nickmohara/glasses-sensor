from mbientlab.metawear import MetaWear, libmetawear
from mbientlab.metawear.cbindings import *
from mbientlab.warble import *
from time import sleep

print("loading..")

address = "C4:89:ED:7D:03:ED"

device = MetaWear(address)
device.connect()

print("hello")

print("Connected to " + device.address)

board = device.board

pattern= LedPattern(repeat_count= Const.LED_REPEAT_INDEFINITELY)
libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
libmetawear.mbl_mw_led_write_pattern(device.board, byref(pattern), LedColor.GREEN)
libmetawear.mbl_mw_led_play(device.board)

sleep(5.0)
libmetawear.mbl_mw_led_stop_and_clear(device.board)
sleep(1.0)
device.disconnect()
