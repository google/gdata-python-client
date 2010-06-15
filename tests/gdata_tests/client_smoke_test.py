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


# This module is used for version 2 of the Google Data APIs.


__author__ = 'j.s@google.com (Jeff Scudder)'


import unittest
import gdata.test_config as conf
import gdata.analytics.client
import gdata.apps.emailsettings.client
import gdata.blogger.client
import gdata.spreadsheets.client
import gdata.calendar_resource.client
import gdata.contacts.client
import gdata.docs.client
import gdata.maps.client
import gdata.projecthosting.client
import gdata.sites.client


class ClientSmokeTest(unittest.TestCase):

  def test_check_auth_client_classes(self):
    conf.check_clients_with_auth(self, (
        gdata.analytics.client.AnalyticsClient,
        gdata.apps.emailsettings.client.EmailSettingsClient,
        gdata.blogger.client.BloggerClient,
        gdata.spreadsheets.client.SpreadsheetsClient,
        gdata.calendar_resource.client.CalendarResourceClient,
        gdata.contacts.client.ContactsClient,
        gdata.docs.client.DocsClient,
        gdata.maps.client.MapsClient,
        gdata.projecthosting.client.ProjectHostingClient,
        gdata.sites.client.SitesClient
    ))


def suite():
  return conf.build_suite([ClientSmokeTest])


if __name__ == '__main__':
  unittest.main()
