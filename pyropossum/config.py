#!/usr/bin/env python3

import json
import logging
import sys

def load_config():
    if len(sys.argv) > 1:
        with open(sys.argv[1],'r') as f:
            return json.load(f)
        pass
    else:
        return {"profile":"pyropossum","region":"us-east-1","stack":"iot3","output":5}

def configure_logging(modname):
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    for module in ('botocore', 'boto3', 'requests'):
        logging.getLogger(module).level = logging.INFO
        pass

    return logging.getLogger(modname)
