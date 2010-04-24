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

from django.utils.simplejson import loads, dumps
import logging
from google.appengine.ext import db
from waveapi import appengine_robot_runner
from waveapi import element
from waveapi import events
from waveapi import robot

GADGET_URL = "http://mindstormsy-robot.appspot.com/static/mindstormsy-gadget.xml"
IMAGE_URL = "http://mindstormsy-robot.appspot.com/static/thumbnail.jpg"
PROFILE_URL = "http://code.google.com/p/mindstormsy"

DEFAULT_ACTION_STRING = "xxx" # All three motors halted

class Action(db.Model):
	desc = db.StringProperty(required=False)
	waveId = db.StringProperty(required=True)

def setActionObject(a, waveId):
	actionObject = getActionObject(waveId)
	actionObject.desc = a
	actionObject.put()

def getActionObject(waveId, shouldCreate=True):
	query = db.GqlQuery("SELECT * FROM Action WHERE waveId = :1", waveId).fetch(1000)
	if len(query) == 0 and shouldCreate:
		actionObject = Action(desc=DEFAULT_ACTION_STRING, waveId=waveId)
		actionObject.put()
		return getActionObject(waveId)
	elif len(query) > 1:
		actionString = query[-1].desc
		query = db.GqlQuery("DELETE FROM Action WHERE waveId = :1", waveId)
		actionObject = Action(desc=actionString, waveId=waveId)
		actionObject.put()
		return getActionObject(waveId)
	elif len(query) == 1:
		return query[0]
	return None

def OnGadgetStateChanged(event, wavelet):
	blip = event.blip
	gadget = blip.all(element.Gadget, url=GADGET_URL)
	if gadget:
		try:
			actionJson = gadget.get("actions")
			actionString = loads(actionJson)[0]
			setActionObject(actionString, wavelet.wave_id)
		except:
			pass

def OnWaveletSelfAdded(event, wavelet):
	setActionObject(DEFAULT_ACTION_STRING, wavelet.wave_id)

if __name__ == '__main__':
	r = robot.Robot('Mindstormsy', image_url=IMAGE_URL, profile_url=PROFILE_URL)
	r.register_handler(events.GadgetStateChanged, OnGadgetStateChanged)
	r.register_handler(events.WaveletSelfAdded, OnWaveletSelfAdded)
	appengine_robot_runner.run(r)