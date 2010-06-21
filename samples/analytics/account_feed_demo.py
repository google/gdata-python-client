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
  demo.PrintAdvancedSegments()
  demo.PrintCustomVarForOneEntry()
  demo.PrintGoalsForOneEntry()
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

    print '-------- Important Feed Data --------'
    print 'Feed Title          = ' + self.feed.title.text
    print 'Feed Id             = ' + self.feed.id.text
    print 'Total Results Found = ' + self.feed.total_results.text
    print 'Start Index         = ' + self.feed.start_index.text
    print 'Results Returned    = ' + self.feed.items_per_page.text

  def PrintAdvancedSegments(self):
    """Prints the advanced segments for this user."""

    print '-------- Advances Segments --------'
    if not self.feed.segment:
      print 'No advanced segments found'
    else:
      for segment in self.feed.segment:
        print 'Segment Name       = ' + segment.name
        print 'Segment Id         = ' + segment.id
        print 'Segment Definition = ' + segment.definition.text

  def PrintCustomVarForOneEntry(self):
    """Prints custom variable information for the first profile that has
    custom variable configured."""

    print '-------- Custom Variables --------'
    if not self.feed.entry:
      print 'No entries found'
    else:
      for entry in self.feed.entry:
        if entry.custom_variable:
          for custom_variable in entry.custom_variable:
            print 'Custom Variable Index = ' + custom_variable.index
            print 'Custom Variable Name  = ' + custom_variable.name
            print 'Custom Variable Scope = ' + custom_variable.scope
          return
      print 'No custom variables defined for this user'

  def PrintGoalsForOneEntry(self):
    """Prints All the goal information for one profile."""

    print '-------- Goal Configuration --------'
    if not self.feed.entry:
      print 'No entries found'
    else:
      for entry in self.feed.entry:
        if entry.goal:
          for goal in entry.goal:
            print 'Goal Number = ' + goal.number
            print 'Goal Name   = ' + goal.name
            print 'Goal Value  = ' + goal.value
            print 'Goal Active = ' + goal.active

            if goal.destination:
              self.PrintDestinationGoal(goal.destination)
            elif goal.engagement:
              self.PrintEngagementGoal(goal.engagement)
          return

  def PrintDestinationGoal(self, destination):
    """Prints the important information for destination goals including all
    the configured steps if they exist.

    Args:
      destination: gdata.data.Destination The destination goal configuration.
    """

    print '----- Destination Goal -----'
    print 'Expression      = ' + destination.expression
    print 'Match Type      = ' + destination.match_type
    print 'Step 1 Required = ' + destination.step1_required
    print 'Case Sensitive  = ' + destination.case_sensitive

    # Print goal steps.
    if destination.step:
      print '----- Destination Goal Steps -----'
      for step in destination.step:
        print 'Step Number = ' + step.number
        print 'Step Name   = ' + step.name
        print 'Step Path   = ' + step.path

  def PrintEngagementGoal(self, engagement):
    """Prints the important information for engagement goals.

    Args:
      engagement: gdata.data.Engagement The engagement goal configuration.
    """

    print '----- Engagement Goal -----'
    print 'Goal Type       = ' + engagement.type
    print 'Goal Engagement = ' + engagement.comparison
    print 'Goal Threshold  = ' + engagement.threshold_value

  def PrintAccountEntries(self):
    """Prints important Analytics data found in each account entry"""

    print '-------- First 1000 Profiles in Account Feed --------'
    if not self.feed.entry:
      print 'No entries found'
    else:
      for entry in self.feed.entry:
        print 'Web Property ID = ' + entry.GetProperty('ga:webPropertyId').value
        print 'Account Name    = ' + entry.GetProperty('ga:accountName').value
        print 'Account Id      = ' + entry.GetProperty('ga:accountId').value
        print 'Profile Name    = ' + entry.title.text
        print 'Profile ID      = ' + entry.GetProperty('ga:profileId').value
        print 'Table ID        = ' + entry.table_id.text
        print 'Currency        = ' + entry.GetProperty('ga:currency').value
        print 'TimeZone        = ' + entry.GetProperty('ga:timezone').value
        if entry.custom_variable:
          print 'This profile has custom variables'
        if entry.goal:
          print 'This profile has goals'


if __name__ == '__main__':
  main()

