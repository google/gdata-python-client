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



# TODO:
#   add text=none to all inits


"""Contains extensions to ElementWrapper objects used with Google Calendar."""

__author__ = 'api.vli (Vivian Li), api.rboyd (Ryan Boyd)'


try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import atom
import gdata


# XML namespaces which are often used in Google Calendar entities.
GCAL_NAMESPACE = 'http://schemas.google.com/gCal/2005'
GCAL_TEMPLATE = '{http://schemas.google.com/gCal/2005}%s'


class CalendarListFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Calendar meta feed flavor of an Atom Feed"""

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_CalendarListEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

class CalendarEventCommentFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Calendar event comments feed flavor of an Atom Feed"""

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_CalendarEventCommentEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

class CalendarEventCommentEntry(gdata.GDataEntry, gdata.LinkFinder):
  """A Google Calendar event comments entry flavor of an Atom Entry"""

def CalendarEventCommentEntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _CalendarEventCommentEntryFromElementTree(element_tree)

class CalendarEventFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Calendar event feed flavor of an Atom Feed"""

  def __init__(self, author=None, category=None, contributor=None,
      generator=None, icon=None, atom_id=None, link=None, logo=None, 
      rights=None, subtitle=None, title=None, updated=None, entry=None, 
      total_results=None, start_index=None, items_per_page=None,
      extension_elements=None, extension_attributes=None, text=None):
     gdata.GDataFeed.__init__(self, author=author, category=category,
                              contributor=contributor, generator=generator,
                              icon=icon,  atom_id=atom_id, link=link,
                              logo=logo, rights=rights, subtitle=subtitle,
                              title=title, updated=updated, entry=entry,
                              total_results=total_results,
                              start_index=start_index,
                              items_per_page=items_per_page,
                              extension_elements=extension_elements,
                              extension_attributes=extension_attributes,
                              text=text)

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_CalendarEventEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)


class CalendarListEntry(gdata.GDataEntry, gdata.LinkFinder):
  """A Google Calendar meta Entry flavor of an Atom Entry """
  
  def __init__(self, author=None, category=None, content=None,
      atom_id=None, link=None, published=None, 
      title=None, updated=None, 
      color=None, access_level=None, hidden=None, timezone=None,
      extension_elements=None, extension_attributes=None, text=None):
    gdata.GDataEntry.__init__(self, author=author, category=category, 
                        content=content, atom_id=atom_id, link=link, 
                        published=published, title=title, 
                        updated=updated, text=None)

    self.color = color
    self.access_level = access_level
    self.hidden = hidden 
    self.timezone = timezone

  def _TransferToElementTree(self, element_tree):
    if self.color:
      element_tree.append(self.color._ToElementTree())
    if self.access_level:
      element_tree.append(self.access_level._ToElementTree())
    if self.hidden:
      element_tree.append(self.hidden._ToElementTree())
    if self.timezone:
      element_tree.append(self.timezone._ToElementTree())

    gdata.GDataEntry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (GCAL_NAMESPACE, 'color'):
      self.color = _ColorFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (GCAL_NAMESPACE, 'accesslevel'):
      self.access_level = _AccessLevelFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (GCAL_NAMESPACE, 'hidden'):
      self.hidden = _HiddenFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (GCAL_NAMESPACE, 'timezone'):
      self.timezone = _TimezoneFromElementTree(child)
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataEntry._TransferFromElementTree(self, element_tree)

def CalendarEventEntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _CalendarEventEntryFromElementTree(element_tree)


class CalendarEventEntry(gdata.GDataEntry):
  """A Google Calendar flavor of an Atom Entry """
  
  def __init__(self, author=None, category=None, content=None,
      atom_id=None, link=None, published=None, 
      title=None, updated=None, 
      transparency=None, comments=None, event_status=None,
      send_event_notifications=None, visibility=None,
      recurrence=None, recurrence_exception=None,
      where=None, when=None, who=None,
      extended_property=None, 
      extension_elements=None, extension_attributes=None, text=None):

    gdata.GDataEntry.__init__(self, author=author, category=category, 
                        content=content,
                        atom_id=atom_id, link=link, published=published,
                        title=title, updated=updated)
    
    self.transparency = transparency 
    self.comments = comments
    self.event_status = event_status 
    self.send_event_notifications = send_event_notifications
    self.visibility = visibility
    self.recurrence = recurrence 
    self.recurrence_exception = recurrence_exception or []
    self.where = where or []
    self.when = when or []
    self.who = who or []
    self.extended_property = extended_property or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    for a_where in self.where:
      element_tree.append(a_where._ToElementTree())
    for a_who in self.who:
      element_tree.append(a_who._ToElementTree())
    for a_when in self.when:
      element_tree.append(a_when._ToElementTree())
    for a_extended_property in self.extended_property:
      element_tree.append(a_extended_property._ToElementTree())
    if self.transparency:
      element_tree.append(self.transparency._ToElementTree())
    if self.visibility:
      element_tree.append(self.visibility._ToElementTree())
    if self.comments:
      element_tree.append(self.comments._ToElementTree())
    if self.send_event_notifications:
      element_tree.append(self.send_event_notifications._ToElementTree())
    if self.event_status:
      element_tree.append(self.event_status._ToElementTree())
    if self.recurrence:
      element_tree.append(self.recurrence._ToElementTree())
    for an_exception in self.recurrence_exception:
      element_tree.append(an_exception._ToElementTree())

    gdata.GDataEntry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'where'):
      self.where.append(_WhereFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'when'):
      self.when.append(_WhenFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'who'):
      self.who.append(_WhoFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'extendedProperty'):
      self.extended_property.append(_ExtendedPropertyFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'visibility'):
      self.visibility=_VisibilityFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'transparency'):
      self.transparency=_TransparencyFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'eventStatus'):
      self.event_status=_EventStatusFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'recurrence'):
      self.recurrence=_RecurrenceFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'recurrenceException'):
      self.recurrence_exception.append(_RecurrenceExceptionFromElementTree(
          child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (GCAL_NAMESPACE, 'sendEventNotifications'):
      self.send_event_notifications=(
          _SendEventNotificationsFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'comments'):
      self.comments=_CommentsFromElementTree(child) 
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataEntry._TransferFromElementTree(self, element_tree)

def CalendarEventEntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _CalendarEventEntryFromElementTree(element_tree)


class Where(atom.AtomBase):
  """The Google Calendar Where element"""

  def __init__(self, value_string=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.value_string = value_string 
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = gdata.GDATA_TEMPLATE % 'where'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

  def _TransferToElementTree(self, element_tree):
    if self.value_string:
      element_tree.attrib['valueString'] = self.value_string
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = gdata.GDATA_TEMPLATE % 'where'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'valueString':
      self.value_string = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)


class ExtendedProperty(atom.AtomBase):
  """The Google Calendar extendedProperty element"""

  def __init__(self, name=None, value=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.name = name 
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.name:
      element_tree.attrib['name'] = self.name
    if self.value:
      element_tree.attrib['value'] = self.value
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = gdata.GDATA_TEMPLATE % 'extendedProperty'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'name':
      self.name = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'value':
      self.value = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)


class When(atom.AtomBase):
  """The Google Calendar When element"""

  def __init__(self, start_time=None, end_time=None, reminder=None, 
      extension_elements=None, extension_attributes=None, text=None):
    self.start_time = start_time 
    self.end_time = end_time 
    self.reminder = reminder or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.start_time:
      element_tree.attrib['startTime'] = self.start_time
    if self.end_time:
      element_tree.attrib['endTime'] = self.end_time
    for a_reminder in self.reminder:
      element_tree.append(a_reminder._ToElementTree())
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = gdata.GDATA_TEMPLATE % 'when'
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'reminder'):
      self.reminder.append(_ReminderFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'startTime':
      self.start_time = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'endTime':
      self.end_time = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)


class Recurrence(atom.AtomBase):
  """The Google Calendar Recurrence element"""

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = gdata.GDATA_TEMPLATE % 'recurrence'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree


class RecurrenceException(atom.AtomBase):
  """The Google Calendar RecurrenceException element"""
  
  def __init__(self, specialized=None, entry_link=None, 
      original_event=None, extension_elements=None, 
      extension_attributes=None, text=None):
    self.specialized = specialized
    self.entry_link = entry_link
    self.original_event = original_event
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    
  def _TransferToElementTree(self, element_tree):
    if self.specialized:
      element_tree.attrib['specialized'] = self.specialized
    if self.entry_link:
      element_tree.append(self.entry_link._ToElementTree())
    if self.original_event:
      element_tree.append(original_event._ToElementTree())
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = gdata.GDATA_TEMPLATE % 'recurrenceException'
    return element_tree
    
  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'entryLink'):
      self.entry_link = gdata._EntryLinkFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'originalEvent'):
      self.original_event = _OriginalEventLinkFromElementTree(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'specialized':
      self.specialized = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute,
          element_tree)
  
 
class OriginalEvent(atom.AtomBase):
  """The Google Calendar OriginalEvent element"""

  def __init__(self, id=None, href=None, when=None, 
      extension_elements=None, extension_attributes=None, text=None):
    self.id = id
    self.href = href 
    self.when = when
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.id:
      element_tree.attrib['id'] = self.id
    if self.href:
      element_tree.attrib['href'] = self.href
    if self.when:
      element_tree.append(self.when._ToElementTree())
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = gdata.GDATA_TEMPLATE % 'originalEvent'
    return element_tree
    
  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'when'):
      self.when = gdata._EntryLinkFromElementTree(child)
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'id':
      self.id = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'href':
      self.href = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute,
          element_tree)


class UriEnumElement(atom.AtomBase):
  def __init__(self, tag, enum_map, attrib_name='value', 
      extension_elements=None, extension_attributes=None, text=None):
    self.tag=tag
    self.enum_map=enum_map
    self.attrib_name=attrib_name
    self.value=None
    self.text=text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
     
  def findKey(self, value):
     res=[item[0] for item in self.enum_map.items() if item[1] == value]
     if res is None or len(res) == 0:
       return None
     return res[0]

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == self.attrib_name:
       val = element_tree.attrib[self.attrib_name]
       if val != '':
          self.value = self.enum_map[val]
       del element_tree.attrib[self.attrib_name]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = gdata.GDATA_TEMPLATE % self.tag
    key = self.findKey(self.value)
    if key is not None:
       element_tree.attrib[self.attrib_name]=key
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

 
class Who(UriEnumElement):
  """The Google Calendar Who element"""
  relEnum = { 'http://schemas.google.com/g/2005#event.attendee' : 'ATTENDEE',
              'http://schemas.google.com/g/2005#event.organizer' : 'ORGANIZER',
              'http://schemas.google.com/g/2005#event.performer' : 'PERFORMER',
              'http://schemas.google.com/g/2005#event.speaker' : 'SPEAKER',
              'http://schemas.google.com/g/2005#message.bcc' : 'BCC',
              'http://schemas.google.com/g/2005#message.cc' : 'CC',
              'http://schemas.google.com/g/2005#message.from' : 'FROM',
              'http://schemas.google.com/g/2005#message.reply-to' : 'REPLY_TO',
              'http://schemas.google.com/g/2005#message.to' : 'TO' }
  
  def __init__(self, extension_elements=None, 
    extension_attributes=None, text=None):
    UriEnumElement.__init__(self, 'who', Who.relEnum, attrib_name='rel',
                            extension_elements=extension_elements,
                            extension_attributes=extension_attributes, 
                            text=text)
    self.name=None
    self.email=None
    self.attendee_status=None
    self.attendee_type=None
    self.rel=None
    
  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'valueString':
       self.name=element_tree.attrib[attribute]
       del element_tree.attrib[attribute]
    elif attribute == 'email':
       self.email=element_tree.attrib[attribute]
       del element_tree.attrib[attribute]
    else:
      UriEnumElement._TakeAttributeFromElementTree(self, attribute, 
          element_tree)
      self.rel=self.value

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'attendeeStatus'):
      self.attendee_status=_AttendeeStatusFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'attendeeType'):
      self.attendee_type=_AttendeeTypeFromElementTree(child)
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TransferToElementTree(self, element_tree):
    self.value=self.rel
    element_tree.attrib['valueString']=self.name
    element_tree.attrib['email']=self.email
    return UriEnumElement._TransferToElementTree(self, element_tree)


class AttendeeStatus(UriEnumElement):
  """The Google Calendar attendeeStatus element"""
  attendee_enum = { 
      'http://schemas.google.com/g/2005#event.accepted' : 'ACCEPTED',
      'http://schemas.google.com/g/2005#event.declined' : 'DECLINED',
      'http://schemas.google.com/g/2005#event.invited' : 'INVITED',
      'http://schemas.google.com/g/2005#event.tentative' : 'TENTATIVE'}
  
  def __init__(self, extension_elements=None, 
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, 'attendeeStatus', AttendeeStatus.attendee_enum,
                            extension_elements=extension_elements,
                            extension_attributes=extension_attributes, 
                            text=text)


class AttendeeType(UriEnumElement):
  """The Google Calendar attendeeType element"""
  attendee_type_enum = { 
      'http://schemas.google.com/g/2005#event.optional' : 'OPTIONAL',
      'http://schemas.google.com/g/2005#event.required' : 'REQUIRED' }
  
  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, 'attendeeType', 
        AttendeeType.attendee_type_enum,
        extension_elements=extension_elements,
        extension_attributes=extension_attributes,text=text)


class Visibility(UriEnumElement):
  """The Google Calendar Visibility element"""
  visibility_enum = { 
      'http://schemas.google.com/g/2005#event.confidential' : 'CONFIDENTIAL',
      'http://schemas.google.com/g/2005#event.default' : 'DEFAULT',
      'http://schemas.google.com/g/2005#event.private' : 'PRIVATE',
      'http://schemas.google.com/g/2005#event.public' : 'PUBLIC' }

  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, 'visibility', Visibility.visibility_enum,
                            extension_elements=extension_elements,
                            extension_attributes=extension_attributes, 
                            text=text)


class Transparency(UriEnumElement):
  """The Google Calendar Transparency element"""
  transparency_enum = { 
      'http://schemas.google.com/g/2005#event.opaque' : 'OPAQUE',
      'http://schemas.google.com/g/2005#event.transparent' : 'TRANSPARENT' }
  
  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, tag='transparency', 
                            enum_map=Transparency.transparency_enum,
                            extension_elements=extension_elements,
                            extension_attributes=extension_attributes, 
                            text=text)


class Comments(atom.AtomBase):
  """The Google Calendar comments element"""

  def __init__(self, rel=None, feed_link=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.rel = rel 
    self.feed_link = feed_link
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.rel:
      element_tree.attrib['rel'] = self.rel
    if self.feed_link:
      element_tree.append(self.feed_link._ToElementTree())
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = gdata.GDATA_TEMPLATE % 'comments'
    return element_tree
    
  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'feedLink'):
      self.feed_link = gdata._FeedLinkFromElementTree(child)
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'rel':
      self.rel = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute,
          element_tree)

class Reminder(atom.AtomBase):
  """The Google Calendar reminder element"""

  def __init__(self, absolute_time=None,
      days=None, hours=None, minutes=None, 
      extension_elements=None,
      extension_attributes=None, text=None):
    self.absolute_time = absolute_time
    if days is not None: 
      self.days = str(days)
    else:
      self.days = None
    if hours is not None:
      self.hours = str(hours)
    else:
      self.hours = None
    if minutes is not None:
      self.minutes = str(minutes)
    else:
      self.minutes = None
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.absolute_time:
      element_tree.attrib['absolute_time'] = self.absolute_time
    if self.days:
      element_tree.attrib['days'] = self.days
    if self.hours:
      element_tree.attrib['hours'] = self.hours
    if self.minutes:
      element_tree.attrib['minutes'] = self.minutes
    element_tree.tag = gdata.GDATA_TEMPLATE % 'reminder'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'absoluteTime':
      self.absolute_time= element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'days':
      self.days = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'hours':
      self.hours = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'minutes':
      self.minutes = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)


class EventStatus(UriEnumElement):
  """The Google Calendar eventStatus element"""
  status_enum = { 'http://schemas.google.com/g/2005#event.canceled' : 'CANCELED',
                 'http://schemas.google.com/g/2005#event.confirmed' : 'CONFIRMED',
                 'http://schemas.google.com/g/2005#event.tentative' : 'TENTATIVE'}
  
  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, tag='eventStatus', 
        enum_map=EventStatus.status_enum,
        extension_elements=extension_elements,
        extension_attributes=extension_attributes, 
        text=text)


class SendEventNotifications(atom.AtomBase):
  """The Google Calendar sendEventNotifications element"""

  def __init__(self, extension_elements=None,
      value=None, extension_attributes=None, text=None):
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.value:
      element_tree.attrib['value'] = self.value
    element_tree.tag = GCAL_TEMPLATE % 'sendEventNotifications'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'value':
      self.value = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)


class Color(atom.AtomBase):
  """The Google Calendar color element"""
  
  def __init__(self, value=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.value:
      element_tree.attrib['value'] = self.value
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = GCAL_TEMPLATE % 'color'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'value':
      self.value = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)


class AccessLevel(atom.AtomBase):
  """The Google Calendar accesslevel element"""
  
  def __init__(self, value=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.value:
      element_tree.attrib['value'] = self.value
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = GCAL_TEMPLATE % 'accesslevel'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'value':
      self.value = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)


class Hidden(atom.AtomBase):
  """The Google Calendar hidden element"""
  
  def __init__(self, extension_elements=None, value=None,
      extension_attributes=None, text=None):
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.value:
      element_tree.attrib['value'] = self.value
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = GCAL_TEMPLATE % 'hidden'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'value':
      self.value = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)


class Timezone(atom.AtomBase):
  """The Google Calendar timezone element"""
  
  def __init__(self, extension_elements=None, value=None,
      extension_attributes=None, text=None):
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.value:
      element_tree.attrib['value'] = self.value
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = GCAL_TEMPLATE % 'timezone'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'value':
      self.value = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)

def CalendarListFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _CalendarListFeedFromElementTree(element_tree)

def CalendarEventFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _CalendarEventFeedFromElementTree(element_tree)

def CalendarEventCommentFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _CalendarEventCommentFeedFromElementTree(element_tree)


# Code to create atom feeds from element trees
_CalendarListFeedFromElementTree = atom._AtomInstanceFromElementTree(
    CalendarListFeed, 'feed', atom.ATOM_NAMESPACE)
_CalendarListEntryFromElementTree = atom._AtomInstanceFromElementTree(
    CalendarListEntry, 'entry', atom.ATOM_NAMESPACE)
_CalendarEventFeedFromElementTree = atom._AtomInstanceFromElementTree(
    CalendarEventFeed, 'feed', atom.ATOM_NAMESPACE)
_CalendarEventEntryFromElementTree = atom._AtomInstanceFromElementTree(
    CalendarEventEntry, 'entry', atom.ATOM_NAMESPACE)
_CalendarEventCommentFeedFromElementTree = atom._AtomInstanceFromElementTree(
    CalendarEventCommentFeed, 'feed', atom.ATOM_NAMESPACE)
_CalendarEventCommentEntryFromElementTree = atom._AtomInstanceFromElementTree(
    CalendarEventCommentEntry, 'entry', atom.ATOM_NAMESPACE)
_WhereFromElementTree = atom._AtomInstanceFromElementTree(
    Where, 'where', gdata.GDATA_NAMESPACE)
_WhenFromElementTree = atom._AtomInstanceFromElementTree(
    When, 'when', gdata.GDATA_NAMESPACE)
_WhoFromElementTree = atom._AtomInstanceFromElementTree(
    Who, 'who', gdata.GDATA_NAMESPACE)
_VisibilityFromElementTree= atom._AtomInstanceFromElementTree(
    Visibility, 'visibility', gdata.GDATA_NAMESPACE)
_TransparencyFromElementTree = atom._AtomInstanceFromElementTree(
    Transparency, 'transparency', gdata.GDATA_NAMESPACE)
_CommentsFromElementTree = atom._AtomInstanceFromElementTree(
    Comments, 'comments', gdata.GDATA_NAMESPACE)
_EventStatusFromElementTree = atom._AtomInstanceFromElementTree(
    EventStatus, 'eventStatus', gdata.GDATA_NAMESPACE)
_SendEventNotificationsFromElementTree = atom._AtomInstanceFromElementTree(
    SendEventNotifications, 'sendEventNotifications', GCAL_NAMESPACE)
_AttendeeStatusFromElementTree = atom._AtomInstanceFromElementTree(
    AttendeeStatus, 'attendeeStatus', gdata.GDATA_NAMESPACE)
_AttendeeTypeFromElementTree = atom._AtomInstanceFromElementTree(
    AttendeeType, 'attendeeType', gdata.GDATA_NAMESPACE)
_ExtendedPropertyFromElementTree = atom._AtomInstanceFromElementTree(
    ExtendedProperty, 'extendedProperty', gdata.GDATA_NAMESPACE)
_RecurrenceFromElementTree = atom._AtomInstanceFromElementTree(
    Recurrence, 'recurrence', gdata.GDATA_NAMESPACE)
_RecurrenceExceptionFromElementTree = atom._AtomInstanceFromElementTree(
    RecurrenceException, 'recurrenceException', gdata.GDATA_NAMESPACE)
_OriginalEventFromElementTree = atom._AtomInstanceFromElementTree(
    OriginalEvent, 'originalEvent', gdata.GDATA_NAMESPACE)
_ColorFromElementTree = atom._AtomInstanceFromElementTree(
    Color, 'color', GCAL_NAMESPACE)
_HiddenFromElementTree = atom._AtomInstanceFromElementTree(
    Hidden, 'hidden', GCAL_NAMESPACE)
_TimezoneFromElementTree = atom._AtomInstanceFromElementTree(
    Timezone, 'timezone', GCAL_NAMESPACE)
_AccessLevelFromElementTree = atom._AtomInstanceFromElementTree(
    AccessLevel, 'accesslevel', GCAL_NAMESPACE)
_ReminderFromElementTree = atom._AtomInstanceFromElementTree(
    Reminder, 'reminder', gdata.GDATA_NAMESPACE)
