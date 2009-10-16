#!/usr/bin/python
#
# Copyright (C) 2007 SIOS Technology, Inc.
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

__author__ = 'tmatsuo@sios.com (Takashi Matsuo)'

import unittest
import time, os
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import re
import pickle

import atom
import atom.http
import atom.service
from atom import mock_http
import gdata.apps
import gdata.apps.service
import getpass

apps_domain = 'test.shehas.net'
apps_username = ''
apps_password = ''


def conceal_secrets(recordings):
  ret = []
  for rec in recordings:
    req, res = rec
    if req.data:
      req.data = re.sub(r'Passwd=[^&]+', 'Passwd=hogehoge', req.data)
    if res.body:
      res.body = re.sub(r'SID=[^\n]+', 'SID=hogehoge', res.body)
      res.body = re.sub(r'LSID=[^\n]+', 'LSID=hogehoge', res.body)
      res.body = re.sub(r'Auth=[^\n]+', 'Auth=hogehoge', res.body)
    if req.headers.has_key('Authorization'):
      req.headers['Authorization'] = 'hogehoge'
    ret.append((req, res))
  return ret

class AppsServiceBaseTest(object):

  def setUp(self):
    self.datafile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "%s.pickle" % self.name)
    if os.path.isfile(self.datafile):
      f = open(self.datafile, "rb")
      data = pickle.load(f)
      f.close()
      http_client = mock_http.MockHttpClient(recordings=data)
    else:
      real_client = atom.http.ProxiedHttpClient()
      http_client = mock_http.MockHttpClient(real_client=real_client)

    email = apps_username + '@' + apps_domain
    self.apps_client = gdata.apps.service.AppsService(
      email=email, domain=apps_domain, password=apps_password,
      source='AppsClient "Unit" Tests')
    self.apps_client.http_client = http_client
    self.apps_client.ProgrammaticLogin()

  def tearDown(self):
    if self.apps_client.http_client.real_client:
      # create pickle file
      f = open(self.datafile, "wb")
      data = conceal_secrets(self.apps_client.http_client.recordings)
      pickle.dump(data, f)
      f.close()

class AppsServiceTestForGetGeneratorForAllRecipients(AppsServiceBaseTest,
                                                     unittest.TestCase):
  name = "AppsServiceTestForGetGeneratorForAllRecipients"
  def testGetGeneratorForAllRecipients(self):
    """Tests GetGeneratorForAllRecipientss method"""
    generator = self.apps_client.GetGeneratorForAllRecipients(
      "b101-20091013151051")
    i = 0
    for recipient_feed in generator:
      for a_recipient in recipient_feed.entry:
        i = i + 1
    self.assert_(i == 102)

class AppsServiceTestForGetGeneratorForAllEmailLists(AppsServiceBaseTest,
                                                     unittest.TestCase):
  name = "AppsServiceTestForGetGeneratorForAllEmailLists"
  def testGetGeneratorForAllEmailLists(self):
    """Tests GetGeneratorForAllEmailLists method"""
    generator = self.apps_client.GetGeneratorForAllEmailLists()
    i = 0
    for emaillist_feed in generator:
      for a_emaillist in emaillist_feed.entry:
        i = i + 1
    self.assert_(i == 105)

class AppsServiceTestForGetGeneratorForAllNicknames(AppsServiceBaseTest,
                                                unittest.TestCase):
  name = "AppsServiceTestForGetGeneratorForAllNicknames"
  def testGetGeneratorForAllNicknames(self):
    """Tests GetGeneratorForAllNicknames method"""
    generator = self.apps_client.GetGeneratorForAllNicknames()
    i = 0
    for nickname_feed in generator:
      for a_nickname in nickname_feed.entry:
        i = i + 1
    self.assert_(i == 102)


class AppsServiceTestForGetGeneratorForAllUsers(AppsServiceBaseTest,
                                                unittest.TestCase):
  name = "AppsServiceTestForGetGeneratorForAllUsers"
    
  def testGetGeneratorForAllUsers(self):
    """Tests GetGeneratorForAllUsers method"""
    generator = self.apps_client.GetGeneratorForAllUsers()
    i = 0
    for user_feed in generator:
      for a_user in user_feed.entry:
        i = i + 1
    self.assert_(i == 102)

if __name__ == '__main__':
  print ('The tests may delete or update your data.')
  apps_username = raw_input('Please enter your username: ')
  apps_password = getpass.getpass()
  unittest.main()
