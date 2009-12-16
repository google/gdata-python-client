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

"""Sample Google Analytics Data Export API Data Feed application.

This sample demonstrates how to make requests and retrieve the important
information from the Google Analytics Data Export API Data Feed. This
sample requires a Google Analytics username and password and uses the
Client Login authorization routine.

  Class DataFeedDemo: Prints all the important Data Feed informantion.
"""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import gdata.analytics.client
import gdata.sample_util

def main():
  """Main function for the sample."""

  demo = DataFeedDemo()
  demo.PrintFeedDetails()
  demo.PrintDataSources()
  demo.PrintFeedAggregates()
  demo.PrintSegmentInfo()
  demo.PrintOneEntry()
  demo.PrintFeedTable()


class DataFeedDemo(object):
  """Gets data from the Data Feed.

  Attributes:
    data_feed: Google Analytics AccountList returned form the API.
  """

  def __init__(self):
    """Inits DataFeedDemo."""

    SOURCE_APP_NAME = 'Google-dataFeedDemoPython-v1'
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

    table_id = gdata.sample_util.get_param(
        name='table_id',
        prompt='Please enter your Google Analytics Table id (format ga:xxxx)')

    # DataFeedQuery simplifies constructing API queries and uri encodes params.
    data_query = gdata.analytics.client.DataFeedQuery({
        'ids': table_id,
        'start-date': '2008-10-01',
        'end-date': '2008-10-30',
        'dimensions': 'ga:source,ga:medium',
        'metrics': 'ga:visits',
        'sort': '-ga:visits',
        'filters': 'ga:medium==referral',
        'max-results': '50'})

    self.feed = my_client.GetDataFeed(data_query)

  def PrintFeedDetails(self):
    """Prints important Analytics related data found at the top of the feed."""

    print '\n-------- Feed Data --------'
    print 'Feed Title          = ' + self.feed.title.text
    print 'Feed Id             = ' + self.feed.id.text
    print 'Total Results Found = ' + self.feed.total_results.text
    print 'Start Index         = ' + self.feed.start_index.text
    print 'Results Returned    = ' + self.feed.items_per_page.text
    print 'Start Date          = ' + self.feed.start_date.text
    print 'End Date            = ' + self.feed.end_date.text

  def PrintDataSources(self):
    """Prints data found in the data source elements.

    This data has information about the Google Analytics account the referenced
    table ID belongs to. Note there is currently exactly one data source in
    the data feed.
    """

    data_source = self.feed.data_source[0]

    print '\n-------- Data Source Data --------'
    print 'Table ID        = ' + data_source.table_id.text
    print 'Table Name      = ' + data_source.table_name.text
    print 'Web Property Id = ' + data_source.GetProperty('ga:webPropertyId').value
    print 'Profile Id      = ' + data_source.GetProperty('ga:profileId').value
    print 'Account Name    = ' + data_source.GetProperty('ga:accountName').value

  def PrintFeedAggregates(self):
    """Prints data found in the aggregates elements.

    This contains the sum of all the metrics defined in the query across.
    This sum spans all the rows matched in the feed.total_results property
    and not just the rows returned by the response.
    """

    aggregates = self.feed.aggregates

    print '\n-------- Metric Aggregates --------'
    for met in aggregates.metric:
      print ''
      print 'Metric Name  = ' + met.name
      print 'Metric Value = ' + met.value
      print 'Metric Type  = ' + met.type
      print 'Metric CI    = ' + met.confidence_interval

  def PrintSegmentInfo(self):
    """Prints segment information if the query has advanced segments
    defined."""

    if self.feed.segment:
      print '-------- Advanced Segments Information --------'
      for segment in self.feed.segment:
        print 'Segment Name       = ' + segment.name
        print 'Segment Id         = ' + segment.id
        print 'Segment Definition = ' + segment.definition.value

  def PrintOneEntry(self):
    """Prints all the important Google Analytics data found in an entry"""

    print '\n-------- One Entry --------'
    if len(self.feed.entry) == 0:
      print 'No entries found'
      return

    entry = self.feed.entry[0]
    print 'ID      = ' + entry.id.text

    for dim in entry.dimension:
      print 'Dimension Name  = ' + dim.name
      print 'Dimension Value = ' + dim.value

    for met in entry.metric:
      print 'Metric Name     = ' + met.name
      print 'Metric Value    = ' + met.value
      print 'Metric Type     = ' + met.type
      print 'Metric CI       = ' + met.confidence_interval

  def PrintFeedTable(self):
    """Prints all the entries as a table."""

    print '\n-------- All Entries In a Table --------'
    for entry in self.feed.entry:
      for dim in entry.dimension:
        print ('Dimension Name = %s \t Dimension Value = %s'
            % (dim.name, dim.value))
      for met in entry.metric:
        print ('Metric Name    = %s \t Metric Value    = %s'
            % (dim.name, dim.value))
      print '---'


if __name__ == '__main__':
  main()

