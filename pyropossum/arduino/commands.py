#!/usr/bin/env python3

import logging
from pyropossum.arduino import core as ardcore

logger = logging.getLogger(__name__)

def byteify(b):
    '''Doesn't currently do anything.  May never do anything.  Its intended purpose is to convert different objects into individual bytes. '''
    if type(b) == int:
        return b
    else:
        return b

def bytesify(bs):
    '''Converts a number of different structures into bytes objects, so they can be passed into a serial connection.'''
    if type(bs) == bytes:
        return bs
    elif type(bs) == int:
        return bytes([bs])
    elif type(bs) == list:
        return bytes([byteify(b) for b in bs])
    elif type(bs) == str:
        return bytesify(int(bs))
    else:
        return bs

def hexify_bytes(bs, header=True):
    '''Convert a bytes object into a hex string for easier inspection.'''
    return ('0x' if header else '') + ''.join(format(x, '02x') for x in bs)

class Command(object):
    '''
    Class to encapsulate a command to send to an Arduino.
    Ideally, every command should be written so as to be idempotent, as the first bit of communication over the serial connection often has issues for some reason.
    '''
    _NOOP = bytesify(0)

    def __init__(self, name, bytestring, responselength, retries=0):
        self.name = name
        self.bytestring = bytestring
        self.responselength = responselength
        self.attempts = 1 + retries
        pass

    def call(self, inputs=None, arduino=None):
        '''
        Actually execute the command, with the provided inputs (if applicable).
        If an Arduino is provided, that's where the command is sent.  Otherwise, this chooses one from the USB-connected arduinos it can detect.
        '''
        if arduino:
            return self._call(arduino, inputs)
        else:
            with ardcore.sopen(timeout=2) as _ard:
                return self._call(_ard, inputs)
            pass
        pass

    def _call(self, ard, inputs=None):
        for i in range(self.attempts):
            logger.debug("Sending command {}, expecting {} response bytes.".format(self.name, self.responselength))
            ard.write(Command._NOOP)
            to_print = bytesify(self.bytestring)
            if inputs:
                to_print += bytesify(inputs)
            ard.write(to_print)
            response = ard.read(self.responselength)
            if response:
                return response
            else:
                logger.debug("No response received.")
                pass
            pass
        logger.warn("No response received.")
        return None

    pass

DISABLE = Command(name="DISABLE",bytestring=1, responselength=1, retries=5)
ENABLE = Command(name="ENABLE",bytestring=2, responselength=1, retries=5)
READ_STATE = Command(name="READ_STATE",bytestring=3, responselength=1, retries=5)
READ_SENSORS = Command(name="READ_SENSORS",bytestring=4, responselength=8, retries=5)
ECHO = Command(name="ECHO",bytestring=5, responselength=1, retries=5)

GET_SERIAL = Command(name="GET_SERIAL",bytestring=32, responselength=1, retries=5)
SET_SERIAL = Command(name="SET_SERIAL",bytestring=33, responselength=1, retries=5)
