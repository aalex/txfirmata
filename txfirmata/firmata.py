#!/usr/bin/env python
"""
Connects to an Arduino.

@author: Alexandre Quessy
@date: December 2015
"""
from twisted.python import log
from twisted.protocols import basic
from txfirmata import sig
from txfirmata import utils

# Constants
PINMODE_INPUT = 0
PINMODE_OUTPUT = 1
PINMODE_PWM = 2
PINMODE_SERVO = 3

VALUE_LOW = 0
VALUE_HIGH = 1

CMD_DIGITAL_MESSAGE = 0x90 # set a digital ouput pin value
CMD_ANALOG_MESSAGE = 0xE0 # set a PWM output pin value
CMD_REPORT_ANALOG = 0xC0 # enable analog input for pin #
CMD_SET_PINMODE = 0xF4 # set a pin to input/output/pwm/etc.
CMD_REPORT_VERSION = 0xF9 # retrieve firmata firmware version
CMD_SYSTEM_RESET = 0xF0
CMD_START_SYSEX = 0xF0
CMD_END_SYSEX = 0xF7
CMD_QUERY_FIRMWARE = 0x79 # query the firmata firmware name


class FirmataProtocol(basic.LineReceiver):
    """
    Simple protocol to send and receive ASCII to/from a plotter.
    """
    def __init__(self, communicator):
        self._buffer = ''
        self._communicator = communicator
        self._communicator._connectedProtocol = self
        self._communicator.connected(True)
        super(FirmataProtocol, self).__init__()
        self.setRawMode() # further data will trigger rawDataReceived

    def lineReceived(self, line):
        # unused, since we called setRawMode
        log.msg("FirmataProtocol: Received: \"%s\"" % (line))

    @utils.log_callable
    def rawDataReceived(self, data):
        txt = _data_to_hex(data)
        log.msg("FirmataProtocol: Received: \"%s\"" % (txt))
        self._buffer = self._buffer + data
        self._handleDataReceived()

    @utils.log_callable
    def _handleDataReceived(self):
        # Sees if we can handle the buffered data, and parse it as Firmata messages
        if len(self._buffer) == 0:
            return
        first_byte = utils.get_first_byte(self._buffer)
        handler = None
        if first_byte < CMD_START_SYSEX:
            # These commands have channel data
            pass

    @utils.log_callable
    def sendRawData(self, data):
        """
        We cannot use sendLine, since it appends the delimiter.
        Hence, we use this method to send data to the Arduino.
        """
        self.transport.write(data)


class FirmataCommunicator(object):
    """
    Two-way communication to and from the Arduino using the FirmataProtocol.
    """
    def __init__(self):
        self._connectedProtocol = None
        # public signals
        # self.digital_received = sig.Signal() # args: pin, value
        # self.analog_received = sig.Signal() # args: pin, value
        self.connected = sig.Signal() # args: success

    def pin_mode(self, pin, mode):
        pass


# TODO: list arduini
# TODO: set pin mode to PINMODE_INPUT
# TODO: int digital_read(int)
# TODO: int analog_read(int)

