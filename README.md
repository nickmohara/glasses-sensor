# Texting and driving experiment

See the full video here: https://youtu.be/sU9WBr3ckrU

Mbientlab MetaMotionC Sensor: https://mbientlab.com/store/metamotionc/

`metawear-and-tv.py` is used for the TV device and `metawear-and-driving.py` is used for the texting and driving device. The only difference is the driving script only actuates when looking down while the TV actuates when you look down and look back up (to pause and then resume play). The texting and driving script is also more sensitive.

Either script can be run with:
```
python3 metawear-and-tv.py C4:89:ED:7D:03:ED
```
where `C4:89:ED:7D:03:ED` is the ID of the bluetooth device.
