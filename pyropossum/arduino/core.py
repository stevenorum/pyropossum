#!/usr/bin/env python3

import json
import logging
import serial.tools.list_ports
import serial
from serial.serialutil import SerialException

logger = logging.getLogger(__name__)

class ArduinoException(Exception):
    '''Exception relating to an Arduino.'''

class NoArduinoConnectedException(ArduinoException):
    '''Exception thrown when an Arduino-touching activity is attempted, but no Arduino is found.'''

class ArduinoCommunicationFailedException(ArduinoException):
    '''Exception thrown when communication with an Arduino fails, for any reason.'''

def dump_port_info(port):
    '''Print a bunch of mostly-useless information about a connected USB device.  Primarily used for debugging during development.'''
    print(dir(port))
    attrs = ['apply_usb_info', 'description', 'device', 'hwid', 'interface', 'location', 'manufacturer', 'name', 'pid', 'product', 'serial_number', 'usb_description', 'usb_info', 'vid']
    fn_attrs = ['usb_info','usb_description']
    port.apply_usb_info()
    for attr in attrs:
        if hasattr(port, attr):
            val = getattr(port, attr)
            if attr in fn_attrs:
                val = getattr(port, attr)()
            print("{attr} : {val}".format(attr=attr, val=val))
            pass
        pass
    pass

BOARDS = {
    (6790,29987):("AMZN/Gikfun","Nano Clone"), # http://amzn.to/2vbf0Qo
    (9025,32822):("AMZN/KOOKYE","Pro Micro/Leonardo Clone"), # http://amzn.to/2tk9eyE
    (1027,24597):("SparkFun","RedBoard") # http://amzn.to/2uBO3It / https://www.sparkfun.com/products/13975
}

def get_arduino_info(p):
    '''Get the manufacturer and type information for an Arduino.'''
    return BOARDS.get((p.vid, p.pid), None)

def find_all_devices():
    return [p for p in serial.tools.list_ports.comports()]

def find_arduinos():
    '''Return all the Arduinos connected to this computer.'''
    return [p for p in serial.tools.list_ports.comports() if get_arduino_info(p)]

def find_arduino_devices():
    '''Returns the device port IDs for each Arduino connected to this computer.'''
    return [p.device for p in find_arduinos()]

def sopen(port=None,baud=9600, **kwargs):
    '''Open a serial connection with the specified Arduino, or an arbitrarily chosen one if none is specified.'''
    port = port if port else find_arduino_devices()[0]
    return serial.Serial(port, baud, **kwargs)

class Arduino(object):
    '''
    Wrapper class for an Arduino serial connection.  Currently doesn't add much, but eventually it might.
    '''
    def __init__(self, port_info, baud=9600, **kwargs):
        self.port_info = port_info
        self.manufacturer = get_arduino_info(self.port_info)[0]
        self.model = get_arduino_info(self.port_info)[1]
        self.device = port_info.device
        self.baud = baud
        self.kwargs = kwargs
        self.serial_connection = None
        pass

    @classmethod
    def discover(cls, *args, **kwargs):
        '''
        Create an Arduino from one found attached to this machine.
        Raises an error if none are found.
        '''
        available = find_arduinos()
        if not available:
            raise NoArduinoConnectedException("No available Arduinos found!")
        return Arduino(available[0], *args, **kwargs)

    def connect(self):
        logger.debug("Opening arduino serial connection.")
        self.serial_connection = serial.Serial(self.device, self.baud, **self.kwargs)
        self.serial_connection.__enter__()
        pass

    def disconnect(self):
        if self.serial_connection:
            logger.debug("Closing arduino serial connection.")
            self.serial_connection.__exit__()
            self.serial_connection = None
            pass
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()
        pass

    def read(self, *args, **kwargs):
        '''
        Read from the Arduino.  Parameters are the same as PySerial's Serial.read() method.
        Raises an error if the serial connection is not established.
        '''
        if not self.serial_connection:
            raise ArduinoCommunicationFailedException("Serial connection not established.")
        try:
            return self.serial_connection.read(*args, **kwargs)
        except SerialException as e:
            logger.exception("Serial communication failed.")
            raise ArduinoCommunicationFailedException("Serial connection failed.", e)
        pass

    def write(self, *args, **kwargs):
        '''
        Write to the Arduino.  Parameters are the same as PySerial's Serial.write() method.
        Raises an error if the serial connection is not established.
        '''
        if not self.serial_connection:
            raise ArduinoCommunicationFailedException("Serial communication not established.")
        try:
            return self.serial_connection.write(*args, **kwargs)
        except SerialException as e:
            logger.exception("Serial communication failed.")
            raise ArduinoCommunicationFailedException("Serial communication failed.", e)
        pass

class ArduinoArray(object):
    '''
    Context manager for handling connections to multiple Arduinos at the same time.
    NOT YET IMPLEMENTED.
    '''
    def __init__(self, arduinos=[], baud=9600, **kwargs):
        self.arduinos = arduinos

    def add_arduino(self, arduino):
        self.arduinos.append(arduino)

    def discover_arduinos(self):
        for arduino in find_arduinos():
            self.arduinos.append(Arduino(arduino))
            pass
        pass

    def __enter__(self):
        for arduino in self.arduinos:
            arduino.__enter__()
            pass
        return self

    def __exit__(self, *args):
        for arduino in self.arduinos:
            arduino.__exit__()
            pass
        pass
