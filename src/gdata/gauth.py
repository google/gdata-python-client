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


import urllib


__author__ = 'j.s@google.com (Jeff Scudder)'


PROGRAMMATIC_AUTH_LABEL = 'GoogleLogin auth='
AUTHSUB_AUTH_LABEL = 'AuthSub token='


def generate_client_login_request_body(email, password, service, source, 
    account_type='HOSTED_OR_GOOGLE', captcha_token=None, 
    captcha_response=None):
  """Creates the body of the autentication request

  See http://code.google.com/apis/accounts/AuthForInstalledApps.html#Request
  for more details.

  Args:
    email: str
    password: str
    service: str
    source: str
    account_type: str (optional) Defaul is 'HOSTED_OR_GOOGLE', other valid
        values are 'GOOGLE' and 'HOSTED'
    captcha_token: str (optional)
    captcha_response: str (optional)

  Returns:
    The HTTP body to send in a request for a client login token.
  """
  # Create a POST body containing the user's credentials.
  request_fields = {'Email': email,
                    'Passwd': password,
                    'accountType': account_type,
                    'service': service,
                    'source': source}
  if captcha_token and captcha_response:
    # Send the captcha token and response as part of the POST body if the
    # user is responding to a captch challenge.
    request_fields['logintoken'] = captcha_token
    request_fields['logincaptcha'] = captcha_response
  return urllib.urlencode(request_fields)


GenerateClientLoginRequestBody = generate_client_login_request_body


def get_client_login_token_string(http_body):
  """Returns the token value for a ClientLoginToken.

  Reads the token from the server's response to a Client Login request and
  creates the token value string to use in requests.

  Args:
    http_body: str The body of the server's HTTP response to a Client Login
        request
 
  Returns:
    The token value string for a ClientLoginToken.
  """
  for response_line in http_body.splitlines():
    if response_line.startswith('Auth='):
      # Strip off the leading Auth= and return the Authorization value.
      return response_line[5:]
  return None


GetClientLoginTokenString = get_client_login_token_string


def get_captcha_challenge(http_body, 
    captcha_base_url='http://www.google.com/accounts/'):
  """Returns the URL and token for a CAPTCHA challenge issued by the server.

  Args:
    http_body: str The body of the HTTP response from the server which 
        contains the CAPTCHA challenge.
    captcha_base_url: str This function returns a full URL for viewing the 
        challenge image which is built from the server's response. This
        base_url is used as the beginning of the URL because the server
        only provides the end of the URL. For example the server provides
        'Captcha?ctoken=Hi...N' and the URL for the image is
        'http://www.google.com/accounts/Captcha?ctoken=Hi...N'

  Returns:
    A dictionary containing the information needed to repond to the CAPTCHA
    challenge, the image URL and the ID token of the challenge. The 
    dictionary is in the form:
    {'token': string identifying the CAPTCHA image,
     'url': string containing the URL of the image}
    Returns None if there was no CAPTCHA challenge in the response.
  """
  contains_captcha_challenge = False
  captcha_parameters = {}
  for response_line in http_body.splitlines():
    if response_line.startswith('Error=CaptchaRequired'):
      contains_captcha_challenge = True
    elif response_line.startswith('CaptchaToken='):
      # Strip off the leading CaptchaToken=
      captcha_parameters['token'] = response_line[13:]
    elif response_line.startswith('CaptchaUrl='):
      captcha_parameters['url'] = '%s%s' % (captcha_base_url,
          response_line[11:])
  if contains_captcha_challenge:
    return captcha_parameters
  else:
    return None


GetCaptchaChallenge = get_captcha_challenge


class ClientLoginToken(object):

  def __init__(self, token_string):
    self.token_string = token_string

  def modify_request(self, http_request):
    http_request.headers['Authorization'] = 'GoogleLogin auth=%s' % (
        self.token_string,)

  ModifyRequest = modify_request
