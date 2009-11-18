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

"""Sample Google Analytics Data Export API Account Feed application.

This sample demonstrates how to retrieve the important data from the Google
Analytics Data Export API Account feed using the Python Client library. This
requires a Google Analytics username and password and uses the Client Login
authorization routine.

  Class AccountFeedDemo: Prints all the import Account Feed data.
"""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import gdata.analytics.client
import gdata.sample_util

def main():
  """Main fucntion for the sample."""

  demo = AccountFeedDemo()
  demo.PrintFeedDetails()
  demo.PrintAccountEntries()


class AccountFeedDemo(object):
  """Prints the Google Analytics account feed

  Attributes:
    account_feed: Google Analytics AccountList returned form the API.
  """

  def __init__(self):
    """Inits AccountFeedDemo."""

    SOURCE_APP_NAME = 'Google-accountFeedDemoPython-v1'
    my_client = gdata.analytics.client.AnalyticsClient(source=SOURCE_APP_NAME)

    try:
      gdata.sample_util.authorize_client(
          my_client,
          service=my_client.auth_service,
          source=SOURCE_APP_NAME,
          scopes=['https://www.google.com/analytics/feeds/'])
    except gdata.client.BadAuthentication:
      exit('Invalid user credentials given.')
    except gdata.client.Error:
      exit('Login Error')

    account_query = gdata.analytics.client.AccountFeedQuery()
    self.feed = my_client.GetAccountFeed(account_query)

  def PrintFeedDetails(self):
    """Prints important Analytics related data found at the top of the feed."""

    print 'Feed Title          = ' + self.feed.title.text
    print 'Feed Id             = ' + self.feed.id.text
    print 'Total Results Found = ' + self.feed.total_results.text
    print 'Start Index         = ' + self.feed.start_index.text
    print 'Results Returned    = ' + self.feed.items_per_page.text

  def PrintAccountEntries(self):
    """Prints important Analytics data found in each entry"""

    for entry in self.feed.entry:
      print '--------------------------'
      print 'Profile Name     = ' + entry.title.text
      print 'Table ID         = ' + entry.table_id.text
      print 'Account Name     = ' + entry.GetProperty('ga:accountId').value
      print 'Profile ID       = ' + entry.GetProperty('ga:accountName').value
      print 'Web Property ID  = ' + entry.GetProperty('ga:webPropertyId').value
      print 'Profile Currency = ' + entry.GetProperty('ga:currency').value
      print 'Profile TimeZone = ' + entry.GetProperty('ga:timezone').value


if __name__ == '__main__':
  main()

