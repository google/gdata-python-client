#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

"""Google Analytics Management API Demo.

This script demonstrates how to retrieve the important data from the Google
Analytics Data Management API using the Python Client library. This example
requires a Google Analytics account with data and a username and password.
Each feed in the Management API is retrieved and printed using the respective
print method in ManagementFeedDemo. To simplify setting filters and query
parameters, each feed has it's own query class. Check the
<code>gdata.analytics.client</code> module for more details on usage.

  main: The main method of this example.
  GetAnalyticsClient: Returns an authorized AnalyticsClient object.
  Class ManagementFeedDemo: Prints all the import Account Feed data.
"""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import gdata.analytics.client
import gdata.sample_util


ACCOUNT_ID = '~all'
WEB_PROPERTY_ID = '~all'
PROFILE_ID = '~all'


def main():
  """Main example script. Un-comment each method to print the feed."""

  demo = ManagementFeedDemo(GetAnalyticsClient())
  demo.PrintAccountFeed()
  # demo.PrintWebPropertyFeed()
  # demo.PrintProfileFeed()
  # demo.PrintGoalFeed()
  # demo.PrintSegmentFeed()


def GetAnalyticsClient():
  """Returns an authorized GoogleAnalayticsClient object.

  Uses the Google Data python samples wrapper to prompt the user for
  credentials then tries to authorize the client object with the
  Google Analytics API.

  Returns:
    An authorized GoogleAnalyticsClient object.
  """

  SOURCE_APP_NAME = 'Analytics-ManagementAPI-Demo-v1'
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

  return my_client


class ManagementFeedDemo(object):
  """The main demo for the management feed.

  Attributes:
    my_client: gdata.analytics.client The AnalyticsClient object for this demo.
  """

  def __init__(self, my_client):
    """Initializes the ManagementFeedDemo class.

    Args:
      my_client: gdata.analytics.client An authorized GoogleAnalyticsClient
          object.
    """
    self.my_client = my_client

  def PrintAccountFeed(self):
    """Requests and prints the important data in the Account Feed.

    Note:
      AccountQuery is used for the ManagementAPI.
      AccountFeedQuery is used for the Data Export API.
    """

    account_query = gdata.analytics.client.AccountQuery()
    results = self.my_client.GetManagementFeed(account_query)

    print '-------- Account Feed Data --------'
    if not results.entry:
      print 'no entries found'
    else:
      for entry in results.entry:
        print 'Account Name    = ' + entry.GetProperty('ga:accountName').value
        print 'Account ID      = ' + entry.GetProperty('ga:accountId').value
        print 'Child Feed Link = ' + entry.GetChildLink('analytics#webproperties').href
        print

  def PrintWebPropertyFeed(self):
    """Requests and prints the important data in the Web Property Feed."""

    web_property_query = gdata.analytics.client.WebPropertyQuery(
        acct_id=ACCOUNT_ID)
    results = self.my_client.GetManagementFeed(web_property_query)

    print '-------- Web Property Feed Data --------'
    if not results.entry:
      print 'no entries found'
    else:
      for entry in results.entry:
        print 'Account ID      = ' + entry.GetProperty('ga:accountId').value
        print 'Web Property ID = ' + entry.GetProperty('ga:webPropertyId').value
        print 'Child Feed Link = ' + entry.GetChildLink('analytics#profiles').href
        print

  def PrintProfileFeed(self):
    """Requests and prints the important data in the Profile Feed.

    Note:
      TableId has a different namespace (dxp:) than all the
      other properties (ga:).
    """

    profile_query = gdata.analytics.client.ProfileQuery(
        acct_id=ACCOUNT_ID, web_prop_id=WEB_PROPERTY_ID)
    results = self.my_client.GetManagementFeed(profile_query)

    print '-------- Profile Feed Data --------'
    if not results.entry:
      print 'no entries found'
    else:
      for entry in results.entry:
        print 'Account ID      = ' + entry.GetProperty('ga:accountId').value
        print 'Web Property ID = ' + entry.GetProperty('ga:webPropertyId').value
        print 'Profile ID      = ' + entry.GetProperty('ga:profileId').value
        print 'Currency        = ' + entry.GetProperty('ga:currency').value
        print 'Timezone        = ' + entry.GetProperty('ga:timezone').value
        print 'TableId         = ' + entry.GetProperty('dxp:tableId').value
        print 'Child Feed Link = ' + entry.GetChildLink('analytics#goals').href
        print

  def PrintGoalFeed(self):
    """Requests and prints the important data in the Goal Feed.

    Note:
      There are two types of goals, destination and engagement which need to
      be handled differently.
    """

    goal_query = gdata.analytics.client.GoalQuery(
        acct_id=ACCOUNT_ID, web_prop_id=WEB_PROPERTY_ID, profile_id=PROFILE_ID)
    results = self.my_client.GetManagementFeed(goal_query)

    print '-------- Goal Feed Data --------'
    if not results.entry:
      print 'no entries found'
    else:
      for entry in results.entry:
        print 'Goal Number = ' + entry.goal.number
        print 'Goal Name   = ' + entry.goal.name
        print 'Goal Value  = ' + entry.goal.value
        print 'Goal Active = ' + entry.goal.active

        if entry.goal.destination:
          self.PrintDestinationGoal(entry.goal.destination)
        elif entry.goal.engagement:
          self.PrintEngagementGoal(entry.goal.engagement)

  def PrintDestinationGoal(self, destination):
    """Prints the important information for destination goals including all
    the configured steps if they exist.

    Args:
      destination: gdata.data.Destination The destination goal configuration.
    """

    print '\t----- Destination Goal -----'
    print '\tExpression      = ' + destination.expression
    print '\tMatch Type      = ' + destination.match_type
    print '\tStep 1 Required = ' + destination.step1_required
    print '\tCase Sensitive  = ' + destination.case_sensitive

    if destination.step:
      print '\t\t----- Destination Goal Steps -----'
      for step in destination.step:
        print '\t\tStep Number = ' + step.number
        print '\t\tStep Name   = ' + step.name
        print '\t\tStep Path   = ' + step.path
        print

  def PrintEngagementGoal(self, engagement):
    """Prints the important information for engagement goals.

    Args:
      engagement: gdata.data.Engagement The engagement goal configuration.
    """

    print '\t----- Engagement Goal -----'
    print '\tGoal Type       = ' + engagement.type
    print '\tGoal Engagement = ' + engagement.comparison
    print '\tGoal Threshold  = ' + engagement.threshold_value
    print

  def PrintSegmentFeed(self):
    """Requests and prints the important data in the Profile Feed."""

    adv_seg_query = gdata.analytics.client.AdvSegQuery()
    results = self.my_client.GetManagementFeed(adv_seg_query)

    print '-------- Advanced Segment Feed Data --------'
    if not results.entry:
      print 'no entries found'
    else:
      for entry in results.entry:
        print 'Segment ID          = ' + entry.segment.id
        print 'Segment Name        = ' + entry.segment.name
        print 'Segment Definition  = ' + entry.segment.definition.text
        print

if __name__ == '__main__':
  main()

