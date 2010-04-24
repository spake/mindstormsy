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
MindstormsyAPI allows you to easily plug your own custom device into Mindstormsy on Google Wave. Using MindstormsyClient.poll(), you can fetch the current action string from the Wave robot and use it to control your device.
This module is especially useful if you don't own a LEGO Mindstorms NXT robot, and/or you want to use Mindstormsy with a different device.
'''

import httplib
from json import loads, dumps
import types
import urllib

SERVER_ERROR = "err"		# Indicates that a non-fatal error occurred on the server
							# Usually means an invalid Wave ID

UNKNOWN_ERROR = "unk"		# Indicates that an error occurred in the MindstormsyAPI
							# Use MindstormsyClient.lastError to get a more detailed explanation about what went wrong

NO_ERROR = 0				# Everything's fine, stop being so paranoid!

CONNECTION_ERROR = 1		# An error occurred while connecting to the Wave robot
							# Could mean a timeout, spelling mistake in the server name, no internet connection, etc.

REQUEST_ERROR = 2			# The connection to the server was successful, but a status code other than 200 OK was returned
							# Or, something failed while reading the response from the server

INVALID_JSON_ERROR = 3		# The JSON returned from the server was invalid, and the parser failed

UNKNOWN_UNKNOWN_ERROR = 4	# Panic!

class MindstormsyClient():
	"""The MindstormsyClient class enables you to fetch action strings from a Mindstormsy-Robot instance on the Google App Engine."""
	def __init__(self, server="mindstormsy-robot.appspot.com", port=80):
		"Initialises the object. Specify your own server (hostname only) if you're running a custom Mindstormsy-Robot instance (and custom port if it's running locally)."
		self._server = server
		self._port = 80
		self.lastError = NO_ERROR
	
	def poll(self, waveId, timeout):
		"Polls the Wave robot. Specify the Wave ID (the user can obtain this through the Mindstormsy gadget in Google Wave) and connection timeout. The method will return the current action for the Wave ID as a string. If there was an error connecting or invalid data was fetched, then UNKNOWN_ERROR will be returned. If you receive an UNKNOWN_ERROR, then check MindstormsyClient.lastError for a more detailed explanation on what went wrong. Refer to the error codes in mindstormsyapi.py for more info. An error on the server (usually the Wave ID not existing in the database yet) will return SERVER_ERROR."
		try:
			conn = httplib.HTTPConnection(self._server, self._port, True, timeout)
			conn.request("GET", "/?id=" + urllib.quote(waveId))
			response = conn.getresponse()
		except KeyboardInterrupt as e:
			raise e
		except:
			self.lastError = CONNECTION_ERROR
			return UNKNOWN_ERROR
		
		try:
			if response.status != 200:
				self.lastError = REQUEST_ERROR
				return UNKNOWN_ERROR
			data = response.read()
			conn.close()
		except KeyboardInterrupt as e:
			raise e
		except:
			self.lastError = REQUEST_ERROR
			return UNKNOWN_ERROR
		
		try:
			action = loads(data)["action"]
			self.lastError = NO_ERROR
			return action
		except KeyboardInterrupt as e:
			raise e
		except:
			self.lastError = INVALID_JSON_ERROR
			return UNKNOWN_ERROR
		
		self.lastError = UNKNOWN_ERROR_ERROR
		return UNKNOWN_ERROR

if __name__ == "__main__":
	print "Import me using 'import mindstormsyapi'."
