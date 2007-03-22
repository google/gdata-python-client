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

"""GCalendarService extends the GDataService to streamline Google Calendar operations.

  GCalendarService: Provides methods to query feeds and manipulate items. Extends 
                GDataService.

  DictionaryToParamList: Function which converts a dictionary into a list of 
                         URL arguments (represented as strings). This is a 
                         utility function used in CRUD operations.
"""

__author__ = 'api.vli (Vivian Li)'

from elementtree import ElementTree
import urllib
import gdata
import app_service
import gdata_service
import gcalendar
import atom


class Error(Exception):
  pass


class RequestError(Error):
  pass


class GCalendarService(gdata_service.GDataService):
  """Client for the Google Calendar service."""

  def __init__(self, email=None, password=None, source=None, 
               server='www.google.com', 
               additional_headers=None):
    gdata_service.GDataService.__init__(self, email=email, password=password,
                                        service='cl', source=source, 
                                        server=server, 
                                        additional_headers=additional_headers)

  
  def Query(self, uri):
    """Performs a query and returns a resulting feed or entry.

    Args:
      feed: string The feed which is to be queried

    Returns:
      On success, a tuple in the form
      (boolean succeeded=True, ElementTree._Element result)
      On failure, a tuple in the form
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """

    result = self.Get(uri)
    return result

  def CalendarQuery(self, query):
    result = self.Query(query.ToUri())
    if isinstance(query, ListCalendarsQuery):
      return gcalendar.CalendarFeedFromString(result.ToString())
    elif isinstance(query, EventCalendarQuery):
      return gcalendar.CalendarEventFeedFromString(result.ToString())
    else:
      print "else result"
      return result
    
  def InsertItem(self, new_item, insert_uri, url_params=None, escape_params=True):
    """Adds an item to Google Calendar.

    Args: 
      new_item: ElementTree._Element A new item which is to be added to 
                Google Calendar.
      insert_uri: the URL to post new items to for the feed
      url_params: dict (optional) Additional URL parameters to be included
                  in the insertion request. 
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      On successful insert, a tuple in the form
      (boolean succeeded=True, ElementTree._Element new item from Google Calendar)
      On failure, a tuple in the form
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """

    response = self.Post(insert_uri, new_item, url_params=url_params,
                         escape_params=escape_params)

    if isinstance(response, atom.Entry):
      return gcalendar.GCalendarItemFromString(response.ToString())

  def DeleteItem(self, item_id, url_params=None, escape_params=True):
    """Removes an item with the specified ID from Google Calendar.

    Args:
      item_id: string The ID of the item to be deleted. Example:
               'http://www.google.com/calendar/feeds/default/private/full/abxhjfgkdhe
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

  def UpdateItem(self, edit_uri, updated_item, url_params=None, 
                 escape_params=True):
    """Updates an existing item.

    Args:
      edit_uri: string The edit link URI for the element being updated
      updated_item: string, ElementTree._Element, or ElementWrapper containing
                    the Atom Entry which will replace the base item which is 
                    stored at the item_id.
      url_params: dict (optional) Additional URL parameters to be included
                  in the update request.
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      On successful update, a tuple in the form
      (boolean succeeded=True, ElementTree._Element new item from Google Calendar)
      On failure, a tuple in the form
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """
    response = self.Put('/%s' % (edit_uri.lstrip('http://www.google.com/')),
                        updated_item, url_params=url_params, 
                        escape_params=escape_params)
    if isinstance(response, atom.Entry):
      return gcalendar.GCalendarItemFromString(response.ToString())


class CalendarQuery(gdata_service.Query):

  def __init__(self, feed=None, text_query=None, params=None,
               categories=None):
    gdata_service.Query.__init__(self, feed, text_query, params,
                                 categories)
    
  def _GetStartMin(self):
    return self['start-min']

  def _SetStartMin(self, val):
    self['start-min'] = val

  start_min = property(_GetStartMin, _SetStartMin, 
      doc="""The start-min query parameter""")

  def _GetStartMax(self):
    return self['start-max']

  def _SetStartMax(self, val):
    self['start-max'] = val

  start_max = property(_GetStartMax, _SetStartMax, 
      doc="""The start-max query parameter""")

  def _GetOrderBy(self):
    return self['orderby']

  def _SetOrderBy(self, val):
    if val is not 'lastmodified' or val is not 'starttime':
      raise Error, "Order By must be either 'lastmodified' or 'startttime'"
    self['orderby'] = val

  orderby = property(_GetOrderBy, _SetOrderBy, 
      doc="""The orderby query parameter""")

  def _GetSortOrder(self):
    return self['sortorder']

  def _SetSortOrder(self, val):
    if val is not 'ascending' or val is not 'descending' or val is not 'a' or val is not 'd' or val is not 'ascend' or val is not 'descend':
      raise Error, "Sort order must be either ascending, ascend, a or descending, descend, d"
    self['sortorder'] = val

  sortorder = property(_GetSortOrder, _SetSortOrder, 
      doc="""The sortorder query parameter""")

  def _GetSingleEvents(self):
    return self['singleevents']

  def _SetSingleEvents(self, val):
    self['singleevents'] = val

  singleevents = property(_GetSingleEvents, _SetSingleEvents, 
      doc="""The singleevents query parameter""")

  def _GetFutureEvents(self):
    return self['futureevents']

  def _SetFutureEvents(self, val):
    self['futureevents'] = val

  futureevents = property(_GetFutureEvents, _SetFutureEvents, 
      doc="""The futureevents query parameter""")

  def _GetRecurrenceExpansionStart(self):
    return self['recurrence-expansion-start']

  def _SetRecurrenceExpansionStart(self, val):
    self['recurrence-expansion-start'] = val

  recurrence_expansion_start = property(_GetRecurrenceExpansionStart, _SetRecurrenceExpansionStart, 
      doc="""The recurrence-expansion-start query parameter""")

  def _GetRecurrenceExpansionEnd(self):
    return self['recurrence-expansion-end']

  def _SetRecurrenceExpansionEnd(self, val):
    self['recurrence-expansion-end'] = val

  recurrence_expansion_end = property(_GetRecurrenceExpansionEnd, _SetRecurrenceExpansionEnd, 
      doc="""The recurrence-expansion-end query parameter""")


class ListCalendarsQuery(CalendarQuery):
  def __init__(self, userId=None, text_query=None,
               params=None, categories=None):
    if userId is None:
      userId = 'default'

    CalendarQuery.__init__(self, feed='http://www.google.com/calendar/feeds/'+userId,
                           text_query=text_query, params=params, categories=categories)

class EventCalendarQuery(CalendarQuery):
  def __init__(self, userId=None, text_query=None,
               params=None, categories=None):
    if userId is None:
      userId = 'default'
    CalendarQuery.__init__(self, feed='http://www.google.com/calendar/feeds/'+userId+'/private/full',
                           text_query=text_query, params=params, categories=categories)
