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
# This test may make an actual HTTP request.


__author__ = 'j.s@google.com (Jeff Scudder)'


import unittest
import atom.http_core
import atom.auth
import atom.client
import atom.mock_http_core


class AtomPubClientEchoTest(unittest.TestCase):

  def test_simple_request_with_no_client_defaults(self):
    client = atom.client.AtomPubClient(atom.mock_http_core.EchoHttpClient())
    self.assert_(client.host is None)
    self.assert_(client.auth_token is None)
    # Make several equivalent requests.
    responses = [client.request('GET', 'http://example.org/'),
                 client.request(http_request=atom.http_core.HttpRequest(
                     'http', 'example.org', uri='/', method='GET')),
                 client.request('GET', 
                     http_request=atom.http_core.HttpRequest('http', 
                         'example.org', uri='/'))]
    for response in responses:
      self.assert_(response.getheader('Echo-Host') == 'example.org:None')
      self.assert_(response.getheader('Echo-Uri') == '/')
      self.assert_(response.getheader('Echo-Scheme') == 'http')
      self.assert_(response.getheader('Echo-Method') == 'GET')

  def test_auth_request_with_no_client_defaults(self):
    client = atom.client.AtomPubClient(atom.mock_http_core.EchoHttpClient())
    token = atom.auth.BasicAuth('Jeff', '123')
    response = client.request('POST', 'https://example.net:8080/', 
        auth_token=token)
    self.assert_(response.getheader('Echo-Host') == 'example.net:8080')
    self.assert_(response.getheader('Echo-Uri') == '/')
    self.assert_(response.getheader('Echo-Scheme') == 'https')
    self.assert_(response.getheader('Authorization') == 'Basic SmVmZjoxMjM=')
    self.assert_(response.getheader('Echo-Method') == 'POST')

  def test_request_with_client_defaults(self):
    client = atom.client.AtomPubClient(atom.mock_http_core.EchoHttpClient(), 
        'example.com', atom.auth.BasicAuth('Jeff', '123'))
    self.assert_(client.host == 'example.com')
    self.assert_(client.auth_token is not None)
    self.assert_(client.auth_token.basic_cookie == 'SmVmZjoxMjM=')
    response = client.request('GET', 'http://example.org/')
    self.assert_(response.getheader('Echo-Host') == 'example.org:None')
    self.assert_(response.getheader('Echo-Uri') == '/')
    self.assert_(response.getheader('Echo-Scheme') == 'http')
    self.assert_(response.getheader('Echo-Method') == 'GET')
    self.assert_(response.getheader('Authorization') == 'Basic SmVmZjoxMjM=')
    response = client.request('GET', '/')
    self.assert_(response.getheader('Echo-Host') == 'example.com:None')
    self.assert_(response.getheader('Echo-Uri') == '/')
    self.assert_(response.getheader('Echo-Scheme') == 'http')
    self.assert_(response.getheader('Authorization') == 'Basic SmVmZjoxMjM=')
    response = client.request('GET', '/', 
        http_request=atom.http_core.HttpRequest(port=99))
    self.assert_(response.getheader('Echo-Host') == 'example.com:99')


def suite():
  return unittest.TestSuite((unittest.makeSuite(AtomPubClientEchoTest, 'test'),
                             ))


if __name__ == '__main__':
  unittest.main()
