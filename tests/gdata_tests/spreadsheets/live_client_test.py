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
# These tests attempt to connect to Google servers.


__author__ = 'j.s@google.com (Jeff Scudder)'


import unittest
import gdata.spreadsheets.client
import gdata.gauth
import gdata.client
import atom.http_core
import atom.mock_http_core
import atom.core
import gdata.data
import gdata.test_config as conf


conf.options.register_option(conf.SPREADSHEET_ID_OPTION)


class SpreadsheetsClientTest(unittest.TestCase):

  def setUp(self):
    self.client = None
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.spreadsheets.client.SpreadsheetsClient()
      conf.configure_client(self.client, 'SpreadsheetsClientTest', 'wise')

  def tearDown(self):
    conf.close_client(self.client)

  def test_create_update_delete_worksheet(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_create_update_delete_worksheet')

    spreadsheet_id = conf.options.get_value('spreadsheetid')
    original_worksheets = self.client.get_worksheets(spreadsheet_id)
    self.assert_(isinstance(original_worksheets,
                               gdata.spreadsheets.data.WorksheetsFeed))
    worksheet_count = int(original_worksheets.total_results.text)

    # Add a new worksheet to the spreadsheet.
    created = self.client.add_worksheet(
        spreadsheet_id, 'a test worksheet', 4, 8)
    self.assert_(isinstance(created,
                               gdata.spreadsheets.data.WorksheetEntry))
    self.assertEqual(created.title.text, 'a test worksheet')
    self.assertEqual(created.row_count.text, '4')
    self.assertEqual(created.col_count.text, '8')

    # There should now be one more worksheet in this spreadsheet.
    updated_worksheets = self.client.get_worksheets(spreadsheet_id)
    new_worksheet_count = int(updated_worksheets.total_results.text)
    self.assertEqual(worksheet_count + 1, new_worksheet_count)

    # Delete our test worksheet.
    self.client.delete(created)
    # We should be back to the original number of worksheets.
    updated_worksheets = self.client.get_worksheets(spreadsheet_id)
    new_worksheet_count = int(updated_worksheets.total_results.text)
    self.assertEqual(worksheet_count, new_worksheet_count)

  def test_create_update_delete_table_and_records(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(
        self.client, 'test_create_update_delete_table_and_records')

    spreadsheet_id = conf.options.get_value('spreadsheetid')
    tables = self.client.get_tables(spreadsheet_id)

    test_worksheet = self.client.add_worksheet(
        spreadsheet_id, 'worksheet x', rows=30, cols=3)

    self.assert_(isinstance(tables, gdata.spreadsheets.data.TablesFeed))
    initial_count = tables.total_results.text

    created_table = self.client.add_table(
        spreadsheet_id, 'Test Table', 'This table is for testing',
        'worksheet x', header_row=5, num_rows=10, start_row=8,
        insertion_mode=None,
        column_headers={'B': 'Food', 'C': 'Drink', 'A': 'Price'})

    # Re-get the list of tables and make sure there are more now.
    updated_tables = self.client.get_tables(spreadsheet_id)
    self.assertEqual(int(initial_count) + 1, 
                     int(updated_tables.total_results.text))

    # Get the records in our new table to make sure it has the correct
    # number of records.
    table_num = int(created_table.get_table_id())
    starting_records = self.client.get_records(spreadsheet_id, table_num)
    self.assertEqual(starting_records.total_results.text, '10')
    self.assert_(starting_records.entry[0].field[0].text is None)
    self.assert_(starting_records.entry[0].field[1].text is None)
    self.assert_(starting_records.entry[1].field[0].text is None)
    self.assert_(starting_records.entry[1].field[1].text is None)

    record1 = self.client.add_record(
        spreadsheet_id, table_num,
        {'Food': 'Cheese', 'Drink': 'Soda', 'Price': '2.99'}, 'icky')
    self.client.add_record(spreadsheet_id, table_num,
                           {'Food': 'Eggs', 'Drink': 'Milk'})
    self.client.add_record(spreadsheet_id, table_num,
                           {'Food': 'Spinach', 'Drink': 'Water'})

    updated_records = self.client.get_records(spreadsheet_id, table_num)
    self.assertEqual(updated_records.entry[10].value_for_name('Price'), '2.99')
    self.assertEqual(updated_records.entry[10].value_for_index('A'), '2.99')
    self.assertEqual(updated_records.entry[10].value_for_name('Drink'),
                     'Soda')
    self.assert_(updated_records.entry[11].value_for_name('Price') is None)
    self.assertEqual(updated_records.entry[11].value_for_name('Drink'),
                     'Milk')
    self.assertEqual(updated_records.entry[12].value_for_name('Drink'),
                     'Water')
    self.assert_(updated_records.entry[1].value_for_index('A') is None)
    self.assert_(updated_records.entry[2].value_for_index('B') is None)
    self.assert_(updated_records.entry[3].value_for_index('C') is None)

    # Cleanup the table.
    self.client.delete(created_table)
    # Delete the test worksheet in which the table was placed.
    self.client.delete(test_worksheet)

    # Make sure we are back to the original count.
    updated_tables = self.client.get_tables(spreadsheet_id)
    self.assertEqual(int(initial_count), 
                     int(updated_tables.total_results.text))


def suite():
  return conf.build_suite([SpreadsheetsClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
