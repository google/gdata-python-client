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

"""Data model classes for parsing and generating XML for the Contacts API."""


__author__ = 'vinces1979@gmail.com (Vince Spicer)'


import atom.core
import gdata
import gdata.data


## Constants from http://code.google.com/apis/gdata/elements.html ##
REL_HOME = 'http://schemas.google.com/g/2005#home'                  
REL_WORK = 'http://schemas.google.com/g/2005#work'                  
REL_OTHER = 'http://schemas.google.com/g/2005#other'                

# AOL Instant Messenger protocol
IM_AIM = 'http://schemas.google.com/g/2005#AIM'
IM_MSN = 'http://schemas.google.com/g/2005#MSN'  # MSN Messenger protocol
IM_YAHOO = 'http://schemas.google.com/g/2005#YAHOO'  # Yahoo Messenger protocol
IM_SKYPE = 'http://schemas.google.com/g/2005#SKYPE'  # Skype protocol          
IM_QQ = 'http://schemas.google.com/g/2005#QQ'  # QQ protocol                   
# Google Talk protocol                                                         
IM_GOOGLE_TALK = 'http://schemas.google.com/g/2005#GOOGLE_TALK'                
IM_ICQ = 'http://schemas.google.com/g/2005#ICQ'  # ICQ protocol                
IM_JABBER = 'http://schemas.google.com/g/2005#JABBER'  # Jabber protocol       
IM_NETMEETING = 'http://schemas.google.com/g/2005#netmeeting'  # NetMeeting    

PHOTO_LINK_REL = 'http://schemas.google.com/contacts/2008/rel#photo'
PHOTO_EDIT_LINK_REL = 'http://schemas.google.com/contacts/2008/rel#edit-photo'

# Different phone types, for moro info see: 
# http://code.google.com/apis/gdata/docs/2.0/elements.html#gdPhoneNumber
PHONE_CAR = 'http://schemas.google.com/g/2005#car'
PHONE_FAX = 'http://schemas.google.com/g/2005#fax'
PHONE_GENERAL = 'http://schemas.google.com/g/2005#general'
PHONE_HOME = REL_HOME
PHONE_HOME_FAX = 'http://schemas.google.com/g/2005#home_fax'
PHONE_INTERNAL = 'http://schemas.google.com/g/2005#internal-extension'
PHONE_MOBILE = 'http://schemas.google.com/g/2005#mobile'
PHONE_OTHER = REL_OTHER
PHONE_PAGER = 'http://schemas.google.com/g/2005#pager'
PHONE_SATELLITE = 'http://schemas.google.com/g/2005#satellite'
PHONE_VOIP = 'http://schemas.google.com/g/2005#voip'
PHONE_WORK = REL_WORK
PHONE_WORK_FAX = 'http://schemas.google.com/g/2005#work_fax'
PHONE_WORK_MOBILE = 'http://schemas.google.com/g/2005#work_mobile'
PHONE_WORK_PAGER = 'http://schemas.google.com/g/2005#work_pager'
PHONE_MAIN = 'http://schemas.google.com/g/2005#main'
PHONE_ASSISTANT = 'http://schemas.google.com/g/2005#assistant'
PHONE_CALLBACK = 'http://schemas.google.com/g/2005#callback'
PHONE_COMPANY_MAIN = 'http://schemas.google.com/g/2005#company_main'
PHONE_ISDN = 'http://schemas.google.com/g/2005#isdn'
PHONE_OTHER_FAX = 'http://schemas.google.com/g/2005#other_fax'
PHONE_RADIO = 'http://schemas.google.com/g/2005#radio'
PHONE_TELEX = 'http://schemas.google.com/g/2005#telex'
PHONE_TTY_TDD = 'http://schemas.google.com/g/2005#tty_tdd'

EXTERNAL_ID_ORGANIZATION = 'organization'

RELATION_MANAGER = 'manager'

CONTACTS_NAMESPACE = 'http://schemas.google.com/contact/2008'
CONTACTS_TEMPLATE = '{%s}%%s' % CONTACTS_NAMESPACE


class Where(atom.core.XmlElement):
  """ The Google Contacts Where element """
  
  _qname = gdata.GDATA_TEMPLATE % 'when'
  
  rel = 'rel'
  label = 'label'
  value_string = 'value_string'


class When(atom.core.XmlElement):
  """ The Google Contacts When element """
  
  _qname = gdata.GDATA_TEMPLATE % 'where'
  
  startTime = 'start_time'
  endTime = 'end_time'
  label = 'label'


class BillingInformation(atom.core.XmlElement):
  """ 
  gContact:billingInformation
  Specifies billing information of the entity represented by the contact. The element cannot be repeated. 
  """
  
  _qname = CONTACTS_TEMPLATE % 'billingInformation'


class Birthday(atom.core.XmlElement):
  """ 
 Stores birthday date of the person represented by the contact. The element cannot be repeated. 
 """
  
  _qname = CONTACTS_TEMPLATE % 'birthday'
  when = 'when'


class CalendarLink(atom.core.XmlElement):
  """ 
  Storage for URL of the contact's calendar. The element can be repeated. 
  """
  
  _qname = CONTACTS_TEMPLATE % 'calendarLink'
  rel = 'rel'
  label = 'label'
  primary = 'primary'
  href = 'href'


class DirectoryServer(atom.core.XmlElement):
  """ 
  A directory server associated with this contact. 
  May not be repeated. 
  """
  
  _qname = CONTACTS_TEMPLATE % 'directoryServer'


class Event(atom.core.XmlElement):
  """
  These elements describe events associated with a contact. 
  They may be repeated
  """
  
  _qname = CONTACTS_TEMPLATE % 'event'
  label = 'label'
  rel = 'rel'
  when = When


class ExternalId(atom.core.XmlElement):
  """
   Describes an ID of the contact in an external system of some kind. 
  This element may be repeated. 
  """
  
  _qname = CONTACTS_TEMPLATE % 'externalId'


def ExternalIdFromString(xml_string):
  return atom.core.parse(ExternalId, xml_string)


class Gender(atom.core.XmlElement):
  """ 
  Specifies the gender of the person represented by the contact.
  The element cannot be repeated. 
  """
  
  _qname = CONTACTS_TEMPLATE % 'directoryServer'
  value = 'value'


class Hobby(atom.core.XmlElement):
  """ 
  Describes an ID of the contact in an external system of some kind. 
  This element may be repeated. 
  """
  
  _qname = CONTACTS_TEMPLATE % 'hobby'


class Initials(atom.core.XmlElement):
  """ Specifies the initials of the person represented by the contact. The 
  element cannot be repeated. """
  
  _qname = CONTACTS_TEMPLATE % 'initials'


class Jot(atom.core.XmlElement):
  """ 
  Storage for arbitrary pieces of information about the contact. Each jot 
  has a type specified by the rel attribute and a text value. 
  The element can be repeated. 
  """
  
  _qname = CONTACTS_TEMPLATE % 'jot'
  rel = 'rel'


class Language(atom.core.XmlElement):
  """ 
 Specifies the preferred languages of the contact. 
 The element can be repeated.

  The language must be specified using one of two mutually exclusive methods: 
  using the freeform @label attribute, or using the @code attribute, whose value 
  must conform to the IETF BCP 47 specification.
  """
  
  _qname = CONTACTS_TEMPLATE % 'language'
  code = 'code'
  label = 'label'


class MaidenName(atom.core.XmlElement):
  """ 
  Specifies maiden name of the person represented by the contact. 
  The element cannot be repeated.
  """
  
  _qname = CONTACTS_TEMPLATE % 'maidenName'


class Mileage(atom.core.XmlElement):
  """ 
  Specifies the mileage for the entity represented by the contact. 
  Can be used for example to document distance needed for reimbursement 
  purposes. The value is not interpreted. The element cannot be repeated.
  """
  
  _qname = CONTACTS_TEMPLATE % 'mileage'


class NickName(atom.core.XmlElement):
  """
  Specifies the nickname of the person represented by the contact. 
  The element cannot be repeated.
  """
  
  _qname = CONTACTS_TEMPLATE % 'nickname'


class Occupation(atom.core.XmlElement):
  """
  Specifies the occupation/profession of the person specified by the contact. 
  The element cannot be repeated.
  """
  
  _qname = CONTACTS_TEMPLATE % 'occupation'


class Priority(atom.core.XmlElement):
  """ 
  Classifies importance of the contact into 3 categories:
    * Low
    * Normal
    * High

  The priority element cannot be repeated. 
  """

  _qname = CONTACTS_TEMPLATE % 'priority'


class Relation(atom.core.XmlElement):
  """
  This element describe another entity (usually a person) that is in a 
  relation of some kind with the contact.
  """

  _qname = CONTACTS_TEMPLATE % 'relation'
  rel = 'rel'
  label = 'label'


class Sensitivity(atom.core.XmlElement):
  """
  Classifies sensitivity of the contact into the following categories:
    * Confidential
    * Normal
    * Personal
    * Private

  The sensitivity element cannot be repeated. 
  """

  _qname = CONTACTS_TEMPLATE % 'sensitivity'
  rel = 'rel'


class UserDefinedField(atom.core.XmlElement):
  """
  Represents an arbitrary key-value pair attached to the contact.
  """

  _qname = CONTACTS_TEMPLATE % 'userDefinedField'
  key = 'key'
  value = 'value'


def UserDefinedFieldFromString(xml_string):
  return atom.core.parse(UserDefinedField, xml_string)


class Website(atom.core.XmlElement):
  """
  Describes websites associated with the contact, including links. 
  May be repeated.
  """

  _qname = CONTACTS_TEMPLATE % 'website'
  
  href = 'href'
  label = 'label'
  primary = 'primary'
  rel = 'rel'


def WebsiteFromString(xml_string):
  return atom.core.parse(Website, xml_string)


class OrgName(atom.core.XmlElement):
  _qname = gdata.GDATA_TEMPLATE % 'orgName'


class OrgJobDescription(atom.core.XmlElement):
  _qname = gdata.GDATA_TEMPLATE % 'orgJobDecscription'

                        
class OrgDepartment(atom.core.XmlElement):
  
  _qname = gdata.GDATA_TEMPLATE % 'orgDepartment'


class OrgTitle(atom.core.XmlElement):
  """The Google Contacts OrgTitle element."""

  _qname = gdata.GDATA_TEMPLATE % 'orgTitle'
  
               
class Organization(atom.core.XmlElement):
  """The Google Contacts Organization element."""
 
  _qname = gdata.GDATA_TEMPLATE % 'organization'
  rel = 'rel'
  label = 'label'
  primary = 'primary'
  org_name = OrgName
  org_title = OrgTitle
  org_job_description = OrgJobDescription
  org_department = OrgDepartment


class PostalAddress(atom.core.XmlElement):
  _qname = gdata.GDATA_TEMPLATE % 'postalAddress'
  rel = 'rel'
  primary = 'primary'


class IM(atom.core.XmlElement):
  """The Google Contacts IM element."""

  _qname = gdata.GDATA_TEMPLATE % 'im'
  address = 'address'
  primary = 'primary'
  protocol = 'protocol'
  label = 'label'
  rel  = 'rel'

                
class Email(atom.core.XmlElement):
  """The Google Contacts Email element."""

  _qname = gdata.GDATA_TEMPLATE % 'email'
  address = 'address'
  primary = 'primary'
  rel = 'rel'
  label = 'label' 


class PhoneNumber(atom.core.XmlElement):
  """The Google Contacts Phone Number element."""

  _qname = gdata.GDATA_TEMPLATE % 'phoneNumber'
  label = 'label'
  primary = 'primary'
  rel = 'rel'
  label = 'label'
  uri = 'uri'


class GivenName(atom.core.XmlElement):
  """ Person's given name. """
     
  _qname = gdata.GDATA_TEMPLATE % 'givenName'
  yomi = 'yomi'


class AdditionalName(atom.core.XmlElement):
  """ Additional name of the person, eg. middle name. """
    
  _qname = gdata.GDATA_TEMPLATE % 'additionalName'
  yomi = 'yomi'


class FamilyName(atom.core.XmlElement):
  """ Person's family name. """
    
  _qname = gdata.GDATA_TEMPLATE % 'familyName'
  yomi = 'yomi'

    
class FullName(atom.core.XmlElement):
  """The Google Contacts Full Name element."""
    
  _qname = gdata.GDATA_TEMPLATE % 'fullName'
  yomi = 'yomi'


class NamePrefix(atom.core.XmlElement):
  """ Honorific prefix, eg. 'Mr' or 'Mrs'. """
    
  _qname = gdata.GDATA_TEMPLATE % 'namePrefix'


class NameSuffix(atom.core.XmlElement):
  """ Honorific suffix, eg. 'san' or 'III'. """
    
  _qname = gdata.GDATA_TEMPLATE % 'nameSuffix'


class Name(atom.core.XmlElement):
  """ 
  Allows storing person's name in a structured way. Consists of given
  name, additional name, family name, prefix, suffix and full name. 
  """
    
  _qname = gdata.GDATA_TEMPLATE % 'name' 
  given_name = GivenName
  additonal_name = AdditionalName
  family_name = FamilyName
  full_name = FullName
  name_prefix = NamePrefix
  name_suffix = NameSuffix


class HouseName(atom.core.XmlElement):
  """
  Used in places where houses or buildings have names (and 
  not necessarily numbers), eg. "The Pillars".
  """
  
  _qname = CONTACTS_TEMPLATE % 'housename'


class Street(atom.core.XmlElement):
  """
  Can be street, avenue, road, etc. This element also includes the house 
  number and room/apartment/flat/floor number.
  """
  
  _qname = CONTACTS_TEMPLATE % 'street'


class POBox(atom.core.XmlElement):
  """
  Covers actual P.O. boxes, drawers, locked bags, etc. This is usually but not
  always mutually exclusive with street
  """
  
  _qname = CONTACTS_TEMPLATE % 'pobox'


class Neighborhood(atom.core.XmlElement):
  """
  This is used to disambiguate a street address when a city contains more than
  one street with the same name, or to specify a small place whose mail is
  routed through a larger postal town. In China it could be a county or a 
  minor city.
  """
  
  _qname = CONTACTS_TEMPLATE % 'neighborhood'


class City(atom.core.XmlElement):
  """
  Can be city, village, town, borough, etc. This is the postal town and not
  necessarily the place of residence or place of business.
  """
  
  _qname = CONTACTS_TEMPLATE % 'city'

class SubRegion(atom.core.XmlElement):
  """
  Handles administrative districts such as U.S. or U.K. counties that are not
   used for mail addressing purposes. Subregion is not intended for 
   delivery addresses.
  """

  _qname = CONTACTS_TEMPLATE % 'subregion'


class Region(atom.core.XmlElement):
  """
  A state, province, county (in Ireland), Land (in Germany), 
  departement (in France), etc.
  """

  _qname = CONTACTS_TEMPLATE % 'region'
  

class PostalCode(atom.core.XmlElement):
  """
  Postal code. Usually country-wide, but sometimes specific to the 
  city (e.g. "2" in "Dublin 2, Ireland" addresses).
  """
  
  _qname = CONTACTS_TEMPLATE % 'postcode'

class Country(atom.core.XmlElement):
  """ The name or code of the country. """

  _qname = CONTACTS_TEMPLATE % 'country'  

class FormattedAddress(atom.core.XmlElement):
  """ The full, unstructured postal address. """
  
  _qname = CONTACTS_TEMPLATE % 'formattedAddress'

  
class StructuredPostalAddress(atom.core.XmlElement):
  """
  Postal address split into components. It allows to store the address in
  locale independent format. The fields can be interpreted and used to 
  generate formatted, locale dependent address. 
  """
  
  _qname = gdata.GDATA_TEMPLATE  % 'structuredPostalAddress'
  
  rel = 'rel'
  mail_class = 'mailClass'
  usage = 'usage'
  label = 'label'
  primary = 'primary'

  housename = HouseName
  street = Street
  pobox = POBox
  neighborhood = Neighborhood
  city = City
  subregion = SubRegion
  region = Region
  postal_code = PostalCode
  country = Country
  formattedAddress = FormattedAddress

class ExtendedProperty(atom.core.XmlElement):
  """ It is possible to set any additional contact- or contact group- related
   information as an exteded property (arbitrary name - value pair) for a
   contact or contact group entry. 
   """
    
  _qname = gdata.GDATA_TEMPLATE % 'extendedProperty'
  name = 'name'
  value = 'value'

class PersonEntry(gdata.data.GDEntry):
  """Represents a google contact"""

  billing_information = BillingInformation
  birthday = Birthday
  calendar_link = [CalendarLink]
  directory_server = DirectoryServer
  event = [Event]
  external_id = [ExternalId]
  gender = Gender
  hobby = [Hobby]
  initals = Initials
  jot = [Jot]
  language= [Language]
  maiden_name = MaidenName
  mileage = Mileage
  nickname = NickName
  occupation = Occupation
  priority = Priority
  relation = [Relation]
  sensitivity = Sensitivity
  user_defined_field = [UserDefinedField]
  website = [Website]
  
  name = Name
  phone_number = [PhoneNumber]
  organization = Organization
  postal_address = [PostalAddress]
  email = [Email]
  im = [IM]
  structured_postal_address = [StructuredPostalAddress]
  extended_property = [ExtendedProperty]
  

class Deleted(atom.core.XmlElement):
  _qname = gdata.GDATA_TEMPLATE % 'deleted'


class GroupMembershipInfo(atom.core.XmlElement):
  """
  Identifies the group to which the contact belongs or belonged.
  The group is referenced by its id.
  """

  _qname = CONTACTS_TEMPLATE % 'groupMembershipInfo'

  href = 'href'
  deleted = 'deleted'


class ContactEntry(PersonEntry):
  """A Google Contacts flavor of an Atom Entry."""

  deleted = Deleted
  group_membership_info = [GroupMembershipInfo]
  organization = Organization

  def GetPhotoLink(self):
    for a_link in self.link:
      if a_link.rel == PHOTO_LINK_REL:
        return a_link
    return None

  def GetPhotoEditLink(self):
    for a_link in self.link:
      if a_link.rel == PHOTO_EDIT_LINK_REL:
        return a_link
    return None

class ContactsFeed(gdata.data.GDFeed):
  entry = [ContactEntry]

class SystemGroup(atom.core.XmlElement):
    _qname = CONTACTS_TEMPLATE % 'systemGroup'
    id = 'id'

class GroupEntry(gdata.data.GDEntry):
  """Represents a contact group."""
  extended_property = [ExtendedProperty]
  system_group = SystemGroup


class GroupsFeed(gdata.data.GDFeed):
  """A Google contact groups feed flavor of an Atom Feed."""
  entry = [GroupEntry]


class ProfileEntry(PersonEntry):
  """A Google Profiles flavor of an Atom Entry."""


def ProfileEntryFromString(xml_string):
  """Converts an XML string into a ProfileEntry object.

  Args:
    xml_string: string The XML describing a Profile entry.

  Returns:
    A ProfileEntry object corresponding to the given XML.
  """
  return atom.core.parse(ProfileEntry, xml_string)


class ProfilesFeed(gdata.data.GDFeed):
  """A Google Profiles feed flavor of an Atom Feed."""
  _qname = atom.data.ATOM_TEMPLATE % 'feed'
  entry = [ProfileEntry]

def ProfilesFeedFromString(xml_string):
  """Converts an XML string into a ProfilesFeed object.

  Args:
    xml_string: string The XML describing a Profiles feed.

  Returns:
    A ProfilesFeed object corresponding to the given XML.
  """
  return atom.core.parse(ProfilesFeed, xml_string)


