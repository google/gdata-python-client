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

__author__ = 'api.rboyd@google.com (Ryan Boyd)'

import unittest
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import atom
import gcalendar
import gcalendar_service
import random
import getpass

# Commented out as dateutil is not in this repository
#from dateutil.parser import parse


username = ''
password = ''


class CalendarServiceUnitTest(unittest.TestCase):
  
  def setUp(self):
    self.cal_client = gcalendar_service.CalendarService()
    self.cal_client.email = username 
    self.cal_client.password = password
    self.cal_client.source = 'GCalendarClient "Unit" Tests'

  def tearDown(self):
    # No teardown needed
    pass  

  def testPostAndDeleteExtendedPropertyEvent(self):
    """Test posting a new entry with an extended property, deleting it"""
    # Get random data for creating event
    r = random.Random()
    r.seed()
    random_event_number = str(r.randint(100000,1000000))
    random_event_title = 'My Random Extended Property Test Event %s' % ( 
        random_event_number)

    # Set event data 
    event = gcalendar.CalendarEventEntry()
    event.author.append(atom.Author(name=atom.Name(text='GData Test user')))
    event.title = atom.Title(text=random_event_title)
    event.content = atom.Content(text='Picnic with some lunch')
    event.extended_property.append(gcalendar.ExtendedProperty(
        name='prop test name', value='prop test value'))

    # Insert event 
    self.cal_client.ProgrammaticLogin()
    new_event = self.cal_client.InsertEvent(event, 
        '/calendar/feeds/default/private/full')

    self.assertEquals(event.extended_property[0].value,
        new_event.extended_property[0].value)

    # Delete the event
    self.cal_client.DeleteEvent(new_event.GetEditLink().href)

  # WARNING: Due to server-side issues, this test takes a while (~60seconds)
  def testPostEntryWithCommentAndDelete(self):
    """Test posting a new entry with an extended property, deleting it"""
    # Get random data for creating event
    r = random.Random()
    r.seed()
    random_event_number = str(r.randint(100000,1000000))
    random_event_title = 'My Random Comments Test Event %s' % (
        random_event_number)

    # Set event data
    event = gcalendar.CalendarEventEntry()
    event.author.append(atom.Author(name=atom.Name(text='GData Test user')))
    event.title = atom.Title(text=random_event_title)
    event.content = atom.Content(text='Picnic with some lunch')

    # Insert event
    self.cal_client.ProgrammaticLogin()
    new_event = self.cal_client.InsertEvent(event,
        '/calendar/feeds/default/private/full')

    # Get comments feed
    comments_url = new_event.comments.feed_link.href
    comments_query = gcalendar_service.CalendarEventCommentQuery(comments_url)
    comments_feed = self.cal_client.CalendarQuery(comments_query)

    # Add comment
    comments_entry = gcalendar.CalendarEventCommentEntry()
    comments_entry.content = atom.Content(text='Comments content')
    comments_entry.author.append(
        atom.Author(name=atom.Name(text='GData Test user'),
            email=atom.Email(text='gdata.ops.demo@gmail.com')))
    new_comments_entry = self.cal_client.InsertEventComment(comments_entry,
        comments_feed.GetPostLink().href)
  
    # Delete the event
    event_to_delete = self.cal_client.GetCalendarEventEntry(new_event.id.text)
    self.cal_client.DeleteEvent(event_to_delete.GetEditLink().href)

  def testPostQueryUpdateAndDeleteEvents(self):
    """Test posting a new entry, updating it, deleting it, querying for it"""

    # Get random data for creating event
    r = random.Random()
    r.seed()
    random_event_number = str(r.randint(100000,1000000))
    random_event_title = 'My Random Test Event %s' % random_event_number
        
    random_start_hour = (r.randint(1,1000000) % 23)
    random_end_hour = random_start_hour + 1
    non_random_start_minute = 0
    non_random_end_minute = 0
    random_month = (r.randint(1,1000000) % 12 + 1)
    random_day_of_month = (r.randint(1,1000000) % 28 + 1)
    non_random_year = 2008
    start_time = '%04d-%02d-%02dT%02d:%02d:00.000-05:00' % (
        non_random_year, random_month, random_day_of_month,
        random_start_hour, non_random_start_minute,)
    end_time = '%04d-%02d-%02dT%02d:%02d:00.000-05:00' % (
        non_random_year, random_month, random_day_of_month,
        random_end_hour, non_random_end_minute,)

    # Set event data 
    event = gcalendar.CalendarEventEntry()
    event.author.append(atom.Author(name=atom.Name(text='GData Test user')))
    event.title = atom.Title(text=random_event_title)
    event.content = atom.Content(text='Picnic with some lunch')
    event.where.append(gcalendar.Where(value_string='Down by the river'))
    event.when.append(gcalendar.When(start_time=start_time,end_time=end_time))

    # Insert event 
    self.cal_client.ProgrammaticLogin()
    new_event = self.cal_client.InsertEvent(event, 
        '/calendar/feeds/default/private/full')

    # Ensure that atom data returned from calendar server equals atom data sent 
    self.assertEquals(event.title.text, new_event.title.text)
    self.assertEquals(event.content.text, new_event.content.text)

    # Ensure that gd:where data returned from calendar equals value sent
    self.assertEquals(event.where[0].value_string,
        new_event.where[0].value_string)

    # Commented out as dateutil is not in this repository
    # Ensure that dates returned from calendar server equals dates sent 
    #start_time_py = parse(event.when[0].start_time)
    #start_time_py_new = parse(new_event.when[0].start_time)
    #self.assertEquals(start_time_py, start_time_py_new)

    #end_time_py = parse(event.when[0].end_time)
    #end_time_py_new = parse(new_event.when[0].end_time)
    #self.assertEquals(end_time_py, end_time_py_new)

    # Update event
    event_to_update = new_event
    updated_title_text = event_to_update.title.text + ' - UPDATED'
    event_to_update.title = atom.Title(text=updated_title_text)

    updated_event = self.cal_client.UpdateEvent(
        event_to_update.GetEditLink().href, event_to_update)

    # Ensure that updated title was set in the updated event
    self.assertEquals(event_to_update.title.text, updated_event.title.text)

    # Delete the event
    self.cal_client.DeleteEvent(updated_event.GetEditLink().href)

    # Ensure deleted event is marked as canceled in the feed
    after_delete_query = gcalendar_service.CalendarEventQuery()
    after_delete_query.updated_min = '2007-01-01'
    after_delete_query.text_query = str(random_event_number) 
    after_delete_query.max_results = '1'
    after_delete_query_result = self.cal_client.CalendarQuery(
        after_delete_query)

    # Ensure feed returned at max after_delete_query.max_results events 
    self.assert_(
        len(after_delete_query_result.entry) <= after_delete_query.max_results)

    # Ensure status of returned event is canceled
    self.assertEquals(after_delete_query_result.entry[0].event_status.value,
        'CANCELED')


class CalendarEventQueryUnitTest(unittest.TestCase):

  def setUp(self):
    self.query = gcalendar_service.CalendarEventQuery()

  def testOrderByValidatesValues(self):
    self.query.orderby = 'lastmodified'
    self.assertEquals(self.query.orderby, 'lastmodified')
    try:
      self.query.orderby = 'illegal input'
      self.fail()
    except gcalendar_service.Error:
      self.assertEquals(self.query.orderby, 'lastmodified')
      
  def testSortOrderValidatesValues(self):
    self.query.sortorder = 'a'
    self.assertEquals(self.query.sortorder, 'a')
    try:
      self.query.sortorder = 'illegal input'
      self.fail()
    except gcalendar_service.Error:
      self.assertEquals(self.query.sortorder, 'a')


if __name__ == '__main__':
  print ('NOTE: Please run these tests only with a test account. ' +
      'The tests may delete or update your data.')
  username = raw_input('Please enter your username: ')
  password = getpass.getpass()
  unittest.main()
