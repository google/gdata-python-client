#!/usr/bin/env python
#
#    Copyright (C) 2009 Google Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


# This module is used for version 2 of the Google Data APIs.


__author__ = 'j.s@google.com (Jeff Scudder)'

import unittest
# Tests for v2 features.
import atom_tests.core_test
import atom_tests.data_test
import atom_tests.http_core_test
import atom_tests.auth_test
import atom_tests.mock_http_core_test
import atom_tests.client_test
import gdata_tests.client_test
import gdata_tests.core_test
import gdata_tests.data_test
import gdata_tests.data_smoke_test
import gdata_tests.client_smoke_test
import gdata_tests.live_client_test
import gdata_tests.gauth_test
import gdata_tests.blogger.data_test
import gdata_tests.blogger.live_client_test
import gdata_tests.spreadsheets.data_test
import gdata_tests.spreadsheets.live_client_test
import gdata_tests.projecthosting.data_test
import gdata_tests.projecthosting.live_client_test
import gdata_tests.sites.data_test
import gdata_tests.sites.live_client_test
import gdata_tests.analytics.data_test
import gdata_tests.analytics.live_client_test
import gdata_tests.contacts.live_client_test
import gdata_tests.contacts.profiles.live_client_test
import gdata_tests.calendar_resource.live_client_test
import gdata_tests.calendar_resource.data_test
import gdata_tests.apps.emailsettings.data_test
import gdata_tests.apps.emailsettings.live_client_test
import gdata_tests.youtube.live_client_test


def suite():
  return unittest.TestSuite((
      gdata_tests.contacts.profiles.live_client_test.suite(),
      atom_tests.core_test.suite(),
      atom_tests.data_test.suite(),
      atom_tests.http_core_test.suite(),
      atom_tests.auth_test.suite(),
      atom_tests.mock_http_core_test.suite(),
      atom_tests.client_test.suite(),
      gdata_tests.client_test.suite(),
      gdata_tests.core_test.suite(),
      gdata_tests.data_test.suite(),
      gdata_tests.data_smoke_test.suite(),
      gdata_tests.client_smoke_test.suite(),
      gdata_tests.live_client_test.suite(),
      gdata_tests.gauth_test.suite(),
      gdata_tests.blogger.data_test.suite(),
      gdata_tests.blogger.live_client_test.suite(),
      gdata_tests.spreadsheets.data_test.suite(),
      gdata_tests.spreadsheets.live_client_test.suite(),
      gdata_tests.projecthosting.data_test.suite(),
      gdata_tests.projecthosting.live_client_test.suite(),
      gdata_tests.sites.data_test.suite(),
      gdata_tests.sites.live_client_test.suite(),
      gdata_tests.analytics.data_test.suite(),
      gdata_tests.analytics.live_client_test.suite(),
      gdata_tests.contacts.live_client_test.suite(),
      gdata_tests.calendar_resource.live_client_test.suite(),
      gdata_tests.calendar_resource.data_test.suite(),
      gdata_tests.apps.emailsettings.live_client_test.suite(),
      gdata_tests.apps.emailsettings.data_test.suite(),
      gdata_tests.youtube.live_client_test.suite(),
      ))


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
