######################################################################
##
## Quick test script for the SerialData class
## 
## Author: Kaisar H
##
## Date: 16th July, 2017
##
######################################################################

from time import sleep
import serial
import SerialData

DEBUG = False
COM_PORT = "COM9"
COM_BAUD = 115200

data = []

def main():
	global DEBUG
	ser = SerialData.SerialData(COM_PORT, COM_BAUD, bytesize=serial.EIGHTBITS, 
		parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, xonxoff=0, rtscts=0, debug=DEBUG )
	
	while True:
		val = ser.next()
		data.append(val)
		print val
		sleep(0.1)
	
if __name__ == '__main__':
	main()
