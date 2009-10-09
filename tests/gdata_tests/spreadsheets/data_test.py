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
import gdata.spreadsheets.data
import gdata.test_config as conf
import atom.core


SPREADSHEET = """<entry xmlns="http://www.w3.org/2005/Atom"
      xmlns:gd="http://schemas.google.com/g/2005" 
      gd:etag='"BxAUSQUJRCp7ImBq"'>
  <id>http://spreadsheets.google.com/feeds/spreadsheets/private/full/key</id>
  <updated>2006-11-17T18:24:18.231Z</updated>
  <title type="text">Groceries R Us</title>
  <content type="text">Groceries R Us</content>
  <link rel="http://schemas.google.com/spreadsheets/2006#worksheetsfeed"
   type="application/atom+xml"
   href="http://spreadsheets.google.com/feeds/worksheets/key/private/full"/>
  <link rel="alternate" type="text/html"
   href="http://spreadsheets.google.com/ccc?key=key"/>
  <link rel="self" type="application/atom+xml"
   href="http://spreadsheets.google.com/feeds/spreadsheets/private/full/key"/>
  <author>
    <name>Fitzwilliam Darcy</name>
    <email>fitz@gmail.com</email>
  </author>
</entry>"""


WORKSHEETS_FEED = """<feed xmlns="http://www.w3.org/2005/Atom"
    xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/"
    xmlns:gs="http://schemas.google.com/spreadsheets/2006"
    xmlns:gd="http://schemas.google.com/g/2005"
    gd:etag='W/"D0cERnk-eip7ImA9WBBXGEg."'>
  <id>http://spreadsheets.google.com/feeds/worksheets/key/private/full</id>
  <updated>2006-11-17T18:23:45.173Z</updated>
  <title type="text">Groceries R Us</title>
  <link rel="alternate" type="text/html"
    href="http://spreadsheets.google.com/ccc?key=key"/>
  <link rel="http://schemas.google.com/g/2005#feed"
    type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/worksheets/key/private/full"/>
  <link rel="self" type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/worksheets/key/private/full"/>
  <link
    rel="http://schemas.google.com/g/2005#post" type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/worksheets/key/private/full"/>
  <author>
    <name>Fitzwilliam Darcy</name>
    <email>fitz@gmail.com</email>
  </author>
  <openSearch:totalResults>1</openSearch:totalResults>
  <openSearch:startIndex>1</openSearch:startIndex>
  <openSearch:itemsPerPage>1</openSearch:itemsPerPage>
  <entry gd:etag='"YDwqeyI."'>
    <id>http://spreadsheets.google.com/feeds/worksheets/0/private/full/1</id>
    <updated>2006-11-17T18:23:45.173Z</updated>
    <title type="text">Sheet1</title>
    <content type="text">Sheet1</content>
    <link rel="http://schemas.google.com/spreadsheets/2006#listfeed"
      type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/list/0/1/private/full"/>
    <link rel="http://schemas.google.com/spreadsheets/2006#cellsfeed"
      type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/cells/0/1/private/full"/>
    <link rel="self" type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/worksheets/0/private/full/1"/>
    <link rel="edit" type="application/atom+xml"
      href="http://spreadsheets.google.com/.../0/.../1/version"/>
    <gs:rowCount>100</gs:rowCount>
    <gs:colCount>20</gs:colCount>
  </entry>
</feed>"""


NEW_WORKSHEET = """<entry xmlns="http://www.w3.org/2005/Atom"
    xmlns:gs="http://schemas.google.com/spreadsheets/2006">
  <title>Expenses</title>
  <gs:rowCount>50</gs:rowCount>
  <gs:colCount>10</gs:colCount>
</entry>"""


EDIT_WORKSHEET = """<entry>
  <id>
    http://spreadsheets.google.com/feeds/worksheets/k/private/full/w
  </id>
  <updated>2007-07-30T18:51:30.666Z</updated>
  <category scheme="http://schemas.google.com/spreadsheets/2006"
    term="http://schemas.google.com/spreadsheets/2006#worksheet"/>
  <title type="text">Income</title>
  <content type="text">Expenses</content>
  <link rel="http://schemas.google.com/spreadsheets/2006#listfeed"
    type="application/atom+xml" 
    href="http://spreadsheets.google.com/feeds/list/k/w/private/full"/>
  <link rel="http://schemas.google.com/spreadsheets/2006#cellsfeed"
    type="application/atom+xml" 
    href="http://spreadsheets.google.com/feeds/cells/k/w/private/full"/>
  <link rel="self" type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/worksheets/k/private/full/w"/>
  <link rel="edit" type="application/atom+xml"
    href="http://spreadsheets.google.com/.../k/private/full/w/v"/>
  <gs:rowCount>45</gs:rowCount>
  <gs:colCount>15</gs:colCount>
</entry>"""


NEW_TABLE = """<entry xmlns="http://www.w3.org/2005/Atom"
    xmlns:gs="http://schemas.google.com/spreadsheets/2006">
  <title type='text'>Table 1</title>
  <summary type='text'>This is a list of all who have registered to vote and
    whether or not they qualify to vote.</summary>
  <gs:worksheet name='Sheet1' />
  <gs:header row='1' />
  <gs:data numRows='0' startRow='2'>
    <gs:column index='B' name='Birthday' />
    <gs:column index='C' name='Age' />
    <gs:column index='A' name='Name' />
    <gs:column index='D' name='CanVote' />
  </gs:data>
</entry>"""


TABLES_FEED = """<?xml version='1.0' encoding='utf-8'?>
<feed xmlns="http://www.w3.org/2005/Atom"
    xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/"
    xmlns:gs="http://schemas.google.com/spreadsheets/2006"
    xmlns:gd="http://schemas.google.com/g/2005"
    gd:etag='W/"DEQHQn84fCt7ImA9WxJTGEU."'>
  <id>
    http://spreadsheets.google.com/feeds/key/tables</id>
  <updated>2009-04-28T02:38:53.134Z</updated>
  <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/spreadsheets/2006#table' />
  <title>Sample table and record feed</title>
  <link rel='alternate' type='text/html'
    href='http://spreadsheets.google.com/ccc?key=key' />
  <link rel='http://schemas.google.com/g/2005#feed'
    type='application/atom+xml'
    href='http://spreadsheets.google.com/feeds/key/tables' />
  <link rel='http://schemas.google.com/g/2005#post'
    type='application/atom+xml'
    href='http://spreadsheets.google.com/feeds/key/tables' />
  <link rel='self' type='application/atom+xml'
    href='http://spreadsheets.google.com/feeds/key/tables' />
  <author>
    <name>Liz</name>
    <email>liz@gmail.com</email>
  </author>
  <openSearch:totalResults>2</openSearch:totalResults>
  <openSearch:startIndex>1</openSearch:startIndex>
  <entry gd:etag='"HBcUVgtWASt7ImBq"'>
    <id>
      http://spreadsheets.google.com/feeds/key/tables/0</id>
    <updated>2009-04-28T01:20:32.707Z</updated>
    <app:edited xmlns:app="http://www.w3.org/2007/app">
      2009-04-28T01:20:32.707Z</app:edited>
    <category scheme='http://schemas.google.com/g/2005#kind'
      term='http://schemas.google.com/spreadsheets/2006#table' />
    <title>Table 1</title>
    <summary>This is a list of all who have registered to vote and
      whether or not they qualify to vote.</summary>
    <content type='application/atom+xml;type=feed'
      src='http://spreadsheets.google.com/feeds/key/records/0' />
    <link rel='self' type='application/atom+xml'
      href='http://spreadsheets.google.com/feeds/key/tables/0' />
    <link rel='edit' type='application/atom+xml'
      href='http://spreadsheets.google.com/feeds/key/tables/0' />
    <gs:worksheet name='Sheet1' />
    <gs:header row='1' />
    <gs:data insertionMode='overwrite' numRows='2' startRow='2'>
      <gs:column index='B' name='Birthday' />
      <gs:column index='C' name='Age' />
      <gs:column index='A' name='Name' />
      <gs:column index='D' name='CanVote' />
    </gs:data>
  </entry>
  <entry gd:etag='"HBcUVgdCGyt7ImBq"'>
    <id>
      http://spreadsheets.google.com/feeds/key/tables/1</id>
    <updated>2009-04-28T01:20:38.313Z</updated>
    <app:edited xmlns:app="http://www.w3.org/2007/app">
      2009-04-28T01:20:38.313Z</app:edited>
    <category scheme='http://schemas.google.com/g/2005#kind'
      term='http://schemas.google.com/spreadsheets/2006#table' />
    <title>Table 2</title>
    <summary>List of detailed information about each voter.</summary>
    <content type='application/atom+xml;type=feed'
      src='http://spreadsheets.google.com/feeds/key/records/1' />
    <link rel='self' type='application/atom+xml'
      href='http://spreadsheets.google.com/feeds/key/tables/1' />
    <link rel='edit' type='application/atom+xml'
      href='http://spreadsheets.google.com/feeds/key/tables/1' />
    <gs:worksheet name='Sheet1' />
    <gs:header row='30' />
    <gs:data insertionMode='overwrite' numRows='10' startRow='34'>
      <gs:column index='C' name='Last' />
      <gs:column index='B' name='First' />
      <gs:column index='D' name='DOB' />
      <gs:column index='E' name='Driver License?' />
    </gs:data>
  </entry>
</feed>"""


NEW_RECORD = """<entry xmlns="http://www.w3.org/2005/Atom"
    xmlns:gs="http://schemas.google.com/spreadsheets/2006">
  <title>Darcy</title>
  <gs:field name='Birthday'>2/10/1785</gs:field>
  <gs:field name='Age'>28</gs:field>
  <gs:field name='Name'>Darcy</gs:field>
  <gs:field name='CanVote'>No</gs:field>
</entry>"""


RECORDS_FEED = """<?xml version='1.0' encoding='utf-8'?>
<feed xmlns="http://www.w3.org/2005/Atom"
    xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/"
    xmlns:gs="http://schemas.google.com/spreadsheets/2006"
    xmlns:gd="http://schemas.google.com/g/2005"
    gd:etag='W/"DEQHQn84fCt7ImA9WxJTGEU."'>
  <id>http://spreadsheets.google.com/feeds/key/records/0</id>
  <updated>2009-04-28T02:38:53.134Z</updated>
  <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/spreadsheets/2006#record' />
  <title>Table 1</title>
  <link rel='alternate' type='text/html'
    href='http://spreadsheets.google.com/pub?key=key' />
  <link rel='http://schemas.google.com/g/2005#feed'
    type='application/atom+xml'
    href='http://spreadsheets.google.com/feeds/key/records/0' />
  <link rel='http://schemas.google.com/g/2005#post'
    type='application/atom+xml'
    href='http://spreadsheets.google.com/feeds/key/records/0' />
  <link rel='self' type='application/atom+xml'
    href='http://spreadsheets.google.com/feeds/key/records/0' />
  <author>
    <name>Liz</name>
    <email>liz@gmail.com</email>
  </author>
  <openSearch:totalResults>2</openSearch:totalResults>
  <openSearch:startIndex>1</openSearch:startIndex>
  <entry gd:etag='"UB8DTlJAKSt7ImA-WkUT"'>
    <id>
      http://spreadsheets.google.com/feeds/key/records/0/cn6ca</id>
    <updated>2009-04-28T02:38:53.134Z</updated>
    <app:edited xmlns:app="http://www.w3.org/2007/app">
      2009-04-28T02:38:53.134Z</app:edited>
    <category scheme='http://schemas.google.com/g/2005#kind'
      term='http://schemas.google.com/spreadsheets/2006#record' />
    <title>Darcy</title>
    <content>Birthday: 2/10/1785, Age: 28, Name: Darcy,
      CanVote: No</content>
    <link rel='self' type='application/atom+xml'
    href='http://spreadsheets.google.com/feeds/key/records/0/cn6ca' />
    <link rel='edit' type='application/atom+xml'
    href='http://spreadsheets.google.com/feeds/key/records/0/cn6ca' />
    <gs:field index='B' name='Birthday'>2/10/1785</gs:field>
    <gs:field index='C' name='Age'>28</gs:field>
    <gs:field index='A' name='Name'>Darcy</gs:field>
    <gs:field index='D' name='CanVote'>No</gs:field>
  </entry>
  <entry gd:etag='"UVBFUEcNRCt7ImA9DU8."'>
    <id>
      http://spreadsheets.google.com/feeds/key/records/0/cokwr</id>
    <updated>2009-04-28T02:38:53.134Z</updated>
    <app:edited xmlns:app="http://www.w3.org/2007/app">
      2009-04-28T02:38:53.134Z</app:edited>
    <category scheme='http://schemas.google.com/g/2005#kind'
      term='http://schemas.google.com/spreadsheets/2006#record' />
    <title>Jane</title>
    <content>Birthday: 1/6/1791, Age: 22, Name: Jane,
      CanVote: Yes</content>
    <link rel='self' type='application/atom+xml'
      href='http://spreadsheets.google.com/feeds/key/records/0/cokwr' />
    <link rel='edit' type='application/atom+xml'
      href='http://spreadsheets.google.com/feeds/key/records/0/cokwr' />
    <gs:field index='B' name='Birthday'>1/6/1791</gs:field>
    <gs:field index='C' name='Age'>22</gs:field>
    <gs:field index='A' name='Name'>Jane</gs:field>
    <gs:field index='D' name='CanVote'>Yes</gs:field>
  </entry>
</feed>"""


LIST_FEED = """<feed xmlns="http://www.w3.org/2005/Atom"
    xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/"
    xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended"
    xmlns:gd="http://schemas.google.com/g/2005"
    gd:etag='W/"D0cERnk-eip7ImA9WBBXGEg."'>
  <id>
    http://spreadsheets.google.com/feeds/list/key/worksheetId/private/full
  </id>
  <updated>2006-11-17T18:23:45.173Z</updated>
  <title type="text">Sheet1</title>
  <link rel="alternate" type="text/html"
    href="http://spreadsheets.google.com/ccc?key=key"/>
  <link rel="http://schemas.google.com/g/2005#feed"
    type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/list/k/w/private/full"/>
  <link rel="http://schemas.google.com/g/2005#post"
    type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/list/k/w/private/full"/>
  <link rel="self" type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/list/k/w/private/full"/>
  <author>
    <name>Fitzwilliam Darcy</name>
    <email>fitz@gmail.com</email>
  </author>
  <openSearch:totalResults>8</openSearch:totalResults>
  <openSearch:startIndex>1</openSearch:startIndex>
  <openSearch:itemsPerPage>8</openSearch:itemsPerPage>
  <entry gd:etag='"S0wCTlpIIip7ImA0X0QI"'>
    <id>http://spreadsheets.google.com/feeds/list/k/w/private/full/r</id>
    <updated>2006-11-17T18:23:45.173Z</updated>
    <category scheme="http://schemas.google.com/spreadsheets/2006"
      term="http://schemas.google.com/spreadsheets/2006#list"/>
    <title type="text">Bingley</title>
    <content type="text">Hours: 10, Items: 2, IPM: 0.0033</content>
    <link rel="self" type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/list/k/w/private/full/r"/>
    <link rel="edit" type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/list/k/w/private/full/r/v"/>
    <gsx:name>Bingley</gsx:name>
    <gsx:hours>10</gsx:hours>
    <gsx:items>2</gsx:items>
    <gsx:ipm>0.0033</gsx:ipm>
  </entry>
  <entry gd:etag='"AxQDSXxjfyp7ImA0ChJVSBI."'>
    <id>
      http://spreadsheets.google.com/feeds/list/k/w/private/full/rowId
    </id>
    <updated>2006-11-17T18:23:45.173Z</updated>
    <category scheme="http://schemas.google.com/spreadsheets/2006"
      term="http://schemas.google.com/spreadsheets/2006#list"/>
    <title type="text">Charlotte</title>
    <content type="text">Hours: 60, Items: 18000, IPM: 5</content>
    <link rel="self" type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/list/k/w/private/full/r"/>
    <link rel="edit" type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/list/k/w/private/full/r/v"/>
    <gsx:name>Charlotte</gsx:name>
    <gsx:hours>60</gsx:hours>
    <gsx:items>18000</gsx:items>
    <gsx:ipm>5</gsx:ipm>
  </entry>
</feed>"""


NEW_ROW = """<entry xmlns="http://www.w3.org/2005/Atom"
    xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended">
  <gsx:hours>1</gsx:hours>
  <gsx:ipm>1</gsx:ipm>
  <gsx:items>60</gsx:items>
  <gsx:name>Elizabeth Bennet</gsx:name>
</entry>"""


UPDATED_ROW = """<entry gd:etag='"S0wCTlpIIip7ImA0X0QI"'
    xmlns="http://www.w3.org/2005/Atom"
    xmlns:gd="http://schemas.google.com/g/2005"
    xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended">
  <id>http://spreadsheets.google.com/feeds/list/k/w/private/full/rowId</id>
  <updated>2006-11-17T18:23:45.173Z</updated>
  <category scheme="http://schemas.google.com/spreadsheets/2006"
    term="http://schemas.google.com/spreadsheets/2006#list"/>
  <title type="text">Bingley</title>
  <content type="text">Hours: 10, Items: 2, IPM: 0.0033</content>
  <link rel="self" type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/list/k/w/private/full/r"/>
  <link rel="edit" type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/list/k/w/private/full/r/v"/>
  <gsx:name>Bingley</gsx:name>
  <gsx:hours>20</gsx:hours>
  <gsx:items>4</gsx:items>
  <gsx:ipm>0.0033</gsx:ipm>
</entry>"""


CELLS_FEED = """<feed xmlns="http://www.w3.org/2005/Atom"
    xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/"
    xmlns:gs="http://schemas.google.com/spreadsheets/2006"
    xmlns:gd="http://schemas.google.com/g/2005"
    gd:etag='W/"D0cERnk-eip7ImA9WBBXGEg."'>
  <id>
    http://spreadsheets.google.com/feeds/cells/key/worksheetId/private/full
  </id>
  <updated>2006-11-17T18:27:32.543Z</updated>
  <title type="text">Sheet1</title>
  <link rel="alternate" type="text/html"
    href="http://spreadsheets.google.com/ccc?key=key"/>
  <link rel="http://schemas.google.com/g/2005#feed" type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/cells/k/w/private/full"/>
  <link rel="http://schemas.google.com/g/2005#post" 
    type="application/atom+xml"
  <link rel="http://schemas.google.com/g/2005#batch"
    type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/cells/k/w/private/full/batch"/>
  <link rel="self" type="application/atom+xml"
    href="http://spreadsheets.google.com/feeds/cells/k/w/private/full"/>
  <author>
    <name>Fitzwilliam Darcy</name>
    <email>fitz@gmail.com</email>
  </author>
  <openSearch:startIndex>1</openSearch:startIndex>
  <openSearch:itemsPerPage>36</openSearch:itemsPerPage>
  <gs:rowCount>100</gs:rowCount>
  <gs:colCount>20</gs:colCount>
  <entry gd:etag='"ImA9D1APFyp7"'>
    <id>
      http://spreadsheets.google.com/feeds/cells/k/w/private/full/R1C1
    </id>
    <updated>2006-11-17T18:27:32.543Z</updated>
    <category scheme="http://schemas.google.com/spreadsheets/2006"
      term="http://schemas.google.com/spreadsheets/2006#cell"/>
    <title type="text">A1</title>
    <content type="text">Name</content>
    <link rel="self" type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/cells/k/w/pr/full/R1C1"/>
    <link rel="edit" type="application/atom+xml"
      href="http://spreadsheets.google.com/./cells/k/w/pr/full/R1C1/bgvjf"/>
    <gs:cell row="1" col="1" inputValue="Name">Name</gs:cell>
  </entry>
  <entry gd:etag='"YD0PS1YXByp7Ig.."'>
    <id>
      http://spreadsheets.google.com/feeds/cells/k/w/private/full/R1C2
    </id>
    <updated>2006-11-17T18:27:32.543Z</updated>
    <category scheme="http://schemas.google.com/spreadsheets/2006"
      term="http://schemas.google.com/spreadsheets/2006#cell"/>
    <title type="text">B1</title>
    <content type="text">Hours</content>
    <link rel="self" type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/cells/k/w/pr/full/R1C2"/>
    <link rel="edit" type="application/atom+xml"
      href="http://spreadsheets.google.com/./cells/k/w/pr/full/R1C2/1pn567"/>
    <gs:cell row="1" col="2" inputValue="Hours">Hours</gs:cell>
  </entry>
  <entry gd:etag='"ImB5CBYSRCp7"'>
    <id>
      http://spreadsheets.google.com/feeds/cells/k/w/private/full/R9C4
    </id>
    <updated>2006-11-17T18:27:32.543Z</updated>
    <category scheme="http://schemas.google.com/spreadsheets/2006"
      term="http://schemas.google.com/spreadsheets/2006#cell"/>
    <title type="text">D9</title>
    <content type="text">5</content>
    <link rel="self" type="application/atom+xml"
      href="http://spreadsheets.google.com/feeds/cells/k/w/pr/full/R9C4"/>
    <link rel="edit" type="application/atom+xml"
      href="http://spreadsheets.google.com/./cells/k/w/pr/full/R9C4/srevc"/>
    <gs:cell row="9" col="4"
      inputValue="=FLOOR(R[0]C[-1]/(R[0]C[-2]*60),.0001)"
      numericValue="5.0">5</gs:cell>
  </entry>
</feed>"""


BATCH_CELLS = """<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:batch="http://schemas.google.com/gdata/batch"
      xmlns:gs="http://schemas.google.com/spreadsheets/2006">
  <id>
    http://spreadsheets.google.com/feeds/cells/key/worksheetId/private/full
  </id>
  <entry>
    <batch:id">A1</batch:id">
    <batch:operation type="update"/>
    <id>
      http://spreadsheets.google.com/feeds/cells/k/w/private/full/cellId
    </id>
    <link rel="edit" type="application/atom+xml"
      href="http://spreadsheets/google.com/./cells/k/w/pr/full/R2C4/v"/>
    <gs:cell row="2" col="4" inputValue="newData"/>
  </entry>
  <entry>
    <batch:id">A2</batch:id">
    <batch:operation type="update"/>
    <title type="text">A2</title>
    <id>
      http://spreadsheets.google.com/feeds/cells/k/w/private/full/cellId
    </id>
    <link rel="edit" type="application/atom+xml"
      href="http://spreadsheets/google.com/feeds/cells/k/w/pr/full/R2C5/v"/>
    <gs:cell row="2" col="5" inputValue="moreInfo"/>
  </entry>
</feed>"""


class SpreadsheetEntryTest(unittest.TestCase):

  def setUp(self):
    self.spreadsheet = atom.core.parse(
        SPREADSHEET, gdata.spreadsheets.data.Spreadsheet)

  def test_check_parsing(self):
    self.assertEqual(self.spreadsheet.etag, '"BxAUSQUJRCp7ImBq"')
    self.assertEqual(self.spreadsheet.id.text,
                     'http://spreadsheets.google.com/feeds/spreadsheets'
                     '/private/full/key')
    self.assertEqual(self.spreadsheet.updated.text,
                     '2006-11-17T18:24:18.231Z')
    self.assertEqual(self.spreadsheet.find_worksheets_feed(),
                     'http://spreadsheets.google.com/feeds/worksheets'
                     '/key/private/full')
    self.assertEqual(self.spreadsheet.find_self_link(),
                     'http://spreadsheets.google.com/feeds/spreadsheets'
                     '/private/full/key')


class ListEntryTest(unittest.TestCase):

  def test_get_and_set_column_value(self):
    row = atom.core.parse(NEW_ROW, gdata.spreadsheets.data.ListEntry)
    row.set_value('hours', '3')
    row.set_value('name', 'Lizzy')
    self.assertEqual(row.get_value('hours'), '3')
    self.assertEqual(row.get_value('ipm'), '1')
    self.assertEqual(row.get_value('items'), '60')
    self.assertEqual(row.get_value('name'), 'Lizzy')
    self.assertEqual(row.get_value('x'), None)
    row.set_value('x', 'Test')
    self.assertEqual(row.get_value('x'), 'Test')
    row_xml = str(row)
    self.assert_(row_xml.find(':x') > -1)
    self.assert_(row_xml.find('>Test</') > -1)
    self.assert_(row_xml.find(':hours') > -1)
    self.assert_(row_xml.find('>3</') > -1)
    self.assert_(row_xml.find(':ipm') > -1)
    self.assert_(row_xml.find('>1</') > -1)
    self.assert_(row_xml.find(':items') > -1)
    self.assert_(row_xml.find('>60</') > -1)
    self.assert_(row_xml.find(':name') > -1)
    self.assert_(row_xml.find('>Lizzy</') > -1)
    self.assertEqual(row_xml.find(':zzz'), -1)
    self.assertEqual(row_xml.find('>foo</'), -1)

  def test_check_parsing(self):
    row = atom.core.parse(NEW_ROW, gdata.spreadsheets.data.ListEntry)
    self.assertEqual(row.get_value('hours'), '1')
    self.assertEqual(row.get_value('ipm'), '1')
    self.assertEqual(row.get_value('items'), '60')
    self.assertEqual(row.get_value('name'), 'Elizabeth Bennet')
    self.assertEqual(row.get_value('none'), None)

    row = atom.core.parse(UPDATED_ROW, gdata.spreadsheets.data.ListEntry)
    self.assertEqual(row.get_value('hours'), '20')
    self.assertEqual(row.get_value('ipm'), '0.0033')
    self.assertEqual(row.get_value('items'), '4')
    self.assertEqual(row.get_value('name'), 'Bingley')
    self.assertEqual(row.get_value('x'), None)
    self.assertEqual(
        row.id.text, 'http://spreadsheets.google.com/feeds/list'
            '/k/w/private/full/rowId')
    self.assertEqual(row.updated.text, '2006-11-17T18:23:45.173Z')
    self.assertEqual(row.content.text, 'Hours: 10, Items: 2, IPM: 0.0033')


class RecordEntryTest(unittest.TestCase):

  def setUp(self):
    self.records = atom.core.parse(
        RECORDS_FEED, gdata.spreadsheets.data.RecordsFeed)

  def test_get_by_index(self):
    self.assertEqual(self.records.entry[0].field[0].index, 'B')
    self.assertEqual(self.records.entry[0].field[0].name, 'Birthday')
    self.assertEqual(self.records.entry[0].field[0].text, '2/10/1785')
    self.assertEqual(self.records.entry[0].value_for_index('B'), '2/10/1785')
    self.assertRaises(gdata.spreadsheets.data.FieldMissing,
                      self.records.entry[0].ValueForIndex, 'E')
    self.assertEqual(self.records.entry[1].value_for_index('D'), 'Yes')

  def test_get_by_name(self):
    self.assertEqual(self.records.entry[0].ValueForName('Birthday'),
                     '2/10/1785')
    self.assertRaises(gdata.spreadsheets.data.FieldMissing,
                      self.records.entry[0].value_for_name, 'Foo')
    self.assertEqual(self.records.entry[1].value_for_name('Age'), '22')


class DataClassSanityTest(unittest.TestCase):

  def test_basic_element_structure(self):
    conf.check_data_classes(self, [
        gdata.spreadsheets.data.Cell, gdata.spreadsheets.data.ColCount,
        gdata.spreadsheets.data.Field, gdata.spreadsheets.data.Column,
        gdata.spreadsheets.data.Data, gdata.spreadsheets.data.Header,
        gdata.spreadsheets.data.RowCount, gdata.spreadsheets.data.Worksheet,
        gdata.spreadsheets.data.Spreadsheet, 
        gdata.spreadsheets.data.SpreadsheetsFeed,
        gdata.spreadsheets.data.WorksheetEntry,
        gdata.spreadsheets.data.WorksheetsFeed,
        gdata.spreadsheets.data.Table,
        gdata.spreadsheets.data.TablesFeed,
        gdata.spreadsheets.data.Record,
        gdata.spreadsheets.data.RecordsFeed,
        gdata.spreadsheets.data.ListRow,
        gdata.spreadsheets.data.ListEntry,
        gdata.spreadsheets.data.ListsFeed,
        gdata.spreadsheets.data.CellEntry,
        gdata.spreadsheets.data.CellsFeed])


def suite():
  return conf.build_suite([SpreadsheetEntryTest, DataClassSanityTest,
                           ListEntryTest, RecordEntryTest])


if __name__ == '__main__':
  unittest.main()


