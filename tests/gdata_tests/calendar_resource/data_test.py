#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
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


__author__ = 'Vic Fryzel <vf@google.com>'


import unittest
import atom.core
from gdata import test_data
import gdata.calendar_resource.data
import gdata.test_config as conf                                                                                   


class CalendarResourceEntryTest(unittest.TestCase):

  def setUp(self):
    self.entry = atom.core.parse(test_data.CALENDAR_RESOURCE_ENTRY,
        gdata.calendar_resource.data.CalendarResourceEntry)
    self.feed = atom.core.parse(test_data.CALENDAR_RESOURCES_FEED,
        gdata.calendar_resource.data.CalendarResourceFeed)

  def testCalendarResourceEntryFromString(self):
    self.assert_(isinstance(self.entry,
        gdata.calendar_resource.data.CalendarResourceEntry))
    self.assertEquals(self.entry.resource_id, 'CR-NYC-14-12-BR')
    self.assertEquals(self.entry.resource_common_name, 'Boardroom')
    self.assertEquals(self.entry.resource_description,
        ('This conference room is in New York City, building 14, floor 12, '
         'Boardroom'))
    self.assertEquals(self.entry.resource_type, 'CR')

  def testCalendarResourceFeedFromString(self):
    self.assertEquals(len(self.feed.entry), 2)
    self.assert_(isinstance(self.feed,
        gdata.calendar_resource.data.CalendarResourceFeed))
    self.assert_(isinstance(self.feed.entry[0],
        gdata.calendar_resource.data.CalendarResourceEntry))
    self.assert_(isinstance(self.feed.entry[1],
        gdata.calendar_resource.data.CalendarResourceEntry))
    self.assertEquals(self.feed.entry[0].resource_id, 'CR-NYC-14-12-BR')
    self.assertEquals(self.feed.entry[0].resource_common_name, 'Boardroom')
    self.assertEquals(self.feed.entry[0].resource_description,
        ('This conference room is in New York City, building 14, floor 12, '
         'Boardroom'))
    self.assertEquals(self.feed.entry[0].resource_type, 'CR')
    self.assertEquals(self.feed.entry[1].resource_id,
        '(Bike)-London-43-Lobby-Bike-1')
    self.assertEquals(self.feed.entry[1].resource_common_name, 'London bike-1')
    self.assertEquals(self.feed.entry[1].resource_description,
        'Bike is in London at building 43\'s lobby.')
    self.assertEquals(self.feed.entry[1].resource_type, '(Bike)')


def suite():
  return conf.build_suite([CalendarResourceEntryTest])


if __name__ == '__main__':
  unittest.main()
