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

"""Unit Tests for Google Analytics Account Feed and Data Feed.

AccountFeedTest: All unit tests for AccountFeed class.
DataFeedTest: All unit tests for DataFeed class.
"""

__author__ = 'api.nickm@google.com (Nick Mihailovski)'


import unittest
from gdata import test_data
import gdata.analytics.data
import atom.core
import gdata.test_config as conf


class AccountFeedTest(unittest.TestCase):
  """Unit test for all custom elements in the Account Feed."""

  def setUp(self):
    """Retrieves the test XML feed into a AccountFeed object."""
    self.feed = atom.core.parse(test_data.ANALYTICS_ACCOUNT_FEED,
                                gdata.analytics.data.AccountFeed)

  def testSegment(self):
    """Tests Segment class in Google Analytics Account Feed."""

    segment = self.feed.segment[0]
    self.assertEquals(segment.id, 'gaid::-11')
    self.assertEquals(segment.name, 'Visits from iPhones')

  def testSegmentDefinition(self):
    """Tests Definition class in Google Analytics Account Feed."""

    definition = self.feed.segment[0].definition
    self.assertEquals(definition.text, 'ga:operatingSystem==iPhone')

  def testEntryTableId(self):
    """Tests custom classes in Google Analytics Account Feed."""

    entry = self.feed.entry[0]
    self.assertEquals(entry.table_id.text, 'ga:1174')

  def testEntryProperty(self):
    """Tests the property classes in Google Analytics Account Feed."""
    property = self.feed.entry[0].property

    self.assertEquals(property[0].name, 'ga:accountId')
    self.assertEquals(property[0].value, '30481')

    self.assertEquals(property[1].name, 'ga:accountName')
    self.assertEquals(property[1].value, 'Google Store')

    self.assertEquals(property[2].name, 'ga:profileId')
    self.assertEquals(property[2].value, '1174')

    self.assertEquals(property[3].name, 'ga:webPropertyId')
    self.assertEquals(property[3].value, 'UA-30481-1')

    self.assertEquals(property[4].name, 'ga:currency')
    self.assertEquals(property[4].value, 'USD')

    self.assertEquals(property[5].name, 'ga:timezone')
    self.assertEquals(property[5].value, 'America/Los_Angeles')

  def testEntryGetProperty(self):
    """Tests GetProperty inherited class in the AccountEntry class."""

    entry = self.feed.entry[0]
    self.assertEquals(entry.GetProperty('ga:accountId').value, '30481')
    self.assertEquals(entry.GetProperty('ga:accountName').value, 'Google Store')
    self.assertEquals(entry.GetProperty('ga:profileId').value, '1174')
    self.assertEquals(entry.GetProperty('ga:webPropertyId').value, 'UA-30481-1')
    self.assertEquals(entry.GetProperty('ga:currency').value, 'USD')
    self.assertEquals(entry.GetProperty('ga:timezone').value, 'America/Los_Angeles')

  def testGoal(self):
    """Tests Goal class in Google Anlaytics Account Feed."""

    goal = self.feed.entry[0].goal[0]
    self.assertEquals(goal.number, '1')
    self.assertEquals(goal.name, 'Completing Order')
    self.assertEquals(goal.value, '10.0')
    self.assertEquals(goal.active, 'true')

  def testDestination(self):
    """Tests Destination class in Google Analytics Account Feed."""

    destination = self.feed.entry[0].goal[0].destination
    self.assertEquals(destination.expression, '/purchaseComplete.html')
    self.assertEquals(destination.case_sensitive, 'false')
    self.assertEquals(destination.match_type, 'regex')
    self.assertEquals(destination.step1_required, 'false')

  def testStep(self):
    """Tests Step class in Google Analytics Account Feed."""

    step = self.feed.entry[0].goal[0].destination.step[0]
    self.assertEquals(step.number, '1')
    self.assertEquals(step.name, 'View Product Categories')
    self.assertEquals(step.path, '/Apps|Accessories|Fun|Kid\+s|Office')

  def testEngagemet(self):
    """Tests Engagement class in Google Analytics Account Feed."""

    engagement = self.feed.entry[0].goal[1].engagement
    self.assertEquals(engagement.type, 'timeOnSite')
    self.assertEquals(engagement.comparison, '>')
    self.assertEquals(engagement.threshold_value, '300')

  def testCustomVariable(self):
    """Tests CustomVariable class in Google Analytics Account Feed."""

    customVar = self.feed.entry[0].custom_variable[0]
    self.assertEquals(customVar.index, '1')
    self.assertEquals(customVar.name, 'My Custom Variable')
    self.assertEquals(customVar.scope, '3')


class DataFeedTest(unittest.TestCase):
  """Unit test for all custom elements in the Data Feed."""

  def setUp(self):
    """Retrieves the test XML feed into a DataFeed object."""

    self.feed = atom.core.parse(test_data.ANALYTICS_DATA_FEED,
                                gdata.analytics.data.DataFeed)

  def testDataFeed(self):
    """Tests custom classes in Google Analytics Data Feed."""

    self.assertEquals(self.feed.start_date.text, '2008-10-01')
    self.assertEquals(self.feed.end_date.text, '2008-10-31')

  def testAggregates(self):
    """Tests Aggregates class in Google Analytics Data Feed."""

    self.assert_(self.feed.aggregates is not None)

  def testAggregatesElements(self):
    """Tests Metrics class in Aggregates class."""

    metric = self.feed.aggregates.metric[0]
    self.assertEquals(metric.confidence_interval, '0.0')
    self.assertEquals(metric.name, 'ga:visits')
    self.assertEquals(metric.type, 'integer')
    self.assertEquals(metric.value, '136540')

    metric = self.feed.aggregates.GetMetric('ga:visits')
    self.assertEquals(metric.confidence_interval, '0.0')
    self.assertEquals(metric.name, 'ga:visits')
    self.assertEquals(metric.type, 'integer')
    self.assertEquals(metric.value, '136540')

  def testDataSource(self):
    """Tests DataSources class in Google Analytics Data Feed."""

    self.assert_(self.feed.data_source[0] is not None)

  def testDataSourceTableId(self):
    """Tests TableId class in the DataSource class."""

    table_id = self.feed.data_source[0].table_id
    self.assertEquals(table_id.text, 'ga:1174')

  def testDataSourceTableName(self):
    """Tests TableName class in the DataSource class."""

    table_name = self.feed.data_source[0].table_name
    self.assertEquals(table_name.text, 'www.googlestore.com')

  def testDataSourceProperty(self):
    """Tests Property clas in the DataSource class."""

    property = self.feed.data_source[0].property
    self.assertEquals(property[0].name, 'ga:profileId')
    self.assertEquals(property[0].value, '1174')

    self.assertEquals(property[1].name, 'ga:webPropertyId')
    self.assertEquals(property[1].value, 'UA-30481-1')

    self.assertEquals(property[2].name, 'ga:accountName')
    self.assertEquals(property[2].value, 'Google Store')

  def testDataSourceGetProperty(self):
    """Tests GetProperty utility method in the DataSource class."""

    ds = self.feed.data_source[0]
    self.assertEquals(ds.GetProperty('ga:profileId').value, '1174')
    self.assertEquals(ds.GetProperty('ga:webPropertyId').value, 'UA-30481-1')
    self.assertEquals(ds.GetProperty('ga:accountName').value, 'Google Store')

  def testSegment(self):
    """Tests Segment class in DataFeed class."""

    segment = self.feed.segment
    self.assertEquals(segment.id, 'gaid::-11')
    self.assertEquals(segment.name, 'Visits from iPhones')

  def testSegmentDefinition(self):
    """Tests Definition class in Segment class."""

    definition = self.feed.segment.definition
    self.assertEquals(definition.text, 'ga:operatingSystem==iPhone')

  def testEntryDimension(self):
    """Tests Dimension class in Entry class."""

    dim = self.feed.entry[0].dimension[0]
    self.assertEquals(dim.name, 'ga:source')
    self.assertEquals(dim.value, 'blogger.com')

  def testEntryGetDimension(self):
    """Tests GetDimension utility method in the Entry class."""

    dim = self.feed.entry[0].GetDimension('ga:source')
    self.assertEquals(dim.name, 'ga:source')
    self.assertEquals(dim.value, 'blogger.com')

    error = self.feed.entry[0].GetDimension('foo')
    self.assertEquals(error, None)

  def testEntryMetric(self):
    """Tests Metric class in Entry class."""

    met = self.feed.entry[0].metric[0]
    self.assertEquals(met.confidence_interval, '0.0')
    self.assertEquals(met.name, 'ga:visits')
    self.assertEquals(met.type, 'integer')
    self.assertEquals(met.value, '68140')

  def testEntryGetMetric(self):
    """Tests GetMetric utility method in the Entry class."""

    met = self.feed.entry[0].GetMetric('ga:visits')
    self.assertEquals(met.confidence_interval, '0.0')
    self.assertEquals(met.name, 'ga:visits')
    self.assertEquals(met.type, 'integer')
    self.assertEquals(met.value, '68140')

    error = self.feed.entry[0].GetMetric('foo')
    self.assertEquals(error, None)

  def testEntryGetObject(self):
    """Tests GetObjectOf utility method in Entry class."""

    entry = self.feed.entry[0]

    dimension = entry.GetObject('ga:source')
    self.assertEquals(dimension.name, 'ga:source')
    self.assertEquals(dimension.value, 'blogger.com')

    metric = entry.GetObject('ga:visits')
    self.assertEquals(metric.name, 'ga:visits')
    self.assertEquals(metric.value, '68140')
    self.assertEquals(metric.type, 'integer')
    self.assertEquals(metric.confidence_interval, '0.0')

    error = entry.GetObject('foo')
    self.assertEquals(error, None)


def suite():
  """Test Account Feed and Data Feed."""
  return conf.build_suite([AccountFeedTest, DataFeedTest])


if __name__ == '__main__':
  unittest.main()
