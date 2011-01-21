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


__author__ = 'Alexandre Vivien <alex@simplecode.fr>'


import unittest
import gdata.client
import gdata.data
import gdata.gauth
import gdata.marketplace.client
import gdata.marketplace.data
import gdata.test_config as conf


conf.options.register_option(conf.APPS_DOMAIN_OPTION)


class LicensingClientTest(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    unittest.TestCase.__init__(self, *args, **kwargs)
    gdata.test_config.options.register(
    'appsid',
    'Enter the Application ID of your Marketplace application',
    description='The Application ID of your Marketplace application')
    gdata.test_config.options.register(
    'appsconsumerkey', 
    'Enter the Consumer Key of your Marketplace application', 
    description='The Consumer Key of your Marketplace application')
    gdata.test_config.options.register(
    'appsconsumersecret',
    'Enter the Consumer Secret of your Marketplace application', 
    description='The Consumer Secret of your Marketplace application')    

  def setUp(self):
    self.client = gdata.marketplace.client.LicensingClient(domain='example.com')
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.marketplace.client.LicensingClient(domain=conf.options.get_value('appsdomain'))
      conf.configure_client(self.client, 'LicensingClientTest', self.client.auth_service, True)
      self.client.auth_token = gdata.gauth.TwoLeggedOAuthHmacToken(conf.options.get_value('appsconsumerkey'), conf.options.get_value('appsconsumersecret'), '')
      self.client.source = 'GData-Python-Client-Test'
      self.client.account_type='HOSTED'
      self.client.http_client.debug = True
      self.app_id = conf.options.get_value('appsid')

  def tearDown(self):
    conf.close_client(self.client)
  
  def testGetLicense(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testGetLicense')
    
    fetched_feed = self.client.GetLicense(app_id=self.app_id)
    self.assertTrue(isinstance(fetched_feed, gdata.marketplace.data.LicenseFeed))
    self.assertTrue(isinstance(fetched_feed.entry[0], gdata.marketplace.data.LicenseEntry))
    entity = fetched_feed.entry[0].content.entity
    self.assertTrue(entity is not None)
    self.assertNotEqual(entity.id, '')
    self.assertNotEqual(entity.enabled, '')
    self.assertNotEqual(entity.customer_id, '')
    self.assertNotEqual(entity.state, '')
    
  def testGetLicenseNotifications(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testGetLicenseNotifications')
    
    fetched_feed = self.client.GetLicenseNotifications(app_id=self.app_id, max_results=2)
    self.assertTrue(isinstance(fetched_feed, gdata.marketplace.data.LicenseFeed))
    self.assertEqual(len(fetched_feed.entry), 2)
    for entry in fetched_feed.entry:
      entity = entry.content.entity
      self.assertTrue(entity is not None)
      self.assertNotEqual(entity.id, '')
      self.assertNotEqual(entity.domain_name, '')
      self.assertNotEqual(entity.installer_email, '')
      self.assertNotEqual(entity.tos_acceptance_time, '')
      self.assertNotEqual(entity.last_change_time, '')
      self.assertNotEqual(entity.product_config_id, '')
      self.assertNotEqual(entity.state, '')
    
    next_uri = fetched_feed.find_next_link()
    fetched_feed_next = self.client.GetLicenseNotifications(uri=next_uri)
    self.assertTrue(isinstance(fetched_feed_next, gdata.marketplace.data.LicenseFeed))
    self.assertTrue(len(fetched_feed_next.entry) <= 2)
    for entry in fetched_feed_next.entry:
      entity = entry.content.entity
      self.assertTrue(entity is not None)
      self.assertNotEqual(entity.id, '')
      self.assertNotEqual(entity.domain_name, '')
      self.assertNotEqual(entity.installer_email, '')
      self.assertNotEqual(entity.tos_acceptance_time, '')
      self.assertNotEqual(entity.last_change_time, '')
      self.assertNotEqual(entity.product_config_id, '')
      self.assertNotEqual(entity.state, '')


def suite():
  return conf.build_suite([LicensingClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
