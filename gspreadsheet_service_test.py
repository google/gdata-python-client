#!/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
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

__author__ = 'api.laurabeth@gmail.com (Laura Beth Lincoln)'

import unittest
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gspreadsheet_service
import gdata_service
import app_service
import gspreadsheet
import atom
import getpass


username = ''
password = ''
ss_key = ''
ws_key = ''



class DocumentQueryTest(unittest.TestCase):
  
  def setUp(self):
    self.query = gspreadsheet_service.DocumentQuery()
    
  def testTitle(self):
    self.query['title'] = 'my title'
    self.assert_(self.query['title'] == 'my title')
    self.assert_(self.query.ToUri() == '?title=my+title')
    
  def testTitleExact(self):
    self.query['title-exact'] = 'true'
    self.assert_(self.query['title-exact'] == 'true')
    self.assert_(self.query.ToUri() == '?title-exact=true')
    

class CellQueryTest(unittest.TestCase):
  
  def setUp(self):
    self.query = gspreadsheet_service.CellQuery()
    
  def testMinRow(self):
    self.query['min-row'] = '1'
    self.assert_(self.query['min-row'] == '1')
    self.assert_(self.query.ToUri() == '?min-row=1')
    
  def testMaxRow(self):
    self.query['max-row'] = '100'
    self.assert_(self.query['max-row'] == '100')
    self.assert_(self.query.ToUri() == '?max-row=100')
    
  def testMinCol(self):
    self.query['min-col'] = '2'
    self.assert_(self.query['min-col'] == '2')
    self.assert_(self.query.ToUri() == '?min-col=2')
    
  def testMaxCol(self):
    self.query['max-col'] = '20'
    self.assert_(self.query['max-col'] == '20')
    self.assert_(self.query.ToUri() == '?max-col=20')
    
  def testRange(self):
    self.query['range'] = 'A1:B4'
    self.assert_(self.query['range'] == 'A1:B4')
    self.assert_(self.query.ToUri() == '?range=A1%3AB4')
    
  def testReturnEmpty(self):
    self.query['return-empty'] = 'false'
    self.assert_(self.query['return-empty'] == 'false')
    self.assert_(self.query.ToUri() == '?return-empty=false')
    

class ListQueryTest(unittest.TestCase):

  def setUp(self):
    self.query = gspreadsheet_service.ListQuery()
    
  def testSpreadsheetQuery(self):
    self.query['sq'] = 'first=john&last=smith'
    self.assert_(self.query['sq'] == 'first=john&last=smith')
    self.assert_(self.query.ToUri() == '?sq=first%3Djohn%26last%3Dsmith')
    
  def testOrderByQuery(self):
    self.query['orderby'] = 'column:first'
    self.assert_(self.query['orderby'] == 'column:first')
    self.assert_(self.query.ToUri() == '?orderby=column%3Afirst')
    
  def testReverseQuery(self):
    self.query['reverse'] = 'true'
    self.assert_(self.query['reverse'] == 'true')
    self.assert_(self.query.ToUri() == '?reverse=true')
    

class SpreadsheetsServiceTest(unittest.TestCase):

  def setUp(self):
    self.key = ss_key 
    self.worksheet = ws_key
    self.gd_client = gspreadsheet_service.SpreadsheetsService()
    self.gd_client.email = username
    self.gd_client.password = password 
    self.gd_client.source = 'SpreadsheetsClient "Unit" Tests'
    self.gd_client.ProgrammaticLogin()
    
    
  def testGetSpreadsheetsFeed(self):
    #feed = self.gd_client.GetSpreadsheetsFeed()
    #self.assert_(isinstance(feed, gspreadsheet.SpreadsheetsSpreadsheetsFeed))
    entry = self.gd_client.GetSpreadsheetsFeed(self.key)
    self.assert_(isinstance(entry, gspreadsheet.SpreadsheetsSpreadsheet))
    
  def testGetWorksheetsFeed(self):
    feed = self.gd_client.GetWorksheetsFeed(self.key)
    self.assert_(isinstance(feed, gspreadsheet.SpreadsheetsWorksheetsFeed))
    entry = self.gd_client.GetWorksheetsFeed(self.key, self.worksheet)
    self.assert_(isinstance(entry, gspreadsheet.SpreadsheetsWorksheet))
    
  def testGetCellsFeed(self):
    feed = self.gd_client.GetCellsFeed(self.key)
    self.assert_(isinstance(feed, gspreadsheet.SpreadsheetsCellsFeed))
    entry = self.gd_client.GetCellsFeed(self.key, cell='R5C1')
    self.assert_(isinstance(entry, gspreadsheet.SpreadsheetsCell))
    
  def testGetListFeed(self):
    feed = self.gd_client.GetListFeed(self.key)
    self.assert_(isinstance(feed, gspreadsheet.SpreadsheetsListFeed))
    entry = self.gd_client.GetListFeed(self.key, row_id='cokwr')
    self.assert_(isinstance(entry, gspreadsheet.SpreadsheetsList))
    
  def testUpdateCell(self):
    self.gd_client.UpdateCell(row='5', col='1', inputValue='', key=self.key)
    self.gd_client.UpdateCell(row='5', col='1', inputValue='newer data', 
         key=self.key)
   
  def testInsertUpdateRow(self):
    entry = self.gd_client.InsertRow(dict(a1='new', b1='row', 
        c1='was', d1='here'), self.key)
    entry = self.gd_client.UpdateRow(entry, dict(a1='newer', 
        b1=entry.custom[1].text, c1=entry.custom[2].text, 
        d1=entry.custom[3].text))
    self.gd_client.DeleteRow(entry)
    
    

if __name__ == '__main__':
  print ('NOTE: Please run these tests only with a test account. ' +
      'The tests may delete or update your data.')
  username = raw_input('Please enter your username: ')
  password = getpass.getpass()
  ss_key = raw_input('Please enter your spreadsheet key: ')
  ws_key = raw_input('Please enter your worksheet key: ')
  unittest.main()
