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

"""AppsClient adds Client Architecture to Provisioning API."""


__author__ = '<Shraddha Gupta shraddhag@google.com>'


import gdata.apps.data
import gdata.client
import gdata.service


class AppsClient(gdata.client.GDClient):
  """Client extension for the Google Provisioning API service.

  Attributes:
    host: string The hostname for the Provisioning API service.
    api_version: string The version of the Provisioning API.
  """

  host = 'apps-apis.google.com'
  api_version = '2.0'
  auth_service = 'apps'
  auth_scopes = gdata.gauth.AUTH_SCOPES['apps']

  def __init__(self, domain, auth_token=None, **kwargs):
    """Constructs a new client for the Provisioning API.

    Args:
      domain: string Google Apps domain name.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes client to make calls to Provisioning API.
    """
    gdata.client.GDClient.__init__(self, auth_token=auth_token, **kwargs)
    self.domain = domain

  def _baseURL(self):
    return '/a/feeds/%s' % self.domain

  def _userURL(self):
    return '%s/user/%s' % (self._baseURL(), self.api_version)

  def _nicknameURL(self):
    return '%s/nickname/%s' % (self._baseURL(), self.api_version)

  def RetrieveAllPages(self, feed, desired_class=gdata.data.GDFeed):
    """Retrieve all pages and add all elements.

    Args:
      feed: gdata.data.GDFeed object with linked elements.
      desired_class: type of feed to be returned.

    Returns:
      desired_class: subclass of gdata.data.GDFeed. 
    """

    next = feed.GetNextLink()
    while next is not None:
      next_feed = self.GetFeed(next.href, desired_class=desired_class)
      for a_entry in next_feed.entry:
        feed.entry.append(a_entry)
      next = next_feed.GetNextLink()
    return feed

  def CreateUser(self, user_name, family_name, given_name, password,
                 suspended=False, admin=None, quota_limit=None,
                 password_hash_function=None,
                 agreed_to_terms=None, change_password=None):
    """Create a user account."""

    uri = self._userURL()
    user_entry = gdata.apps.data.UserEntry()
    user_entry.login = gdata.apps.data.Login(user_name=user_name,
        password=password, suspended=suspended, admin=admin,
        hash_function_name=password_hash_function,
        agreed_to_terms=agreed_to_terms,
        change_password=change_password)
    user_entry.name = gdata.apps.data.Name(family_name=family_name,
                                           given_name=given_name)
    return self.Post(user_entry, uri)

  def RetrieveUser(self, user_name):
    """Retrieve a user account.

    Args:
      user_name: string user_name to be retrieved.

    Returns:
      gdata.apps.data.UserEntry
    """

    uri = '%s/%s' % (self._userURL(), user_name)
    return self.GetEntry(uri, desired_class=gdata.apps.data.UserEntry)

  def RetrievePageOfUsers(self, start_username=None):
    """Retrieve one page of users in this domain.

    Args:
      start_username: string user to start from for retrieving a page of users.

    Returns:
      gdata.apps.data.UserFeed
    """

    uri = self._userURL()
    if start_username is not None:
      uri += '?startUsername=%s' % start_username
    return self.GetFeed(uri, desired_class=gdata.apps.data.UserFeed)

  def RetrieveAllUsers(self):
    """Retrieve all users in this domain.

    Returns:
      gdata.apps.data.UserFeed
    """

    ret = self.RetrievePageOfUsers()
    # pagination
    return self.RetrieveAllPages(ret, gdata.apps.data.UserFeed)

  def UpdateUser(self, user_name, user_entry):
    """Update a user account.

    Args:
      user_name: string user_name to be updated.
      user_entry: gdata.apps.data.UserEntry updated user entry.

    Returns:
      gdata.apps.data.UserEntry
    """

    uri = '%s/%s' % (self._userURL(), user_name)
    return self.Update(entry=user_entry, uri=uri)

  def DeleteUser(self, user_name):
    """Delete a user account."""

    uri = '%s/%s' % (self._userURL(), user_name)
    self.Delete(uri)

  def CreateNickname(self, user_name, nickname):
    """Create a nickname for a user.

    Args:
      user_name: string user whose nickname is being created.
      nickname: string nickname.

    Returns:
      gdata.apps.data.NicknameEntry
    """

    uri = self._nicknameURL()
    nickname_entry = gdata.apps.data.NicknameEntry()
    nickname_entry.login = gdata.apps.data.Login(user_name=user_name)
    nickname_entry.nickname = gdata.apps.data.Nickname(name=nickname)
    return self.Post(nickname_entry, uri)

  def RetrieveNickname(self, nickname):
    """Retrieve a nickname.

    Args:
      nickname: string nickname to be retrieved.

    Returns:
      gdata.apps.data.NicknameEntry
    """

    uri = '%s/%s' % (self._nicknameURL(), nickname)
    return self.GetEntry(uri, desired_class=gdata.apps.data.NicknameEntry)

  def RetrieveNicknames(self, user_name):
    """Retrieve nicknames of the user.

    Args:
      user_name: string user whose nicknames are retrieved.

    Returns:
      gdata.apps.data.NicknameFeed
    """

    uri = '%s?username=%s' % (self._nicknameURL(), user_name)
    ret = self.GetFeed(uri, desired_class=gdata.apps.data.NicknameFeed)
    # pagination
    return self.RetrieveAllPages(ret, gdata.apps.data.NicknameFeed)

  def DeleteNickname(self, nickname):
    """Delete a nickname."""

    uri = '%s/%s' % (self._nicknameURL(), nickname)
    self.Delete(uri)
