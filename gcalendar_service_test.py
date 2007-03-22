#!/usr/bin/python
#
# Copyright (C) 2006 Google Inc.
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

__author__ = 'jscudder@google.com (Jeff Scudder)'

import unittest
from elementtree import ElementTree
import gcalendar_service
import gdata_service
import app_service
import atom

class GCalendarServiceUnitTest(unittest.TestCase):
  
  def setUp(self):
    self.gd_client = gcalendar_service.GCalendarService()
    self.gd_client.email = 'gdata.ops.demo@gmail.com'
    self.gd_client.password = 'gmail-brybg'
    self.gd_client.source = 'GCalendarClient "Unit" Tests'

  def tearDown(self):
    # No teardown needed
    pass  

 
  def testQuery(self):
    
    my_query = gcalendar_service.EventCalendarQuery()
#    my_query = gcalendar_service.ListCalendarsQuery()
#    my_query.start_min = '2006-03-16T00:00:00'
#    my_query.start_max = '2006-03-24T23:59:59'
#    my_query['max-results'] = '25'
    self.gd_client.ProgrammaticLogin()
    print "uri is ", my_query.ToUri()
    result = self.gd_client.CalendarQuery(my_query)
    for calentry in result.entry:
      print calentry.__class__.__name__
      print 'id: ', calentry.id.text
      print 'transparency: ', calentry.transparency.value
      print 'visibility: ', calentry.visibility.value
      for awho in calentry.who:
        print "who ", awho.name, ' rel=', awho.rel, " status=", awho.attendeeStatus, " type=", awho.attendeeType

      calentry.visibility.value='CONFIDENTIAL'
#      print "back to xml ", calentry
   
    
#    self.assert_(isinstance(result, atom.Feed))
      
        
if __name__ == '__main__':
  unittest.main()
