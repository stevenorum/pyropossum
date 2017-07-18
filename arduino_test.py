#!/usr/bin/env python3

from pyropossum.arduino.core import Arduino
from pyropossum.arduino.commands import ENABLE, DISABLE
import time

OUTPUT_PIN = 5

with Arduino.discover(timeout=1) as arduino:
    for i in range(1,10):
        print("Enabling for {} seconds.".format(i))
        ENABLE.call(inputs=OUTPUT_PIN, arduino=arduino)
        print("Enabled.")
        time.sleep(i)
        print("Disabling for {} seconds.".format(i))
        DISABLE.call(inputs=OUTPUT_PIN, arduino=arduino)
        time.sleep(i)
        print("Disabled.")
