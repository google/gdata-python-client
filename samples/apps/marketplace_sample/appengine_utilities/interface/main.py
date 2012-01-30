'''
Copyright (c) 2008, appengine-utilities project
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the appengine-utilities project nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import os, cgi, __main__
from google.appengine.ext.webapp import template
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext import db

from appengine_utilities import cron

class MainPage(webapp.RequestHandler):
    def get(self):
        c = cron.Cron()
        query = cron._AppEngineUtilities_Cron.all()
        results = query.fetch(1000) 
        template_values = {"cron_entries" : results}
        path = os.path.join(os.path.dirname(__file__), 'templates/scheduler_form.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        if str(self.request.get('action')) == 'Add':
            cron.Cron().add_cron(str(self.request.get('cron_entry')))
        elif str(self.request.get('action')) == 'Delete':
            entry = db.get(db.Key(str(self.request.get('key'))))
            entry.delete()
        query = cron._AppEngineUtilities_Cron.all()
        results = query.fetch(1000) 
        template_values = {"cron_entries" : results}
        path = os.path.join(os.path.dirname(__file__), 'templates/scheduler_form.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication(
                                       [('/gaeutilities/', MainPage)],
                                       debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()