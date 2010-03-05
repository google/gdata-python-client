#!/usr/bin/env python
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

"""Contains Unit Tests for Google Profiles API.

  ProfilesServiceTest: Provides methods to test feeds and manipulate items.

  ProfilesQueryTest: Constructs a query object for the profiles feed.
                 Extends Query.
"""

__author__ = 'jtoledo (Julian Toledo)'


import getopt
import getpass
import sys
import unittest
import gdata.contacts
import gdata.contacts.service


email = ''
password = ''
domain = ''
server = 'www.google.com'

GDATA_VER_HEADER = 'GData-Version'

class ProfilesServiceTest(unittest.TestCase):

  def setUp(self):    
    additional_headers = {GDATA_VER_HEADER: 3}
    self.gd_client = gdata.contacts.service.ContactsService(
        contact_list=domain, additional_headers=additional_headers )
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'GoogleInc-ProfilesPythonTest-1'
    self.gd_client.ProgrammaticLogin()

  def testGetFeedUriCustom(self):
    uri = self.gd_client.GetFeedUri(kind='profiles', scheme='https')
    self.assertEquals(
        'https://%s/m8/feeds/profiles/domain/%s/full' % (server, domain), uri)

  def testGetProfileFeedUriDefault(self):
    self.gd_client.contact_list = 'domain.com'
    self.assertEquals('/m8/feeds/profiles/domain/domain.com/full',
                      self.gd_client.GetFeedUri('profiles'))

  def testCleanUriNeedsCleaning(self):
    self.assertEquals('/relative/uri', self.gd_client._CleanUri(
        'http://www.google.com/relative/uri'))

  def testCleanUriDoesNotNeedCleaning(self):
    self.assertEquals('/relative/uri', self.gd_client._CleanUri(
        '/relative/uri'))

  def testGetProfilesFeed(self):
    feed = self.gd_client.GetProfilesFeed()
    self.assert_(isinstance(feed, gdata.contacts.ProfilesFeed))

  def testGetProfile(self):
    # Gets an existing entry
    feed = self.gd_client.GetProfilesFeed()
    entry = feed.entry[0]
    self.assert_(isinstance(entry, gdata.contacts.ProfileEntry))
    self.assertEquals(entry.title.text,
                      self.gd_client.GetProfile(entry.id.text).title.text)
    self.assertEquals(entry._children,
                      self.gd_client.GetProfile(entry.id.text)._children)

  def testUpdateProfile(self):
    feed = self.gd_client.GetProfilesFeed()
    entry = feed.entry[1]
    original_occupation = entry.occupation
    entry.occupation = gdata.contacts.Occupation(text='TEST')
    updated = self.gd_client.UpdateProfile(entry.GetEditLink().href, entry)
    self.assertEquals('TEST', updated.occupation.text)
    updated.occupation = original_occupation
    self.gd_client.UpdateProfile(updated.GetEditLink().href, updated)


if __name__ == '__main__':

  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw=', 'domain='])
  except getopt.error, msg:
    print ('Profiles Tests\nNOTE: Please run these tests only with a test '
           'account. The tests may delete or update your data.\n'
           '\nUsage: service_test.py --email=EMAIL '
           '--password=PASSWORD --domain=DOMAIN\n')
    sys.exit(2)

  # Process options
  for option, arg in opts:
    if option == '--email':
      email = arg
    elif option == '--pw':
      password = arg
    elif option == '--domain':
      domain = arg

  while not email:
    print 'NOTE: Please run these tests only with a test account.'
    email = raw_input('Please enter your email: ')
  while not password:
    password = getpass.getpass('Please enter password: ')
    if not password:
      print 'Password cannot be blank.'
  while not domain:
    print 'NOTE: Please run these tests only with a test account.'
    domain = raw_input('Please enter your Apps domain: ')

  suite = unittest.makeSuite(ProfilesServiceTest)
  unittest.TextTestRunner().run(suite)

