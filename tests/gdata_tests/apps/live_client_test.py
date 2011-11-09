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

"""Live client tests for the Provisioning API."""

# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


__author__ = 'Shraddha Gupta <shraddhag@google.com>'


import random
import unittest
import gdata.apps.client
import gdata.apps.data
import gdata.client
import gdata.data
import gdata.gauth
import gdata.test_config as conf

conf.options.register_option(conf.APPS_DOMAIN_OPTION)


class AppsClientTest(unittest.TestCase):

  def setUp(self):
    self.client = gdata.apps.client.AppsClient(
        domain='example.com')
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.apps.client.AppsClient(
          domain=conf.options.get_value('appsdomain'))
      if conf.options.get_value('ssl') == 'true':
        self.client.ssl = True
      conf.configure_client(self.client, 'AppsClientTest',
          self.client.auth_service, True)

  def tearDown(self):
    conf.close_client(self.client)

  def testClientConfiguration(self):
    self.assertEqual('apps-apis.google.com', self.client.host)
    self.assertEqual('2.0', self.client.api_version)
    self.assertEqual('apps', self.client.auth_service)
    self.assertEqual(
        ('https://apps-apis.google.com/a/feeds/user/',
         'https://apps-apis.google.com/a/feeds/policies/',
         'https://apps-apis.google.com/a/feeds/alias/',
         'https://apps-apis.google.com/a/feeds/groups/'),
        self.client.auth_scopes)
    if conf.options.get_value('runlive') == 'true':
      self.assertEqual(self.client.domain,
          conf.options.get_value('appsdomain'))
    else:
      self.assertEqual(self.client.domain, 'example.com')

  def testMakeUserProvisioningUri(self):
    self.assertEqual('/a/feeds/%s/user/2.0' % self.client.domain,
        self.client._userURL())

  def testMakeNicknameProvisioningUri(self):
    self.assertEqual('/a/feeds/%s/nickname/2.0' % self.client.domain,
        self.client._nicknameURL())

  def testCreateRetrieveUpdateDelete(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testCreateUpdateDelete')

    rnd_number = random.randrange(0, 100001)
    username = 'test_user%s' % (rnd_number)
    nickname = 'test_alias%s' % (rnd_number)

    new_entry = self.client.CreateUser(
        user_name=username, given_name='Elizabeth', family_name='Smith',
        password='password', admin='true')

    self.assert_(isinstance(new_entry,
        gdata.apps.data.UserEntry))
    self.assertEquals(new_entry.name.given_name, 'Elizabeth')
    self.assertEquals(new_entry.name.family_name, 'Smith')
    self.assertEquals(new_entry.login.user_name, username)
    self.assertEquals(new_entry.login.admin, 'true')

    fetched_entry = self.client.RetrieveUser(user_name=username)
    self.assertEquals(fetched_entry.name.given_name, 'Elizabeth')
    self.assertEquals(fetched_entry.name.family_name, 'Smith')
    self.assertEquals(fetched_entry.login.user_name, username)
    self.assertEquals(fetched_entry.login.admin, 'true')

    new_entry.name.given_name = 'Joe'
    new_entry.name.family_name = 'Brown'
    updated_entry = self.client.UpdateUser(
        user_name=username, user_entry=new_entry)
    self.assert_(isinstance(updated_entry,
        gdata.apps.data.UserEntry))
    self.assertEqual(updated_entry.name.given_name, 'Joe')
    self.assertEqual(updated_entry.name.family_name, 'Brown')

    new_nickname = self.client.CreateNickname(user_name=username,
        nickname=nickname)
    self.assert_(isinstance(new_nickname,
        gdata.apps.data.NicknameEntry))
    self.assertEquals(new_nickname.login.user_name, username)
    self.assertEquals(new_nickname.nickname.name, nickname)

    fetched_alias = self.client.RetrieveNickname(nickname)
    self.assertEquals(fetched_alias.login.user_name, username)
    self.assertEquals(fetched_alias.nickname.name, nickname)

    self.client.DeleteNickname(nickname)
    self.client.DeleteUser(username)


def suite():
  return conf.build_suite([AppsClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
