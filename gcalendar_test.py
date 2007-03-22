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


__author__ = 'api.jscudder@gmail.com (Jeff Scudder)'


import unittest
from elementtree import ElementTree
import atom 
import gdata
import test_data
import gcalendar


class CalendarFeedTest(unittest.TestCase):
  
  def setUp(self):
    self.calendar_feed = gcalendar.CalendarFeedFromString(test_data.CALENDAR_FEED)

  def testEntryCount(self):
    # Assert the number of items in the feed of calendars
    self.assertEquals(len(self.calendar_feed.entry),2)

  def testToAndFromString(self):
    # Assert the appropriate type for each entry
    for an_entry in self.calendar_feed.entry:
      self.assert_(isinstance(an_entry, gcalendar.CalendarEntry), 
          'Entry must be an instance of CalendarEntry')

    # Regenerate feed from xml text
    new_calendar_feed = gcalendar.CalendarFeedFromString(str(self.calendar_feed))
    for an_entry in new_calendar_feed.entry:
      self.assert_(isinstance(an_entry, gcalendar.CalendarEntry), 
          'Entry in regenerated feed must be an instance of CalendarEntry')

  def testAuthor(self):
    """Tests the existence of a <atom:author> and verifies the name and email"""

    # Assert that each element in the feed author list is an atom.Author
    for an_author in self.calendar_feed.author:
      self.assert_(isinstance(an_author, atom.Author), 
          "Calendar feed <atom:author> element must be an instance of atom.Author: %s" % an_author)

    # Assert the feed author name is as expected
    self.assertEquals(self.calendar_feed.author[0].name.text, 'GData Ops Demo')

    # Assert the feed author name is as expected
    self.assertEquals(self.calendar_feed.author[0].email.text, 'gdata.ops.demo@gmail.com')

    # Assert one of the values for an entry author
    self.assertEquals(self.calendar_feed.entry[0].author[0].name.text, 'GData Ops Demo')
    self.assertEquals(self.calendar_feed.entry[0].author[0].email.text, 'gdata.ops.demo@gmail.com')

  def testId(self):
    """Tests the existence of a <atom:id> in the feed and entries and verifies the value"""

    # Assert the feed id exists and is an atom.Id
    self.assert_(isinstance(self.calendar_feed.id, atom.Id), 
        "Calendar feed <atom:id> element must be an instance of atom.Id: %s" % self.calendar_feed.id)

    # Assert the feed id value is as expected 
    self.assertEquals(self.calendar_feed.id.text, 'http://www.google.com/calendar/feeds/default')

    # Assert that each entry has an id which is an atom.Id
    for an_entry in self.calendar_feed.entry:
      self.assert_(isinstance(an_entry.id, atom.Id),
          "Calendar entry <atom:id> element must be an instance of atom.Id: %s" % an_entry.id)

    # Assert one of the values for an id
    self.assertEquals(self.calendar_feed.entry[1].id.text, 'http://www.google.com/calendar/feeds/default/jnh21ovnjgfph21h32gvms2758%40group.calendar.google.com')

  def testPublished(self):
    """Tests the existence of a <atom:published> in the entries and verifies the value"""

    # Assert that each entry has a published value which is an atom.Published
    for an_entry in self.calendar_feed.entry:
      self.assert_(isinstance(an_entry.published, atom.Published),
          "Calendar entry <atom:published> element must be an instance of atom.Published: %s" % an_entry.published)

    # Assert one of the values for published is as expected
    self.assertEquals(self.calendar_feed.entry[1].published.text, '2007-03-20T22:48:57.837Z')

  def testUpdated(self):
    """Tests the existence of a <atom:updated> in the feed and the entries and verifies the value"""

    # Assert that the feed updated element exists and is an atom.Updated
    self.assert_(isinstance(self.calendar_feed.updated, atom.Updated), 
        "Calendar feed <atom:updated> element must be an instance of atom.Updated: %s" % self.calendar_feed.updated)

    # Assert that each entry has a updated value which is an atom.Updated
    for an_entry in self.calendar_feed.entry:
      self.assert_(isinstance(an_entry.updated, atom.Updated),
          "Calendar entry <atom:updated> element must be an instance of atom.Updated: %s" % an_entry.updated)

    # Assert the feed updated value is as expected
    self.assertEquals(self.calendar_feed.updated.text, '2007-03-20T22:48:57.833Z')

    # Assert one of the values for updated
    self.assertEquals(self.calendar_feed.entry[0].updated.text, '2007-03-20T22:48:52.000Z')

  def testTitle(self):
    """Tests the existence of a <atom:title> in the feed and the entries and verifies the value"""

    # Assert that the feed title element exists and is an atom.Title
    self.assert_(isinstance(self.calendar_feed.title, atom.Title), 
        "Calendar feed <atom:title> element must be an instance of atom.Title: %s" % self.calendar_feed.title)

    # Assert that each entry has a title value which is an atom.Title
    for an_entry in self.calendar_feed.entry:
      self.assert_(isinstance(an_entry.title, atom.Title),
          "Calendar entry <atom:title> element must be an instance of atom.Title: %s" % an_entry.title)

    # Assert the feed title value is as expected
    self.assertEquals(self.calendar_feed.title.text, 'GData Ops Demo\'s Calendar List')

    # Assert one of the values for title 
    self.assertEquals(self.calendar_feed.entry[0].title.text, 'GData Ops Demo')

  def testColor(self):
    """Tests the existence of a <gCal:color> and verifies the value"""
    
    # Assert the color is present and is a gcalendar.Color
    for an_entry in self.calendar_feed.entry:
      self.assert_(isinstance(an_entry.color, gcalendar.Color), 
          "Calendar feed <gCal:color> element must be an instance of gcalendar.Color: %s" % an_entry.color)

    # Assert the color value is as expected
    self.assertEquals(self.calendar_feed.entry[0].color.value, '#2952A3')

  def testAccessLevel(self):
    """Tests the existence of a <gCal:accesslevel> element and verifies the
     value"""

    # Assert the access_level is present and is a gcalendar.AccessLevel
    for an_entry in self.calendar_feed.entry:
      self.assert_(isinstance(an_entry.access_level, gcalendar.AccessLevel), 
          "Calendar feed <gCal:accesslevel> element must be an instance of gcalendar.AccessLevel: %s" % an_entry.access_level)

    # Assert the access_level value is as expected
    self.assertEquals(self.calendar_feed.entry[0].access_level.value, 'owner')

  def testTimezone(self):
    """Tests the existence of a <gCal:timezone> element and verifies the
     value"""

    # Assert the timezone is present and is a gcalendar.Timezone
    for an_entry in self.calendar_feed.entry:
      self.assert_(isinstance(an_entry.timezone, gcalendar.Timezone), 
          "Calendar feed <gCal:timezone> element must be an instance of gcalendar.Timezone: %s" % an_entry.timezone)

    # Assert the timezone value is as expected
    self.assertEquals(self.calendar_feed.entry[0].timezone.value, 'America/Los_Angeles')

  def testHidden(self):
    """Tests the existence of a <gCal:hidden> element and verifies the
     value"""

    # Assert the hidden is present and is a gcalendar.Hidden
    for an_entry in self.calendar_feed.entry:
      self.assert_(isinstance(an_entry.hidden, gcalendar.Hidden), 
          "Calendar feed <gCal:hidden> element must be an instance of gcalendar.Hidden: %s" % an_entry.hidden)

    # Assert the hidden value is as expected
    self.assertEquals(self.calendar_feed.entry[0].hidden.value, 'false')

  def testOpenSearch(self):
    """Tests the existence of <openSearch:startIndex>"""
    # Assert that the elements exist and are the appropriate type
    self.assert_(isinstance(self.calendar_feed.start_index, gdata.StartIndex),
          "Calendar feed <openSearch:startIndex> element must be an instance of gdata.StartIndex: %s" % self.calendar_feed.start_index)

    # Assert the values for each openSearch element are as expected
    self.assertEquals(self.calendar_feed.start_index.text, '1')

  def testGenerator(self):
    """Tests the existence of <atom:generator> and verifies the value"""
    # Assert that the element exists and is of the appropriate type
    self.assert_(isinstance(self.calendar_feed.generator, atom.Generator),
          "Calendar feed <atom:generator> element must be an instance of atom.Generator: %s" % self.calendar_feed.generator)

    # Assert the generator version, uri and text are as expected
    self.assertEquals(self.calendar_feed.generator.text, 'Google Calendar')
    self.assertEquals(self.calendar_feed.generator.version, '1.0')
    self.assertEquals(self.calendar_feed.generator.uri, 'http://www.google.com/calendar')


class CalendarFeedTestRegenerated(CalendarFeedTest):
  def setUp(self):    
    old_calendar_feed = gcalendar.CalendarFeedFromString(test_data.CALENDAR_FEED)
    self.calendar_feed = gcalendar.CalendarFeedFromString(str(old_calendar_feed))

class CalendarEventFeedTest(unittest.TestCase):
  
  def setUp(self):
    self.calendar_event_feed = gcalendar.CalendarEventFeedFromString(test_data.CALENDAR_FULL_EVENT_FEED)

  def testEntryCount(self):
    # Assert the number of items in the feed of events
    self.assertEquals(len(self.calendar_event_feed.entry),10)

  def testToAndFromString(self):
    # Assert the appropriate type for each entry
    for an_entry in self.calendar_event_feed.entry:
      self.assert_(isinstance(an_entry, gcalendar.CalendarEventEntry), "Entry must be an instance of a CalendarEventEntry")

    # Regenerate feed from xml text
    new_calendar_event_feed = gcalendar.CalendarEventFeedFromString(str(self.calendar_event_feed))
    for an_entry in new_calendar_event_feed.entry:
      self.assert_(isinstance(an_entry, gcalendar.CalendarEventEntry), "Entry in regenerated feed must be an instance of CalendarEventEntry")

  def testAuthor(self):
    """Tests the existence of a <atom:author> and verifies the name and email"""

    # Assert that each element in the feed author list is an atom.Author
    for an_author in self.calendar_event_feed.author:
      self.assert_(isinstance(an_author, atom.Author), 
          "Calendar event feed <atom:author> element must be an instance of atom.Author: %s" % an_author)

    # Assert the feed author name is as expected
    self.assertEquals(self.calendar_event_feed.author[0].name.text, 'GData Ops Demo')

    # Assert the feed author name is as expected
    self.assertEquals(self.calendar_event_feed.author[0].email.text, 'gdata.ops.demo@gmail.com')

    # Assert one of the values for an entry author
    self.assertEquals(self.calendar_event_feed.entry[0].author[0].name.text, 'GData Ops Demo')
    self.assertEquals(self.calendar_event_feed.entry[0].author[0].email.text, 'gdata.ops.demo@gmail.com')

  def testId(self):
    """Tests the existence of a <atom:id> in the feed and entries and verifies the value"""

    # Assert the feed id exists and is an atom.Id
    self.assert_(isinstance(self.calendar_event_feed.id, atom.Id), 
        "Calendar event feed <atom:id> element must be an instance of atom.Id: %s" % self.calendar_event_feed.id)

    # Assert the feed id value is as expected 
    self.assertEquals(self.calendar_event_feed.id.text, 'http://www.google.com/calendar/feeds/default/private/full')

    # Assert that each entry has an id which is an atom.Id
    for an_entry in self.calendar_event_feed.entry:
      self.assert_(isinstance(an_entry.id, atom.Id),
          "Calendar event entry <atom:id> element must be an instance of atom.Id: %s" % an_entry.id)

    # Assert one of the values for an id
    self.assertEquals(self.calendar_event_feed.entry[1].id.text, 'http://www.google.com/calendar/feeds/default/private/full/2qt3ao5hbaq7m9igr5ak9esjo0')

  def testPublished(self):
    """Tests the existence of a <atom:published> in the entries and verifies the value"""

    # Assert that each entry has a published value which is an atom.Published
    for an_entry in self.calendar_event_feed.entry:
      self.assert_(isinstance(an_entry.published, atom.Published),
          "Calendar event entry <atom:published> element must be an instance of atom.Published: %s" % an_entry.published)

    # Assert one of the values for published is as expected
    self.assertEquals(self.calendar_event_feed.entry[1].published.text, '2007-03-20T21:26:04.000Z')

  def testUpdated(self):
    """Tests the existence of a <atom:updated> in the feed and the entries and verifies the value"""

    # Assert that the feed updated element exists and is an atom.Updated
    self.assert_(isinstance(self.calendar_event_feed.updated, atom.Updated), 
        "Calendar feed <atom:updated> element must be an instance of atom.Updated: %s" % self.calendar_event_feed.updated)

    # Assert that each entry has a updated value which is an atom.Updated
    for an_entry in self.calendar_event_feed.entry:
      self.assert_(isinstance(an_entry.updated, atom.Updated),
          "Calendar event entry <atom:updated> element must be an instance of atom.Updated: %s" % an_entry.updated)

    # Assert the feed updated value is as expected
    self.assertEquals(self.calendar_event_feed.updated.text, '2007-03-20T21:29:57.000Z')

    # Assert one of the values for updated
    self.assertEquals(self.calendar_event_feed.entry[3].updated.text, '2007-03-20T21:25:46.000Z')

  def testTitle(self):
    """Tests the existence of a <atom:title> in the feed and the entries and verifies the value"""

    # Assert that the feed title element exists and is an atom.Title
    self.assert_(isinstance(self.calendar_event_feed.title, atom.Title), 
        "Calendar feed <atom:title> element must be an instance of atom.Title: %s" % self.calendar_event_feed.title)

    # Assert that each entry has a title value which is an atom.Title
    for an_entry in self.calendar_event_feed.entry:
      self.assert_(isinstance(an_entry.title, atom.Title),
          "Calendar event entry <atom:title> element must be an instance of atom.Title: %s" % an_entry.title)

    # Assert the feed title value is as expected
    self.assertEquals(self.calendar_event_feed.title.text, 'GData Ops Demo')

    # Assert one of the values for title 
    self.assertEquals(self.calendar_event_feed.entry[0].title.text, 'test deleted')

  def testPostLink(self):
    """Tests the existence of a <atom:link> with a rel='...#post' and verifies the value"""

    # Assert that each link in the feed is an atom.Link
    for a_link in self.calendar_event_feed.link:
      self.assert_(isinstance(a_link, atom.Link),
          "Calendar event entry <atom:link> element must be an instance of atom.Link: %s" % a_link)

    # Assert post link exists
    self.assert_(self.calendar_event_feed.GetPostLink() is not None)

    # Assert the post link value is as expected
    self.assertEquals(self.calendar_event_feed.GetPostLink().href, 'http://www.google.com/calendar/feeds/default/private/full')

  def testOpenSearch(self):
    """Tests the existence of <openSearch:totalResults>, <openSearch:startIndex>, <openSearch:itemsPerPage>"""
    # Assert that the elements exist and are the appropriate type
    self.assert_(isinstance(self.calendar_event_feed.total_results, gdata.TotalResults),
          "Calendar event feed <openSearch:totalResults> element must be an instance of gdata.TotalResults: %s" % self.calendar_event_feed.total_results)
    self.assert_(isinstance(self.calendar_event_feed.start_index, gdata.StartIndex),
          "Calendar event feed <openSearch:startIndex> element must be an instance of gdata.StartIndex: %s" % self.calendar_event_feed.start_index)
    self.assert_(isinstance(self.calendar_event_feed.items_per_page, gdata.ItemsPerPage),
          "Calendar event feed <openSearch:itemsPerPage> element must be an instance of gdata.ItemsPerPage: %s" % self.calendar_event_feed.items_per_page)

    # Assert the values for each openSearch element are as expected
    self.assertEquals(self.calendar_event_feed.total_results.text, '10')
    self.assertEquals(self.calendar_event_feed.start_index.text, '1')
    self.assertEquals(self.calendar_event_feed.items_per_page.text, '25')

  def testGenerator(self):
    """Tests the existence of <atom:generator> and verifies the value"""
    # Assert that the element exists and is of the appropriate type
    self.assert_(isinstance(self.calendar_event_feed.generator, atom.Generator),
          "Calendar event feed <atom:generator> element must be an instance of atom.Generator: %s" % self.calendar_event_feed.generator)

    # Assert the generator version, uri and text are as expected
    self.assertEquals(self.calendar_event_feed.generator.text, 'Google Calendar')
    self.assertEquals(self.calendar_event_feed.generator.version, '1.0')
    self.assertEquals(self.calendar_event_feed.generator.uri, 'http://www.google.com/calendar')

  def testCategory(self):
    """Tests the existence of <atom:category> and verifies the value"""
    # Assert that the element exists and is of the appropriate type and value
    for a_category in self.calendar_event_feed.category:
      self.assert_(isinstance(a_category, atom.Category),
          "Calendar event feed <atom:category> element must be an instance of atom.Category: %s" % a_category)
      self.assertEquals(a_category.scheme, 'http://schemas.google.com/g/2005#kind')
      self.assertEquals(a_category.term, 'http://schemas.google.com/g/2005#event')

    for an_event in self.calendar_event_feed.entry:
      for a_category in an_event.category:
        self.assert_(isinstance(a_category, atom.Category),
            "Calendar event feed entry <atom:category> element must be an instance of atom.Category: %s" % a_category)
        self.assertEquals(a_category.scheme, 'http://schemas.google.com/g/2005#kind')
        self.assertEquals(a_category.term, 'http://schemas.google.com/g/2005#event')


  def testSendEventNotifications(self):
    """Test the existence of <gCal:sendEventNotifications> 
    and verifies the value"""
    # Assert that the element exists and is of the appropriate type and value
    for an_event in self.calendar_event_feed.entry:
      self.assert_(isinstance(an_event.send_event_notifications, 
          gcalendar.SendEventNotifications),
          ("Calendar event feed entry <gCal:sendEventNotifications> element " +
          "must be an instance of gcalendar.SendEventNotifications: %s") % (
          an_event.send_event_notifications,))
   
    # Assert the <gCal:sendEventNotifications> are as expected 
    self.assertEquals(
        self.calendar_event_feed.entry[0].send_event_notifications.value,
        'false')

    self.assertEquals(
        self.calendar_event_feed.entry[2].send_event_notifications.value,
        'true')

  def testEventStatus(self):
    """Test the existence of <gd:eventStatus> 
    and verifies the value"""
    # Assert that the element exists and is of the appropriate type and value
    for an_event in self.calendar_event_feed.entry:
      self.assert_(isinstance(an_event.event_status, 
          gcalendar.EventStatus),
          ("Calendar event feed entry <gd:eventStatus> element " +
          "must be an instance of gcalendar.EventStatus: %s") % (
          an_event.event_status,))
   
    # Assert the <gd:eventStatus> are as expected 
    self.assertEquals(
        self.calendar_event_feed.entry[0].event_status.value,
        'CANCELED')

    self.assertEquals(
        self.calendar_event_feed.entry[1].event_status.value,
        'CONFIRMED')


#class GBaseItemTest(unittest.TestCase):
#
#  def setUp(self):
#    self.item = gbase.GBaseItem()
#    
#  def testToAndFromString(self):
#    self.item.label.append(gbase.Label(text='my label'))
#    self.assert_(self.item.label[0].text == 'my label')
#    self.item.item_type = gbase.ItemType(text='products')
#    self.assert_(self.item.item_type.text == 'products')
#    new_item = gbase.GBaseItemFromString(self.item.ToString())
#    self.assert_(self.item.label[0].text == new_item.label[0].text)
#    self.assert_(self.item.item_type.text == new_item.item_type.text)
#
#
#class GBaseItemFeedTest(unittest.TestCase):
#
#  def setUp(self):
#    #self.item_feed = gbase.GBaseItemFeed()
#    self.item_feed = gbase.GBaseItemFeedFromString(test_data.GBASE_FEED)
#
#  def testToAndFromString(self):
#    self.assert_(len(self.item_feed.entry) == 3)
#    for an_entry in self.item_feed.entry:
#      self.assert_(isinstance(an_entry, gbase.GBaseItem))
#    new_item_feed = gbase.GBaseItemFeedFromString(str(self.item_feed))
#    for an_entry in new_item_feed.entry:
#      self.assert_(isinstance(an_entry, gbase.GBaseItem))
#    
#  def testLinkFinderFindsHtmlLink(self):
#    for entry in self.item_feed.entry:
#      # All Base entries should have a self link
#      self.assert_(entry.GetSelfLink() is not None)
#      # All Base items should have an HTML link
#      self.assert_(entry.GetHtmlLink() is not None)
#      # None of the Base items should have an edit link
#      self.assert_(entry.GetEditLink() is None)
#
#
#class GBaseSnippetFeedTest(unittest.TestCase):
#
#  def setUp(self):
#    #self.item_feed = gbase.GBaseItemFeed()
#    self.snippet_feed = gbase.GBaseSnippetFeedFromString(test_data.GBASE_FEED)
#
#  def testToAndFromString(self):
#    self.assert_(len(self.snippet_feed.entry) == 3)
#    for an_entry in self.snippet_feed.entry:
#      self.assert_(isinstance(an_entry, gbase.GBaseSnippet))
#    new_snippet_feed = gbase.GBaseItemFeedFromString(str(self.snippet_feed))
#    for an_entry in new_snippet_feed.entry:
#      self.assert_(isinstance(an_entry, gbase.GBaseSnippet))
#    
    
if __name__ == '__main__':
  unittest.main()
