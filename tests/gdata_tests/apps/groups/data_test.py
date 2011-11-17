#!/usr/bin/python2.4
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Data model tests for the Groups Provisioning API."""


__author__ = 'Shraddha gupta <shraddhag@google.com>'


import unittest
import atom.core
from gdata import test_data
import gdata.apps.groups.data
import gdata.test_config as conf


class GroupEntryTest(unittest.TestCase):

  def setUp(self):
    self.entry = atom.core.parse(test_data.GROUP_ENTRY,
        gdata.apps.groups.data.GroupEntry, 2)
    self.feed = atom.core.parse(test_data.GROUP_FEED,
        gdata.apps.groups.data.GroupFeed, 2)

  def testGroupEntryFromString(self):
    self.assert_(isinstance(self.entry,
        gdata.apps.groups.data.GroupEntry))
    self.assertEquals(self.entry.group_id, 'trial@srkapps.com')
    self.assertEquals(self.entry.group_name, 'Trial')
    self.assertEquals(self.entry.email_permission, 'Domain')
    self.assertEquals(self.entry.description, 'For try')

  def testGroupFeedFromString(self):
    self.assertEquals(len(self.feed.entry), 2)
    self.assert_(isinstance(self.feed,
        gdata.apps.groups.data.GroupFeed))
    self.assert_(isinstance(self.feed.entry[0],
        gdata.apps.groups.data.GroupEntry))
    self.assert_(isinstance(self.feed.entry[1],
        gdata.apps.groups.data.GroupEntry))
    self.assertEquals(
        self.feed.entry[0].find_edit_link(),
        ('http://apps-apis.google.com/a/feeds/group/2.0/srkapps.com/'
         'firstgroup%40srkapps.com'))
    self.assertEquals(self.feed.entry[0].group_id, 'firstgroup@srkapps.com')
    self.assertEquals(self.feed.entry[0].group_name, 'FirstGroup')
    self.assertEquals(self.feed.entry[0].email_permission, 'Domain')
    self.assertEquals(self.feed.entry[0].description, 'First group')
    self.assertEquals(
        self.feed.entry[1].find_edit_link(),
        ('http://apps-apis.google.com/a/feeds/group/2.0/srkapps.com/'
         'trial%40srkapps.com'))
    self.assertEquals(self.feed.entry[1].group_id, 'trial@srkapps.com')
    self.assertEquals(self.feed.entry[1].group_name, 'Trial')
    self.assertEquals(self.feed.entry[1].email_permission, 'Domain')
    self.assertEquals(self.feed.entry[1].description, 'For try')


class GroupMemberEntryTest(unittest.TestCase):

  def setUp(self):
    self.entry = atom.core.parse(test_data.GROUP_MEMBER_ENTRY,
        gdata.apps.groups.data.GroupMemberEntry)
    self.feed = atom.core.parse(test_data.GROUP_MEMBER_FEED,
        gdata.apps.groups.data.GroupMemberFeed)

  def testGroupMemberEntryFromString(self):
    self.assert_(isinstance(self.entry,
        gdata.apps.groups.data.GroupMemberEntry))
    self.assertEquals(self.entry.member_id, 'abcd12310@srkapps.com')
    self.assertEquals(self.entry.member_type, 'User')
    self.assertEquals(self.entry.direct_member, 'true')

  def testGroupMemberFeedFromString(self):
    self.assertEquals(len(self.feed.entry), 2)
    self.assert_(isinstance(self.feed,
        gdata.apps.groups.data.GroupMemberFeed))
    self.assert_(isinstance(self.feed.entry[0],
        gdata.apps.groups.data.GroupMemberEntry))
    self.assert_(isinstance(self.feed.entry[1],
        gdata.apps.groups.data.GroupMemberEntry))
    self.assertEquals(
        self.feed.entry[0].find_edit_link(),
        ('http://apps-apis.google.com/a/feeds/group/2.0/srkapps.com/trial/'
         'member/abcd12310%40srkapps.com'))
    self.assertEquals(self.feed.entry[0].member_id, 'abcd12310@srkapps.com')
    self.assertEquals(self.feed.entry[0].member_type, 'User')
    self.assertEquals(self.feed.entry[0].direct_member, 'true')
    self.assertEquals(
        self.feed.entry[1].find_edit_link(),
        ('http://apps-apis.google.com/a/feeds/group/2.0/srkapps.com/trial/'
         'member/neha.technocrat%40srkapps.com'))
    self.assertEquals(self.feed.entry[1].member_id,
        'neha.technocrat@srkapps.com')
    self.assertEquals(self.feed.entry[1].member_type, 'User')
    self.assertEquals(self.feed.entry[1].direct_member, 'true')


def suite():
  return conf.build_suite([GroupEntryTest, GroupMemberEntryTest])


if __name__ == '__main__':
  unittest.main()
