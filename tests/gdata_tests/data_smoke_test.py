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


__author__ = 'j.s@google.com (Jeff Scudder)'


import unittest
import gdata.test_config as conf
import gdata.data
import gdata.acl.data
import gdata.analytics.data
import gdata.dublincore.data
import gdata.books.data



class DataSmokeTest(unittest.TestCase):

  def test_check_all_data_classes(self):
    conf.check_data_classes(self, (
        gdata.data.TotalResults, gdata.data.StartIndex,
        gdata.data.ItemsPerPage, gdata.data.ExtendedProperty,
        gdata.data.GDEntry, gdata.data.GDFeed, gdata.data.BatchId,
        gdata.data.BatchOperation, gdata.data.BatchStatus,
        gdata.data.BatchEntry, gdata.data.BatchInterrupted,
        gdata.data.BatchFeed, gdata.data.EntryLink, gdata.data.FeedLink,
        gdata.data.AdditionalName, gdata.data.Comments, gdata.data.Country,
        gdata.data.Email, gdata.data.FamilyName, gdata.data.Im,
        gdata.data.GivenName, gdata.data.NamePrefix, gdata.data.NameSuffix,
        gdata.data.FullName, gdata.data.Name, gdata.data.OrgDepartment,
        gdata.data.OrgName, gdata.data.OrgSymbol, gdata.data.OrgTitle,
        gdata.data.Organization, gdata.data.When, gdata.data.Who,
        gdata.data.OriginalEvent, gdata.data.PhoneNumber,
        gdata.data.PostalAddress, gdata.data.Rating, gdata.data.Recurrence,
        gdata.data.RecurrenceException, gdata.data.Reminder,
        gdata.data.Agent, gdata.data.HouseName, gdata.data.Street,
        gdata.data.PoBox, gdata.data.Neighborhood, gdata.data.City,
        gdata.data.Subregion, gdata.data.Region, gdata.data.Postcode,
        gdata.data.Country, gdata.data.FormattedAddress,
        gdata.data.StructuredPostalAddress, gdata.data.Where,
        gdata.data.AttendeeType, gdata.data.AttendeeStatus,
        gdata.acl.data.AclRole, gdata.acl.data.AclScope,
        gdata.acl.data.AclEntry, gdata.acl.data.AclFeed,
        gdata.analytics.data.Dimension,
        gdata.analytics.data.EndDate,
        gdata.analytics.data.Metric,
        gdata.analytics.data.Aggregates,
        gdata.analytics.data.DataEntry,
        gdata.analytics.data.Property,
        gdata.analytics.data.StartDate,
        gdata.analytics.data.TableId,
        gdata.analytics.data.AccountEntry,
        gdata.analytics.data.TableName,
        gdata.analytics.data.DataSource,
        gdata.analytics.data.AccountFeed,
        gdata.analytics.data.DataFeed,
        gdata.dublincore.data.Creator,
        gdata.dublincore.data.Date,
        gdata.dublincore.data.Description,
        gdata.dublincore.data.Format,
        gdata.dublincore.data.Identifier,
        gdata.dublincore.data.Language,
        gdata.dublincore.data.Publisher,
        gdata.dublincore.data.Rights,
        gdata.dublincore.data.Subject,
        gdata.dublincore.data.Title,
        gdata.books.data.CollectionEntry,
        gdata.books.data.CollectionFeed,
        gdata.books.data.Embeddability,
        gdata.books.data.OpenAccess,
        gdata.books.data.Review,
        gdata.books.data.Viewability,
        gdata.books.data.VolumeEntry,
        gdata.books.data.VolumeFeed,
    ))


def suite():
  return conf.build_suite([DataSmokeTest])


if __name__ == '__main__':
  unittest.main()
