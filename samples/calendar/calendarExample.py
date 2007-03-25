#!/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
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


__author__ = 'api.rboyd@gmail.com (Ryan Boyd)'


from elementtree import ElementTree
import gcalendar_service
import gdata_service
import app_service
import gcalendar
import atom
import getopt
import sys
import string


class CalendarSample:

  def __init__(self, email, password):
    self.cal_client = gcalendar_service.CalendarService()
    self.cal_client.email = email
    self.cal_client.password = password
    self.cal_client.source = 'Calendar-Python-Sample-1.0'
    self.cal_client.ProgrammaticLogin()
   
  def _PrintUserCalendars(self): 
    feed = self.cal_client.GetCalendarListFeed()
    print feed.title.text
    for i, a_calendar in enumerate(feed.entry):
      print '\t%s. %s' % (i, a_calendar.title.text,)

  def _PrintAllEventsOnDefaultCalendar(self):
    feed = self.cal_client.GetCalendarEventFeed()
    print 'Events on Primary Calendar: %s' % (feed.title.text,)
    for i, an_event in enumerate(feed.entry):
      print '\t%s. %s' % (i, an_event.title.text,)
      for p, a_participant in enumerate(an_event.who):
        print '\t\t%s. %s' % (p, a_participant.email,)
        print '\t\t\t%s' % (a_participant.name,)
        print '\t\t\t%s' % (a_participant.attendee_status.value,)

  def _FullTextQuery(self, text_query='Drinks'):
    print 'Full text query for events on Primary Calendar: \'%s\'' % (
        text_query,)
    query = gcalendar_service.CalendarEventQuery('default', 'private', 'full',
        text_query)
    feed = self.cal_client.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
      print '\t%s. %s' % (i, an_event.title.text,)
      print '\t\t%s. %s' % (i, an_event.content.text,)
      for a_when in an_event.when:
        print '\t\tStart time: %s' % (a_when.start_time,)
        print '\t\tEnd time:   %s' % (a_when.end_time,)

  def _DateRangeQuery(self, start_date='2007-01-01', end_date='2007-07-01'):
    print 'Date range query for events on Primary Calendar: %s to %s' % (
        start_date, end_date,)
    query = gcalendar_service.CalendarEventQuery('default', 'private', 'full')
    query.start_min = start_date
    query.start_max = end_date 
    feed = self.cal_client.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
      print '\t%s. %s' % (i, an_event.title.text,)
      for a_when in an_event.when:
        print '\t\tStart time: %s' % (a_when.start_time,)
        print '\t\tEnd time:   %s' % (a_when.end_time,)

  #def _CreateEvent
  #def _CreateSingleEvent
  #def _CreateRecurringEvent
  #def _UpdateTitle
  #def _AddReminder
  #def _AddExtendedProperty
    
  def Run(self):
    self._PrintUserCalendars()
    self._PrintAllEventsOnDefaultCalendar()
    self._FullTextQuery()
    self._DateRangeQuery()
 
def main():
  user = ''
  pw = ''

  sample = CalendarSample(user, pw)
  sample.Run()


if __name__ == '__main__':
  main()
