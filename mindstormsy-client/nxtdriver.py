#!/usr/bin/python
#
# Copyright (C) 2010 George Caley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
nxtdriver is an easy way to control a LEGO Mindstorms NXT robot over Bluetooth through Python.

To make the module work, you must have PySerial installed on your computer; you can download it from http://pyserial.sourceforge.net.
'''

import sys

try:
	import serial # kudos to pyserial @ http://pyserial.sourceforge.net
except ImportError:
	print "ERROR: nxtdriver requires PySerial to run"
	print "Download and install it from http://pyserial.sourceforge.net and try again"
	sys.exit(1)

# Constants

MOTOR_A = '\x00'
MOTOR_B = '\x01'
MOTOR_C = '\x02'

ON = '\x01'
OFF = '\x02'

MIN_POWER = -100
MAX_POWER = 100
DEFAULT_POWER = 75

class Driver:
	"""This class represents a connection to the LEGO Mindstorms NXT robot."""
	
	def __init__(self, serialPort):
		"Initialises the Driver. Make sure you know the serial port that was created when you paired the robot with your computer over Bluetooth."
		self._serialPort = serialPort
		self.open()
	
	def open(self):
		"Opens the serial connection to the robot. This is done automatically when the class is initialised."
		self._conn = serial.Serial(self._serialPort)
	
	def close(self):
		"Closes the serial connection to the robot."
		self._conn.close()
	
	def sendBytes(self, bytes):
		"Sends bytes to the robot."
		self._conn.write(bytes)
	
	def setMotor(self, motor, state, power=DEFAULT_POWER):
		"Sets one of the motors on the robot with the parameters specified. You must provide the motor (MOTOR_A, MOTOR_B or MOTOR_C), the state (ON or OFF). The motor power (MIN_POWER to MAX_POWER) is optional. All the constants are found in the nxtdriver module."
		self.sendBytes(self.message(motor, state, power=power))
	
	def message(self, motor, state, power=DEFAULT_POWER):
		"Compiles a message to be sent to the robot. Accepts the same parameters as Driver.setMotor(), and returns the compiled bytes. Multiple messages can be joined together and then sent as one through Driver.sendBytes()."
		power = max(min(power, MAX_POWER), MIN_POWER)
		if power < 0: power += 255
		return '\r\x00\x80\x04' + motor + chr(power) + state + '\x01\x00\x20\x00\x00\x00\x00\x00'

if __name__ == "__main__":
	print "Import me using 'import nxtdriver'."