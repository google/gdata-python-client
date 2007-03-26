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
import time


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

  def _InsertEvent(self, title='Tennis with Beth', 
      content='Meet for a quick lesson', where='On the courts',
      start_time=None, end_time=None, recurrence_data=None):
    
    event = gcalendar.CalendarEventEntry()
    event.author.append(atom.Author(name=atom.Name(text='CalendarExample')))
    event.title = atom.Title(text=title)
    event.content = atom.Content(text=content)
    event.where.append(gcalendar.Where(value_string=where))

    if recurrence_data is not None:
      # Set a recurring event
      event.recurrence = gcalendar.Recurrence(text=recurrence_data)
    else:
      if start_time is None:
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
        end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', 
            time.gmtime(time.time() + 3600))
        event.when.append(gcalendar.When(start_time=start_time, 
            end_time=end_time))
    
    new_event = self.cal_client.InsertEvent(event, 
        '/calendar/feeds/default/private/full')
    
    return new_event
    
  def _InsertSingleEvent(self, title='One-time Tennis with Beth',
      content='Meet for a quick lesson', where='On the courts',
      start_time=None, end_time=None):

    new_event = self._InsertEvent(title, content, where, start_time, end_time, 
        recurrence_data=None)

    print 'New single event inserted: %s' % (new_event.id.text,)
    print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
    print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)

    return new_event

  def _InsertRecurringEvent(self, title='Weekly Tennis with Beth',
      content='Meet for a quick lesson', where='On the courts',
      recurrence_data=None):

    if recurrence_data is None:
      recurrence_data = ('DTSTART;VALUE=DATE:20070501\r\n'
        + 'DTEND;VALUE=DATE:20070502\r\n'
        + 'RRULE:FREQ=WEEKLY;BYDAY=Tu;UNTIL=20070904\r\n')

    new_event = self._InsertEvent(title, content, where, 
        recurrence_data=recurrence_data, start_time=None, end_time=None)
    
    print 'New recurring event inserted: %s' % (new_event.id.text,)
    print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
    print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)
  
    return new_event

  def _UpdateTitle(self, event, new_title='Updated event title'):
    previous_title = event.title.text
    event.title.text = new_title
    print 'Updating title of event from:\'%s\' to:\'%s\'' % (
        previous_title, event.title.text,) 
    return self.cal_client.UpdateEvent(event.GetEditLink().href, event)

  def _AddReminder(self, event, minutes=10):
    for a_when in event.when:
      if len(a_when.reminder) > 0:
        a_when.reminder[0].minutes = minutes
      else:
        a_when.reminder.append(gcalendar.Reminder(minutes=minutes))

    print 'Adding %d minute reminder to event' % (minutes,)
    return self.cal_client.UpdateEvent(event.GetEditLink().href, event)

  def _AddExtendedProperty(self, event, 
      name='http://www.example.com/schemas/2005#mycal.id', value='1234'):
    event.extended_property.append(
        gcalendar.ExtendedProperty(name=name, value=value))  
    print 'Adding extended property to event: \'%s\'=\'%s\'' % (name, value,)
    return self.cal_client.UpdateEvent(event.GetEditLink().href, event)
    
  def Run(self):
    self._PrintUserCalendars()
    self._PrintAllEventsOnDefaultCalendar()
    self._FullTextQuery()
    self._DateRangeQuery()
    see = self._InsertSingleEvent()
    see_u_title = self._UpdateTitle(see, 'New title for single event')
    see_u_reminder = self._AddReminder(see_u_title, minutes=30)
    see_u_ext_prop = self._AddExtendedProperty(see_u_reminder, 
        name='propname', value='propvalue')
    ree = self._InsertRecurringEvent()
    
 
def main():
  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["user=", "pw="])
  except getopt.error, msg:
    print 'python calendarExample.py --user [usename] --pw [password] '
    sys.exit(2)

  user = ''
  pw = ''
  key = ''
  # Process options
  for o, a in opts:
    if o == "--user":
      user = a
    elif o == "--pw":
      pw = a

  if user == '' or pw == '':
    print 'python calendarExample.py --user [usename] --pw [password] '
    sys.exit(2)

  sample = CalendarSample(user, pw)
  sample.Run()


if __name__ == '__main__':
  main()
