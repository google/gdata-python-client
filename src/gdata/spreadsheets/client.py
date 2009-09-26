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


"""Contains a client to communicate with the Google Spreadsheets servers.

For documentation on the Spreadsheets API, see:
http://code.google.com/apis/spreadsheets/
"""


__author__ = 'j.s@google.com (Jeff Scudder)'


import gdata.client
import gdata.spreadsheets.data
import atom.data
import atom.http_core


SPREADSHEETS_URL = ('http://spreadsheets.google.com/feeds/spreadsheets'
                    '/private/full')
WORKSHEETS_URL = ('http://spreadsheets.google.com/feeds/worksheets/'
                  '%s/private/full')
WORKSHEET_URL = ('http://spreadsheets.google.com/feeds/worksheets/'
                 '%s/private/full/%s')
TABLES_URL = 'http://spreadsheets.google.com/feeds/%s/tables'


class SpreadsheetsClient(gdata.client.GDClient):
  api_version = '3'
  auth_serice = 'wise'
  auth_scopes = ['https://spreadsheets.google.com/feeds/',
                 'http://spreadsheets.google.com/feeds/']

  def get_spreadsheets(self, auth_token=None,
                       desired_class=gdata.spreadsheets.data.SpreadsheetsFeed,
                       **kwargs):
    """Obtains a feed with the spreadsheets belonging to the current user.
    
    Args:
      auth_token: An object which sets the Authorization HTTP header in its
                  modify_request method. Recommended classes include
                  gdata.gauth.ClientLoginToken and gdata.gauth.AuthSubToken
                  among others. Represents the current user. Defaults to None
                  and if None, this method will look for a value in the
                  auth_token member of SpreadsheetsClient.
      desired_class: class descended from atom.core.XmlElement to which a
                     successful response should be converted. If there is no
                     converter function specified (converter=None) then the
                     desired_class will be used in calling the
                     atom.core.parse function. If neither
                     the desired_class nor the converter is specified, an
                     HTTP reponse object will be returned. Defaults to
                     gdata.spreadsheets.data.SpreadsheetsFeed.
    """
    return self.get_feed(SPREADSHEETS_URL, auth_token=auth_token,
                         desired_class=desired_class, **kwargs)

  def get_worksheets(self, spreadsheet_key, auth_token=None,
                     desired_class=gdata.spreadsheets.data.WorksheetsFeed,
                     **kwargs):
    """Finds the worksheets within a given spreadsheet.
   
    Args:
      spreadsheet_key: str, The unique ID of this containing spreadsheet. This
                       can be the ID from the URL or as provided in a
                       Spreadsheet entry.
      auth_token: An object which sets the Authorization HTTP header in its
                  modify_request method. Recommended classes include
                  gdata.gauth.ClientLoginToken and gdata.gauth.AuthSubToken
                  among others. Represents the current user. Defaults to None
                  and if None, this method will look for a value in the
                  auth_token member of SpreadsheetsClient.
      desired_class: class descended from atom.core.XmlElement to which a
                     successful response should be converted. If there is no
                     converter function specified (converter=None) then the
                     desired_class will be used in calling the
                     atom.core.parse function. If neither
                     the desired_class nor the converter is specified, an
                     HTTP reponse object will be returned. Defaults to
                     gdata.spreadsheets.data.WorksheetsFeed.
    """
    return self.get_feed(WORKSHEETS_URL % spreadsheet_key,
                         auth_token=auth_token, desired_class=desired_class,
                         **kwargs)

  def add_worksheet(self, spreadsheet_key, title, rows, cols,
                    auth_token=None, **kwargs):
    """Creates a new worksheet entry in the spreadsheet.
    
    Args:
      spreadsheet_key: str, The unique ID of this containing spreadsheet. This
                       can be the ID from the URL or as provided in a
                       Spreadsheet entry.
      title: str, The title to be used in for the worksheet.
      rows: str or int, The number of rows this worksheet should start with.
      cols: str or int, The number of columns this worksheet should start with.
      auth_token: An object which sets the Authorization HTTP header in its
                  modify_request method. Recommended classes include
                  gdata.gauth.ClientLoginToken and gdata.gauth.AuthSubToken
                  among others. Represents the current user. Defaults to None
                  and if None, this method will look for a value in the
                  auth_token member of SpreadsheetsClient.
    """
    new_worksheet = gdata.spreadsheets.data.WorksheetEntry(
        title=atom.data.Title(text=title),
        row_count=gdata.spreadsheets.data.RowCount(text=str(rows)),
        col_count=gdata.spreadsheets.data.ColCount(text=str(cols)))
    return self.post(new_worksheet, WORKSHEETS_URL % spreadsheet_key,
                     auth_token=auth_token, **kwargs)

  def get_worksheet(self, spreadsheet_key, worksheet_id,
                    desired_class=gdata.spreadsheets.data.WorksheetEntry,
                    auth_token=None, **kwargs):
    """Retrieves a single worksheet."""
    return self.get_entry(WORKSHEET_URL % (spreadsheet_key, worksheet_id,),
                          auth_token=auth_token, desired_class=desired_class,
                          **kwargs)


class Query(gdata.client.Query):

  def __init__(self, order_by=None, **kwargs):
    gdata.client.Query.__init__(self, **kwargs)
    self.order_by = order_by

  def modify_request(self, http_request):
    gdata.client._add_query_param('orderby', self.order_by, http_request)
    gdata.client.Query.modify_request(self, http_request)

  ModifyRequest = modify_request
