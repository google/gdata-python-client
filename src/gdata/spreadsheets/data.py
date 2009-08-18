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


"""Provides classes and constants for the XML in the Google Spreadsheets API.

Documentation for the raw XML which these classes represent can be found here:
http://code.google.com/apis/spreadsheets/docs/3.0/reference.html#Elements
"""


__author__ = 'j.s@google.com (Jeff Scudder)'


import atom.core
import gdata.data


GS_TEMPLATE = '{http://schemas.google.com/spreadsheets/2006}%s'
GSX_NAMESPACE = 'http://schemas.google.com/spreadsheets/2006/extended'


INSERT_MODE = 'insert'
OVERWRITE_MODE = 'overwrite'


WORKSHEETS_REL = 'http://schemas.google.com/spreadsheets/2006#worksheetsfeed'


class Error(object):
  pass


class HeaderNotSet(Error):
  """The desired column header had no value for the row in the list feed."""


class Cell(atom.core.XmlElement):
  """The gs:cell element.

  A cell in the worksheet. The <gs:cell> element can appear only as a child
  of <atom:entry>.
  """
  _qname = GS_TEMPLATE % 'cell'
  col = 'col'
  input_value = 'inputValue'
  numeric_value = 'numericValue'
  row = 'row'


class ColCount(atom.core.XmlElement):
  """The gs:colCount element.

  Indicates the number of columns in the worksheet, including columns that
  contain only empty cells. The <gs:colCount> element can appear as a child
  of <atom:entry> or <atom:feed>
  """
  _qname = GS_TEMPLATE % 'colCount'


class Field(atom.core.XmlElement):
  """The gs:field element.

  A field—a single cell within a record. Contained in an <atom:entry>.
  """
  _qname = GS_TEMPLATE % 'field'
  index = 'index'
  name = 'name'


class Column(Field):
  """The gs:column element."""
  _qname = GS_TEMPLATE % 'column'


class Data(atom.core.XmlElement):
  """The gs:data element.

  A data region of a table. Contained in an <atom:entry> element.
  """
  _qname = GS_TEMPLATE % 'data'
  column = [Column]
  insertion_mode = 'insertionMode'
  num_rows = 'numRows'
  start_row = 'startRow'


class Header(atom.core.XmlElement):
  """The gs:header element.

  Indicates which row is the header row. Contained in an <atom:entry>.
  """
  _qname = GS_TEMPLATE % 'header'
  row = 'row'


class RowCount(atom.core.XmlElement):
  """The gs:rowCount element.

  Indicates the number of total rows in the worksheet, including rows that
  contain only empty cells. The <gs:rowCount> element can appear as a
  child of <atom:entry> or <atom:feed>.
  """
  _qname = GS_TEMPLATE % 'rowCount'


class Worksheet(atom.core.XmlElement):
  """The gs:worksheet element.

  The worksheet where the table lives.Contained in an <atom:entry>.
  """
  _qname = GS_TEMPLATE % 'worksheet'
  name = 'name'


class Spreadsheet(gdata.data.GDEntry):
  """An Atom entry which represents a Google Spreadsheet."""

  def find_worksheets_feed(self):
    return self.find_url(WORKSHEETS_REL)

  FindWorksheetsFeed = find_worksheets_feed
  

class SpreadsheetsFeed(gdata.data.GDFeed):
  """An Atom feed listing a user's Google Spreadsheets."""
  entry = [Spreadsheet]


class WorksheetEntry(gdata.data.GDEntry):
  """An Atom entry representing a single worksheet in a spreadsheet."""
  row_count = RowCount
  col_count = ColCount


class WorksheetsFeed(gdata.data.GDFeed):
  """A feed containing the worksheets in a single spreadsheet."""
  entry = [Worksheet]


class Table(gdata.data.GDEntry):
  """An Atom entry that represents a subsection of a worksheet.

  A table allows you to treat part or all of a worksheet somewhat like a
  table in a database—that is, as a set of structured data items. Tables
  don't exist until you explicitly create them—before you can use a table
  feed, you have to explicitly define where the table data comes from.
  """
  data = Data
  header = Header


class TablesFeed(gdata.data.GDFeed):
  """An Atom feed containing the tables defined within a worksheet."""
  entry = [Table]  


class Record(gdata.data.GDEntry):
  """An Atom entry representing a single record in a table.

  Note that the order of items in each record is the same as the order of
  columns in the table definition, which may not match the order of
  columns in the GUI.
  """
  field = [Field]


class RecordsFeed(gdata.data.GDFeed):
  """An Atom feed containing the individuals records in a table."""
  entry = [Record]


class ListEntry(gdata.data.GDEntry):
  """An Atom entry representing a worksheet row in the list feed.

  The values for a particular column can be get and set using 
  x.get_value('columnheader') and x.set_value('columnheader', 'value').
  See also the explanation of column names in the ListFeed class.
  """

  def get_value(self, column_name):
    #TODO: implement search through row fields for column name 
    pass

  def set_value(self, column_name):
    #TODO: implement find and set field in this row.
    pass


class ListsFeed(gdata.data.GDFeed):
  """An Atom feed in which each entry represents a row in a worksheet.

  The first row in the worksheet is used as the column names for the values
  in each row. If a header cell is empty, then a unique column ID is used
  for the gsx element name.

  Spaces in a column name are removed from the name of the corresponding
  gsx element.

  Caution: The columnNames are case-insensitive. For example, if you see
  a <gsx:e-mail> element in a feed, you can't know whether the column
  heading in the original worksheet was "e-mail" or "E-Mail".

  Note: If two or more columns have the same name, then subsequent columns
  of the same name have _n appended to the columnName. For example, if the
  first column name is "e-mail", followed by columns named "E-Mail" and
  "E-mail", then the columnNames will be gsx:e-mail, gsx:e-mail_2, and
  gsx:e-mail_3 respectively.
  """
  entry = [ListEntry]


class CellEntry(gdata.data.BatchEntry):
  """An Atom entry representing a single cell in a worksheet."""
  cell = Cell


class CellsFeed(gdata.data.BatchFeed):
  """An Atom feed contains one entry per cell in a worksheet.
  
  The cell feed supports batch operations, you can send multiple cell
  operations in one HTTP request.
  """
  entry = [CellEntry]
