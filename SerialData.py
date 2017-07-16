######################################################################
##
## Serial data wrapper
## Source: https://github.com/danparsons/SerialGraph
## 
######################################################################

from threading import Thread
import serial
import sys
import time

DEBUG = False

buf = ''
def rx(ser):
    """Receive serial data"""
    global buf
    tmpbuf = ''
    while ser:
        time.sleep(0.001)
        # Keep reading until an entire line is in the buffer, then return the last line
        tmpbuf = tmpbuf + ser.read(size=ser.inWaiting())
        if '\n' in tmpbuf:
            lines = tmpbuf.split('\n')
            buf = lines[-2]
            tmpbuf = lines[-1]
            if DEBUG:
                print "Serial data:\n%s" % lines[-2]

class SerialData(object):
    """Handle the serial port"""
    def __init__(self, port, baudrate, bytesize, parity, stopbits, xonxoff, rtscts, debug):
        global DEBUG
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.ser = None
        self.buf = ''
        self.debug = debug
        DEBUG = self.debug
        
        try:
            self.ser = serial.Serial(
                port = self.port,
                baudrate = self.baudrate,
                bytesize = self.bytesize,
                parity = self.parity,
                stopbits = self.stopbits,
                timeout = 0.1,
                xonxoff = self.xonxoff,
                rtscts = self.rtscts,
                interCharTimeout = None
            )
        except serial.serialutil.SerialException:
            print "*********************** Serial port connection failure"
            self.ser = None
        else:
            Thread(target=rx, args=(self.ser,)).start()
            
    def next(self):
        if not self.ser:
            print "Serial port error"
            return 0
            #sys.exit(-1)
        try:
            val = int(buf.split(',')[0].strip())
            return val
        except ValueError:
            print 'Invalid data: ', buf
    def get(self, index):
        if not self.ser:
            print "Serial port error"
            return 0
            #sys.exit(-1)
        try:
            val = buf.split(',')[index].strip()
            print val
            return val
        except ValueError:
            print 'Invalid data: ', buf
    def getstr(self):
        if not self.ser:
            print "Serial port error"
            return 0
            #sys.exit(-1)
        try:
            return buf
        except ValueError:
            print 'Invalid data: ', buf
    def __del__(self):
        if self.ser:
            self.ser.close()
