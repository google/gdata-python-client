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

"""Data model tests for the Provisioning API."""


__author__ = 'Shraddha Gupta <shraddhag@google.com>'


import unittest
import atom.core
from gdata import test_data
import gdata.apps.data
import gdata.test_config as conf


class UserEntryTest(unittest.TestCase):

  def setUp(self):
    self.entry = atom.core.parse(test_data.USER_ENTRY1,
        gdata.apps.data.UserEntry)
    self.feed = atom.core.parse(test_data.USER_FEED1,
        gdata.apps.data.UserFeed)

  def testUserEntryFromString(self):
    self.assert_(isinstance(self.entry,
        gdata.apps.data.UserEntry))
    self.assertEquals(self.entry.name.given_name, 'abcd33')
    self.assertEquals(self.entry.name.family_name, 'efgh3')
    self.assertEquals(self.entry.login.user_name, 'abcd12310')
    self.assertEquals(self.entry.login.suspended, 'false')
    self.assertEquals(self.entry.login.admin, 'false')
    self.assertEquals(self.entry.quota.limit, '25600')

  def testUserFeedFromString(self):
    self.assertEquals(len(self.feed.entry), 2)
    self.assert_(isinstance(self.feed, gdata.apps.data.UserFeed))
    self.assert_(isinstance(self.feed.entry[0], gdata.apps.data.UserEntry))
    self.assert_(isinstance(self.feed.entry[1], gdata.apps.data.UserEntry))
    self.assertEquals(self.feed.entry[0].find_edit_link(),
        ('https://apps-apis.google.com/a/feeds/srkapps.com/user/2.0/user8306'))
    self.assertEquals(self.feed.entry[0].name.given_name, 'FirstName8306')
    self.assertEquals(self.feed.entry[0].name.family_name, 'LastName8306')
    self.assertEquals(self.feed.entry[0].login.user_name, 'user8306')
    self.assertEquals(self.feed.entry[0].login.admin, 'false')
    self.assertEquals(self.feed.entry[0].login.suspended, 'false')
    self.assertEquals(self.feed.entry[0].login.change_password, 'false')
    self.assertEquals(self.feed.entry[0].login.ip_whitelisted, 'false')
    self.assertEquals(self.feed.entry[0].quota.limit, '25600')
    self.assertEquals(
        self.feed.entry[1].find_edit_link(),
        ('https://apps-apis.google.com/a/feeds/srkapps.com/user/2.0/user8307'))
    self.assertEquals(self.feed.entry[1].name.given_name, 'FirstName8307')
    self.assertEquals(self.feed.entry[1].name.family_name, 'LastName8307')
    self.assertEquals(self.feed.entry[1].login.user_name, 'user8307')
    self.assertEquals(self.feed.entry[1].login.admin, 'false')
    self.assertEquals(self.feed.entry[1].login.suspended, 'false')
    self.assertEquals(self.feed.entry[1].login.change_password, 'false')
    self.assertEquals(self.feed.entry[1].login.ip_whitelisted, 'false')
    self.assertEquals(self.feed.entry[1].quota.limit, '25600')


class NicknameEntryTest(unittest.TestCase):

  def setUp(self):
    self.entry = atom.core.parse(test_data.NICKNAME_ENTRY,
        gdata.apps.data.NicknameEntry)
    self.feed = atom.core.parse(test_data.NICKNAME_FEED,
        gdata.apps.data.NicknameFeed)

  def testNicknameEntryFromString(self):
    self.assert_(isinstance(self.entry,
        gdata.apps.data.NicknameEntry))
    self.assertEquals(self.entry.nickname.name, 'nehag')
    self.assertEquals(self.entry.login.user_name, 'neha')

  def testNicknameFeedFromString(self):
    self.assertEquals(len(self.feed.entry), 2)
    self.assert_(isinstance(self.feed,
        gdata.apps.data.NicknameFeed))
    self.assert_(isinstance(self.feed.entry[0],
        gdata.apps.data.NicknameEntry))
    self.assert_(isinstance(self.feed.entry[1],
        gdata.apps.data.NicknameEntry))
    self.assertEquals(
        self.feed.entry[0].find_edit_link(),
        ('https://apps-apis.google.com/a/feeds/srkapps.net/'
         'nickname/2.0/nehag'))
    self.assertEquals(self.feed.entry[0].nickname.name, 'nehag')
    self.assertEquals(self.feed.entry[0].login.user_name, 'neha')
    self.assertEquals(
        self.feed.entry[1].find_edit_link(),
        ('https://apps-apis.google.com/a/feeds/srkapps.net/'
         'nickname/2.0/richag'))
    self.assertEquals(self.feed.entry[1].nickname.name, 'richag')
    self.assertEquals(self.feed.entry[1].login.user_name, 'richa')


def suite():
  return conf.build_suite([UserEntryTest, NicknameEntryTest])


if __name__ == '__main__':
  unittest.main()
