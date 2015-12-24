#!/usr/bin/env python
"""
The guess_arduino_port function.

@author: Alexandre Quessy
@date: December 2015
"""
import glob
from twisted.python import log


def guess_arduino_port():
    """
    Finds the first UNIX device that matches /dev/ttyACM0 or /dev/ttyUSB0, for example.
    @return: Its full path.
    @rtype: C{str}
    """
    ttys = glob.glob("/dev/tty*")
    PROSPECTS = [
        "ttyACM", # GNU/Linux for Uno or Mega 2560
        "ttyUSB", # GNU/Linux for older board
        "tty.usbmodem", # OS X for Uno or Mega 2560
        "tty.usbserial", # OS X for older boards
    ]
    for tty in ttys:
        for prospect is PROSPECTS:
            if prospect in tty:
                log.msg("Found Arduino %s" % (tty))
                return tty
    log.msg("Default to %s" % ("/dev/null"))
    return '/dev/null'

