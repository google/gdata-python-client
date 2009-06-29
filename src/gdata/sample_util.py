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


"""Provides utility functions used with command line samples."""

# This module is used for version 2 of the Google Data APIs.

import sys
import getpass
import gdata.gauth

__author__ = 'j.s@google.com (Jeff Scudder)'


CLIENT_LOGIN = 1
AUTHSUB = 2
OAUTH = 3


def get_param(name, prompt='', secret=False, ask=True):
  # First, check for a command line parameter.
  for i in xrange(len(sys.argv)):
    if sys.argv[i].startswith('--%s=' % name):
      return sys.argv[i].split('=')[1]
    elif sys.argv[i] == '--%s' % name:
      return sys.argv[i + 1]
  if ask:
    # If it was not on the command line, ask the user to input the value.
    prompt = '%s: ' % prompt
    if secret:
      return getpass.getpass(prompt)
    else:
      return raw_input(prompt)
  else:
    return None


def authorize_client(client, auth_type=None, service=None, source=None,
                     scopes=None):
  """Uses command line arguments, or prompts user for token values."""
  if auth_type is None:
    auth_type = int(get_param(
        'auth_type', 'Please choose the authorization mechanism you want'
        ' to use.\n'
        '1. to use your email address and password (ClientLogin)\n'
        '2. to use a web browser to visit an auth web page (AuthSub)\n'
        '3. if you have registed to use OAuth\n'))

  if auth_type == CLIENT_LOGIN:
    email = get_param('email', 'Please enter your username')
    password = get_param('password', 'Password', True)
    if service is None:
      service = get_param(
          'service', 'What is the name of the service you wish to access?'
          '\n(See list:'
          ' http://code.google.com/apis/gdata/faq.html#clientlogin)')
    if source is None:
      source = get_param('source', ask=False)
    client.client_login(email, password, source=source, service=service)
  elif auth_type == AUTHSUB:
    auth_sub_token = get_param('auth_sub_token', ask=False)
    session_token = get_param('session_token', ask=False)
    if scopes is None:
      scopes = get_param(
          'scopes', 'Enter the URL prefixes (scopes) for the resources you '
          'would like to access.\nFor multiple scope URLs, place a comma '
          'between each URL.\n'
          'Example: http://www.google.com/calendar/feeds/,'
          'http://www.google.com/m8/feeds/\n').split(',')
    if client.auth_token is None:
      if session_token:
        client.auth_token = gdata.gauth.AuthSubToken(session_token, scopes)
        return
      elif auth_sub_token:
        client.auth_token = gdata.gauth.AuthSubToken(auth_sub_token, scopes)
        client.upgrade_token()
        return

      auth_url = gdata.gauth.generate_auth_sub_url(
          'http://gauthmachine.appspot.com/authsub', scopes)
      print 'Visit the following URL in your browser to authorize this app:'
      print str(auth_url)
      print 'After agreeing to authorize the app, copy the token value from the'
      print ' URL. Example: "www.google.com/?token=ab12" token value is ab12'
      token_value = raw_input('Please enter the token value: ')
      single_use_token = gdata.gauth.AuthSubToken(token_value, scopes)
      client.auth_token = single_use_token
      client.upgrade_token()
  elif auth_type == OAUTH:
    pass
  else:
    print 'Invalid authorization type.'
    return None


def print_options():
  """Displays usage information, available command line params."""
  # TODO: fill in the usage description for authorizing the client.
  print ''
  
