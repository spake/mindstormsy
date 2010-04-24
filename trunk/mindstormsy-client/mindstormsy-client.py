#!/usr/bin/python
#
# Mindstormsy-Client combines the MindstormsyAPI with the nxtdriver module to enable the controlling
# of a LEGO Mindstorms NXT robot through the Mindstormsy Wave Robot and Gadget.
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

from mindstormsyapi import MindstormsyClient, SERVER_ERROR, UNKNOWN_ERROR
import nxtdriver
from optparse import OptionParser
import sys

def main():
	# Parse the command line arguments
	
	parser = OptionParser()
	parser.add_option("-w",	"--waveId",
		dest="waveId",
		action="store",
		type="string",
		help="REQUIRED. Click on the 'Get Wave ID' button in the Mindstormsy gadget to retrieve this. Be sure to enclose the ID within single quotes, as bash doesn't like exclamation points outside of them.",
		metavar="ID")
	parser.add_option("-s", "--serialPort",
		dest="serialPort",
		action="store",
		type="string",
		help="REQUIRED. The name of the serial port that was created when you paired your NXT robot with the computer...you have already paired it, right?",
		metavar="PORT")
	parser.add_option("-p", "--power",
		dest="power",
		action="store",
		type="int",
		help="The power at which the motors will drive. Can be any value between 0 and 100. Although 100 is tempting, it will drain your battery very quickly!",
		metavar="POWER",
		default=75)
	parser.add_option("-t", "--timeout",
		dest="timeout",
		action="store",
		type="int",
		help="The number of seconds each attempt to poll the server will last. If the timeout expires, it simply tries again. Don't make it 1 if you're on a slow internet connection!",
		metavar="TIMEOUT",
		default=2)
	
	(options, args) = parser.parse_args()
	
	waveId = options.waveId
	serialPort = options.serialPort
	power = options.power
	reversePower = power * -1
	timeout = options.timeout
	
	if not waveId or not serialPort:
		parser.error("waveId and serialPort are both required arguments, and make sure that waveId is enclosed within single quotes")
	
	# Create our client object
	# This is used to poll the Wave robot
	client = MindstormsyClient()
	
	# Begin by opening the Bluetooth connection
	
	print "Opening connection to robot on", serialPort
	d = nxtdriver.Driver(serialPort)
	motors = nxtdriver.MOTOR_A + nxtdriver.MOTOR_B + nxtdriver.MOTOR_C
	print "Connection established"
	
	# Now the polling starts
	
	prev = '\x00' * 3
	while 1:
		try:
			# This gets the current action from the Wave robot using MindstormsyAPI
			# Each action consists of three characters, and each character represents a motor
			# f = forward, r = reverse, and x = stop/halt
			curr = client.poll(waveId, timeout)
			if len(curr) == 3:
				if curr == SERVER_ERROR:
					print "Received error code from the server."
					print "Verify that the Wave ID you used (%s) was correct, and try again." % waveId
					sys.exit(1)
				elif curr == UNKNOWN_ERROR:
					print "Poll failed"
					continue
				
				forward = list()
				reverse = list()
				halt = list()
				bigmsg = ""
				
				for i in range(3):
					if curr[i] != prev[i]:
						if curr[i] == "f":
							forward.append(i)
						elif curr[i] == "r":
							reverse.append(i)
						elif curr[i] == "x":
							halt.append(i)
					
				for n in forward:
					bigmsg += d.message(motors[n], nxtdriver.ON, power=power)
				for n in reverse:
					bigmsg += d.message(motors[n], nxtdriver.ON, power=reversePower)
				for n in halt:
					bigmsg += d.message(motors[n], nxtdriver.OFF)
				
				if bigmsg != "":
					d.sendBytes(bigmsg)
				prev = curr
			else:
				print "Action of length", len(curr), "received, discarding"
		except KeyboardInterrupt:
			print
			d.close()
			break

if __name__ == "__main__":
	main()
