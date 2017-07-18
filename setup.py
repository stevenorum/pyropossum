#!/usr/bin/env python3

from setuptools import setup

setup(
    name = "pyropossum",
    version = "0.0.1",
    author = "Steve Norum",
    author_email = "stevenorum@gmail.com",
    description = ("Tools for controlling stuff through THE CLOUD!!1!"),
    license = "Beerware",
    keywords = "iot arduino aws sqs",
    url = "http://drelabs.com",
    packages=['pyropossum','pyropossum/arduino', 'pyropossum/aws'],
    scripts = [
        'scripts/pyro-on',
        'scripts/pyro-off',
        'scripts/pyro-daemon',
    ]
)
