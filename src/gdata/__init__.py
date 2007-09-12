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


"""Contains classes representing Google Data elements.

  Extends Atom classes to add Google Data specific elements.
"""


__author__ = 'api.jscudder (Jeffrey Scudder)'

import os
try:
  from xml.etree import cElementTree as ElementTree
except ImportError:
  try:
    import cElementTree as ElementTree
  except ImportError:
    from elementtree import ElementTree
import atom


# XML namespaces which are often used in GData entities.
GDATA_NAMESPACE = 'http://schemas.google.com/g/2005'
GDATA_TEMPLATE = '{http://schemas.google.com/g/2005}%s'
OPENSEARCH_NAMESPACE = 'http://a9.com/-/spec/opensearchrss/1.0/'
OPENSEARCH_TEMPLATE = '{http://a9.com/-/spec/opensearchrss/1.0/}%s'
BATCH_NAMESPACE = 'http://schemas.google.com/gdata/batch'

class Error(Exception):
  pass

class MediaSource(object):
  """GData Entries can refer to media sources, so this class provides a
  place to store references to these objects along with some metadata.
  """
  
  def __init__(self, file_handle=None, content_type=None, content_length=None,
      file_path=None, file_name=None):
    """Creates an object of type MediaSource.

    Args:
      file_handle: A file handle pointing to the file to be encapsulated in the
                   MediaSource
      content_type: string The MIME type of the file. Required if a file_handle
                    is given.
      content_length: int The size of the file. Required if a file_handle is
                      given.
      file_path: string (optional) A full path name to the file. Used in
                    place of a file_handle.
      file_name: string The name of the file without any path information.
                 Required if a file_handle is given.
    """
    self.file_handle = file_handle
    self.content_type = content_type
    self.content_length = content_length
    self.file_name = file_name

    if (file_handle is None and content_type is not None and
        file_path is not None):

        self.setFile(file_path, content_type)

  def setFile(self, file_name, content_type):
    """A helper function which can create a file handle from a given filename
    and set the content type and length all at once.

    Args:
      file_name: string The path and file name to the file containing the media
      content_type: string A MIME type representing the type of the media
    """

    self.file_handle = open(file_name, 'rb')
    self.content_type = content_type
    self.content_length = os.path.getsize(file_name)
    self.file_name = os.path.basename(file_name)
  

class LinkFinder(atom.LinkFinder):
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
    
  def GetEditMediaLink(self):
    """The Picasa API mistakenly returns media-edit rather than edit-media, but
    this may change soon.
    """
    for a_link in self.link:
      if a_link.rel == 'edit-media':
        return a_link
      if a_link.rel == 'media-edit':
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


class TotalResults(atom.AtomBase):
  """opensearch:TotalResults for a GData feed"""
  
  _tag = 'totalResults'
  _namespace = OPENSEARCH_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()

  def __init__(self, extension_elements=None,
     extension_attributes=None, text=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


def TotalResultsFromString(xml_string):
  return atom.CreateClassFromXMLString(TotalResults, xml_string)

  
class StartIndex(atom.AtomBase):
  """The opensearch:startIndex element in GData feed"""

  _tag = 'startIndex'
  _namespace = OPENSEARCH_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()

  def __init__(self, extension_elements=None, 
      extension_attributes=None, text=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


def StartIndexFromString(xml_string):
  return atom.CreateClassFromXMLString(StartIndex, xml_string)


class ItemsPerPage(atom.AtomBase):
  """The opensearch:itemsPerPage element in GData feed"""

  _tag = 'itemsPerPage'
  _namespace = OPENSEARCH_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()

  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


def ItemsPerPageFromString(xml_string):
  return atom.CreateClassFromXMLString(ItemsPerPage, xml_string)


class GDataEntry(atom.Entry, LinkFinder):
  """Extends Atom Entry to provide data processing"""

  _tag = atom.Entry._tag
  _namespace = atom.Entry._namespace
  _children = atom.Entry._children.copy()
  _attributes = atom.Entry._attributes.copy()

  def __GetId(self):
    return self.__id

  # This method was created to strip the unwanted whitespace from the id's 
  # text node.
  def __SetId(self, id):
    self.__id = id
    if id is not None:
      self.__id.text = id.text.strip()

  id = property(__GetId, __SetId)
  
  def IsMedia(self):
    """Determines whether or not an entry is a GData Media entry.
    """
    if (self.GetEditMediaLink()):
      return True
    else:
      return False
  
  def GetMediaURL(self):
    """Returns the URL to the media content, if the entry is a media entry.
    Otherwise returns None.
    """
    if not self.IsMedia():
      return None
    else:
      return self.content.src


def GDataEntryFromString(xml_string):
  """Creates a new GDataEntry instance given a string of XML."""
  return atom.CreateClassFromXMLString(GDataEntry, xml_string)


class GDataFeed(atom.Feed, LinkFinder):
  """A Feed from a GData service"""

  _tag = 'feed'
  _namespace = atom.ATOM_NAMESPACE
  _children = atom.Feed._children.copy()
  _attributes = atom.Feed._attributes.copy()
  _children['{%s}totalResults' % OPENSEARCH_NAMESPACE] = ('total_results', 
                                                          TotalResults)
  _children['{%s}startIndex' % OPENSEARCH_NAMESPACE] = ('start_index', 
                                                        StartIndex)
  _children['{%s}itemsPerPage' % OPENSEARCH_NAMESPACE] = ('items_per_page',
                                                          ItemsPerPage)
               # Add a conversion rule for atom:entry to make it into a GData
               # Entry.
  _children['{%s}entry' % atom.ATOM_NAMESPACE] = ('entry', [GDataEntry])

  def __GetId(self):
    return self.__id

  def __SetId(self, id):
    self.__id = id
    if id is not None:
      self.__id.text = id.text.strip()

  id = property(__GetId, __SetId)

  def __GetGenerator(self):
    return self.__generator

  def __SetGenerator(self, generator):
    self.__generator = generator
    if generator is not None:
      self.__generator.text = generator.text.strip()

  generator = property(__GetGenerator, __SetGenerator)

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


def GDataFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(GDataFeed, xml_string)


class BatchId(atom.AtomBase):
  _tag = 'id'
  _namespace = BATCH_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()


def BatchIdFromString(xml_string):
  return atom.CreateClassFromXMLString(BatchId, xml_string)


class BatchOperation(atom.AtomBase):
  _tag = 'operation'
  _namespace = BATCH_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['type'] = 'type'

  def __init__(self, op_type=None, extension_elements=None, 
               extension_attributes=None,
               text=None):
    self.type = op_type
    atom.AtomBase.__init__(self, 
                           extension_elements=extension_elements, 
                           extension_attributes=extension_attributes, 
                           text=text)


def BatchOperationFromString(xml_string):
  return atom.CreateClassFromXMLString(BatchOperation, xml_string)


class BatchStatus(atom.AtomBase):
  """The batch:status element present in a batch response entry.
  
  A status element contains the code (HTTP response code) and 
  reason as elements. In a single request these fields would
  be part of the HTTP response, but in a batch request each
  Entry operation has a corresponding Entry in the response
  feed which includes status information.

  See http://code.google.com/apis/gdata/batch.html#Handling_Errors
  """

  _tag = 'status'
  _namespace = BATCH_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['code'] = 'code'
  _attributes['reason'] = 'reason'
  _attributes['content-type'] = 'content_type'

  def __init__(self, code=None, reason=None, content_type=None, 
               extension_elements=None, extension_attributes=None, text=None):
    self.code = code
    self.reason = reason
    self.content_type = content_type
    atom.AtomBase.__init__(self, extension_elements=extension_elements,
                           extension_attributes=extension_attributes, 
                           text=text)


def BatchStatusFromString(xml_string):
  return atom.CreateClassFromXMLString(BatchStatus, xml_string)


class BatchEntry(GDataEntry):
  """An atom:entry for use in batch requests.

  The BatchEntry contains additional members to specify the operation to be
  performed on this entry and a batch ID so that the server can reference
  individual operations in the response feed. For more information, see:
  http://code.google.com/apis/gdata/batch.html
  """

  _tag = GDataEntry._tag
  _namespace = GDataEntry._namespace
  _children = GDataEntry._children.copy()
  _children['{%s}operation' % BATCH_NAMESPACE] = ('batch_operation', BatchOperation) 
  _children['{%s}id' % BATCH_NAMESPACE] = ('batch_id', BatchId)
  _children['{%s}status' % BATCH_NAMESPACE] = ('batch_status', BatchStatus)
  _attributes = GDataEntry._attributes.copy()

  def __init__(self, author=None, category=None, content=None,
      contributor=None, atom_id=None, link=None, published=None, rights=None,
      source=None, summary=None, control=None, title=None, updated=None,
      batch_operation=None, batch_id=None, batch_status=None,
      extension_elements=None, extension_attributes=None, text=None):
    self.batch_operation = batch_operation
    self.batch_id = batch_id
    self.batch_status = batch_status
    GDataEntry.__init__(self, author=author, category=category, 
        content=content, contributor=contributor, atom_id=atom_id, link=link, 
        published=published, rights=rights, source=source, summary=summary, 
        control=control, title=title, updated=updated, 
        extension_elements=extension_elements, 
        extension_attributes=extension_attributes, text=text)


def BatchEntryFromString(xml_string):
  return atom.CreateClassFromXMLString(BatchEntry, xml_string)


class BatchInterrupted(atom.AtomBase):
  """The batch:interrupted element sent if batch request was interrupted.
  
  Only appears in a feed if some of the batch entries could not be processed.
  See: http://code.google.com/apis/gdata/batch.html#Handling_Errors
  """

  _tag = 'interrupted'
  _namespace = BATCH_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['reason'] = 'reason'
  _attributes['success'] = 'success'
  _attributes['failures'] = 'failures'
  _attributes['parsed'] = 'parsed'

  def __init__(self, reason=None, success=None, failures=None, parsed=None, 
               extension_elements=None, extension_attributes=None, text=None):
    self.reason = reason
    self.success = success
    self.failures = failures
    self.parsed = parsed
    atom.AtomBase.__init__(self, extension_elements=extension_elements,
                           extension_attributes=extension_attributes, 
                           text=text)


def BatchInterruptedFromString(xml_string):
  return atom.CreateClassFromXMLString(BatchInterrupted, xml_string)


class BatchFeed(GDataFeed):
  """A feed containing a list of batch request entries."""

  _tag = GDataFeed._tag
  _namespace = GDataFeed._namespace
  _children = GDataFeed._children.copy()
  _attributes = GDataFeed._attributes.copy()
  _children['{%s}entry' % atom.ATOM_NAMESPACE] = ('entry', [BatchEntry])
  _children['{%s}interrupted' % BATCH_NAMESPACE] = ('interrupted', BatchInterrupted)

  def __init__(self, author=None, category=None, contributor=None,
      generator=None, icon=None, atom_id=None, link=None, logo=None,
      rights=None, subtitle=None, title=None, updated=None, entry=None,
      total_results=None, start_index=None, items_per_page=None,
      interrupted=None,
      extension_elements=None, extension_attributes=None, text=None):
    self.interrupted = interrupted
    GDataFeed.__init__(self, author=author, category=category, 
                       contributor=contributor, generator=generator, 
                       icon=icon, atom_id=atom_id, link=link, 
                       logo=logo, rights=rights, subtitle=subtitle,
                       title=title, updated=updated, entry=entry,
                       total_results=total_results, start_index=start_index,
                       items_per_page=items_per_page,
                       extension_elements=extension_elements, 
                       extension_attributes=extension_attributes,
                       text=text)


def BatchFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(BatchFeed, xml_string)
  

class EntryLink(atom.AtomBase):
  """The gd:entryLink element"""

  _tag = 'entryLink'
  _namespace = GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  # The entry used to be an atom.Entry, now it is a GDataEntry.
  _children['{%s}entry' % atom.ATOM_NAMESPACE] = ('entry', GDataEntry)
  _attributes['rel'] = 'rel',
  _attributes['readOnly'] = 'read_only'
  _attributes['href'] = 'href'
  
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
    

def EntryLinkFromString(xml_string):
  return atom.CreateClassFromXMLString(EntryLink, xml_string)


class FeedLink(atom.AtomBase):
  """The gd:feedLink element"""

  _tag = 'feedLink'
  _namespace = GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _children['{%s}feed' % atom.ATOM_NAMESPACE] = ('feed', GDataFeed)
  _attributes['rel'] = 'rel'
  _attributes['readOnly'] = 'read_only'
  _attributes['countHint'] = 'count_hint'
  _attributes['href'] = 'href'

  def __init__(self, count_hint=None, href=None, read_only=None, rel=None,
      feed=None, extension_elements=None, extension_attributes=None,
      text=None):
    self.count_hint = count_hint 
    self.href = href
    self.read_only = read_only
    self.rel = rel
    self.feed = feed
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


def FeedLinkFromString(xml_string):
  return atom.CreateClassFromXMLString(EntryLink, xml_string)
