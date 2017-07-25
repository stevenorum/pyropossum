#!/usr/bin/env python3

from pyropossum.config import configure_logging

logger = configure_logging(__name__)

class LED(object):

    def __init__(self, pin):
        self.pin = pin
        self.state = False
        pass

    def on(self):
        logger.info("pin {} : now on (was {})".format(self,pin, "on" if self.state else "off"))
        self.state = True
        pass
    def off(self):
        logger.info("pin {} : now off (was {})".format(self,pin, "on" if self.state else "off"))
        self.state = False
        pass
