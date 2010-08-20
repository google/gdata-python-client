#!/usr/bin/env python
#
# Copyright (C) 2010 Google Inc.
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

"""Functional Tests for Google Analytics Account Feed and Data Feed.

AnalyticsClientTest: Tests making live requests to Google Analytics API.
"""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import unittest
import gdata.client
import gdata.data
import gdata.gauth
import gdata.analytics.client
import gdata.test_config as conf


conf.options.register_option(conf.GA_TABLE_ID)


class AnalyticsClientTest(unittest.TestCase):
  """Tests creating an Account Feed query and making a request to the
  Google Analytics Account Feed."""

  def setUp(self):
    """Creates an AnalyticsClient object."""

    self.client = None
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.analytics.client.AnalyticsClient()
      self.client.http_client.debug = True

      conf.configure_client(
          self.client,
          'AnalyticsClientTest',
          self.client.auth_service)

  def testAccountFeed(self):
    """Tests if the Account Feed exists."""

    if not conf.options.get_value('runlive') == 'true':
      return
    conf.configure_cache(self.client, 'testAccountFeed')

    account_query = gdata.analytics.client.AccountFeedQuery({
        'max-results': '1'
    })

    feed = self.client.GetAccountFeed(account_query)
    self.assert_(feed.entry is not None)

    properties = [
        'ga:accountId',
        'ga:accountName',
        'ga:profileId',
        'ga:webPropertyId',
        'ga:currency',
        'ga:timezone'
    ]

    entry = feed.entry[0]
    for prop in properties:
      property = entry.GetProperty(prop)
      self.assertEquals(property.name, prop)

  def testDataFeed(self):
    """Tests if the Data Feed exists."""

    start_date = '2008-10-01'
    end_date = '2008-10-02'
    metrics = 'ga:visits'

    if not conf.options.get_value('runlive') == 'true':
      return
    conf.configure_cache(self.client, 'testDataFeed')

    data_query = gdata.analytics.client.DataFeedQuery({
      'ids': conf.options.get_value('table_id'),
      'start-date': start_date,
      'end-date': end_date,
      'metrics' : metrics,
      'max-results': '1'
    })
    feed = self.client.GetDataFeed(data_query)

    self.assert_(feed.entry is not None)
    self.assertEquals(feed.start_date.text, start_date)
    self.assertEquals(feed.end_date.text, end_date)
    self.assertEquals(feed.entry[0].GetMetric(metrics).name, metrics)

  def testManagementFeed(self):
    """Tests of the Management Feed exists."""

    if not conf.options.get_value('runlive') == 'true':
      return
    conf.configure_cache(self.client, 'testManagementFeed')

    account_query = gdata.analytics.client.AccountQuery()
    feed = self.client.GetManagementFeed(account_query)

    self.assert_(feed.entry is not None)

  def tearDown(self):
    """Closes client connection."""
    conf.close_client(self.client)


def suite():
  return conf.build_suite([AnalyticsClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())

