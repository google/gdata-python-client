#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data model classes for the Provisioning API."""


__author__ = 'Shraddha Gupta shraddhag@google.com>'


import atom.core
import atom.data
import gdata.apps
import gdata.data


class Login(atom.core.XmlElement):

  _qname = gdata.apps.APPS_TEMPLATE % 'login'
  user_name = 'userName'
  password = 'password'
  hash_function_name = 'hashFunctionName'
  suspended = 'suspended'
  admin = 'admin'
  agreed_to_terms = 'agreedToTerms'
  change_password = 'changePasswordAtNextLogin'
  ip_whitelisted = 'ipWhitelisted'


class Name(atom.core.XmlElement):

  _qname = gdata.apps.APPS_TEMPLATE % 'name'
  given_name = 'givenName'
  family_name = 'familyName'


class Quota(atom.core.XmlElement):

  _qname = gdata.apps.APPS_TEMPLATE % 'quota'
  limit = 'limit'


class UserEntry(gdata.data.GDEntry):

  _qname = atom.data.ATOM_TEMPLATE % 'entry'
  login = Login
  name = Name
  quota = Quota


class UserFeed(gdata.data.GDFeed):

  entry = [UserEntry]


class Nickname(atom.core.XmlElement):

  _qname = gdata.apps.APPS_TEMPLATE % 'nickname'
  name = 'name'


class NicknameEntry(gdata.data.GDEntry):

  _qname = atom.data.ATOM_TEMPLATE % 'entry'
  nickname = Nickname
  login = Login


class NicknameFeed(gdata.data.GDFeed):

  entry = [NicknameEntry]
