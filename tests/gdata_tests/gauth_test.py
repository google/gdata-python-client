#!/usr/bin/env python
#
# Copyright (C) 2009 Google Inc.
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
import gdata.gauth
import atom.http_core
import gdata.test_config as conf


class AuthSubTest(unittest.TestCase):

  def test_generate_request_url(self):
    url = gdata.gauth.generate_auth_sub_url('http://example.com', 
        ['http://example.net/scope1'])
    self.assertTrue(isinstance(url, atom.http_core.Uri))
    self.assertEqual(url.query['secure'], '0')
    self.assertEqual(url.query['session'], '1')
    self.assertEqual(url.query['scope'], 'http://example.net/scope1')
    self.assertEqual(atom.http_core.Uri.parse_uri(
        url.query['next']).query['auth_sub_scopes'],
        'http://example.net/scope1')
    self.assertEqual(atom.http_core.Uri.parse_uri(url.query['next']).path, 
        '/')
    self.assertEqual(atom.http_core.Uri.parse_uri(url.query['next']).host, 
        'example.com')

  def test_from_url(self):
    token_str = gdata.gauth.auth_sub_string_from_url(
        'http://example.com?token=123abc')[0]
    self.assertEqual(token_str, '123abc')

  def test_from_http_body(self):
    token_str = gdata.gauth.auth_sub_string_from_body('Something\n'
        'Token=DQAA...7DCTN\n'
        'Expiration=20061004T123456Z\n')
    self.assertEqual(token_str, 'DQAA...7DCTN')

  def test_modify_request(self):
    token = gdata.gauth.AuthSubToken('tval')
    request = atom.http_core.HttpRequest()
    token.modify_request(request)
    self.assertEqual(request.headers['Authorization'], 'AuthSub token=tval')

  def test_create_and_upgrade_tokens(self):
    token = gdata.gauth.AuthSubToken.from_url(
        'http://example.com?token=123abc')
    self.assertTrue(isinstance(token, gdata.gauth.AuthSubToken))
    self.assertEqual(token.token_string, '123abc')
    self.assertEqual(token.scopes, [])
    token._upgrade_token('Token=456def')
    self.assertEqual(token.token_string, '456def')
    self.assertEqual(token.scopes, [])


class TokensToAndFromBlobs(unittest.TestCase):

  def test_client_login_conversion(self):
    token = gdata.gauth.ClientLoginToken('test|key')
    copy = gdata.gauth.token_from_blob(gdata.gauth.token_to_blob(token))
    self.assertEqual(token.token_string, copy.token_string)
    self.assertTrue(isinstance(copy, gdata.gauth.ClientLoginToken))

  def test_authsub_conversion(self):
    token = gdata.gauth.AuthSubToken('test|key')
    copy = gdata.gauth.token_from_blob(gdata.gauth.token_to_blob(token))
    self.assertEqual(token.token_string, copy.token_string)
    self.assertTrue(isinstance(copy, gdata.gauth.AuthSubToken))
    
    scopes = ['http://example.com', 'http://other||test', 'thir|d']
    token = gdata.gauth.AuthSubToken('key-=', scopes)
    copy = gdata.gauth.token_from_blob(gdata.gauth.token_to_blob(token))
    self.assertEqual(token.token_string, copy.token_string)
    self.assertTrue(isinstance(copy, gdata.gauth.AuthSubToken))
    self.assertEqual(token.scopes, scopes)


def suite():
  return conf.build_suite([AuthSubTest, TokensToAndFromBlobs])


if __name__ == '__main__':
  unittest.main()
