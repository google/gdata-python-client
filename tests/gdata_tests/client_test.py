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
import gdata.data
import atom.mock_http_core
import StringIO


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

  def test_client_login(self):
    client = gdata.client.GDClient()
    client.http_client = atom.mock_http_core.SettableHttpClient(200, 'OK', 
        'SID=DQAAAGgA...7Zg8CTN\n'
        'LSID=DQAAAGsA...lk8BBbG\n'
        'Auth=DQAAAGgA...dk3fA5N', {'Content-Type': 'text/plain'})
    client.client_login('me@example.com', 'password', 'wise', 'unit test')
    self.assertTrue(isinstance(client.auth_token, gdata.gauth.ClientLoginToken))
    self.assertEqual(client.auth_token.token_string, 'DQAAAGgA...dk3fA5N')


class AuthSubTest(unittest.TestCase):

  def test_get_and_upgrade_token(self):
    client = gdata.client.GDClient()
    client.http_client = atom.mock_http_core.SettableHttpClient(200, 'OK', 
        'Token=UpgradedTokenVal\n'
        'Extra data', {'Content-Type': 'text/plain'})

    page_url = 'http://example.com/showcalendar.html?token=CKF50YzIHxCTKMAg'

    client.auth_token = gdata.gauth.AuthSubToken.from_url(page_url)

    self.assertTrue(isinstance(client.auth_token, gdata.gauth.AuthSubToken))
    self.assertEqual(client.auth_token.token_string, 'CKF50YzIHxCTKMAg')

    upgraded = client.upgrade_token()

    self.assertTrue(isinstance(client.auth_token, gdata.gauth.AuthSubToken))
    self.assertEqual(client.auth_token.token_string, 'UpgradedTokenVal')
    self.assertEqual(client.auth_token, upgraded)

    # Ensure passing in a token returns without modifying client's auth_token.
    client.http_client.set_response(200, 'OK', 'Token=4567', {})
    upgraded = client.upgrade_token(
        gdata.gauth.AuthSubToken.from_url('?token=1234'))
    self.assertEqual(upgraded.token_string, '4567')
    self.assertEqual(client.auth_token.token_string, 'UpgradedTokenVal')
    self.assertNotEqual(client.auth_token, upgraded)

    # Test exception cases
    client.auth_token = None
    self.assertRaises(gdata.client.UnableToUpgradeToken, client.upgrade_token,
                      None)
    self.assertRaises(gdata.client.UnableToUpgradeToken, client.upgrade_token)


class RequestTest(unittest.TestCase):

  def test_simple_request(self):
    client = gdata.client.GDClient()
    client.http_client = atom.mock_http_core.EchoHttpClient()
    response = client.request('GET', 'https://example.com/test')
    self.assertEqual(response.getheader('Echo-Host'), 'example.com:None')
    self.assertEqual(response.getheader('Echo-Uri'), '/test')
    self.assertEqual(response.getheader('Echo-Scheme'), 'https')
    self.assertEqual(response.getheader('Echo-Method'), 'GET')

    http_request = atom.http_core.HttpRequest(
        uri=atom.http_core.Uri(scheme='http', host='example.net', port=8080),
        method='POST', headers={'X': 1})
    http_request.add_body_part('test', 'text/plain')
    response = client.request(http_request=http_request)
    self.assertEqual(response.getheader('Echo-Host'), 'example.net:8080')
    # A Uri with path set to None should default to /.
    self.assertEqual(response.getheader('Echo-Uri'), '/')
    self.assertEqual(response.getheader('Echo-Scheme'), 'http')
    self.assertEqual(response.getheader('Echo-Method'), 'POST')
    self.assertEqual(response.getheader('Content-Type'), 'text/plain')
    self.assertEqual(response.getheader('X'), '1')
    self.assertEqual(response.read(), 'test')

    # Use the same request object from above, but overwrite the request path
    # by passing in a URI.
    response = client.request(uri='/new/path?p=1', http_request=http_request)
    self.assertEqual(response.getheader('Echo-Host'), 'example.net:8080')
    self.assertEqual(response.getheader('Echo-Uri'), '/new/path?p=1')
    self.assertEqual(response.getheader('Echo-Scheme'), 'http')
    self.assertEqual(response.read(), 'test')

  def test_gdata_version_header(self):
    client = gdata.client.GDClient()
    client.http_client = atom.mock_http_core.EchoHttpClient()

    response = client.request('GET', 'http://example.com')
    self.assertEqual(response.getheader('GData-Version'), None)

    client.api_version = '2'
    response = client.request('GET', 'http://example.com')
    self.assertEqual(response.getheader('GData-Version'), '2')

  def test_redirects(self):
    client = gdata.client.GDClient()
    client.http_client = atom.mock_http_core.MockHttpClient()
    # Add the redirect response for the initial request.
    first_request = atom.http_core.HttpRequest('http://example.com/1', 
                                               'POST')
    client.http_client.add_response(first_request, 302, None, 
        {'Location': 'http://example.com/1?gsessionid=12'})
    second_request = atom.http_core.HttpRequest(
        'http://example.com/1?gsessionid=12', 'POST')
    client.http_client.AddResponse(second_request, 200, 'OK', body='Done')

    response = client.Request('POST', 'http://example.com/1')
    self.assertEqual(response.status, 200)
    self.assertEqual(response.reason, 'OK')
    self.assertEqual(response.read(), 'Done')

    redirect_loop_request = atom.http_core.HttpRequest(
        'http://example.com/2?gsessionid=loop', 'PUT')
    client.http_client.add_response(redirect_loop_request, 302, None, 
        {'Location': 'http://example.com/2?gsessionid=loop'})
    try:
      response = client.request(method='PUT', uri='http://example.com/2?gsessionid=loop')
      self.fail('Loop URL should have redirected forever.')
    except gdata.client.RedirectError, err:
      self.assert_(str(err).startswith('Too many redirects from server'))

  def test_exercise_exceptions(self):
    # TODO
    pass

  def test_converter_vs_desired_class(self):

    def bad_converter(string):
      return 1
  
    class TestClass(atom.core.XmlElement):
      _qname = '{http://www.w3.org/2005/Atom}entry'
    
    client = gdata.client.GDClient()
    client.http_client = atom.mock_http_core.EchoHttpClient()
    test_entry = gdata.data.GEntry()
    result = client.post(test_entry, 'http://example.com')
    self.assertTrue(isinstance(result, gdata.data.GEntry))
    result = client.post(test_entry, 'http://example.com', converter=bad_converter)
    self.assertEquals(result, 1)
    result = client.post(test_entry, 'http://example.com', desired_class=TestClass)
    self.assertTrue(isinstance(result, TestClass))


class CreateConverterTest(unittest.TestCase):
  
  def test_create_converter(self):
    e = gdata.data.GEntry()
    fake_response = StringIO.StringIO(
        '<entry xmlns="http://www.w3.org/2005/Atom"><title>x</title></entry>')
    converter_function = gdata.client.create_converter(e)
    entry = converter_function(fake_response)
    self.assertTrue(isinstance(entry, gdata.data.GEntry))
    self.assertEqual(entry.get_elements('title')[0].text, 'x')


class QueryTest(unittest.TestCase):

  def test_query_modifies_request(self):
    request = atom.http_core.HttpRequest()
    gdata.client.Query(
        text_query='foo', categories=['a', 'b']).modify_request(request)
    self.assertEqual(request.uri.query, {'q': 'foo', 'categories': 'a,b'})

  def test_client_uses_query_modification(self):
    """If the Query is passed as an unexpected param it should apply"""
    client = gdata.client.GDClient()
    client.http_client = atom.mock_http_core.EchoHttpClient()
    query = gdata.client.Query(max_results=7)

    client.http_client = atom.mock_http_core.SettableHttpClient(
        201, 'CREATED', gdata.data.GDEntry().ToString(), {})
    response = client.get('https://example.com/foo', a_random_param=query)
    self.assertEqual(
        client.http_client.last_request.uri.query['max-results'], '7')


class VersionConversionTest(unittest.TestCase):

  def test_use_default_version(self):
    self.assertEquals(gdata.client.get_xml_version(None), 1)

  def test_str_to_int_version(self):
    self.assertEquals(gdata.client.get_xml_version('1'), 1)
    self.assertEquals(gdata.client.get_xml_version('2'), 2)
    self.assertEquals(gdata.client.get_xml_version('2.1.2'), 2)
    self.assertEquals(gdata.client.get_xml_version('10.4'), 10)

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
                             unittest.makeSuite(AuthSubTest, 'test'),
                             unittest.makeSuite(RequestTest, 'test'),
                             unittest.makeSuite(QueryTest, 'test'),
                             unittest.makeSuite(CreateConverterTest, 'test')))


if __name__ == '__main__':
  unittest.main()
