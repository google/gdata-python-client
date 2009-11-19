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

"""DocsClient extends gdata.client.GDClient to streamline DocList API calls."""


__author__ = 'e.bidelman (Eric Bidelman)'

import mimetypes
import urllib
import atom.data
import atom.url
import gdata.client
import gdata.docs.data


# Feed URI templates
DOCLIST_FEED_URI = '/feeds/default/private/full/'
FOLDERS_FEED_TEMPLATE = DOCLIST_FEED_URI + '%s/contents'
ACL_FEED_TEMPLATE = DOCLIST_FEED_URI + '%s/acl'
REVISIONS_FEED_TEMPLATE = DOCLIST_FEED_URI + '%s/revisions'


class DocsClient(gdata.client.GDClient):
  """Client extension for the Google Documents List API."""

  host = 'docs.google.com'  # default server for the API
  api_version = '3.0'  # default major version for the service.
  auth_service = 'writely'
  auth_scopes = ['http://docs.google.com/feeds/',
                 'https://docs.google.com/feeds/']

  def __init__(self, auth_token=None, **kwargs):
    """Constructs a new client for the DocList API.

    Args:
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: The other parameters to pass to gdata.client.GDClient constructor.
    """
    gdata.client.GDClient.__init__(self, auth_token=auth_token, **kwargs)

  def get_file_content(self, uri, auth_token=None, **kwargs):
    """Fetches the file content from the specified uri.

    This method is useful for downloading/exporting a file within enviornments
    like Google App Engine, where the user does not have the ability to write
    the file to a local disk.

    Args:
      uri: str The full URL to fetch the file contents from.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.request().

    Returns:
      The binary file content.

    Raises:
      gdata.client.RequestError: on error response from server.
    """
    server_response = self.request('GET', uri, auth_token=auth_token, **kwargs)
    if server_response.status != 200:
      raise  gdata.client.RequestError, {'status': server_response.status,
                                         'reason': server_response.reason,
                                         'body': server_response.read()}
    return server_response.read()

  GetFileContent = get_file_content

  def _download_file(self, uri, file_path, auth_token=None, **kwargs):
    """Downloads a file to disk from the specified URI.

    Note: to download a file in memory, use the GetFileContent() method.

    Args:
      uri: str The full URL to download the file from.
      file_path: str The full path to save the file to.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.get_file_content().

    Raises:
      gdata.client.RequestError: on error response from server.
    """
    f = open(file_path, 'wb')
    try:
      f.write(self.get_file_content(uri, auth_token=auth_token, **kwargs))
    except gdata.client.RequestError, e:
      f.close()
      raise e
    f.flush()
    f.close()

  _DownloadFile = _download_file

  def get_doclist(self, uri=None, limit=None, auth_token=None, **kwargs):
    """Retrieves the main doclist feed containing the user's items.

    Args:
      uri: str (optional) A URI to query the doclist feed.
      limit: int (optional) A maximum cap for the number of results to
          return in the feed. By default, the API returns a maximum of 100
          per page. Thus, if you set limit=5000, you will get <= 5000
          documents (guarenteed no more than 5000), and will need to follow the
          feed's next links (feed.GetNextLink()) to the rest. See
          get_everything(). Similarly, if you set limit=50, only <= 50
          documents are returned. Note: if the max-results parameter is set in
          the uri parameter, it is chosen over a value set for limit.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.get_feed().

    Returns:
      gdata.docs.data.DocList feed.
    """
    if uri is None:
      uri = DOCLIST_FEED_URI

    url = atom.url.parse_url(uri)

    # Add max-results param if it wasn't included in the uri.
    if limit is not None and not 'max-results' in url.params:
      url.params['max-results'] = limit

    return self.get_feed(str(url), desired_class=gdata.docs.data.DocList,
                         auth_token=auth_token, **kwargs)

  GetDocList = get_doclist

  def get_doc(self, resource_id, etag=None, auth_token=None, **kwargs):
    """Retrieves a particular document given by its resource id.

    Args:
      resource_id: str The document/item's resource id. Example spreadsheet:
          'spreadsheet%3A0A1234567890'.
      etag: str (optional) The document/item's etag value to be used in a
          conditional GET. See http://code.google.com/apis/documents/docs/3.0/
          developers_guide_protocol.html#RetrievingCached.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.get_entry().

    Returns:
      A gdata.docs.data.DocsEntry object representing the retrieved entry.

    Raises:
      ValueError if the resource_id is not a valid format.
    """
    match = gdata.docs.data.RESOURCE_ID_PATTERN.match(resource_id)
    if match is None:
      raise ValueError, 'Invalid resource id: %s' % resource_id
    return self.get_entry(
        DOCLIST_FEED_URI + resource_id, etag=etag,
        desired_class=gdata.docs.data.DocsEntry,
        auth_token=auth_token, **kwargs)

  GetDoc = get_doc

  def get_everything(self, uri=None, auth_token=None, **kwargs):
    """Retrieves the user's entire doc list.

    The method makes multiple HTTP requests (by following the feed's next links)
    in order to fetch the user's entire document list.

    Args:
      uri: str (optional) A URI to query the doclist feed with.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.GetDocList().

    Returns:
      A list of gdata.docs.data.DocsEntry objects representing the retrieved
      entries.
    """
    if uri is None:
      uri = DOCLIST_FEED_URI

    feed = self.GetDocList(uri=uri, auth_token=auth_token, **kwargs)
    entries = feed.entry

    while feed.GetNextLink() is not None:
      feed = self.GetDocList(
          feed.GetNextLink().href, auth_token=auth_token, **kwargs)
      entries.extend(feed.entry)

    return entries

  GetEverything = get_everything

  def get_acl_permissions(self, resource_id, auth_token=None, **kwargs):
    """Retrieves a the ACL sharing permissions for a document.

    Args:
      resource_id: str The document/item's resource id. Example for pdf:
          'pdf%3A0A1234567890'.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.get_feed().

    Returns:
      A gdata.docs.data.AclFeed object representing the document's ACL entries.

    Raises:
      ValueError if the resource_id is not a valid format.
    """
    match = gdata.docs.data.RESOURCE_ID_PATTERN.match(resource_id)
    if match is None:
      raise ValueError, 'Invalid resource id: %s' % resource_id

    return self.get_feed(
        ACL_FEED_TEMPLATE % resource_id, desired_class=gdata.docs.data.AclFeed,
        auth_token=auth_token, **kwargs)

  GetAclPermissions = get_acl_permissions

  def get_revisions(self, resource_id, auth_token=None, **kwargs):
    """Retrieves the revision history for a document.

    Args:
      resource_id: str The document/item's resource id. Example for pdf:
          'pdf%3A0A1234567890'.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.get_feed().

    Returns:
      A gdata.docs.data.RevisionFeed representing the document's revisions.

    Raises:
      ValueError if the resource_id is not a valid format.
    """
    match = gdata.docs.data.RESOURCE_ID_PATTERN.match(resource_id)
    if match is None:
      raise ValueError, 'Invalid resource id: %s' % resource_id

    return self.get_feed(
        REVISIONS_FEED_TEMPLATE % resource_id,
        desired_class=gdata.docs.data.RevisionFeed, auth_token=auth_token,
        **kwargs)

  GetRevisions = get_revisions

  def create(self, doc_type, title, folder_or_id=None, writers_can_invite=None,
             auth_token=None, **kwargs):
    """Creates a new item in the user's doclist.

    Args:
      doc_type: str The type of object to create. For example: 'document',
          'spreadsheet', 'folder', 'presentation'.
      title: str A title for the document.
      folder_or_id: DocsEntry or str (optional) Folder entry or the resouce id
          of a folder to create the object under. Note: A valid resouce id for a
          folder is of the form: folder%3Afolder_id.
      writers_can_invite: bool (optional) False prevents collaborators from
          being able to invite others to edit or view the document.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.post().

    Returns:
      gdata.docs.data.DocsEntry containing information newly created item.
    """
    entry = gdata.docs.data.DocsEntry(title=atom.data.Title(text=title))
    entry.category.append(gdata.docs.data.make_kind_category(doc_type))

    if isinstance(writers_can_invite, gdata.docs.data.WritersCanInvite):
      entry.writers_can_invite = writers_can_invite
    elif isinstance(writers_can_invite, bool):
      entry.writers_can_invite = gdata.docs.data.WritersCanInvite(
          value=str(writers_can_invite).lower())

    uri = DOCLIST_FEED_URI

    if folder_or_id is not None:
      if isinstance(folder_or_id, gdata.docs.data.DocsEntry):
        # Verify that we're uploading the resource into to a folder.
        if folder_or_id.get_document_type() == gdata.docs.data.FOLDER_LABEL:
          uri = folder_or_id.content.src
        else:
          raise gdata.client.Error, 'Trying to upload item to a non-folder.'
      else:
        uri = FOLDERS_FEED_TEMPLATE % folder_or_id

    return self.post(entry, uri, auth_token=auth_token, **kwargs)

  Create = create

  def move(self, source_entry, folder_entry=None,
           keep_in_folders=False, auth_token=None, **kwargs):
    """Moves an item into a different folder (or to the root document list).

    Args:
      source_entry: gdata.docs.data.DocsEntry An object representing the source
          document/folder.
      folder_entry: gdata.docs.data.DocsEntry (optional) An object representing
          the destination folder. If None, set keep_in_folders to
          True to remove the item from all parent folders.
      keep_in_folders: boolean (optional) If True, the source entry
          is not removed from any existing parent folders it is in.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.post().

    Returns:
      A gdata.docs.data.DocsEntry of the moved entry or True if just moving the
      item out of all folders (e.g. Move(source_entry)).
    """
    entry = gdata.docs.data.DocsEntry(id=source_entry.id)

    # Remove the item from any folders it is already in.
    if not keep_in_folders:
      for folder in source_entry.InFolders():
        self.delete(
            '%s/contents/%s' % (folder.href, source_entry.resource_id.text),
            force=True)

    # If we're moving the resource into a folder, verify it is a folder entry.
    if folder_entry is not None:
      if folder_entry.get_document_type() == gdata.docs.data.FOLDER_LABEL:
        return self.post(entry, folder_entry.content.src,
                         auth_token=auth_token, **kwargs)
      else:
        raise gdata.client.Error, 'Trying to move item into a non-folder.'

    return True

  Move = move

  def upload(self, media, title, folder_or_uri=None, content_type=None,
             auth_token=None, **kwargs):
    """Uploads a file to Google Docs.

    Args:
      media: A gdata.data.MediaSource object containing the file to be
          uploaded or a string of the filepath.
      title: str The title of the document on the server after being
          uploaded.
      folder_or_uri: gdata.docs.data.DocList or str (optional) An object with
          a link to the folder or the uri to upload the file to.
          Note: A valid uri for a folder is of the form:
                /feeds/default/private/full/folder%3Afolder_id/contents
      content_type: str (optional) The file's mimetype. If not provided, the
          one in the media source object is used or the mimetype is inferred
          from the filename (if media is a string). When media is a filename,
          it is always recommended to pass in a content type.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.post().

    Returns:
      A gdata.docs.data.DocsEntry containing information about uploaded doc.
    """
    if folder_or_uri is not None:
      if isinstance(folder_or_uri, gdata.docs.data.DocsEntry):
        # Verify that we're uploading the resource into to a folder.
        if folder_or_uri.get_document_type() == gdata.docs.data.FOLDER_LABEL:
          uri = folder_or_uri.content.src
        else:
          raise gdata.client.Error, 'Trying to upload item to a non-folder.'
      else:
        uri = folder_or_uri
    else:
      uri = DOCLIST_FEED_URI

    # Create media source if media is a filepath.
    if isinstance(media, (str, unicode)):
      mimetype = mimetypes.guess_type(media)[0]
      if mimetype is None and content_type is None:
        raise ValueError, ("Unknown mimetype. Please pass in the file's "
                           "content_type")
      else:
        media = gdata.data.MediaSource(file_path=media,
                                       content_type=content_type)

    entry = gdata.docs.data.DocsEntry(title=atom.data.Title(text=title))

    return self.post(entry, uri, media_source=media,
                     desired_class=gdata.docs.data.DocsEntry,
                     auth_token=auth_token, **kwargs)

  Upload = upload

  def download(self, entry_or_id_or_url, file_path, extra_params=None,
               auth_token=None, **kwargs):
    """Downloads a file from the Document List to local disk.

    Note: to download a file in memory, use the GetFileContent() method.

    Args:
      entry_or_id_or_url: gdata.docs.data.DocsEntry or string representing a
          resource id or URL to download the document from (such as the content
          src link).
      file_path: str The full path to save the file to.
      extra_params: dict (optional) A map of any further parameters to control
          how the document is downloaded/exported. For example, exporting a
          spreadsheet as a .csv: extra_params={'gid': 0, 'exportFormat': 'csv'}
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self._download_file().

    Raises:
      gdata.client.RequestError if the download URL is malformed or the server's
      response was not successful.
      ValueError if entry_or_id_or_url was a resource id for a filetype
      in which the download link cannot be manually constructed (e.g. pdf).
    """
    if isinstance(entry_or_id_or_url, gdata.docs.data.DocsEntry):
      url = entry_or_id_or_url.content.src
    else:
      if gdata.docs.data.RESOURCE_ID_PATTERN.match(entry_or_id_or_url):
        url = gdata.docs.data.make_content_link_from_resource_id(
            entry_or_id_or_url)
      else:
        url = entry_or_id_or_url

    if extra_params is not None:
      if 'exportFormat' in extra_params and url.find('/Export?') == -1:
        raise gdata.client.Error, ('This entry type cannot be exported '
                                   'as a different format.')

      if 'gid' in extra_params and url.find('spreadsheets') == -1:
        raise gdata.client.Error, 'gid param is not valid for this doc type.'

      url += '&' + urllib.urlencode(extra_params)

    self._download_file(url, file_path, auth_token=auth_token, **kwargs)

  Download = download

  def export(self, entry_or_id_or_url, file_path, gid=None, auth_token=None,
             **kwargs):
    """Exports a document from the Document List in a different format.

    Args:
      entry_or_id_or_url: gdata.docs.data.DocsEntry or string representing a
          resource id or URL to download the document from (such as the content
          src link).
      file_path: str The full path to save the file to.  The export
          format is inferred from the the file extension.
      gid: str (optional) grid id for downloading a single grid of a
          spreadsheet. The param should only be used for .csv and .tsv
          spreadsheet exports.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the user's data.
      kwargs: Other parameters to pass to self.download().

    Raises:
      gdata.client.RequestError if the download URL is malformed or the server's
      response was not successful.
    """
    extra_params = {}

    match = gdata.docs.data.FILE_EXT_PATTERN.match(file_path)
    if match:
      extra_params['exportFormat'] = match.group(1)

    if gid is not None:
      extra_params['gid'] = gid

    self.download(entry_or_id_or_url, file_path, extra_params,
                  auth_token=auth_token, **kwargs)

  Export = export
