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

"""Contains extensions to Atom objects used with Google Spreadsheets.
"""

__author__ = 'api.laurabeth@gmail.com (Laura Beth Lincoln)'


try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import atom
import gdata
import re
import string


# XML namespaces which are often used in Google Spreadsheets entities.
GSPREADSHEETS_NAMESPACE = 'http://schemas.google.com/spreadsheets/2006'
GSPREADSHEETS_TEMPLATE = '{http://schemas.google.com/spreadsheets/2006}%s'

GSPREADSHEETS_EXTENDED_NAMESPACE = ('http://schemas.google.com/spreadsheets'
                                    '/2006/extended')
GSPREADSHEETS_EXTENDED_TEMPLATE = ('{http://schemas.google.com/spreadsheets'
                                   '/2006/extended}%s')

class SpreadsheetsSpreadsheetsFeed(gdata.GDataFeed):
  """A feed containing Google Spreadsheets Spreadsheets"""

  def _TransferToElementTree(self, element_tree):
    for an_entry in self.entry:
      element_tree.append(an_entry._ToElementTree())
    gdata.GDataFeed._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_SpreadsheetsSpreadsheetFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataFeed._TransferFromElementTree(self, element_tree)

def SpreadsheetsSpreadsheetsFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SpreadsheetsSpreadsheetsFeedFromElementTree(element_tree)

def _SpreadsheetsSpreadsheetsFeedFromElementTree(element_tree):
  return atom._XFromElementTree(SpreadsheetsSpreadsheetsFeed, 'feed', 
      atom.ATOM_NAMESPACE, element_tree)
      
class SpreadsheetsWorksheetsFeed(gdata.GDataFeed):
  """A feed containing Google Spreadsheets Spreadsheets"""

  def _TransferToElementTree(self, element_tree):
    for an_entry in self.entry:
      element_tree.append(an_entry._ToElementTree())
    gdata.GDataFeed._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_SpreadsheetsWorksheetFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, 
          child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataFeed._TransferFromElementTree(self, element_tree)

def SpreadsheetsWorksheetsFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SpreadsheetsWorksheetsFeedFromElementTree(element_tree)

def _SpreadsheetsWorksheetsFeedFromElementTree(element_tree):
  return atom._XFromElementTree(SpreadsheetsWorksheetsFeed, 'feed', 
      atom.ATOM_NAMESPACE, element_tree)
      
class SpreadsheetsCellsFeed(gdata.GDataFeed):
  """A feed containing Google Spreadsheets Cells"""

  def _TransferToElementTree(self, element_tree):
    for an_entry in self.entry:
      element_tree.append(an_entry._ToElementTree())
    gdata.GDataFeed._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_SpreadsheetsCellFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (GSPREADSHEETS_NAMESPACE, 'rowCount'):
      self.extension_elements.append(_RowCountFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (GSPREADSHEETS_NAMESPACE, 'colCount'):
      self.extension_elements.append(_ColCountFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataFeed._TransferFromElementTree(self, element_tree)

def SpreadsheetsCellsFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SpreadsheetsCellsFeedFromElementTree(element_tree)

def _SpreadsheetsCellsFeedFromElementTree(element_tree):
  return atom._XFromElementTree(SpreadsheetsCellsFeed, 'feed', 
      atom.ATOM_NAMESPACE, element_tree)
      
class SpreadsheetsListFeed(gdata.GDataFeed):
  """A feed containing Google Spreadsheets Spreadsheets"""

  def _TransferToElementTree(self, element_tree):
    for an_entry in self.entry:
      element_tree.append(an_entry._ToElementTree())
    gdata.GDataFeed._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_SpreadsheetsListFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataFeed._TransferFromElementTree(self, element_tree)

def SpreadsheetsListFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SpreadsheetsListFeedFromElementTree(element_tree)

def _SpreadsheetsListFeedFromElementTree(element_tree):
  return atom._XFromElementTree(SpreadsheetsListFeed, 'feed', 
      atom.ATOM_NAMESPACE, element_tree)

class SpreadsheetsSpreadsheet(atom.Entry):
  """A Google Spreadsheets flavor of a Spreadsheet Atom Entry """
  
  def __init__(self, author=None, category=None, content=None,
      contributor=None, atom_id=None, link=None, published=None, rights=None,
      source=None, summary=None, title=None, updated=None,
      text=None, extension_elements=None, extension_attributes=None):
    self.author = author or []
    self.category = category or []
    self.content = content
    self.contributor = contributor or []
    self.id = atom_id
    self.link = link or []
    self.published = published
    self.rights = rights
    self.source = source
    self.summary = summary
    self.title = title
    self.updated = updated
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    
def SpreadsheetsSpreadsheetFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SpreadsheetsSpreadsheetFromElementTree(element_tree)

def _SpreadsheetsSpreadsheetFromElementTree(element_tree):
  return atom._XFromElementTree(SpreadsheetsSpreadsheet, 'entry', 
      atom.ATOM_NAMESPACE, element_tree)


class SpreadsheetsWorksheet(atom.Entry):
  """A Google Spreadsheets flavor of a Worksheet Atom Entry """
  
  def __init__(self, author=None, category=None, content=None,
      contributor=None, atom_id=None, link=None, published=None, rights=None,
      source=None, summary=None, title=None, updated=None, row_count=None,
      col_count=None, text=None, extension_elements=None, 
      extension_attributes=None):
    self.author = author or []
    self.category = category or []
    self.content = content
    self.contributor = contributor or []
    self.id = atom_id
    self.link = link or []
    self.published = published
    self.rights = rights
    self.source = source
    self.summary = summary
    self.title = title
    self.updated = updated
    self.row_count = row_count
    self.col_count = col_count
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.append(self.row_count._ToElementTree())
    element_tree.append(self.col_count._ToElementTree())
    atom.Entry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (GSPREADSHEETS_NAMESPACE, 'rowCount'):
      self.row_count = _RowCountFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (GSPREADSHEETS_NAMESPACE, 'colCount'):
      self.col_count = _ColCountFromElementTree(child)
      element_tree.remove(child)
    else:
      atom.Entry._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    atom.Entry._TransferFromElementTree(self, element_tree)

def SpreadsheetsWorksheetFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SpreadsheetsWorksheetFromElementTree(element_tree)

def _SpreadsheetsWorksheetFromElementTree(element_tree):
  return atom._XFromElementTree(SpreadsheetsWorksheet, 'entry', 
      atom.ATOM_NAMESPACE, element_tree)


class SpreadsheetsCell(atom.Entry):
  """A Google Spreadsheets flavor of a Cell Atom Entry """
  
  def __init__(self, author=None, category=None, content=None,
      contributor=None, atom_id=None, link=None, published=None, rights=None,
      source=None, summary=None, title=None, updated=None, cell=None, 
      text=None, extension_elements=None, extension_attributes=None):
    self.author = author or []
    self.category = category or []
    self.content = content
    self.contributor = contributor or []
    self.id = atom_id
    self.link = link or []
    self.published = published
    self.rights = rights
    self.source = source
    self.summary = summary
    self.title = title
    self.updated = updated
    self.cell = cell
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.append(self.cell._ToElementTree())
    atom.Entry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (GSPREADSHEETS_NAMESPACE, 'cell'):
      self.cell = _CellFromElementTree(child)
      element_tree.remove(child)
    else:
      atom.Entry._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    atom.Entry._TransferFromElementTree(self, element_tree)

def SpreadsheetsCellFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SpreadsheetsCellFromElementTree(element_tree)

def _SpreadsheetsCellFromElementTree(element_tree):
  return atom._XFromElementTree(SpreadsheetsCell, 'entry', 
      atom.ATOM_NAMESPACE, element_tree)


class SpreadsheetsList(atom.Entry):
  """A Google Spreadsheets flavor of a List Atom Entry """
  
  def __init__(self, author=None, category=None, content=None,
      contributor=None, atom_id=None, link=None, published=None, rights=None,
      source=None, summary=None, title=None, updated=None, custom=None, 
      text=None, extension_elements=None, extension_attributes=None):
    self.author = author or []
    self.category = category or []
    self.content = content
    self.contributor = contributor or []
    self.id = atom_id
    self.link = link or []
    self.published = published
    self.rights = rights
    self.source = source
    self.summary = summary
    self.title = title
    self.updated = updated
    self.custom = custom or {}
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    for key, a_custom in self.custom.items():
      element_tree.append(a_custom._ToElementTree())
    atom.Entry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    namespace_uri, local_tag = string.split(child.tag[1:], "}", 1)
    if namespace_uri == GSPREADSHEETS_EXTENDED_NAMESPACE:
      self.custom[local_tag] = _CustomFromElementTree(child)
      element_tree.remove(child)
    else:
      atom.Entry._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    atom.Entry._TransferFromElementTree(self, element_tree)

def SpreadsheetsListFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SpreadsheetsListFromElementTree(element_tree)

def _SpreadsheetsListFromElementTree(element_tree):
  return atom._XFromElementTree(SpreadsheetsList, 'entry', 
      atom.ATOM_NAMESPACE, element_tree)


class ColCount(atom.AtomBase):
  """The Google Spreadsheets colCount element """

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = GSPREADSHEETS_TEMPLATE % 'colCount'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

def ColCountFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _ColCountFromElementTree(element_tree)

def _ColCountFromElementTree(element_tree):
  return atom._XFromElementTree(ColCount, 'colCount', GSPREADSHEETS_NAMESPACE,
      element_tree)
      

class RowCount(atom.AtomBase):
  """The Google Spreadsheets rowCount element """

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = GSPREADSHEETS_TEMPLATE % 'rowCount'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

def RowCountFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _RowCountFromElementTree(element_tree)

def _RowCountFromElementTree(element_tree):
  return atom._XFromElementTree(RowCount, 'rowCount', GSPREADSHEETS_NAMESPACE,
      element_tree)
      

class Cell(atom.AtomBase):
  """The Google Spreadsheets cell element """
  
  def __init__(self, text=None, row=None, col=None, inputValue=None, 
      numericValue=None, extension_elements=None, extension_attributes=None):
    self.text = text
    self.row = row
    self.col = col
    self.inputValue = inputValue
    self.numericValue = numericValue
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    
  def _TransferToElementTree(self, element_tree):
    element_tree.tag = GSPREADSHEETS_TEMPLATE % 'cell'
    element_tree.attrib['row'] = self.row
    element_tree.attrib['col'] = self.col
    if self.inputValue:
      element_tree.attrib['inputValue'] = self.inputValue
    if self.numericValue:
      element_tree.attrib['numericValue'] = self.numericValue
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree
    
  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'row':
      self.row = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'col':
      self.col = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'inputValue':
      self.inputValue = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'numericValue':
      self.numericValue = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)

def CellFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _CellFromElementTree(element_tree)
  
def _CellFromElementTree(element_tree):
  return atom._XFromElementTree(Cell, 'cell', GSPREADSHEETS_NAMESPACE,
      element_tree)
      

class Custom(atom.AtomBase):
  """The Google Spreadsheets custom element"""

  def __init__(self, column=None, text=None, extension_elements=None,
      extension_attributes=None):
    self.column = column   # The name of the column
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    
  def _TransferToElementTree(self, element_tree):
    element_tree.tag = GSPREADSHEETS_EXTENDED_TEMPLATE % self.column
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

def CustomFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _CustomFromElementTree(element_tree)

def _CustomFromElementTree(element_tree):
  namespace_uri, local_tag = string.split(element_tree.tag[1:], "}", 1)
  if namespace_uri == GSPREADSHEETS_EXTENDED_NAMESPACE:
    new_custom = atom._XFromElementTree(Custom, local_tag, 
        GSPREADSHEETS_EXTENDED_NAMESPACE, element_tree)
    new_custom.column = local_tag
    return new_custom
  return None
