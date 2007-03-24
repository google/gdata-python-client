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

"""GBaseService extends the GDataService to streamline Google Base operations.

  GBaseService: Provides methods to query feeds and manipulate items. Extends 
                GDataService.

  DictionaryToParamList: Function which converts a dictionary into a list of 
                         URL arguments (represented as strings). This is a 
                         utility function used in CRUD operations.
"""

__author__ = 'api.jscudder (Jeffrey Scudder)'

from elementtree import ElementTree
import urllib
import gdata
import app_service
import gdata_service
import gbase
import atom


class Error(Exception):
  pass


class RequestError(Error):
  pass


class GBaseService(gdata_service.GDataService):
  """Client for the Google Base service."""

  def __init__(self, email=None, password=None, source=None, 
               server='base.google.com', api_key=None, 
               additional_headers=None):
    gdata_service.GDataService.__init__(self, email=email, password=password,
                                        service='gbase', source=source, 
                                        server=server, 
                                        additional_headers=additional_headers)
    self.api_key = api_key
  
  def _SetAPIKey(self, api_key):
    if not isinstance(self.additional_headers, dict):
      self.additional_headers = {}
    self.additional_headers['X-Google-Key'] = api_key

  def __SetAPIKey(self, api_key):
    self._SetAPIKey(api_key)

  def _GetAPIKey(self):
    if 'X-Google-Key' not in self.additional_headers:
      return None
    else:
      return self.additional_headers['X-Google-Key']

  def __GetAPIKey(self):
    return self._GetAPIKey()

  api_key = property(__GetAPIKey, __SetAPIKey,
      doc="""Get or set the API key to be included in all requests.""")
    
  def Query(self, uri):
    """Performs a style query and returns a resulting feed or entry.

    Args:
      feed: string The feed which is to be queried. Examples: 'items', 
                   'snippets', 'attributes', etc.
      bq_string: string The query string as described at 
                 http://code.google.com/apis/base/query-lang-spec.html .
      url_params: dict (optional) Additional URL parameters to be included
                  in the query. These are translated into query arguments 
                  in the form '&dict_key=value&...'. 
                  Example: {'max-results': '250'} becomes &max-results=250
      escape_params: boolean (optional) If false, the calling code has already
                     ensured that the query will form a valid URL (all 
                     reserved characters have been escaped). If true, this 
                     method will escape the query and any URL parameters 
                     provided.

    Returns:
      On success, a tuple in the form
      (boolean succeeded=True, ElementTree._Element result)
      On failure, a tuple in the form
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """
    
    result = self.Get(uri)
    if isinstance(result, atom.Entry):
      return gbase.GBaseItemFromString(result.ToString())
    return result

  def QuerySnippetsFeed(self, uri):
    return gbase.GBaseSnippetFeedFromString(str(self.Get(uri)))

  def QueryItemsFeed(self, uri):
    return gbase.GBaseItemFeedFromString(str(self.Get(uri)))

  def QueryAttributesFeed(self, uri):
    return gbase.GBaseAttributesFeedFromString(str(self.Get(uri)))

  def QueryItemTypesFeed(self, uri):
    return gbase.GBaseItemTypesFeedFromString(str(self.Get(uri)))

  def QueryLocalesFeed(self, uri):
    return gbase.GBaseLocalesFeedFromString(str(self.Get(uri)))

  def GetItem(self, uri):
    return gbase.GBaseItemFromString(str(self.Get(uri)))

  def GetSnippet(self, uri):
    return gbase.GBaseSnippetFromString(str(self.Get(uri)))

  def GetAttribute(self, uri):
    return gbase.GBaseAttributeEntryFromString(str(self.Get(uri)))

  def GetItemType(self, uri):
    return gbase.GBaseItemTypeEntryFromString(str(self.Get(uri)))

  def GetLocale(self, uri):
    return gdata.GDataEntryFromString(str(self.Get(uri)))

  def InsertItem(self, new_item, url_params=None, escape_params=True):
    """Adds an item to Google Base.

    Args: 
      new_item: ElementTree._Element A new item which is to be added to 
                Google Base.
      url_params: dict (optional) Additional URL parameters to be included
                  in the insertion request. 
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      On successful insert, a tuple in the form
      (boolean succeeded=True, ElementTree._Element new item from Google Base)
      On failure, a tuple in the form
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """

    response = self.Post(new_item, '/base/feeds/items', url_params=url_params,
                         escape_params=escape_params)

    if isinstance(response, atom.Entry):
      return gbase.GBaseItemFromString(response.ToString())

  def DeleteItem(self, item_id, url_params=None, escape_params=True):
    """Removes an item with the specified ID from Google Base.

    Args:
      item_id: string The ID of the item to be deleted. Example:
               'http://www.google.com/base/feeds/items/13185446517496042648'
      url_params: dict (optional) Additional URL parameters to be included
                  in the deletion request.
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      On successful deletion, a tuple in the form
      (boolean succeeded=True,)
      On failure, a tuple in the form
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """
    
    return self.Delete('/%s' % (item_id.lstrip('http://www.google.com/')),
                       url_params=url_params, escape_params=escape_params)
                           
  def UpdateItem(self, item_id, updated_item, url_params=None, 
                 escape_params=True):
    """Updates an existing item.

    Args:
      item_id: string The ID of the item to be updated.  Example:
               'http://www.google.com/base/feeds/items/13185446517496042648'
      updated_item: string, ElementTree._Element, or ElementWrapper containing
                    the Atom Entry which will replace the base item which is 
                    stored at the item_id.
      url_params: dict (optional) Additional URL parameters to be included
                  in the update request.
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      On successful update, a tuple in the form
      (boolean succeeded=True, ElementTree._Element new item from Google Base)
      On failure, a tuple in the form
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """
    
    response = self.Put(updated_item, 
        '/%s' % (item_id.lstrip('http://www.google.com/')), 
        url_params=url_params, escape_params=escape_params)
    if isinstance(response, atom.Entry):
      return gbase.GBaseItemFromString(response.ToString())
    

class BaseQuery(gdata_service.Query):

  def _GetBaseQuery(self):
    return self['bq']

  def _SetBaseQuery(self, base_query):
    self['bq'] = base_query

  bq = property(_GetBaseQuery, _SetBaseQuery, 
      doc="""The bq query parameter""")
