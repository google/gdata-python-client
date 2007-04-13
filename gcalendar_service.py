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

"""CalendarService extends the GDataService to streamline Google Calendar operations.

  CalendarService: Provides methods to query feeds and manipulate items. Extends 
                GDataService.

  DictionaryToParamList: Function which converts a dictionary into a list of 
                         URL arguments (represented as strings). This is a 
                         utility function used in CRUD operations.
"""

__author__ = 'api.vli (Vivian Li)'

try:
  from xml.etree import ElementTree
except ImportError:
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


class CalendarService(gdata_service.GDataService):
  """Client for the Google Calendar service."""

  def __init__(self, email=None, password=None, source=None, 
               server='www.google.com', 
               additional_headers=None):
    gdata_service.GDataService.__init__(self, email=email, password=password,
                                        service='cl', source=source, 
                                        server=server, 
                                        additional_headers=additional_headers)

  def GetCalendarEventFeed(self, uri='/calendar/feeds/default/private/full'):
    return gcalendar.CalendarEventFeedFromString(str(self.Get(uri)))

  def GetCalendarEventEntry(self, uri):
    return gcalendar.CalendarEventEntryFromString(str(self.Get(uri)))

  def GetCalendarListFeed(self, uri='/calendar/feeds/default/'):
    return gcalendar.CalendarListFeedFromString(str(self.Get(uri)))

  def GetCalendarListEntry(self, uri):
    return gcalendar.CalendarListEntryFromString(str(self.Get(uri)))

  def GetCalendarEventCommentFeed(self, uri):
    return gcalendar.CalendarEventCommentFeedFromString(str(self.Get(uri)))

  def GetCalendarEventCommentEntry(self, uri):
    return gcalendar.CalendarEventCommentEntryFromString(str(self.Get(uri)))
 
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
    if isinstance(query, CalendarEventQuery):
      return gcalendar.CalendarEventFeedFromString(result.ToString())
    elif isinstance(query, CalendarListQuery):
      return gcalendar.CalendarListFeedFromString(result.ToString())
    elif isinstance(query, CalendarEventCommentQuery):
      return gcalendar.CalendarEventCommentFeedFromString(result.ToString())
    else:
      print "else result"
      return result
    
  def InsertEvent(self, new_event, insert_uri, url_params=None, 
                  escape_params=True):
    """Adds an event to Google Calendar.

    Args: 
      new_event: ElementTree._Element A new event which is to be added to 
                Google Calendar.
      insert_uri: the URL to post new events to the feed
      url_params: dict (optional) Additional URL parameters to be included
                  in the insertion request. 
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      On successful insert, a tuple in the form
      (boolean succeeded=True, ElementTree._Element new event from Google 
      Calendar) On failure, a tuple in the form:
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """

    response = self.Post(new_event, insert_uri, url_params=url_params,
                         escape_params=escape_params)

    if isinstance(response, atom.Entry):
      return gcalendar.CalendarEventEntryFromString(response.ToString())

  def InsertEventComment(self, new_entry, insert_uri, url_params=None,
                  escape_params=True):
    """Adds an entry to Google Calendar.

    Args:
      new_entry: ElementTree._Element A new entry which is to be added to
                Google Calendar.
      insert_uri: the URL to post new entrys to the feed
      url_params: dict (optional) Additional URL parameters to be included
                  in the insertion request.
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      On successful insert, a tuple in the form
      (boolean succeeded=True, ElementTree._Element new entry from Google
      Calendar) On failure, a tuple in the form:
      (boolean succeeded=False, {'status': HTTP status code from server,
                                 'reason': HTTP reason from the server,
                                 'body': HTTP body of the server's response})
    """

    response = self.Post(new_entry, insert_uri, url_params=url_params,
                         escape_params=escape_params)

    if isinstance(response, atom.Entry):
      return gcalendar.CalendarEventCommentEntryFromString(response.ToString())

  def DeleteEvent(self, edit_uri, extra_headers=None, 
      url_params=None, escape_params=True):
    """Removes an event with the specified ID from Google Calendar.

    Args:
      event_id: string The ID of the event to be deleted. Example:
               'http://www.google.com/calendar/feeds/default/private/full/abx'
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
    
    url_prefix = 'http://%s/' % self.server
    if edit_uri.startswith(url_prefix):
      edit_uri = edit_uri[len(url_prefix):]
    return self.Delete('/%s' % edit_uri,
                       url_params=url_params, escape_params=escape_params)

  def UpdateEvent(self, edit_uri, updated_event, url_params=None, 
                 escape_params=True):
    """Updates an existing event.

    Args:
      edit_uri: string The edit link URI for the element being updated
      updated_event: string, ElementTree._Element, or ElementWrapper containing
                    the Atom Entry which will replace the event which is 
                    stored at the edit_url 
      url_params: dict (optional) Additional URL parameters to be included
                  in the update request.
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      On successful update, a tuple in the form
      (boolean succeeded=True, ElementTree._Element new event from Google 
      Calendar) On failure, a tuple in the form:
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """
    url_prefix = 'http://%s/' % self.server
    if edit_uri.startswith(url_prefix):
      edit_uri = edit_uri[len(url_prefix):]
    response = self.Put(updated_event, '/%s' % edit_uri,
                        url_params=url_params, 
                        escape_params=escape_params)
    if isinstance(response, atom.Entry):
      return gcalendar.CalendarEventEntryFromString(response.ToString())


class CalendarEventQuery(gdata_service.Query):

  def __init__(self, user='default', visibility='private', projection='full',
               text_query=None, params=None, categories=None):
    gdata_service.Query.__init__(self, feed='http://www.google.com/calendar/feeds/'+
                           '%s/%s/%s' % (user, visibility, projection,),
                           text_query=text_query, params=params, 
                           categories=categories)
    
  def _GetStartMin(self):
    if 'start-min' in self.keys():
      return self['start-min']
    else:
      return None

  def _SetStartMin(self, val):
    self['start-min'] = val

  start_min = property(_GetStartMin, _SetStartMin, 
      doc="""The start-min query parameter""")

  def _GetStartMax(self):
    if 'start-max' in self.keys():
      return self['start-max']
    else:
      return None

  def _SetStartMax(self, val):
    self['start-max'] = val

  start_max = property(_GetStartMax, _SetStartMax, 
      doc="""The start-max query parameter""")

  def _GetOrderBy(self):
    if 'orderby' in self.keys():
      return self['orderby']
    else:
      return None

  def _SetOrderBy(self, val):
    if val is not 'lastmodified' and val is not 'starttime':
      raise Error, "Order By must be either 'lastmodified' or 'starttime'"
    self['orderby'] = val

  orderby = property(_GetOrderBy, _SetOrderBy, 
      doc="""The orderby query parameter""")

  def _GetSortOrder(self):
    if 'sortorder' in self.keys():
      return self['sortorder']
    else:
      return None

  def _SetSortOrder(self, val):
    if (val is not 'ascending' and val is not 'descending' 
        and val is not 'a' and val is not 'd' and val is not 'ascend'
        and val is not 'descend'):
      raise Error, "Sort order must be either ascending, ascend, " + (
          "a or descending, descend, or d")
    self['sortorder'] = val

  sortorder = property(_GetSortOrder, _SetSortOrder, 
      doc="""The sortorder query parameter""")

  def _GetSingleEvents(self):
    if 'singleevents' in self.keys():
      return self['singleevents']
    else:
      return None

  def _SetSingleEvents(self, val):
    self['singleevents'] = val

  singleevents = property(_GetSingleEvents, _SetSingleEvents, 
      doc="""The singleevents query parameter""")

  def _GetFutureEvents(self):
    if 'futureevents' in self.keys():
      return self['futureevents']
    else:
      return None

  def _SetFutureEvents(self, val):
    self['futureevents'] = val

  futureevents = property(_GetFutureEvents, _SetFutureEvents, 
      doc="""The futureevents query parameter""")

  def _GetRecurrenceExpansionStart(self):
    if 'recurrence-expansion-start' in self.keys():
      return self['recurrence-expansion-start']
    else:
      return None

  def _SetRecurrenceExpansionStart(self, val):
    self['recurrence-expansion-start'] = val

  recurrence_expansion_start = property(_GetRecurrenceExpansionStart, 
      _SetRecurrenceExpansionStart, 
      doc="""The recurrence-expansion-start query parameter""")

  def _GetRecurrenceExpansionEnd(self):
    if 'recurrence-expansion-end' in self.keys():
      return self['recurrence-expansion-end']
    else:
      return None

  def _SetRecurrenceExpansionEnd(self, val):
    self['recurrence-expansion-end'] = val

  recurrence_expansion_end = property(_GetRecurrenceExpansionEnd, 
      _SetRecurrenceExpansionEnd, 
      doc="""The recurrence-expansion-end query parameter""")

class CalendarListQuery(gdata_service.Query): 
  """Queries the Google Calendar meta feed"""

  def __init__(self, userId=None, text_query=None,
               params=None, categories=None):
    if userId is None:
      userId = 'default'

    gdata_service.Query.__init__(self, feed='http://www.google.com/calendar/feeds/'
                           +userId,
                           text_query=text_query, params=params,
                           categories=categories)

class CalendarEventCommentQuery(gdata_service.Query): 
  """Queries the Google Calendar event comments feed"""

  def __init__(self, feed=None):
    gdata_service.Query.__init__(self, feed=feed)
