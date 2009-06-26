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


import atom.core
import atom.data


GDATA_TEMPLATE = '{http://schemas.google.com/g/2005}%s'
OPENSEARCH_TEMPLATE = '{http://a9.com/-/spec/opensearchrss/1.0/}%s'
BATCH_TEMPLATE = '{http://schemas.google.com/gdata/batch}%s'


# Labels used in batch request entries to specify the desired CRUD operation.
BATCH_INSERT = 'insert'
BATCH_UPDATE = 'update'
BATCH_DELETE = 'delete'
BATCH_QUERY = 'query'


class Error(Exception):
  pass


class MissingRequiredParameters(Error):
  pass


class LinkFinder(atom.data.LinkFinder):
  """Mixin used in Feed and Entry classes to simplify link lookups by type.
  
  Provides lookup methods for edit, edit-media, post, ACL and other special
  links which are common across Google Data APIs.
  """

  def find_html_link(self):
    """Finds the first link with rel of alternate and type of text/html."""
    for link in self.link:
      if link.rel == 'alternate' and link.type == 'text/html':
        return link.href
    return None

  FindHtmlLink = find_html_link

  def get_html_link(self):
    for a_link in self.link:
      if a_link.rel == 'alternate' and a_link.type == 'text/html':
        return a_link
    return None

  GetHtmlLink = get_html_link

  def find_post_link(self):
    """Get the URL to which new entries should be POSTed.

    The POST target URL is used to insert new entries.

    Returns:
      A str for the URL in the link with a rel matching the POST type.
    """
    return self.find_url('http://schemas.google.com/g/2005#post')

  FindPostLink = find_post_link

  def get_post_link(self):
    return self.get_link('http://schemas.google.com/g/2005#post')

  GetPostLink = get_post_link

  def find_acl_link(self):
    return self.find_url(
        'http://schemas.google.com/acl/2007#accessControlList')

  FindAclLink = find_acl_link

  def get_acl_link(self):
    return self.get_link(
        'http://schemas.google.com/acl/2007#accessControlList')

  GetAclLink = get_acl_link

  def find_feed_link(self):
    return self.find_url('http://schemas.google.com/g/2005#feed')

  FindFeedLink = find_feed_link

  def get_feed_link(self):
    return self.get_link('http://schemas.google.com/g/2005#feed')

  GetFeedLink = get_feed_link

  def find_previous_link(self):
    return self.find_url('previous')

  FindPreviousLink = find_previous_link

  def get_previous_link(self):
    return self.get_link('previous')

  GetPreviousLink = get_previous_link


class TotalResults(atom.core.XmlElement):
  """opensearch:TotalResults for a GData feed."""
  _qname = OPENSEARCH_TEMPLATE % 'totalResults'


class StartIndex(atom.core.XmlElement):
  """The opensearch:startIndex element in GData feed."""
  _qname = OPENSEARCH_TEMPLATE % 'startIndex'


class ItemsPerPage(atom.core.XmlElement):
  """The opensearch:itemsPerPage element in GData feed."""
  _qname = OPENSEARCH_TEMPLATE % 'itemsPerPage'


class ExtendedProperty(atom.core.XmlElement):
  """The Google Data extendedProperty element.

  Used to store arbitrary key-value information specific to your
  application. The value can either be a text string stored as an XML
  attribute (.value), or an XML node (XmlBlob) as a child element.

  This element is used in the Google Calendar data API and the Google
  Contacts data API.
  """
  _qname = GDATA_TEMPLATE % 'extendedProperty'
  name = 'name'
  value = 'value'

  def get_xml_blob(self):
    """Returns the XML blob as an atom.core.XmlElement.

    Returns:
      An XmlElement representing the blob's XML, or None if no
      blob was set.
    """
    if self._other_elements:
      return self._other_elements[0]
    else:
      return None

  GetXmlBlob = get_xml_blob

  def set_xml_blob(self, blob):
    """Sets the contents of the extendedProperty to XML as a child node.

    Since the extendedProperty is only allowed one child element as an XML
    blob, setting the XML blob will erase any preexisting member elements
    in this object.

    Args:
      blob: str  or atom.core.XmlElement representing the XML blob stored in
            the extendedProperty.
    """
    # Erase any existing extension_elements, clears the child nodes from the
    # extendedProperty.
    if isinstance(blob, atom.core.XmlElement):
      self._other_elements = [blob]
    else:
      self._other_elements = [atom.core.parse(str(blob))]

  SetXmlBlob = set_xml_blob


class GDEntry(atom.data.Entry, LinkFinder):
  """Extends Atom Entry to provide data processing"""
  etag = '{http://schemas.google.com/g/2005}etag'

  def get_id(self):
    if self.id is not None and self.id.text is not None:
      return self.id.text.strip()
    return None

  GetId = get_id

  def is_media(self):
    if self.find_media_edit_link():
      return True
    return False

  IsMedia = is_media

  def find_media_link(self):
    """Returns the URL to the media content, if the entry is a media entry.
    Otherwise returns None.
    """
    if self.is_media():
      return self.content.src
    return None

  FindMediaLink = find_media_link


class GDFeed(atom.data.Feed, LinkFinder):
  """A Feed from a GData service."""
  etag = '{http://schemas.google.com/g/2005}etag'
  total_results = TotalResults
  start_index = StartIndex
  items_per_page = ItemsPerPage
  entry = [GDEntry]
  
  def get_id(self):
    if self.id is not None and self.id.text is not None:
      return self.id.text.strip()
    return None

  GetId = get_id

  def get_generator(self):
    if self.generator and self.generator.text:
      return self.generator.text.strip()
    return None


class BatchId(atom.core.XmlElement):
  _qname = BATCH_TEMPLATE % 'id'


class BatchOperation(atom.core.XmlElement):
  _qname = BATCH_TEMPLATE % 'operation'
  type = 'type'


class BatchStatus(atom.core.XmlElement):
  """The batch:status element present in a batch response entry.

  A status element contains the code (HTTP response code) and
  reason as elements. In a single request these fields would
  be part of the HTTP response, but in a batch request each
  Entry operation has a corresponding Entry in the response
  feed which includes status information.

  See http://code.google.com/apis/gdata/batch.html#Handling_Errors
  """
  _qname = BATCH_TEMPLATE % 'status'
  code = 'code'
  reason = 'reason'
  content_type = 'content-type'


class BatchEntry(GDEntry):
  """An atom:entry for use in batch requests.

  The BatchEntry contains additional members to specify the operation to be
  performed on this entry and a batch ID so that the server can reference
  individual operations in the response feed. For more information, see:
  http://code.google.com/apis/gdata/batch.html
  """
  batch_operation = BatchOperation
  batch_id = BatchId
  batch_status = BatchStatus


class BatchInterrupted(atom.core.XmlElement):
  """The batch:interrupted element sent if batch request was interrupted.

  Only appears in a feed if some of the batch entries could not be processed.
  See: http://code.google.com/apis/gdata/batch.html#Handling_Errors
  """
  _qname = BATCH_TEMPLATE % 'interrupted'
  reason = 'reason'
  success = 'success'
  failures = 'failures'
  parsed = 'parsed'


class BatchFeed(GDFeed):
  """A feed containing a list of batch request entries."""
  interrupted = BatchInterrupted
  entry = [BatchEntry]

  def add_batch_entry(self, entry=None, id_url_string=None,
      batch_id_string=None, operation_string=None):
    """Logic for populating members of a BatchEntry and adding to the feed.

    If the entry is not a BatchEntry, it is converted to a BatchEntry so
    that the batch specific members will be present.

    The id_url_string can be used in place of an entry if the batch operation
    applies to a URL. For example query and delete operations require just
    the URL of an entry, no body is sent in the HTTP request. If an
    id_url_string is sent instead of an entry, a BatchEntry is created and
    added to the feed.

    This method also assigns the desired batch id to the entry so that it
    can be referenced in the server's response. If the batch_id_string is
    None, this method will assign a batch_id to be the index at which this
    entry will be in the feed's entry list.

    Args:
      entry: BatchEntry, atom.data.Entry, or another Entry flavor (optional)
          The entry which will be sent to the server as part of the batch
          request. The item must have a valid atom id so that the server
          knows which entry this request references.
      id_url_string: str (optional) The URL of the entry to be acted on. You
          can find this URL in the text member of the atom id for an entry.
          If an entry is not sent, this id will be used to construct a new
          BatchEntry which will be added to the request feed.
      batch_id_string: str (optional) The batch ID to be used to reference
          this batch operation in the results feed. If this parameter is None,
          the current length of the feed's entry array will be used as a
          count. Note that batch_ids should either always be specified or
          never, mixing could potentially result in duplicate batch ids.
      operation_string: str (optional) The desired batch operation which will
          set the batch_operation.type member of the entry. Options are
          'insert', 'update', 'delete', and 'query'

    Raises:
      MissingRequiredParameters: Raised if neither an id_ url_string nor an
          entry are provided in the request.

    Returns:
      The added entry.
    """
    if entry is None and id_url_string is None:
      raise MissingRequiredParameters('supply either an entry or URL string')
    if entry is None and id_url_string is not None:
      entry = BatchEntry(id=atom.data.Id(text=id_url_string))
    if batch_id_string is not None:
      entry.batch_id = BatchId(text=batch_id_string)
    elif entry.batch_id is None or entry.batch_id.text is None:
      entry.batch_id = BatchId(text=str(len(self.entry)))
    if operation_string is not None:
      entry.batch_operation = BatchOperation(type=operation_string)
    self.entry.append(entry)
    return entry

  AddBatchEntry = add_batch_entry

  def add_insert(self, entry, batch_id_string=None):
    """Add an insert request to the operations in this batch request feed.

    If the entry doesn't yet have an operation or a batch id, these will
    be set to the insert operation and a batch_id specified as a parameter.

    Args:
      entry: BatchEntry The entry which will be sent in the batch feed as an
          insert request.
      batch_id_string: str (optional) The batch ID to be used to reference
          this batch operation in the results feed. If this parameter is None,
          the current length of the feed's entry array will be used as a
          count. Note that batch_ids should either always be specified or
          never, mixing could potentially result in duplicate batch ids.
    """
    self.add_batch_entry(entry=entry, batch_id_string=batch_id_string,
        operation_string=BATCH_INSERT)

  AddInsert = add_insert

  def add_update(self, entry, batch_id_string=None):
    """Add an update request to the list of batch operations in this feed.

    Sets the operation type of the entry to insert if it is not already set
    and assigns the desired batch id to the entry so that it can be
    referenced in the server's response.

    Args:
      entry: BatchEntry The entry which will be sent to the server as an
          update (HTTP PUT) request. The item must have a valid atom id
          so that the server knows which entry to replace.
      batch_id_string: str (optional) The batch ID to be used to reference
          this batch operation in the results feed. If this parameter is None,
          the current length of the feed's entry array will be used as a
          count. See also comments for AddInsert.
    """
    self.add_batch_entry(entry=entry, batch_id_string=batch_id_string,
        operation_string=BATCH_UPDATE)

  AddUpdate = add_update

  def add_delete(self, url_string=None, entry=None, batch_id_string=None):
    """Adds a delete request to the batch request feed.

    This method takes either the url_string which is the atom id of the item
    to be deleted, or the entry itself. The atom id of the entry must be
    present so that the server knows which entry should be deleted.

    Args:
      url_string: str (optional) The URL of the entry to be deleted. You can
         find this URL in the text member of the atom id for an entry.
      entry: BatchEntry (optional) The entry to be deleted.
      batch_id_string: str (optional)

    Raises:
      MissingRequiredParameters: Raised if neither a url_string nor an entry
          are provided in the request.
    """
    self.add_batch_entry(entry=entry, id_url_string=url_string,
        batch_id_string=batch_id_string, operation_string=BATCH_DELETE)

  AddDelete = add_delete

  def add_query(self, url_string=None, entry=None, batch_id_string=None):
    """Adds a query request to the batch request feed.

    This method takes either the url_string which is the query URL
    whose results will be added to the result feed. The query URL will
    be encapsulated in a BatchEntry, and you may pass in the BatchEntry
    with a query URL instead of sending a url_string.

    Args:
      url_string: str (optional)
      entry: BatchEntry (optional)
      batch_id_string: str (optional)

    Raises:
      MissingRequiredParameters
    """
    self.add_batch_entry(entry=entry, id_url_string=url_string,
        batch_id_string=batch_id_string, operation_string=BATCH_QUERY)

  AddQuery = add_query

  def find_batch_link(self):
    return self.find_url('http://schemas.google.com/g/2005#batch')

  FindBatchLink = find_batch_link


class EntryLink(atom.core.XmlElement):
  """The gd:entryLink element"""
  _qname = GDATA_TEMPLATE % 'entryLink'
  entry = GDEntry
  rel = 'rel'
  read_only = 'readOnly'
  href = 'href'


class FeedLink(atom.core.XmlElement):
  """The gd:feedLink element"""
  _qname = GDATA_TEMPLATE % 'feedLink'
  feed = GDFeed
  rel = 'rel'
  read_only = 'readOnly'
  count_hint = 'countHint'
  href = 'href'


# TODO: once atom Link exists, inherit from that.
class Link(atom.core.XmlElement):
  _qname = '{http://www.w3.org/2005/Atom}link'
  rel = 'rel'
  href = 'href'


# TODO: remove this once atom Entry and Feed exist.
class FeedEntryParent(atom.core.XmlElement):
  etag = '{http://schemas.google.com/g/2005}etag'
  link = [Link]

  def find_url(self, rel):
    for link in self.link:
      if link.rel == rel and link.href:
        return link.href
    return None


# TODO: once atom Entry exists, inherit from that.
class GEntry(FeedEntryParent):
  _qname = '{http://www.w3.org/2005/Atom}entry'

  def get_edit_url(self):
    return self.find_url('edit')

  GetEditUrl = get_edit_url


def entry_from_string(xml_string, version=1, encoding='UTF-8'):
  return atom.core.parse(xml_string, GEntry, version, encoding)


EntryFromString = entry_from_string


# TODO: once atom Feed exists, inherit from that.
class GFeed(FeedEntryParent):
  _qname = '{http://www.w3.org/2005/Atom}feed'
  entry = [GEntry]

  def get_next_url(self):
    return self.find_url('next')

  GetNextUrl = get_next_url


def feed_from_string(xml_string, version=1, encoding='UTF-8'):
  return atom.core.parse(xml_string, GFeed, version, encoding)


FeedFromString = feed_from_string
