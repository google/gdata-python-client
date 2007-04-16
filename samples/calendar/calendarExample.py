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


try:
  from xml.etree import ElementTree
except ImportError:
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


class CalendarExample:

  def __init__(self, email, password):
    """Creates a CalendarService and provides ClientLogin auth details to it.
    The email and password are required arguments for ClientLogin.  The 
    CalendarService automatically sets the service to be 'cl', as is 
    appropriate for calendar.  The 'source' defined below is an arbitrary 
    string, but should be used to reference your name or the name of your
    organization, the app name and version, with '-' between each of the three
    values.  The account_type is specified to authenticate either 
    Google Accounts or Google Apps accounts.  See gdata_service or 
    http://code.google.com/apis/accounts/AuthForInstalledApps.html for more
    info on ClientLogin.  NOTE: ClientLogin should only be used for installed 
    applications and not for multi-user web applications."""

    self.cal_client = gcalendar_service.CalendarService()
    self.cal_client.email = email
    self.cal_client.password = password
    self.cal_client.source = 'Google-Calendar_Python_Sample-1.0'
    self.cal_client.ProgrammaticLogin()

  def _PrintUserCalendars(self): 
    """Retrieves the list of calendars to which the authenticated user either
    owns or subscribes to.  This is the same list as is represented in the 
    Google Calendar GUI.  Although we are only printing the title of the 
    calendar in this case, other information, including the color of the
    calendar, the timezone, and more.  See CalendarListEntry for more details
    on available attributes."""

    feed = self.cal_client.GetCalendarListFeed()
    print feed.title.text
    for i, a_calendar in enumerate(feed.entry):
      print '\t%s. %s' % (i, a_calendar.title.text,)

  def _PrintAllEventsOnDefaultCalendar(self):
    """Retrieves all events on the primary calendar for the authenticated user.
    In reality, the server limits the result set intially returned.  You can 
    use the max_results query parameter to allow the server to send additional
    results back (see query parameter use in DateRangeQuery for more info).
    Additionally, you can page through the results returned by using the 
    feed.GetNextLink().href value to get the location of the next set of
    results."""
  
    feed = self.cal_client.GetCalendarEventFeed()
    print 'Events on Primary Calendar: %s' % (feed.title.text,)
    for i, an_event in enumerate(feed.entry):
      print '\t%s. %s' % (i, an_event.title.text,)
      for p, a_participant in enumerate(an_event.who):
        print '\t\t%s. %s' % (p, a_participant.email,)
        print '\t\t\t%s' % (a_participant.name,)
        print '\t\t\t%s' % (a_participant.attendee_status.value,)

  def _FullTextQuery(self, text_query='Tennis'):
    """Retrieves events from the calendar which match the specified full-text
    query.  The full-text query searches the title and content of an event,
    but it does not search the value of extended properties at the time of
    this writing.  It uses the default (primary) calendar of the authenticated
    user and uses the private visibility/full projection feed.  Please see:
    http://code.google.com/apis/calendar/reference.html#Feeds 
    for more information on the feed types.  Note: as we're not specifying
    any query parameters other than the full-text query, recurring events
    returned will not have gd:when elements in the response.  Please see
    the Google Calendar API query paramters reference for more info:
    http://code.google.com/apis/calendar/reference.html#Parameters"""

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
    """Retrieves events from the server which occur during the specified date
    range.  This uses the CalendarEventQuery class to generate the URL which is
    used to retrieve the feed.  For more information on valid query parameters,
    see: http://code.google.com/apis/calendar/reference.html#Parameters"""

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
    """Inserts a basic event using either start_time/end_time definitions
    or gd:recurrence RFC2445 icalendar syntax.  Specifying both types of
    dates is not valid.  Note how some members of the CalendarEventEntry
    class use arrays and others do not.  Members which are allowed to occur
    more than once in the calendar or GData "kinds" specifications are stored
    as arrays.  Even for these elements, Google Calendar may limit the number
    stored to 1.  The general motto to use when working with the Calendar data
    API is that functionality not available through the GUI will not be 
    available through the API.  Please see the GData Event "kind" document:
    http://code.google.com/apis/gdata/elements.html#gdEventKind
    for more information"""
    
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
        # Use current time for the start_time and have the event last 1 hour
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
    """Uses the _InsertEvent helper method to insert a single event which
    does not have any recurrence syntax specified."""

    new_event = self._InsertEvent(title, content, where, start_time, end_time, 
        recurrence_data=None)

    print 'New single event inserted: %s' % (new_event.id.text,)
    print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
    print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)

    return new_event

  def _InsertRecurringEvent(self, title='Weekly Tennis with Beth',
      content='Meet for a quick lesson', where='On the courts',
      recurrence_data=None):
    """Users the _InsertEvent helper method to insert a recurring event which
    has only RFC2445 icalendar recurrence syntax specified.  Note the use of
    carriage return/newline pairs at the end of each line in the syntax.  Even 
    when specifying times (as opposed to only dates), VTIMEZONE syntax is not
    required if you use a standard Java timezone ID.  Please see the docs for
    more information on gd:recurrence syntax:
    http://code.google.com/apis/gdata/elements.html#gdRecurrence
    """ 

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
    """Updates the title of the specified event with the specified new_title.
    Note that the UpdateEvent method (like InsertEvent) returns the 
    CalendarEventEntry object based upon the data returned from the server
    after the event is inserted.  This represents the 'official' state of
    the event on the server.  The 'edit' link returned in this event can
    be used for future updates.  Due to the use of the 'optimistic concurrency'
    method of version control, most GData services do not allow you to send 
    multiple update requests using the same edit URL.  Please see the docs:
    http://code.google.com/apis/gdata/reference.html#Optimistic-concurrency
    """

    previous_title = event.title.text
    event.title.text = new_title
    print 'Updating title of event from:\'%s\' to:\'%s\'' % (
        previous_title, event.title.text,) 
    return self.cal_client.UpdateEvent(event.GetEditLink().href, event)

  def _AddReminder(self, event, minutes=10):
    """Adds a reminder to the event.  This uses the default reminder settings
    for the user to determine what type of notifications are sent (email, sms,
    popup, etc.) and sets the reminder for 'minutes' number of minutes before
    the event.  Note: you can only use values for minutes as specified in the
    Calendar GUI."""

    for a_when in event.when:
      if len(a_when.reminder) > 0:
        a_when.reminder[0].minutes = minutes
      else:
        a_when.reminder.append(gcalendar.Reminder(minutes=minutes))

    print 'Adding %d minute reminder to event' % (minutes,)
    return self.cal_client.UpdateEvent(event.GetEditLink().href, event)

  def _AddExtendedProperty(self, event, 
      name='http://www.example.com/schemas/2005#mycal.id', value='1234'):
    """Adds an arbitrary name/value pair to the event.  This value is only
    exposed through the API.  Extended properties can be used to store extra
    information needed by your application.  The recommended format is used as
    the default arguments above.  The use of the URL format is to specify a 
    namespace prefix to avoid collisions between different applications."""

    event.extended_property.append(
        gcalendar.ExtendedProperty(name=name, value=value))  
    print 'Adding extended property to event: \'%s\'=\'%s\'' % (name, value,)
    return self.cal_client.UpdateEvent(event.GetEditLink().href, event)

  def _DeleteEvent(self, event):
    """Given an event object returned for the calendar server, this method
    deletes the event.  The edit link present in the event is the URL used
    in the HTTP DELETE request."""

    self.cal_client.DeleteEvent(event.GetEditLink().href)
    
  def Run(self, delete='false'):
    """Runs each of the example methods defined above.  Note how the result
    of the _InsertSingleEvent call is used for updating the title and the
    result of updating the title is used for inserting the reminder and 
    again with the insertion of the extended property.  This is due to the
    Calendar's use of GData's optimistic concurrency versioning control system:
    http://code.google.com/apis/gdata/reference.html#Optimistic-concurrency
    """

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

    # Delete entries if delete argument='true'
    if delete == 'true':
      print 'Deleting created events'
      self.cal_client.DeleteEvent(see_u_ext_prop.GetEditLink().href)
      self.cal_client.DeleteEvent(ree.GetEditLink().href)
    
 
def main():
  """Runs the CalendarExample application with the provided username and
  and password values.  Authentication credentials are required.  
  NOTE: It is recommended that you run this sample using a test account."""

  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["user=", "pw=", "delete="])
  except getopt.error, msg:
    print ('python calendarExample.py --user [username] --pw [password] ' + 
        '--delete [true|false] ')
    sys.exit(2)

  user = ''
  pw = ''
  delete = 'false'

  # Process options
  for o, a in opts:
    if o == "--user":
      user = a
    elif o == "--pw":
      pw = a
    elif o == "--delete":
      delete = a

  if user == '' or pw == '':
    print ('python calendarExample.py --user [username] --pw [password] ' + 
        '--delete [true|false] ')
    sys.exit(2)

  sample = CalendarExample(user, pw)
  sample.Run(delete)

if __name__ == '__main__':
  main()
