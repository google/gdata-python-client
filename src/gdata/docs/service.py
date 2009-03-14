#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.
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

"""DocsService extends the GDataService to streamline Google Documents
  operations.

  DocsService: Provides methods to query feeds and manipulate items.
                    Extends GDataService.

  DocumentQuery: Queries a Google Document list feed.

  DocumentAclQuery: Queries a Google Document Acl feed.
"""


__author__ = ('api.jfisher (Jeff Fisher), '
              'api.eric@google.com (Eric Bidelman)')

import re
import atom
import gdata.service
import gdata.docs


# XML Namespaces used in Google Documents entities.
DATA_KIND_SCHEME = 'http://schemas.google.com/g/2005#kind'
DOCUMENT_KIND_TERM = 'http://schemas.google.com/docs/2007#document'
SPREADSHEET_KIND_TERM = 'http://schemas.google.com/docs/2007#spreadsheet'
PRESENTATION_KIND_TERM = 'http://schemas.google.com/docs/2007#presentation'
FOLDER_KIND_TERM = 'http://schemas.google.com/docs/2007#folder'
PDF_KIND_TERM = 'http://schemas.google.com/docs/2007#pdf'

LABEL_SCHEME = 'http://schemas.google.com/g/2005/labels'
STARRED_LABEL_TERM = LABEL_SCHEME + '#starred'
TRASHED_LABEL_TERM = LABEL_SCHEME + '#trashed'
HIDDEN_LABEL_TERM = LABEL_SCHEME + '#hidden'
MINE_LABEL_TERM = LABEL_SCHEME + '#mine'
PRIVATE_LABEL_TERM = LABEL_SCHEME + '#private'
SHARED_WITH_DOMAIN_LABEL_TERM = LABEL_SCHEME + '#shared-with-domain'

FOLDERS_SCHEME_PREFIX = 'http://schemas.google.com/docs/2007/folders/'

DOWNLOAD_SPREADSHEET_FORMATS = {
  'xls': '4',
  'ods': '13',
  'pdf': '12',
  'csv': '5',
  'tsv': '23',
  'html': '102'
  }

# File extensions of documents that are permitted to be uploaded or downloaded.
SUPPORTED_FILETYPES = {
  'CSV': 'text/csv',
  'TSV': 'text/tab-separated-values',
  'TAB': 'text/tab-separated-values',
  'DOC': 'application/msword',
  'ODS': 'application/x-vnd.oasis.opendocument.spreadsheet',
  'ODT': 'application/vnd.oasis.opendocument.text',
  'RTF': 'application/rtf',
  'SXW': 'application/vnd.sun.xml.writer',
  'TXT': 'text/plain',
  'XLS': 'application/vnd.ms-excel',
  'PDF': 'application/pdf',
  'PNG': 'image/png',
  'PPT': 'application/vnd.ms-powerpoint',
  'PPS': 'application/vnd.ms-powerpoint',
  'HTM': 'text/html',
  'HTML': 'text/html',
  'ZIP': 'application/zip',
  'SWF': 'application/x-shockwave-flash'
  }


class DocsService(gdata.service.GDataService):

  """Client extension for the Google Documents service Document List feed."""

  __FILE_EXT_PATTERN = re.compile('.*\.([a-zA-Z]{3,}$)')

  def __init__(self, email=None, password=None, source=None,
               server='docs.google.com', additional_headers=None, **kwargs):
    """Creates a client for the Google Documents service.

    Args:
      email: string (optional) The user's email address, used for
          authentication.
      password: string (optional) The user's password.
      source: string (optional) The name of the user's application.
      server: string (optional) The name of the server to which a connection
          will be opened. Default value: 'docs.google.com'.
      **kwargs: The other parameters to pass to gdata.service.GDataService
          constructor.
    """
    gdata.service.GDataService.__init__(
        self, email=email, password=password, service='writely', source=source,
        server=server, additional_headers=additional_headers, **kwargs)

  def _UploadFile(self, media_source, title, category, folder_or_uri=None):
    """Uploads a file to the Document List feed.

    Args:
      media_source: A gdata.MediaSource object containing the file to be
          uploaded.
      title: string The title of the document on the server after being
          uploaded.
      category: An atom.Category object specifying the appropriate document
          type.
      folder_or_uri: DocumentListEntry or string (optional) An object with a
          link to a folder or a uri to a folder to upload to.
          Note: A valid uri for a folder is of the form:
                /feeds/folders/private/full/folder%3Afolder_id

    Returns:
      A GDataEntry containing information about the document created on
      the Google Documents service.
    """
    if folder_or_uri:
      try:
        uri = folder_or_uri.content.src
      except AttributeError:
        uri = folder_or_uri
    else:
      uri = '/feeds/documents/private/full'

    entry = gdata.GDataEntry()
    entry.title = atom.Title(text=title)
    entry.category.append(category)
    entry = self.Post(entry, uri, media_source=media_source,
                      extra_headers={'Slug': media_source.file_name},
                      converter=gdata.docs.DocumentListEntryFromString)
    return entry

  def _DownloadFile(self, uri, file_path):
    """Downloads a file from the Document List.

    Args:
      uri: string The full Export URL to download the document from.
      file_path: string The full path to save the file to.  The export
          format is inferred from the the file extension.
    """
    media_source = self.GetMedia(uri)
    f = open(file_path, 'wb')
    f.write(media_source.file_handle.read())
    f.flush()
    f.close()

  def _MoveIntoFolder(self, source_entry, folder_entry, category):
    """Moves a document into a folder in the Document List Feed.

    Args:
      source_entry: DocumentListEntry An object representing the source 
          document/folder.
      folder_entry: DocumentListEntry An object with a link to the destination 
          folder.
      category: atom.Category An object specifying the appropriate document
          type.

    Returns:
      A GDataEntry containing information about the document created on
      the Google Documents service.
    """
    entry = gdata.GDataEntry()
    entry.id = source_entry.id
    entry.category.append(category)
    entry = self.Post(entry, folder_entry.content.src)
    return entry

  def Query(self, uri, converter=gdata.docs.DocumentListFeedFromString):
    """Queries the Document List feed and returns the resulting feed of
       entries.

    Args:
      uri: string The full URI to be queried. This can contain query
          parameters, a hostname, or simply the relative path to a Document
          List feed. The DocumentQuery object is useful when constructing
          query parameters.
      converter: func (optional) A function which will be executed on the
          retrieved item, generally to render it into a Python object.
          By default the DocumentListFeedFromString function is used to
          return a DocumentListFeed object. This is because most feed
          queries will result in a feed and not a single entry.
    """
    return self.Get(uri, converter=converter)

  def QueryDocumentListFeed(self, uri):
    """Retrieves a DocumentListFeed by retrieving a URI based off the Document
       List feed, including any query parameters. A DocumentQuery object can
       be used to construct these parameters.

    Args:
      uri: string The URI of the feed being retrieved possibly with query
          parameters.

    Returns:
      A DocumentListFeed object representing the feed returned by the server.
    """
    return self.Get(uri, converter=gdata.docs.DocumentListFeedFromString)

  def GetDocumentListEntry(self, uri):
    """Retrieves a particular DocumentListEntry by its unique URI.

    Args:
      uri: string The unique URI of an entry in a Document List feed.

    Returns:
      A DocumentListEntry object representing the retrieved entry.
    """
    return self.Get(uri, converter=gdata.docs.DocumentListEntryFromString)

  def GetDocumentListFeed(self, uri=None):
    """Retrieves a feed containing all of a user's documents.

    Args:
      uri: string A full URI to query the Document List feed.
    """
    if not uri:
      uri = gdata.docs.service.DocumentQuery().ToUri()
    return self.QueryDocumentListFeed(uri)

  def GetDocumentListAclEntry(self, uri):
    """Retrieves a particular DocumentListAclEntry by its unique URI.

    Args:
      uri: string The unique URI of an entry in a Document List feed.

    Returns:
      A DocumentListAclEntry object representing the retrieved entry.
    """
    return self.Get(uri, converter=gdata.docs.DocumentListAclEntryFromString)

  def GetDocumentListAclFeed(self, uri):
    """Retrieves a feed containing all of a user's documents.

    Args:
      uri: string The URI of a document's Acl feed to retrieve.

    Returns:
      A DocumentListAclFeed object representing the ACL feed
      returned by the server.
    """
    return self.Get(uri, converter=gdata.docs.DocumentListAclFeedFromString)

  def UploadPresentation(self, media_source, title, folder_or_uri=None):
    """Uploads a presentation inside of a MediaSource object to the Document
       List feed with the given title.

    Args:
      media_source: MediaSource The MediaSource object containing a
          presentation file to be uploaded.
      title: string The title of the presentation on the server after being
          uploaded.
      folder_or_uri: DocumentListEntry or string (optional) An object with a
          link to a folder or a uri to a folder to upload to.
          Note: A valid uri for a folder is of the form:
                /feeds/folders/private/full/folder%3Afolder_id

    Returns:
      A GDataEntry containing information about the presentation created on the
      Google Documents service.
    """
    category = atom.Category(scheme=DATA_KIND_SCHEME,
                             term=PRESENTATION_KIND_TERM)
    return self._UploadFile(media_source, title, category, folder_or_uri)

  def UploadSpreadsheet(self, media_source, title, folder_or_uri=None):
    """Uploads a spreadsheet inside of a MediaSource object to the Document
       List feed with the given title.

    Args:
      media_source: MediaSource The MediaSource object containing a spreadsheet
          file to be uploaded.
      title: string The title of the spreadsheet on the server after being
          uploaded.
      folder_or_uri: DocumentListEntry or string (optional) An object with a
          link to a folder or a uri to a folder to upload to.
          Note: A valid uri for a folder is of the form:
                /feeds/folders/private/full/folder%3Afolder_id

    Returns:
      A GDataEntry containing information about the spreadsheet created on the
      Google Documents service.
    """
    category = atom.Category(scheme=DATA_KIND_SCHEME,
                             term=SPREADSHEET_KIND_TERM)
    return self._UploadFile(media_source, title, category, folder_or_uri)

  def UploadDocument(self, media_source, title, folder_or_uri=None):
    """Uploads a document inside of a MediaSource object to the Document List
       feed with the given title.

    Args:
      media_source: MediaSource The gdata.MediaSource object containing a
          document file to be uploaded.
      title: string The title of the document on the server after being
          uploaded.
      folder_or_uri: DocumentListEntry or string (optional) An object with a
          link to a folder or a uri to a folder to upload to.
          Note: A valid uri for a folder is of the form:
                /feeds/folders/private/full/folder%3Afolder_id

    Returns:
      A GDataEntry containing information about the document created on the
      Google Documents service.
    """
    category = atom.Category(scheme=DATA_KIND_SCHEME,
                             term=DOCUMENT_KIND_TERM)
    return self._UploadFile(media_source, title, category, folder_or_uri)

  def DownloadDocument(self, entry_or_resource_id, file_path):
    """Downloads a document from the Document List.

    Args:
      entry_or_resource_id: DoclistEntry or string of the document
          resource id to download.
      file_path: string The full path to save the file to.  The export
          format is inferred from the the file extension.
    """
    ext = ''
    match = self.__FILE_EXT_PATTERN.match(file_path)
    if match:
      ext = match.group(1)

    if isinstance(entry_or_resource_id, gdata.docs.DocumentListEntry):
      resource_id = entry_or_resource_id.resourceId.text
    else:
      resource_id = entry_or_resource_id

    resource_id = resource_id.replace(':', '%3A')
    doc_id = resource_id[resource_id.find('%3A') + 3:]

    export_uri = '/feeds/download/documents/Export'
    export_uri += '?docID=%s&exportFormat=%s' % (doc_id, ext)
    self._DownloadFile(export_uri, file_path)

  def DownloadPresentation(self, entry_or_resource_id, file_path):
    """Downloads a presentation from the Document List.

    Args:
      entry_or_resource_id: DoclistEntry or string of the presentation
        resource id to download.
      file_path: string The full path to save the file to.  The export
          format is inferred from the the file extension.
    """
    ext = ''
    match = self.__FILE_EXT_PATTERN.match(file_path)
    if match:
      ext = match.group(1)

    if isinstance(entry_or_resource_id, gdata.docs.DocumentListEntry):
      resource_id = entry_or_resource_id.resourceId.text
    else:
      resource_id = entry_or_resource_id

    resource_id = resource_id.replace(':', '%3A')
    doc_id = resource_id[resource_id.find('%3A') + 3:]

    export_uri = '/feeds/download/presentations/Export'
    export_uri += '?docID=%s&exportFormat=%s' % (doc_id, ext)
    self._DownloadFile(export_uri, file_path)

  def DownloadSpreadsheet(self, entry_or_resource_id, file_path, gid=0):
    """Downloads a spreadsheet from the Document List.

    Args:
      entry_or_resource_id: DoclistEntry or string of the spreadsheet
        resource id to download.
      file_path: string The full path to save the file to.  The export
          format is inferred from the the file extension.
      gid: string or int (optional) The grid/sheet number to download.
          Used only for tsv and csv exports.
    """
    ext = ''
    match = self.__FILE_EXT_PATTERN.match(file_path)
    if match:
      ext = match.group(1)

    if isinstance(entry_or_resource_id, gdata.docs.DocumentListEntry):
      resource_id = entry_or_resource_id.resourceId.text
    else:
      resource_id = entry_or_resource_id

    resource_id = resource_id.replace(':', '%3A')
    key = resource_id[resource_id.find('%3A') + 3:]

    export_uri = ('http://spreadsheets.google.com'
                  '/feeds/download/spreadsheets/Export')
    export_uri += '?key=%s&fmcmd=%s' % (key,
                                        DOWNLOAD_SPREADSHEET_FORMATS[ext])
    if ext == 'csv' or ext == 'tsv':
      export_uri += '&gid=' + str(gid)
    self._DownloadFile(export_uri, file_path)

  def CreateFolder(self, title, folder_or_uri=None):
    """Creates a folder in the Document List feed.

    Args:
      title: string The title of the folder on the server after being created.
      folder_or_uri: DocumentListEntry or string (optional) An object with a
          link to a folder or a uri to a folder to upload to.
          Note: A valid uri for a folder is of the form:
                /feeds/folders/private/full/folder%3Afolder_id

    Returns:
      A GDataEntry containing information about the folder created on
      the Google Documents service.
    """
    if folder_or_uri:
      try:
        uri = folder_or_uri.content.src
      except AttributeError:
        uri = folder_or_uri
    else:
      uri = '/feeds/documents/private/full'

    category = atom.Category(scheme=DATA_KIND_SCHEME, term=FOLDER_KIND_TERM)
    folder_entry = gdata.GDataEntry()
    folder_entry.title = atom.Title(text=title)
    folder_entry.category.append(category)
    folder_entry = self.Post(folder_entry, uri)

    return folder_entry

  def MoveDocumentIntoFolder(self, document_entry, folder_entry):
    """Moves a document into a folder in the Document List Feed.

    Args:
      document_entry: DocumentListEntry An object representing the source
          document.
      folder_entry: DocumentListEntry An object representing the destination
          folder.

    Returns:
      A GDataEntry containing information about the document created on
      the Google Documents service.
    """
    category = atom.Category(scheme=DATA_KIND_SCHEME,
                             term=DOCUMENT_KIND_TERM)
    return self._MoveIntoFolder(document_entry, folder_entry, category)

  def MovePresentationIntoFolder(self, document_entry, folder_entry):
    """Moves a presentation into a folder in the Document List Feed.

    Args:
      document_entry: DocumentListEntry An object representing the source
          document.
      folder_entry: DocumentListEntry An object representing the destination
          folder.

    Returns:
      A GDataEntry containing information about the document created on
      the Google Documents service.
    """
    category = atom.Category(scheme=DATA_KIND_SCHEME,
                             term=PRESENTATION_KIND_TERM)
    return self._MoveIntoFolder(document_entry, folder_entry, category)

  def MoveSpreadsheetIntoFolder(self, document_entry, folder_entry):
    """Moves a spreadsheet into a folder in the Document List Feed.

    Args:
      document_entry: DocumentListEntry An object representing the source
          document.
      folder_entry: DocumentListEntry An object representing the destination
          folder.

    Returns:
      A GDataEntry containing information about the document created on
      the Google Documents service.
    """
    category = atom.Category(scheme=DATA_KIND_SCHEME,
                             term=SPREADSHEET_KIND_TERM)
    return self._MoveIntoFolder(document_entry, folder_entry, category)

  def MoveFolderIntoFolder(self, src_folder_entry, dest_folder_entry):
    """Moves a folder into another folder.

    Args:
      src_folder_entry: DocumentListEntry An object with a link to the
          source folder.
      dest_folder_entry: DocumentListEntry An object with a link to the
          destination folder.

    Returns:
      A GDataEntry containing information about the folder created on
      the Google Documents service.
    """
    category = atom.Category(scheme=DATA_KIND_SCHEME,
                             term=FOLDER_KIND_TERM)
    return self._MoveIntoFolder(src_folder_entry, dest_folder_entry, category)

  def MoveOutOfFolder(self, source_entry):
    """Moves a document into a folder in the Document List Feed.

    Args:
      source_entry: DocumentListEntry An object representing the source
          document/folder.

    Returns:
      True if the entry was moved out.
    """
    return self.Delete(source_entry.GetEditLink().href)


class DocumentQuery(gdata.service.Query):

  """Object used to construct a URI to query the Google Document List feed"""

  def __init__(self, feed='/feeds/documents', visibility='private',
      projection='full', text_query=None, params=None,
      categories=None):
    """Constructor for Document List Query

    Args:
      feed: string (optional) The path for the feed. (e.g. '/feeds/documents')
      visibility: string (optional) The visibility chosen for the current feed.
      projection: string (optional) The projection chosen for the current feed.
      text_query: string (optional) The contents of the q query parameter. This
                  string is URL escaped upon conversion to a URI.
      params: dict (optional) Parameter value string pairs which become URL
          params when translated to a URI. These parameters are added to
          the query's items.
      categories: list (optional) List of category strings which should be
          included as query categories. See gdata.service.Query for
          additional documentation.

    Yields:
      A DocumentQuery object used to construct a URI based on the Document
      List feed.
    """
    self.visibility = visibility
    self.projection = projection
    gdata.service.Query.__init__(self, feed, text_query, params, categories)

  def ToUri(self):
    """Generates a URI from the query parameters set in the object.

    Returns:
      A string containing the URI used to retrieve entries from the Document
      List feed.
    """
    old_feed = self.feed
    self.feed = '/'.join([old_feed, self.visibility, self.projection])
    new_feed = gdata.service.Query.ToUri(self)
    self.feed = old_feed
    return new_feed

  def AddNamedFolder(self, email, folder_name):
    """Adds a named folder category, qualified by a schema.

    This function lets you query for documents that are contained inside a
    named folder without fear of collision with other categories.

    Args:
      email: string The email of the user who owns the folder.
      folder_name: string The name of the folder.

      Returns:
        The string of the category that was added to the object.
    """

    category = '{%s%s}%s' % (FOLDERS_SCHEME_PREFIX, email, folder_name)
    self.categories.append(category)
    return category

  def RemoveNamedFolder(self, email, folder_name):
    """Removes a named folder category, qualified by a schema.

    Args:
      email: string The email of the user who owns the folder.
      folder_name: string The name of the folder.

      Returns:
        The string of the category that was removed to the object.
    """
    category = '{%s%s}%s' % (FOLDERS_SCHEME_PREFIX, email, folder_name)
    self.categories.remove(category)
    return category


class DocumentAclQuery(gdata.service.Query):

  """Object used to construct a URI to query a Document's ACL feed"""

  def __init__(self, resource_id, feed='/feeds/acl/private/full'):
    """Constructor for Document ACL Query

    Args:
      resource_id: string The resource id. (e.g. 'document%3Adocument_id',
          'spreadsheet%3Aspreadsheet_id', etc.)
      feed: string (optional) The path for the feed.
          (e.g. '/feeds/acl/private/full')

    Yields:
      A DocumentAclQuery object used to construct a URI based on the Document
      ACL feed.
    """
    self.resource_id = resource_id
    gdata.service.Query.__init__(self, feed)

  def ToUri(self):
    """Generates a URI from the query parameters set in the object.

    Returns:
      A string containing the URI used to retrieve entries from the Document
      ACL feed.
    """
    return '%s/%s' % (gdata.service.Query.ToUri(self), self.resource_id)
