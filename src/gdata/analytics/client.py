#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.
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

"""AnalyticsClient extends gdata.client.GDClient to streamline
Google Analytics Data Export API calls."""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import atom.data
import gdata.client
import gdata.analytics.data
import gdata.gauth


class AnalyticsClient(gdata.client.GDClient):
  """Client extension for the Google Analytics API service."""

  api_version = '2'
  auth_service = 'analytics'
  auth_scopes = gdata.gauth.AUTH_SCOPES['analytics']
  account_type = 'GOOGLE'

  def __init__(self, auth_token=None, **kwargs):
    """Constructs a new client for the Google Analytics Data Export API.

    Args:
      auth_token: gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken (optional) Authorizes this client to edit the user's data.
      kwargs: The other parameters to pass to gdata.client.GDClient
          constructor.
    """

    gdata.client.GDClient.__init__(self, auth_token=auth_token, **kwargs)

  def get_account_feed(self, feed_uri, auth_token=None, **kwargs):
    """Makes a request to the Analytics API Account Feed.

    Args:
      feed_uri: str or gdata.analytics.AccountFeedQuery The Analytics Account
          Feed uri to define what data to retrieve from the API. Can also be
          used with a gdata.analytics.AccountFeedQuery object.
    """

    return self.get_feed(feed_uri,
                         desired_class=gdata.analytics.data.AccountFeed,
                         auth_token=auth_token,
                         **kwargs)

  GetAccountFeed = get_account_feed

  def get_data_feed(self, feed_uri, auth_token=None, **kwargs):
    """Makes a request to the Analytics API Data Feed.

    Args:
      feed_uri: str or gdata.analytics.AccountFeedQuery The Analytics Data
          Feed uri to define what data to retrieve from the API. Can also be
          used with a gdata.analytics.AccountFeedQuery object.
    """

    return self.get_feed(feed_uri,
                         desired_class=gdata.analytics.data.DataFeed,
                         auth_token=auth_token,
                         **kwargs)

  GetDataFeed = get_data_feed


class AccountFeedQuery(gdata.client.GDQuery):
  """Account Feed query class to simplify constructing Account Feed Urls.

  To use this class, you can either pass a dict in the constructor that has
  all the data feed query parameters as keys.
     queryUrl = DataFeedQuery({'max-results': '10000'})

  Alternatively you can add new parameters directly to the query object.
     queryUrl = DataFeedQuery()
     queryUrl.query['max-results'] = '10000'

  Args:
    query: dict (optional) Contains all the GA Data Feed query parameters
        as keys.
  """

  scheme = 'https'
  host = 'www.google.com'
  path = '/analytics/feeds/accounts/default'

  def __init__(self, query=None, **kwargs):
    self.query = query or {}
    gdata.client.GDQuery(self, **kwargs)


class DataFeedQuery(gdata.client.GDQuery):
  """Data Feed query class to simplify constructing Data Feed Urls.

  To use this class, you can either pass a dict in the constructor that has
  all the data feed query parameters as keys.
     queryUrl = DataFeedQuery({'start-date': '2008-10-01'})

  Alternatively you can add new parameters directly to the query object.
     queryUrl = DataFeedQuery()
     queryUrl.query['start-date'] = '2008-10-01'

  Args:
    query: dict (optional) Contains all the GA Data Feed query parameters
        as keys.
  """

  scheme = 'https'
  host = 'www.google.com'
  path = '/analytics/feeds/data'

  def __init__(self, query=None, **kwargs):
    self.query = query or {}
    gdata.client.GDQuery(self, **kwargs)

