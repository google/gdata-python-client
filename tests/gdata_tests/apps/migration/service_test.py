#!/usr/bin/python2.4
#
# Copyright 2008 Google Inc. All Rights Reserved.
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

"""Test for Email Migration service."""


__author__ = 'google-apps-apis@googlegroups.com'


import getpass
import unittest
import gdata.apps.migration.service


domain = ''
admin_email = ''
admin_password = ''
username = ''
MESSAGE = """From: joe@blow.com
To: jane@doe.com
Date: Mon, 29 Sep 2008 20:00:34 -0500 (CDT)
Subject: %s

%s"""


class MigrationTest(unittest.TestCase):
  """Test for the MigrationService."""

  def setUp(self):
    self.ms = gdata.apps.migration.service.MigrationService(
        email=admin_email, password=admin_password, domain=domain)
    self.ms.ProgrammaticLogin()

  def testImportMail(self):
    self.ms.ImportMail(user_name=username,
                       mail_message=MESSAGE % ('Test subject', 'Test body'),
                       mail_item_properties=['IS_STARRED'],
                       mail_labels=['Test'])

  def testImportMultipleMails(self):
    for i in xrange(1, 10):
      self.ms.AddMailEntry(mail_message=MESSAGE % ('Test thread %d' % i,
                                                   'Test thread'),
                           mail_item_properties=['IS_UNREAD'],
                           mail_labels=['Test', 'Thread'],
                           identifier=str(i))
    self.ms.ImportMultipleMails(user_name=username)


if __name__ == '__main__':
  print("Google Apps Email Migration Service Tests\n\n"
        "NOTE: Please run these tests only with a test user account.\n")
  domain = raw_input('Google Apps domain: ')
  admin_email = '%s@%s' % (raw_input('Administrator username: '), domain)
  admin_password = getpass.getpass('Administrator password: ')
  username = raw_input('Test username: ')
  unittest.main()
