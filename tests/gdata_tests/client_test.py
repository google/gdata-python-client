#!/usr/bin/env python
#
# Copyright (C) 2008, 2009 Google Inc.
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
import gdata.client
import gdata.gauth
import atom.mock_http_core


# old imports
import getpass
import gdata.auth
import gdata.service
import atom.http_interface


class ClientLoginTest(unittest.TestCase):

  def test_token_request(self):
    client = gdata.client.GDClient()
    client.http_client = atom.mock_http_core.SettableHttpClient(200, 'OK', 
        'SID=DQAAAGgA...7Zg8CTN\n'
        'LSID=DQAAAGsA...lk8BBbG\n'
        'Auth=DQAAAGgA...dk3fA5N', {'Content-Type': 'text/plain'})
    token = client.request_client_login_token('email', 'pw', 'cp', 'test')
    self.assertTrue(isinstance(token, gdata.gauth.ClientLoginToken))
    self.assertEqual(token.token_string, 'DQAAAGgA...dk3fA5N')

    # Test a server response without a ClientLogin token.`
    client.http_client.set_response(200, 'OK', 'SID=12345\nLSID=34567', {})
    self.assertRaises(gdata.client.ClientLoginTokenMissing,
        client.request_client_login_token, 'email', 'pw', '', '')

    # Test a 302 redirect from the server on a login request.
    client.http_client.set_response(302, 'ignored', '', {})
    # TODO: change the exception class to one in gdata.client.
    self.assertRaises(gdata.service.BadAuthenticationServiceURL,
        client.request_client_login_token, 'email', 'pw', '', '')

    # Test a CAPTCHA challenge from the server
    client.http_client.set_response(403, 'Access Forbidden', 
        'Url=http://www.google.com/login/captcha\n'
        'Error=CaptchaRequired\n'
        'CaptchaToken=DQAAAGgA...dkI1LK9\n'
        # TODO: verify this sample CAPTCHA URL matches an
        # actual challenge from the server.
        'CaptchaUrl=Captcha?ctoken=HiteT4bVoP6-yFkHPibe7O9EqxeiI7lUSN', {})
    try:
      token = client.request_client_login_token('email', 'pw', '', '')
      self.fail('should raise a CaptchaChallenge on a 403 with a '
                'CaptchRequired error.')
    except gdata.client.CaptchaChallenge, challenge:
      self.assertEquals(challenge.captcha_url, 
          'http://www.google.com/accounts/'
          'Captcha?ctoken=HiteT4bVoP6-yFkHPibe7O9EqxeiI7lUSN')
      self.assertEquals(challenge.captcha_token, 'DQAAAGgA...dkI1LK9')

    # Test an unexpected response, a 404 for example.
    client.http_client.set_response(404, 'ignored', '', {})
    self.assertRaises(gdata.client.ClientLoginFailed,
        client.request_client_login_token, 'email', 'pw', '', '')


# Tests for v1 client code
class AuthSubUrlTest(unittest.TestCase):
  
  def testGenerateNextWithScope(self):
    next = 'http://example.com/test'
    scope = 'http://www.google.com/calendar/feeds/'
    request_url = gdata.client.GenerateAuthSubRequestUrl(next, scope)
    self.assert_(request_url.find('example.com') > -1)
    self.assert_(request_url.find('calendar') > -1)

  def testGenerateNextWithMultipleScopes(self):
    next = 'http://example.com/test'
    scope = ['http://www.google.com/calendar/feeds/', 
             'http://spreadsheets.google.com/feeds/']
    request_url = gdata.client.GenerateAuthSubRequestUrl(next, scope)
    self.assert_(request_url.find('example.com') > -1)
    self.assert_(request_url.find('calendar') > -1)
    self.assert_(request_url.find('spreadsheets') > -1)

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
    auth_token = gdata.auth.AuthSubToken(token, [scope1, scope2])
    self.client.token_store.add_token(auth_token)
    self.assert_(self.client.token_store.find_token(scope1) == auth_token)
    self.assert_(self.client.token_store.find_token(scope2) == auth_token)
    self.assert_(isinstance(self.client.token_store.find_token('foo'), 
        atom.http_interface.GenericToken))
    self.assert_(
        self.client.token_store.find_token('foo%s' % scope1) != auth_token)
    self.assert_(isinstance(self.client.token_store.find_token(
            'foo%s' % scope1), 
        atom.http_interface.GenericToken))
    self.assert_(
        self.client.token_store.find_token('%sfoo' % scope1) == auth_token)
    self.client.token_store.remove_token(auth_token)
    self.assert_(self.client.token_store.find_token('%sfoo' % scope1) != auth_token) 
    self.assert_(isinstance(self.client.token_store.find_token(
            '%sfoo' % scope1), 
        atom.http_interface.GenericToken))
    self.assert_(self.client.token_store.find_token(scope2) != auth_token)
# End tests for v1 client code


def suite():
  return unittest.TestSuite((unittest.makeSuite(ClientLoginTest, 'test'),
                             ))


if __name__ == '__main__':
  unittest.main()
