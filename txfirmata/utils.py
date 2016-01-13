#!/usr/bin/env python
"""
The guess_arduino_port function.

@author: Alexandre Quessy
@date: December 2015
"""
import glob
from twisted.python import log


CMD_START_SYSEX = 0xF0
CMD_END_SYSEX = 0xF7

def list_arduino_ports():
    """
    Lists all UNIX device that match /dev/ttyACM0 or /dev/ttyUSB0, for example.
    @rtype: C{list}
    """
    ttys = glob.glob("/dev/tty*")
    PROSPECTS = [
        "ttyACM", # GNU/Linux for Uno or Mega 2560
        "ttyUSB", # GNU/Linux for older board
        "tty.usbmodem", # OS X for Uno or Mega 2560
        "tty.usbserial", # OS X for older boards
    ]
    ret = []
    for tty in ttys:
        for prospect in PROSPECTS:
            if prospect in tty:
                ret.append(tty)
    return ret


def guess_arduino_port():
    """
    Finds the first UNIX device that matches /dev/ttyACM0 or /dev/ttyUSB0, for example.
    @return: Its full path.
    @rtype: C{str}
    """
    ttys = list_arduino_ports()
    if len(ttys) > 0:
        log.msg("Found Arduino %s" % (ttys[0]))
        return ttys[0]
    log.msg("Default to %s" % ("/dev/null"))
    return '/dev/null'


def convert_to_two_bytes(value):
    """
    @type value: C{int}
    @rtype: C{bytearray}
    @return: least-significatn byte, most significant byte
    """
    return bytearray([value % 128, value >> 7])


def convert_to_sysex(sysex_command, data):
    """
    @type sysex_command: C{int}
    @type data: C{bytearray}
    @rtype: C{bytearray}
    """
    msg = bytearray([CMD_START_SYSEX, sysex_command])
    msg.extend(data)
    msg.append(CMD_END_SYSEX)
    return msg


def str_to_bytearray(data):
    """
    @type data: C{str}
    @rtype: C{bytearray}
    """
    # we could also do: return map(ord, data), but it's slower
    return bytearray(data) # FIXME: we might need to convert the str to an encoding


def get_first_byte(data):
    """
    @type data: C{bytearray}
    @rtype: C{int}
    """
    return data[0]


def data_to_hex(data):
    """
    @type data: C{bytearray}
    @rtype: C{str}
    """
    txt = ''.join('%02x' % (i) for i in data)
    return txt


def log_callable(func):
    """
    Decorator to automatically log each time this function of method is called.
    """
    def func_wrapper(*args, **kwargs):
        log.msg("%s(%s, %s)" % (func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return func_wrapper

