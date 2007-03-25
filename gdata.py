#!/usr/bin/python
#
# Copyright (C) 2006 Google Inc.
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


"""Contains classes representing GData elements.

  Extends Atom classes to add GData specific elements.


"""


__author__ = 'api.jscudder (Jeffrey Scudder)'


from elementtree import ElementTree
import atom


# XML namespaces which are often used in GData entities.
GDATA_NAMESPACE = 'http://schemas.google.com/g/2005'
GDATA_TEMPLATE = '{http://schemas.google.com/g/2005}%s'
OPENSEARCH_NAMESPACE = 'http://a9.com/-/spec/opensearchrss/1.0/'
OPENSEARCH_TEMPLATE = '{http://a9.com/-/spec/opensearchrss/1.0/}%s'


class LinkFinder(object):
  """An "interface" providing methods to find link elements

  GData Entry elements often contain multiple links which differ in the rel
  attribute or content type. Often, developers are interested in a specific
  type of link so this class provides methods to find specific classes of
  links.

  This class is used as a mixin in GData entries.
  """

  def GetSelfLink(self):
    """Find the first link with rel set to 'self'

    Returns:
      An atom.Link or none if none of the links had rel equal to 'self'
    """

    for a_link in self.link:
      if a_link.rel == 'self':
        return a_link
    return None

  def GetEditLink(self):
    for a_link in self.link:
      if a_link.rel == 'edit':
        return a_link
    return None

  def GetHtmlLink(self):
    """Find the first link with rel of alternate and type of text/html

    Returns:
      An atom.Link or None if no links matched
    """
    for a_link in self.link:
      if a_link.rel == 'alternate' and a_link.type == 'text/html':
        return a_link
    return None

  def GetPostLink(self):
    for a_link in self.link:
      if a_link.rel == 'http://schemas.google.com/g/2005#post':
        return a_link
    return None

  def GetFeedLink(self):
    for a_link in self.link:
      if a_link.rel == 'http://schemas.google.com/g/2005#feed':
        return a_link
    return None

  def GetNextLink(self):
    for a_link in self.link:
      if a_link.rel == 'next':
        return a_link
    return None



class GDataFeed(atom.Feed, LinkFinder):
  """A Feed from a GData service"""

  def __init__(self, author=None, category=None, contributor=None,
      generator=None, icon=None, atom_id=None, link=None, logo=None, 
      rights=None, subtitle=None, title=None, updated=None, entry=None, 
      total_results=None, start_index=None, items_per_page=None,
      extension_elements=None, extension_attributes=None, text=None):
    """Constructor for Source
    
    Args:
      author: list (optional) A list of Author instances which belong to this
          class.
      category: list (optional) A list of Category instances
      contributor: list (optional) A list on Contributor instances
      generator: Generator (optional) 
      icon: Icon (optional) 
      id: Id (optional) The entry's Id element
      link: list (optional) A list of Link instances
      logo: Logo (optional) 
      rights: Rights (optional) The entry's Rights element
      subtitle: Subtitle (optional) The entry's subtitle element
      title: Title (optional) the entry's title element
      updated: Updated (optional) the entry's updated element
      entry: list (optional) A list of the Entry instances contained in the 
          feed.
      text: String (optional) The text contents of the element. This is the 
          contents of the Entry's XML text node. 
          (Example: <foo>This is the text</foo>)
      extension_elements: list (optional) A list of ExtensionElement instances
          which are children of this element.
      extension_attributes: dict (optional) A dictionary of strings which are 
          the values for additional XML attributes of this element.
    """

    self.author = author or []
    self.category = category or []
    self.contributor = contributor or []
    self.generator = generator
    self.icon = icon
    self.id = atom_id
    self.link = link or []
    self.logo = logo
    self.rights = rights
    self.subtitle = subtitle
    self.title = title
    self.updated = updated
    self.entry = entry or []
    self.total_results = total_results
    self.start_index = start_index
    self.items_per_page = items_per_page
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.total_results:
      element_tree.append(self.total_results._ToElementTree())
    if self.items_per_page:
      element_tree.append(self.items_per_page._ToElementTree())
    if self.start_index:
      element_tree.append(self.start_index._ToElementTree())
    atom.Feed._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (OPENSEARCH_NAMESPACE, 'totalResults'):
      self.total_results = _TotalResultsFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (OPENSEARCH_NAMESPACE, 'startIndex'):
      self.start_index = _StartIndexFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (OPENSEARCH_NAMESPACE, 'itemsPerPage'):
      self.items_per_page = _ItemsPerPageFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'id'):
      atom.Feed._TakeChildFromElementTree(self, child, element_tree)
      # Remove whitespace from the id element.
      if self.id and self.id.text:
        self.id.text = self.id.text.strip()
    elif child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'generator'):
      atom.Feed._TakeChildFromElementTree(self, child, element_tree)
      # Remove whitespace from the generator element.
      if self.generator and self.generator.text:
        self.generator.text = self.generator.text.strip()
    else:
      atom.Feed._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    atom.Feed._TransferFromElementTree(self, element_tree)

def GDataFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  to_return =  _GDataFeedFromElementTree(element_tree)
  return to_return

def _GDataFeedFromElementTree(element_tree):
  return atom._XFromElementTree(GDataFeed, 'feed', atom.ATOM_NAMESPACE, 
      element_tree)


class GDataEntry(atom.Entry, LinkFinder):
  """Extends Atom Entry to provide data processing"""
  
  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'id'):
      atom.Entry._TakeChildFromElementTree(self, child, element_tree)
      if self.id and self.id.text:
        self.id.text = self.id.text.strip()
    else:
      atom.Entry._TakeChildFromElementTree(self, child, element_tree)
  
def GDataEntryFromString(xml_string):
  """Creates a new GDataEntry instance given a string of XML."""

  element_tree = ElementTree.fromstring(xml_string)
  return _GDataEntryFromElementTree(element_tree)

_GDataEntryFromElementTree = atom._AtomInstanceFromElementTree(GDataEntry, 
    'entry', atom.ATOM_NAMESPACE)

class TotalResults(atom.AtomBase):
  """opensearch:TotalResults for a GData feed"""

  def __init__(self, extension_elements=None,
     extension_attributes=None, text=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = OPENSEARCH_TEMPLATE % 'totalResults'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

def TotalResultsFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _TotalResultsFromElementTree(element_tree)

def _TotalResultsFromElementTree(element_tree):
  return atom._XFromElementTree(TotalResults, 'totalResults',
      OPENSEARCH_NAMESPACE, element_tree)

  
class StartIndex(atom.AtomBase):
  """The opensearch:StartIndex element in GData feed"""

  def __init__(self, extension_elements=None, 
      extension_attributes=None, text=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = OPENSEARCH_TEMPLATE % 'startIndex'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

def StartIndexFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _StartIndexFromElementTree(element_tree)

def _StartIndexFromElementTree(element_tree):
  return atom._XFromElementTree(StartIndex, 'startIndex', 
      OPENSEARCH_NAMESPACE, element_tree)
      

class ItemsPerPage(atom.AtomBase):
  """The opensearch:itemsPerPage element in GData feed"""

  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = OPENSEARCH_TEMPLATE % 'itemsPerPage'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

def ItemsPerPageFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _ItemsPerPageFromElementTree(element_tree)

def _ItemsPerPageFromElementTree(element_tree):
  return atom._XFromElementTree(ItemsPerPage, 'itemsPerPage', 
      OPENSEARCH_NAMESPACE, element_tree)
 
 
class EntryLink(atom.AtomBase):
  """The gd:entryLink element"""
  
  def __init__(self, href=None, read_only=None, rel=None,
      entry=None, extension_elements=None, 
      extension_attributes=None, text=None):
    self.href = href
    self.read_only = read_only
    self.rel = rel
    self.entry = entry
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    
  def _TransferToElementTree(self, element_tree):
    if self.href:
      element_tree.attrib['href'] = self.href
    if self.read_only:
      element_tree.attrib['readOnly'] = self.read_only
    if self.rel:
      element_tree.attrib['rel'] = self.rel
    if self.entry:
      element_tree.append(self.entry._ToElementTree())
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = GDATA_TEMPLATE % 'entryLink'
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (GDATA_NAMESPACE, 'entry'):
      self.entry = _EntryLinkFromElementTree(child)
      element_tree.remove(child)
    else:
      GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'href':
      self.href = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'readOnly':
      self.read_only = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute,
          element_tree)

def _EntryLinkFromElementTree(element_tree):
  return atom._XFromElementTree(EntryLink, 'feedLink',
      GDATA_NAMESPACE, element_tree)


class FeedLink(atom.AtomBase):
  """The gd:feedLink element"""

  def __init__(self, count_hint=None, href=None, read_only=None, rel=None,
      feed=None, extension_elements=None, extension_attributes=None, text=None):
    self.count_hint = count_hint 
    self.href = href
    self.read_only = read_only
    self.rel = rel
    self.feed = feed
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.count_hint:
      element_tree.attrib['countHint'] = self.count_hint
    if self.href:
      element_tree.attrib['href'] = self.href
    if self.read_only:
      element_tree.attrib['readOnly'] = self.read_only
    if self.rel:
      element_tree.attrib['rel'] = self.rel
    if self.feed:
      element_tree.append(self.feed._ToElementTree())
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = GDATA_TEMPLATE % 'feedLink'
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (GDATA_NAMESPACE, 'feed'):
      self.feed = _GDataFeedFromElementTree(child)
      element_tree.remove(child)
    else:
      GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'countHint':
      self.count_hint = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'href':
      self.href = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'readOnly':
      self.read_only = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'rel':
      self.rel = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute,
          element_tree)  

def _FeedLinkFromElementTree(element_tree):
  return atom._XFromElementTree(FeedLink, 'feedLink',
      GDATA_NAMESPACE, element_tree)
