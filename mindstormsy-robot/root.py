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

import cgi
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
import main
import logging
from django.utils.simplejson import loads, dumps
import urllib

class MainPage(webapp.RequestHandler):
	def get(self):
		waveId = self.request.get("id")
		if waveId == "" or not waveId:
			self.response.set_status(302)
			self.response.headers["Location"] = "http://code.google.com/p/mindstormsy"
			self.response.out.write("<html><body><a href=\"http://code.google.com/p/mindstormsy\">http://code.google.com/p/mindstormsy</a></body></html>")
			return
		self.response.headers["Content-type"] = "application/json"
		waveId = urllib.unquote(waveId)
		actionObject = main.getActionObject(waveId, shouldCreate=False)
		if actionObject:
			actionString = actionObject.desc
		else:
			actionString = "err"
		actionJson = dumps({"action": actionString})
		self.response.out.write(actionJson)

application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def m():
	run_wsgi_app(application)

if __name__ == "__main__":
	m()