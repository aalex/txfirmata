#!/usr/bin/env python
"""
Connects to an Arduino

@author: Alexandre Quessy
@date: December 2015
"""
from twisted.python import log
from twisted.python import usage
from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
import sys
import os
import glob

EXAMPLES_DIR = "examples"

def _is_in_project_dir():
    d = os.path.split(os.path.dirname(os.path.abspath(__file__)))[1]
    return d == EXAMPLES_DIR

def _add_project_dir_to_python_path():
    d = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    sys.path.insert(0, d)
    os.environ["PATH"] += ":%s" % (os.path.join(d, EXAMPLES_DIR))


class Options(usage.Options):
    """
    Command line options for this program
    """
    optFlags = [
        ["verbose", "v", "Print many info"],
    ]
    optParameters = [
        ["outfile", "o", None, "Logfile [default: sys.stdout]"],
        ["baudrate", "b", None, "Serial baudrate [default: 57600]"],
        ["port", "p", None, "Serial Port device"],
    ]



if __name__ == '__main__':
    if _is_in_project_dir():
        _add_project_dir_to_python_path()

    from txfirmata import utils
    from txfirmata import firmata

    options = Options()
    # defaults
    baudrate = 57600
    filename = None
    port = utils.guess_arduino_port()
    try:
        options.parseOptions()
    except usage.UsageError, errortext:
        print("%s: %s" % (sys.argv[0], errortext))
        print("%s: Try --help for usage details." % (sys.argv[0]))
        raise SystemExit, 1

    # Logging option
    logFile = options.opts["outfile"]
    if logFile is None:
        logFile = sys.stdout
    log.startLogging(logFile)

    # Verbose
    if options.opts['verbose']:
        print("TODO: be verbose")
    # Baud rate
    if options.opts["baudrate"]:
        baudrate = int(options.opts["baudrate"])
    # Port
    if options.opts["port"]:
        port = options.opts["port"]

    # Open it
    log.msg("Attempting to open %s at %dbps as a %s device" % (port, baudrate, firmata.FirmataProtocol.__name__))
    communicator = firmata.FirmataCommunicator()
    s = SerialPort(firmata.FirmataProtocol(communicator), port, reactor, baudrate=baudrate)
    reactor.run()

