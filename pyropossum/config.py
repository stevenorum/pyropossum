#!/usr/bin/env python3

import json
import logging
import os
import sys

def load_json_file(fname, throw_if_missing = False):
    if not os.path.isfile(fname):
        if throw_if_missing:
            raise RuntimeError("File {} does not exist.".format(fname))
        else:
            return None
    with open(fname,'r') as f:
        return json.load(f)

CONFIG_LOCATIONS = [
    os.path.join(os.path.expanduser('~'), '.pyropossum/config.json'),
    "/etc/pyropossum/config.json"
]

def load_config():
    for location in CONFIG_LOCATIONS:
        config = load_json_file(location)
        if config:
            return config
        pass
    return {"profile":"pyropossum","region":"us-east-1","stack":"iot3","output":5}

def configure_logging(modname):
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    for module in ('botocore', 'boto3', 'requests'):
        logging.getLogger(module).level = logging.INFO
        pass

    return logging.getLogger(modname)
