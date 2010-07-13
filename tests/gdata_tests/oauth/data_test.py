#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'samuel.cyprian@gmail.com (Samuel Cyprian)'

import unittest
from gdata import oauth, test_config

HTTP_METHOD_POST = 'POST'
VERSION = '1.0'


class OauthUtilsTest(unittest.TestCase):
  def test_build_authenticate_header(self):
    self.assertEqual(oauth.build_authenticate_header(), 
                     {'WWW-Authenticate' :'OAuth realm=""'})
    self.assertEqual(oauth.build_authenticate_header('foo'), 
                     {'WWW-Authenticate': 'OAuth realm="foo"'})
    
  def test_escape(self):
    #Special cases
    self.assertEqual(oauth.escape('~'), '~')
    self.assertEqual(oauth.escape('/'), '%2F')
    self.assertEqual(oauth.escape('+'), '%2B')
    self.assertEqual(oauth.escape(' '), '%20')
    self.assertEqual(oauth.escape('Peter Strömberg'), 
                       'Peter%20Str%C3%B6mberg')
  
  def test_generate_timestamp(self):
      self.assertTrue(oauth.generate_timestamp()>0)
      self.assertTrue(type(oauth.generate_timestamp()) is type(0))
      
  def test_generate_nonce(self):
    DEFAULT_NONCE_LENGTH = 8
    self.assertTrue(len(oauth.generate_nonce()) is DEFAULT_NONCE_LENGTH)
    self.assertTrue(type(oauth.generate_nonce()) is type(''))
      
class OAuthConsumerTest(unittest.TestCase):
  def setUp(self):
    self.key = 'key'
    self.secret = 'secret'
    self.consumer = oauth.OAuthConsumer(self.key, self.secret)
  
  def test_OAuthConsumer_attr_key(self):
    self.assertEqual(self.consumer.key, self.key)

  def test_OAuthConsumer_attr_secret(self):
    self.assertEqual(self.consumer.secret, self.secret)
     
class OAuthTokenTest(unittest.TestCase):
  def setUp(self):
    self.key = 'key'
    self.secret = 'secret'
    self.token = oauth.OAuthToken(self.key, self.secret)
        
  def test_OAuthToken_attr_key(self):
    self.assertEqual(self.token.key, self.key)

  def test_OAuthToken_attr_secret(self):
    self.assertEqual(self.token.secret, self.secret)
      
  def test_to_string(self):
    self.assertEqual(self.token.to_string(), 
                     'oauth_token_secret=secret&oauth_token=key')
    t = oauth.OAuthToken('+', '%')
    self.assertEqual(t.to_string(), 
                     'oauth_token_secret=%25&oauth_token=%2B')

  def test_from_string(self):
    s = 'oauth_token_secret=secret&oauth_token=key'
    t = oauth.OAuthToken.from_string(s)
    self.assertEqual(t.key, 'key')
    self.assertEqual(t.secret, 'secret')
    t = oauth.OAuthToken.from_string('oauth_token_secret=%25&oauth_token=%2B')
    self.assertEqual(t.key, '+')
    self.assertEqual(t.secret, '%')

  def test___str__(self):
    self.assertEqual(str(self.token), 
                     'oauth_token_secret=secret&oauth_token=key')
    t = oauth.OAuthToken('+', '%')
    self.assertEqual(str(t), 'oauth_token_secret=%25&oauth_token=%2B')
        
class OAuthParameters(object):
  CONSUMER_KEY = 'oauth_consumer_key'
  TOKEN = 'oauth_token'
  SIGNATURE_METHOD = 'oauth_signature_method'
  SIGNATURE = 'oauth_signature'
  TIMESTAMP = 'oauth_timestamp'
  NONCE = 'oauth_nonce'
  VERSION = 'oauth_version'
  CALLBACK = 'oauth_callback'
  
  ALL_PARAMETERS = (CONSUMER_KEY,
                    TOKEN,
                    SIGNATURE_METHOD,
                    SIGNATURE,
                    TIMESTAMP,
                    NONCE,
                    VERSION)
    
class OAuthTest(unittest.TestCase):
  def setUp(self):
    self.consumer = oauth.OAuthConsumer('a56b5ff0a637ab283d1d8e32ced37a9c', 
                                        '9a3248210c84b264b56b98c0b872bc8a')
    self.token = oauth.OAuthToken('5b2cafbf20b11bace53b29e37d8a673d', 
                                  '3f71254637df2002d8819458ae4f6c51')
    self.http_url = 'http://dev.alicehub.com/server/api/newsfeed/update/'
    
    self.http_method = HTTP_METHOD_POST

class OAuthRequestTest(OAuthTest):
  def setUp(self):
    super(OAuthRequestTest, self).setUp()
    self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
    
    self.non_oauth_param_message = 'message'
    self.non_oauth_param_context_id = 'context_id'
    self.parameters = {OAuthParameters.CONSUMER_KEY:self.consumer.key,
                       OAuthParameters.TOKEN: self.token.key,
                       OAuthParameters.SIGNATURE_METHOD: 'HMAC-SHA1',
                       OAuthParameters.SIGNATURE:
                       '947ysBZiMn6FGZ11AW06Ioco4mo=',
                       OAuthParameters.TIMESTAMP: '1278573584',
                       OAuthParameters.NONCE: '1770704051',
                       OAuthParameters.VERSION: VERSION,
                       self.non_oauth_param_message:'hey',
                       self.non_oauth_param_context_id:'',}
    oauth_params_string = """ 
      oauth_nonce="1770704051", 
      oauth_timestamp="1278573584", 
      oauth_consumer_key="a56b5ff0a637ab283d1d8e32ced37a9c", 
      oauth_signature_method="HMAC-SHA1", 
      oauth_version="1.0", 
      oauth_token="5b2cafbf20b11bace53b29e37d8a673d", 
      oauth_signature="947ysBZiMn6FGZ11AW06Ioco4mo%3D"
    """
    self.oauth_header_with_realm = {'Authorization': """OAuth 
    realm="http://example.com", %s """ % oauth_params_string}
    self.oauth_header_without_realm = {'Authorization': 'OAuth %s' 
                                       % oauth_params_string}
    
    
    self.additional_param = 'foo'
    self.additional_value = 'bar'
    
    self.oauth_request = oauth.OAuthRequest(self.http_method, 
                                            self.http_url, 
                                            self.parameters)
      
  def test_set_parameter(self):
    self.oauth_request.set_parameter(self.additional_param, 
                                     self.additional_value)
    self.assertEqual(self.oauth_request.get_parameter(self.additional_param), 
                     self.additional_value)
      
  def test_get_parameter(self):
    self.assertRaises(oauth.OAuthError, 
                      self.oauth_request.get_parameter, 
                      self.additional_param)
    self.oauth_request.set_parameter(self.additional_param, 
                                     self.additional_value)
    self.assertEqual(self.oauth_request.get_parameter(self.additional_param), 
                     self.additional_value)
      
  def test__get_timestamp_nonce(self):
    self.assertEqual(self.oauth_request._get_timestamp_nonce(), 
                     (self.parameters[OAuthParameters.TIMESTAMP],
                      self.parameters[OAuthParameters.NONCE]))
    
  def test_get_nonoauth_parameters(self):
    non_oauth_params = self.oauth_request.get_nonoauth_parameters()
    self.assertTrue(non_oauth_params.has_key(self.non_oauth_param_message))
    self.assertFalse(non_oauth_params.has_key(OAuthParameters.CONSUMER_KEY))
      
  def test_to_header(self):
    realm = 'google'
    header_without_realm = self.oauth_request.to_header()\
    .get('Authorization')
    header_with_realm = self.oauth_request.to_header(realm)\
    .get('Authorization')
    self.assertTrue(header_with_realm.find(realm))
    for k in OAuthParameters.ALL_PARAMETERS:
      self.assertTrue(header_without_realm.find(k) > -1)
      self.assertTrue(header_with_realm.find(k) > -1)

  def check_for_params_in_string(self, params, s):
    for k, v in params.iteritems():
      self.assertTrue(s.find(oauth.escape(k)) > -1)
      self.assertTrue(s.find(oauth.escape(v)) > -1)
          
  def test_to_postdata(self):
    post_data = self.oauth_request.to_postdata()
    self.check_for_params_in_string(self.parameters, post_data)
            
  def test_to_url(self):
    GET_url = self.oauth_request.to_url()
    self.assertTrue(GET_url\
                    .find(self.oauth_request.get_normalized_http_url()) > -1)
    self.assertTrue(GET_url.find('?') > -1)
    self.check_for_params_in_string(self.parameters, GET_url)
      
  def test_get_normalized_parameters(self):
    _params = self.parameters.copy()
    normalized_params = self.oauth_request.get_normalized_parameters()
    self.assertFalse(normalized_params\
                     .find(OAuthParameters.SIGNATURE + '=') > -1)
    self.assertTrue(self.parameters.get(OAuthParameters.SIGNATURE) is None)
    
    key_values = [tuple(kv.split('=')) for kv in normalized_params.split('&')]
    del _params[OAuthParameters.SIGNATURE]
    expected_key_values = _params.items()
    expected_key_values.sort()
    
    for k, v in expected_key_values:
      self.assertTrue(expected_key_values.index((k,v))\
                      is key_values.index((oauth.escape(k), oauth.escape(v))))
      
  def test_get_normalized_http_method(self):
    lower_case_http_method = HTTP_METHOD_POST.lower()
    self.oauth_request.http_method = lower_case_http_method
    self.assertEqual(self.oauth_request.get_normalized_http_method(), 
                     lower_case_http_method.upper())
        
  def test_get_normalized_http_url(self):
    url1 = 'HTTP://Example.com:80/resource?id=123'
    expected_url1 = "http://example.com/resource"
    self.oauth_request.http_url = url1
    self.assertEqual(self.oauth_request.get_normalized_http_url(), 
                     expected_url1)
    
    url2 = 'HTTPS://Example.com:443/resource?id=123'
    expected_url2 = "https://example.com/resource"
    self.oauth_request.http_url = url2
    self.assertEqual(self.oauth_request.get_normalized_http_url(), 
                     expected_url2)
    
    url3 = 'HTTP://Example.com:8080/resource?id=123'
    expected_url3 = "http://example.com:8080/resource"
    self.oauth_request.http_url = url3
    self.assertEqual(self.oauth_request.get_normalized_http_url(), 
                     expected_url3)
      
  def test_sign_request(self):
    expected_signature = self.oauth_request.parameters\
    .get(OAuthParameters.SIGNATURE)
    del self.oauth_request.parameters[OAuthParameters.SIGNATURE]
    self.oauth_request.sign_request(self.signature_method, 
                                    self.consumer, 
                                    self.token)
    self.assertEqual(self.oauth_request.parameters\
                     .get(OAuthParameters.SIGNATURE), expected_signature)

  def test_build_signature(self):
    expected_signature = self.oauth_request.parameters\
    .get(OAuthParameters.SIGNATURE)
    self.assertEqual(self.oauth_request.build_signature(self.signature_method, 
                                                        self.consumer,
                                                         self.token), 
                                                         expected_signature)
    
  def test_from_request(self):
    request = oauth.OAuthRequest.from_request(self.http_method, self.http_url, 
                                              self.oauth_header_with_realm, 
                                              {}, 
                                              "message=hey&context_id=")
    self.assertEqual(request.__dict__, self.oauth_request.__dict__)
    self.assertTrue(isinstance(request, oauth.OAuthRequest))
      
  def test_from_consumer_and_token(self):
    request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                                                         self.token, 
                                                         self.http_method, 
                                                         self.http_url)
    self.assertTrue(isinstance(request, oauth.OAuthRequest))
      
  def test_from_token_and_callback(self):
    callback = 'http://example.com'
    request = oauth.OAuthRequest.from_token_and_callback(self.token, 
                                                         callback, 
                                                         self.http_method, 
                                                         self.http_url)
    self.assertTrue(isinstance(request, oauth.OAuthRequest))
    self.assertEqual(request.get_parameter(OAuthParameters.CALLBACK), callback)

  def test__split_header(self):
    del self.parameters[self.non_oauth_param_message]
    del self.parameters[self.non_oauth_param_context_id]
    self.assertEqual(oauth.OAuthRequest._split_header(self\
        .oauth_header_with_realm['Authorization']), self.parameters)
    self.assertEqual(oauth.OAuthRequest._split_header(self\
        .oauth_header_without_realm['Authorization']), self.parameters)

  def test_split_url_string(self):
    qs = "a=1&c=hi%20there&empty="
    expected_result = {'a': '1',
                       'c': 'hi there',
                       'empty': ''}
    self.assertEqual(oauth.OAuthRequest._split_url_string(qs), expected_result)
        
class OAuthServerTest(OAuthTest):
  def setUp(self):
    super(OAuthServerTest, self).setUp()
    self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
    self.data_store = MockOAuthDataStore()
    self.user = MockUser('Foo Bar')
    
    self.request_token_url = "http://example.com/oauth/request_token"
    self.access_token_url = "http://example.com/oauth/access_token"
    
    self.oauth_server = oauth.OAuthServer(self.data_store, 
                      {self.signature_method.get_name():self.signature_method})
      
  def _prepare_request(self, request, token = None):
    request.set_parameter(OAuthParameters.SIGNATURE_METHOD, 
                          self.signature_method.get_name())
    request.set_parameter(OAuthParameters.NONCE, oauth.generate_nonce())
    request.set_parameter(OAuthParameters.TIMESTAMP, 
                          oauth.generate_timestamp())
    request.sign_request(self.signature_method, self.consumer, token)
      
  def _get_token(self, request):
    self._prepare_request(request)
    return self.oauth_server.fetch_request_token(request)
  
  def _get_authorized_token(self, request):
    req_token = self._get_token(request)
    return self.oauth_server.authorize_token(req_token, self.user)
  
  def test_set_data_store(self):
    self.oauth_server.data_store = None
    self.assertTrue(self.oauth_server.data_store is None)
    self.oauth_server.set_data_store(self.data_store)
    self.assertTrue(self.oauth_server.data_store is not None)
    self.assertTrue(isinstance(self.oauth_server.data_store, 
                               oauth.OAuthDataStore))
      
  def test_get_data_store(self):
    self.assertEqual(self.oauth_server.data_store, self.data_store)
        
  def test_add_signature_method(self):
    signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
    self.oauth_server.add_signature_method(signature_method)
    self.assertTrue(isinstance(self.oauth_server.signature_methods\
                               .get(signature_method.get_name()), 
                               oauth.OAuthSignatureMethod_PLAINTEXT))
      
  def test_fetch_request_token(self):
    initial_request = oauth.OAuthRequest.from_consumer_and_token(
                                              self.consumer,
                                              http_method=self.http_method, 
                                              http_url=self.request_token_url
                                              )
    req_token_1 = self._get_token(initial_request)
    authorization_request = oauth.OAuthRequest.from_consumer_and_token(
                                                 self.consumer, 
                                                 req_token_1, 
                                                 http_method=self.http_method, 
                                                 http_url=self.http_url
                                                 )
    req_token_2 = self._get_token(authorization_request)
    self.assertEqual(req_token_1.key, req_token_2.key)
    self.assertEqual(req_token_1.secret, req_token_2.secret)
      
  def _get_token_for_authorization(self):
    request = oauth.OAuthRequest.from_consumer_and_token(
                                             self.consumer,
                                             http_method=self.http_method, 
                                             http_url=self.request_token_url
                                             )
    request_token = self._get_token(request)
    authorization_request = oauth.OAuthRequest.from_consumer_and_token(
                                                 self.consumer, 
                                                 request_token, 
                                                 http_method=self.http_method, 
                                                 http_url=self.http_url
                                                 )
    return self._get_authorized_token(authorization_request)
      
  def test_authorize_token(self):
    authorized_token = self._get_token_for_authorization()
    self.assertTrue(authorized_token is not None)
      
  def _get_access_token_request(self, authorized_token):
    access_token_request = oauth.OAuthRequest.from_consumer_and_token(
                                                self.consumer, 
                                                authorized_token, 
                                                http_method=self.http_method, 
                                                http_url=self.access_token_url
                                                )
    self._prepare_request(access_token_request, authorized_token)
    return access_token_request
      
  def test_fetch_access_token(self):
    authorized_token = self._get_token_for_authorization()
    access_token_request = self._get_access_token_request(authorized_token)
    access_token = self.oauth_server.fetch_access_token(access_token_request)
    self.assertTrue(access_token is not None)
    self.assertNotEqual(str(authorized_token), str(access_token))
    # Try to fetch access_token with used request token
    self.assertRaises(oauth.OAuthError, self.oauth_server.fetch_access_token, 
                      access_token_request)
      
  def test_verify_request(self):
    authorized_token = self._get_token_for_authorization()
    access_token_request = self._get_access_token_request(authorized_token)
    access_token = self.oauth_server.fetch_access_token(access_token_request)
    param1 = 'p1'
    value1 = 'v1'
    api_request = oauth.OAuthRequest.from_consumer_and_token(
                                                 self.consumer, 
                                                 access_token, 
                                                 http_method=self.http_method, 
                                                 http_url=self.http_url, 
                                                 parameters={param1:value1}
                                                 )
    self._prepare_request(api_request, access_token)
    result = self.oauth_server.verify_request(api_request)
    self.assertTrue(result is not None)
    consumer, token, parameters = result
    self.assertEqual(parameters.get(param1), value1)
  
  def test_get_callback(self):
    request = oauth.OAuthRequest.from_consumer_and_token(
                                                 self.consumer, 
                                                 None, 
                                                 http_method=self.http_method, 
                                                 http_url=self.http_url
                                                 )
    self._prepare_request(request)
    cb_url = 'http://example.com/cb'
    request.set_parameter(OAuthParameters.CALLBACK, cb_url)
    self.assertEqual(self.oauth_server.get_callback(request), cb_url)
      
  def test_build_authenticate_header(self):
    self.assertEqual(oauth.build_authenticate_header(), {'WWW-Authenticate': 
                                                         'OAuth realm=""'})
    self.assertEqual(oauth.build_authenticate_header('foo'), 
                     {'WWW-Authenticate': 'OAuth realm="foo"'})
        
class OAuthClientTest(OAuthTest):
  def setUp(self):
    super(OAuthClientTest, self).setUp()
    self.oauth_client = oauth.OAuthClient(self.consumer, self.token)
      
  def test_get_consumer(self):
    consumer = self.oauth_client.get_consumer()
    self.assertTrue(isinstance(consumer, oauth.OAuthConsumer))
    self.assertEqual(consumer.__dict__, self.consumer.__dict__)
      
  def test_get_token(self):
    token = self.oauth_client.get_token()
    self.assertTrue(isinstance(token, oauth.OAuthToken))
    self.assertEqual(token.__dict__, self.token.__dict__)
    
#Mockup OAuthDataStore
TOKEN_TYPE_REQUEST = 'request'
TOKEN_TYPE_ACCESS = 'access'
class MockOAuthDataStore(oauth.OAuthDataStore):
  def __init__(self):
    self.consumer = oauth.OAuthConsumer('a56b5ff0a637ab283d1d8e32ced37a9c', 
                                        '9a3248210c84b264b56b98c0b872bc8a')

    self.consumer_db = {self.consumer.key: self.consumer}
    self.request_token_db = {}
    self.access_token_db = {}
    self.nonce = None
      
  def lookup_consumer(self, key):
    return self.consumer_db.get(key)

  def lookup_token(self, oauth_consumer, token_type, token_field):
    data = None
    if token_type == TOKEN_TYPE_REQUEST:
      data = self.request_token_db.get(token_field)
    elif token_type == TOKEN_TYPE_ACCESS:
      data = self.access_token_db.get(token_field)
    
    if data:
        token, consumer, authenticated_user = data
        if consumer.key == oauth_consumer.key:
          return token
    return None

  def lookup_nonce(self, oauth_consumer, oauth_token, nonce):
    is_used = self.nonce == nonce
    self.nonce = nonce
    return is_used

  def fetch_request_token(self, oauth_consumer):
    token = oauth.OAuthToken("5b2cafbf20b11bace53b29e37d8a673dRT", 
                             "3f71254637df2002d8819458ae4f6c51RT")
    self.request_token_db[token.key] = (token, oauth_consumer, None)
    return token

  def fetch_access_token(self, oauth_consumer, oauth_token):
    data = self.request_token_db.get(oauth_token.key)
    if data:
      del self.request_token_db[oauth_token.key]
      request_token, consumer, authenticated_user = data
      access_token = oauth.OAuthToken("5b2cafbf20b11bace53b29e37d8a673dAT", 
                                      "3f71254637df2002d8819458ae4f6c51AT")
      self.access_token_db[access_token.key] = (access_token, 
                                                consumer, 
                                                authenticated_user)
      return access_token
    else:
      return None

  def authorize_request_token(self, oauth_token, user):
    data = self.request_token_db.get(oauth_token.key)
    if data and data[2] == None:
      request_token, consumer, authenticated_user = data
      authenticated_user = user
      self.request_token_db[request_token.key] = (request_token, 
                                                  consumer, 
                                                  authenticated_user)
      return request_token
    else:
      return None
    
#Mock user
class MockUser(object):
  def __init__(self, name):
    self.name = name
        
def suite():
  return test_config.build_suite([OauthUtilsTest, 
                                OAuthConsumerTest,
                                OAuthTokenTest,
                                OAuthRequestTest,
                                OAuthServerTest,
                                OAuthClientTest])

if __name__ == '__main__':
  unittest.main()