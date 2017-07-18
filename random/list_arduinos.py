#!/usr/bin/env python3

from pyropossum.arduino import core as ardcore

arduinos = ardcore.find_arduinos()

for arduino in arduinos:
    ardcore.dump_port_info(arduino)
