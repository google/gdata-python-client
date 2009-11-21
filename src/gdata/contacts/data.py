#!/usr/bin/python
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


"""Contains the data classes of the Google Contacts Data API"""


__author__ = 'j.s@google.com (Jeff Scudder)'


import atom.core
import atom.data
import gdata.contacts.data
import gdata.data
import gdata.opensearch.data


GCONTACT_TEMPLATE = '{http://schemas.google.com/contact/2008/}%s'


class GroupMembershipInfo(atom.core.XmlElement):
  """Denotes contact's group membership"""
  _qname = GCONTACT_TEMPLATE % 'groupMembershipInfo'
  href = 'href'
  deleted = 'deleted'


class SystemGroup(atom.core.XmlElement):
  """Element that if present marks that a group is a system one"""
  _qname = GCONTACT_TEMPLATE % 'systemGroup'
  id = 'id'


class ContactGroupEntry(gdata.data.BatchEntry):
  """Describes a contact group entry"""
  system_group = SystemGroup
  extended_property = [gdata.data.ExtendedProperty]
  deleted = gdata.data.Deleted


class ContactGroupFeed(gdata.data.BatchFeed):
  """Describes a contact group feed"""
  entry = [ContactGroupEntry]


class BillingInformation(atom.core.XmlElement):
  """Contact's billing information"""
  _qname = GCONTACT_TEMPLATE % 'billingInformation'


class Birthday(atom.core.XmlElement):
  """Contact's birth date"""
  _qname = GCONTACT_TEMPLATE % 'birthday'
  when = 'when'


class CalendarLink(atom.core.XmlElement):
  """Contact related calendar link"""
  _qname = GCONTACT_TEMPLATE % 'calendarLink'
  label = 'label'
  primary = 'primary'
  href = 'href'
  rel = 'rel'


class DirectoryServer(atom.core.XmlElement):
  """Contact's directory server"""
  _qname = GCONTACT_TEMPLATE % 'directoryServer'


class Event(atom.core.XmlElement):
  """Contact's events"""
  _qname = GCONTACT_TEMPLATE % 'event'
  rel = 'rel'
  when = gdata.data.When
  label = 'label'


class ExternalId(atom.core.XmlElement):
  """Contact's external id field"""
  _qname = GCONTACT_TEMPLATE % 'externalId'
  label = 'label'
  rel = 'rel'
  value = 'value'


class Gender(atom.core.XmlElement):
  """Contact's gender"""
  _qname = GCONTACT_TEMPLATE % 'gender'
  value = 'value'


class Hobby(atom.core.XmlElement):
  """Contact's hobby"""
  _qname = GCONTACT_TEMPLATE % 'hobby'


class Initials(atom.core.XmlElement):
  """Contact's initials"""
  _qname = GCONTACT_TEMPLATE % 'initials'


class Jot(atom.core.XmlElement):
  """Contact's jot"""
  _qname = GCONTACT_TEMPLATE % 'jot'
  rel = 'rel'


class Language(atom.core.XmlElement):
  """Contact's language field"""
  _qname = GCONTACT_TEMPLATE % 'language'
  code = 'code'
  label = 'label'


class MaidenName(atom.core.XmlElement):
  """Contact's maiden name"""
  _qname = GCONTACT_TEMPLATE % 'maidenName'


class Mileage(atom.core.XmlElement):
  """Contact's mileage"""
  _qname = GCONTACT_TEMPLATE % 'mileage'


class Nickname(atom.core.XmlElement):
  """Contact's nickname"""
  _qname = GCONTACT_TEMPLATE % 'nickname'


class Occupation(atom.core.XmlElement):
  """Contact's hobby"""
  _qname = GCONTACT_TEMPLATE % 'occupation'


class Priority(atom.core.XmlElement):
  """Contact's priority"""
  _qname = GCONTACT_TEMPLATE % 'priority'
  rel = 'rel'


class Relation(atom.core.XmlElement):
  """Contact's relation"""
  _qname = GCONTACT_TEMPLATE % 'relation'
  label = 'label'
  rel = 'rel'


class Sensitivity(atom.core.XmlElement):
  """Contact's sensitivity"""
  _qname = GCONTACT_TEMPLATE % 'sensitivity'
  rel = 'rel'


class ShortName(atom.core.XmlElement):
  """Contact's short name"""
  _qname = GCONTACT_TEMPLATE % 'shortName'


class Subject(atom.core.XmlElement):
  """Contact's subject"""
  _qname = GCONTACT_TEMPLATE % 'subject'


class UserDefinedField(atom.core.XmlElement):
  """Contact's user defined field"""
  _qname = GCONTACT_TEMPLATE % 'userDefinedField'
  value = 'value'
  key = 'key'


class Website(atom.core.XmlElement):
  """Contact related website"""
  _qname = GCONTACT_TEMPLATE % 'website'
  rel = 'rel'
  label = 'label'
  primary = 'primary'
  href = 'href'


class PersonEntry(gdata.data.GDEntry):
  """Describes a person entry"""
  event = [Event]
  billing_information = BillingInformation
  calendar_link = [CalendarLink]
  phone_number = [gdata.data.PhoneNumber]
  short_name = ShortName
  im = [gdata.data.Im]
  user_defined_field = [UserDefinedField]
  relation = [Relation]
  organization = [gdata.data.Organization]
  directory_server = DirectoryServer
  where = gdata.data.Where
  hobby = [Hobby]
  email = [gdata.data.Email]
  gender = Gender
  jot = [Jot]
  extended_property = [gdata.data.ExtendedProperty]
  website = [Website]
  name = gdata.data.Name
  subject = Subject
  postal_address = [gdata.data.PostalAddress]
  maiden_name = MaidenName
  birthday = Birthday
  language = [Language]
  mileage = Mileage
  initials = Initials
  priority = Priority
  occupation = Occupation
  structured_postal_address = [gdata.data.StructuredPostalAddress]
  nickname = Nickname
  external_id = [ExternalId]
  sensitivity = Sensitivity


class ProfileEntry(gdata.data.BatchEntry):
  """Describes a profile entry"""


class ProfileFeed(gdata.data.BatchFeed):
  """Describes a profile feed"""
  entry = [ProfileEntry]


class ContactEntry(gdata.data.BatchEntry):
  """Describes a contact entry"""
  group_membership_info = [GroupMembershipInfo]
  deleted = gdata.data.Deleted


class ContactFeed(gdata.data.BatchFeed):
  """Describes a contact feed"""
  entry = [ContactEntry]


