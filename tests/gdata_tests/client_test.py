#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
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


__author__ = 'api.jscudder (Jeff Scudder)'


import unittest
import getpass
import atom.mock_service
import gdata.client
import gdata.service


class AuthSubUrlTest(unittest.TestCase):
  
  def testGenerateNextWithScope(self):
    next = 'http://example.com/test'
    scope = 'http://www.google.com/calendar/feeds/'
    request_url = gdata.client.GenerateAuthSubRequestUrl(next, scope)
    self.assertTrue(request_url.find('example.com') > -1)
    self.assertTrue(request_url.find('calendar') > -1)

  def testGenerateNextWithMultipleScopes(self):
    next = 'http://example.com/test'
    scope = ['http://www.google.com/calendar/feeds/', 
             'http://spreadsheets.google.com/feeds/']
    request_url = gdata.client.GenerateAuthSubRequestUrl(next, scope)
    self.assertTrue(request_url.find('example.com') > -1)
    self.assertTrue(request_url.find('calendar') > -1)
    self.assertTrue(request_url.find('spreadsheets') > -1)

  def testExtractTokenWithScope(self):
    url = ('http://example.com/test?authsub_token_scope=http%3A%2F%2F'
           'www.google.com%2Fcalendar%2Ffeeds%2F&token=yeF3EE&foo=1')
    (token, scopes) = gdata.client.ExtractToken(url)
    self.assert_(token == 'AuthSub token=yeF3EE')
    self.assert_(scopes[0] == 'http://www.google.com/calendar/feeds/')

  def testExtractTokenWithMultipleScopes(self):
    url = ('http://example.com/test?authsub_token_scope=http%3A%2F%2F'
           'www.google.com%2Fcalendar%2Ffeeds%2F+http%3A%2F%2F'
           'spreadsheets.google.com%2Ffeeds%2F&token=KyeF3E6Mma')
    (token, scopes) = gdata.client.ExtractToken(url)
    self.assert_(token == 'AuthSub token=KyeF3E6Mma')
    self.assert_(len(scopes) == 2)
    self.assert_(scopes[0] == 'http://www.google.com/calendar/feeds/')
    self.assert_(scopes[1] == 'http://spreadsheets.google.com/feeds/')


class GDataClientTest(unittest.TestCase):

  def setUp(self):
    self.client = gdata.client.GDataClient()

  def testFindTokenForScope(self):
    # Add a test token with two scopes
    token = 'AuthSub token=KyeF3E6Mma'
    scope1 = 'http://www.google.com/calendar/feeds/'
    scope2 = 'http://spreadsheets.google.com/feeds/'
    self.client.StoreAuthSubToken(token, [scope1, scope2])
    self.assert_(self.client.FindTokenForScope(scope1) == token)
    self.assert_(self.client.FindTokenForScope(scope2) == token)
    self.assert_(self.client.FindTokenForScope('foo') == None)
    self.assert_(self.client.FindTokenForScope('foo%s' % scope1) == None)
    self.assert_(self.client.FindTokenForScope('%sfoo' % scope1) == token)
    del self.client.tokens[scope1]
    self.assert_(self.client.FindTokenForScope('%sfoo' % scope1) == None)
    self.assert_(self.client.FindTokenForScope(scope2) == token)


if __name__ == '__main__':
  unittest.main()
