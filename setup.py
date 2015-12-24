#!/usr/bin/env python
"""
txosc installation script
"""
from setuptools import setup
import txfirmata

setup(
    name = "txfirmata",
    version = txfirmata.__version__,
    author = "Alexandre Quessy",
    author_email = "alexandre@quessy.net",
    url = "http://github.com/aalex/txfirmata",
    description = "Firmata Arduino Protocol for Twisted",
    license="MIT/X",
    packages = ["txfirmata", "txfirmata/test"],
    long_description = """Firmata is a protocol for communicating with microcontrollers from software on a computer. This library implements Firmata for the Twisted Python framework.""",
    classifiers = [
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
        ]
    )

