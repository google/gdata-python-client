#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.
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

# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


__author__ = 'Vic Fryzel <vf@google.com>'


import unittest
import gdata.client
import gdata.data
import gdata.gauth
import gdata.calendar_resource.client
import gdata.calendar_resource.data
import gdata.test_config as conf


conf.options.register_option(conf.APPS_DOMAIN_OPTION)


class CalendarResourceClientTest(unittest.TestCase):

  def setUp(self):
    self.client = gdata.calendar_resource.client.CalendarResourceClient(
        domain='example.com')
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.calendar_resource.client.CalendarResourceClient(
          domain=conf.options.get_value('appsdomain'))
      if conf.options.get_value('ssl') == 'true':
        self.client.ssl = True
      conf.configure_client(self.client, 'CalendarResourceClientTest',
          self.client.auth_service, True)

  def tearDown(self):
    conf.close_client(self.client)

  def testClientConfiguration(self):
    self.assertEqual('apps-apis.google.com', self.client.host)
    self.assertEqual('2.0', self.client.api_version)
    self.assertEqual('apps', self.client.auth_service)
    self.assertEqual(
        ('http://www.google.com/a/feeds/',
         'https://www.google.com/a/feeds/',
         'http://apps-apis.google.com/a/feeds/',
         'https://apps-apis.google.com/a/feeds/'), self.client.auth_scopes)
    if conf.options.get_value('runlive') == 'true':
      self.assertEqual(self.client.domain, conf.options.get_value('appsdomain'))
    else:
      self.assertEqual(self.client.domain, 'example.com')

  def testMakeResourceFeedUri(self):
    self.assertEqual('/a/feeds/calendar/resource/2.0/%s/' % self.client.domain,
        self.client.MakeResourceFeedUri())
    self.assertEqual('/a/feeds/calendar/resource/2.0/%s/CR-NYC-14-12-BR'
        % self.client.domain,
        self.client.MakeResourceFeedUri(resource_id='CR-NYC-14-12-BR'))
    self.assertEqual('/a/feeds/calendar/resource/2.0/%s/?test=1'
        % self.client.domain,
        self.client.MakeResourceFeedUri(params={'test': 1}))
    self.assertEqual('/a/feeds/calendar/resource/2.0/%s/CR-NYC-14-12-BR?test=1'
        % self.client.domain,
        self.client.MakeResourceFeedUri(resource_id='CR-NYC-14-12-BR',
            params={'test': 1}))

  def testCreateRetrieveUpdateDelete(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testCreateUpdateDelete')

    try:
      new_entry = self.client.CreateResource(
          'CR-NYC-14-12-BR', 'Boardroom',
          ('This conference room is in New York City, building 14, floor 12, '
           'Boardroom'), 'CR')
    except Exception, e:
      print e
      self.client.delete_resource('CR-NYC-14-12-BR')
      # If the test failed to run to completion
      # the resource may already exist
      new_entry = self.client.CreateResource(
          'CR-NYC-14-12-BR', 'Boardroom',
          ('This conference room is in New York City, building 14, floor 12, '
           'Boardroom'), 'CR')

    self.assert_(isinstance(new_entry,
        gdata.calendar_resource.data.CalendarResourceEntry))
    self.assertEqual(new_entry.resource_id, 'CR-NYC-14-12-BR')
    self.assertEqual(new_entry.resource_common_name, 'Boardroom')
    self.assertEqual(new_entry.resource_description,
        ('This conference room is in New York City, building 14, floor 12, '
         'Boardroom'))
    self.assertEqual(new_entry.resource_type, 'CR')

    fetched_entry = self.client.get_resource(resource_id='CR-NYC-14-12-BR')
    self.assert_(isinstance(fetched_entry,
        gdata.calendar_resource.data.CalendarResourceEntry))
    self.assertEqual(fetched_entry.resource_id, 'CR-NYC-14-12-BR')
    self.assertEqual(fetched_entry.resource_common_name, 'Boardroom')
    self.assertEqual(fetched_entry.resource_description,
        ('This conference room is in New York City, building 14, floor 12, '
         'Boardroom'))
    self.assertEqual(fetched_entry.resource_type, 'CR')

    new_entry.resource_id = 'CR-MTV-14-12-BR'
    new_entry.resource_common_name = 'Executive Boardroom'
    new_entry.resource_description = 'This conference room is in Mountain View'
    new_entry.resource_type = 'BR'
    updated_entry = self.client.update(new_entry)
    self.assert_(isinstance(updated_entry,
        gdata.calendar_resource.data.CalendarResourceEntry))
    self.assertEqual(updated_entry.resource_id, 'CR-MTV-14-12-BR')
    self.assertEqual(updated_entry.resource_common_name, 'Executive Boardroom')
    self.assertEqual(updated_entry.resource_description,
        'This conference room is in Mountain View')
    self.assertEqual(updated_entry.resource_type, 'BR')

    self.client.delete_resource('CR-NYC-14-12-BR')


def suite():
  return conf.build_suite([CalendarResourceClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
