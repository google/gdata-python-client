#!/usr/bin/python
#
# Copyright (C) 2007 SIOS Technology, Inc.
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

"""Contains objects used with Google Apps."""

__author__ = 'tmatsuo@sios.com (Takashi MATSUO)'

try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import atom
import gdata

# XML namespaces which are often used in Google Apps entity.
APPS_NAMESPACE = 'http://schemas.google.com/apps/2006'
APPS_TEMPLATE = '{http://schemas.google.com/apps/2006}%s'

class NicknameEntry(gdata.GDataEntry):
  """A Google Apps flavor of an Atom Entry for Nickname"""

  def __init__(self, author=None, category=None, content=None,
               atom_id=None, link=None, published=None, 
               title=None, updated=None,
               login=None, nickname=None,
               extended_property=None, 
               extension_elements=None, extension_attributes=None, text=None):

    gdata.GDataEntry.__init__(self, author=author, category=category, 
                              content=content,
                              atom_id=atom_id, link=link, published=published,
                              title=title, updated=updated)
    self.login = login
    self.nickname = nickname
    self.extended_property = extended_property or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.login:
      self.login._BecomeChildElement(element_tree)
    if self.nickname:
      self.nickname._BecomeChildElement(element_tree)
    gdata.GDataEntry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (APPS_NAMESPACE, 'login'):
      self.login = _LoginFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (APPS_NAMESPACE, 'nickname'):
      self.nickname = _NicknameFromElementTree(child)
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

def NicknameEntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _NicknameEntryFromElementTree(element_tree)

_NicknameEntryFromElementTree = atom._AtomInstanceFromElementTree(
  NicknameEntry, 'entry', atom.ATOM_NAMESPACE)

class NicknameFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Apps Nickname feed flavor of an Atom Feed"""

  def __init__(self, author=None, category=None, contributor=None,
               generator=None, icon=None, atom_id=None, link=None, logo=None, 
               rights=None, subtitle=None, title=None, updated=None,
               entry=None, total_results=None, start_index=None,
               items_per_page=None, extension_elements=None,
               extension_attributes=None, text=None):
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
      self.entry.append(_NicknameEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

def NicknameFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _NicknameFeedFromElementTree(element_tree)

_NicknameFeedFromElementTree = atom._AtomInstanceFromElementTree(
    NicknameFeed, 'feed', atom.ATOM_NAMESPACE)

class UserEntry(gdata.GDataEntry):
  """A Google Apps flavor of an Atom Entry"""

  def __init__(self, author=None, category=None, content=None,
               atom_id=None, link=None, published=None, 
               title=None, updated=None,
               login=None, name=None, quota=None, who=None, feed_link=None,
               extended_property=None, 
               extension_elements=None, extension_attributes=None, text=None):

    gdata.GDataEntry.__init__(self, author=author, category=category, 
                              content=content,
                              atom_id=atom_id, link=link, published=published,
                              title=title, updated=updated)
    self.login = login
    self.name = name
    self.quota = quota
    self.who = who
    self.feed_link = feed_link or []
    self.extended_property = extended_property or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.login:
      self.login._BecomeChildElement(element_tree)
    if self.name:
      self.name._BecomeChildElement(element_tree)
    if self.quota:
      self.quota._BecomeChildElement(element_tree)
    if self.who:
      self.who._BecomeChildElement(element_tree)
    for a_feed_link in self.feed_link:
      a_feed_link._BecomeChildElement(element_tree)
    gdata.GDataEntry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (APPS_NAMESPACE, 'login'):
      self.login = _LoginFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (APPS_NAMESPACE, 'name'):
      self.name = _NameFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (APPS_NAMESPACE, 'quota'):
      self.quota = _QuotaFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'feedLink'):
      self.feed_link.append(gdata._FeedLinkFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'who'):
      self.who = _WhoFromElementTree(child)
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

def UserEntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _UserEntryFromElementTree(element_tree)

_UserEntryFromElementTree = atom._AtomInstanceFromElementTree(
  UserEntry, 'entry', atom.ATOM_NAMESPACE)

class UserFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Apps User feed flavor of an Atom Feed"""

  def __init__(self, author=None, category=None, contributor=None,
               generator=None, icon=None, atom_id=None, link=None, logo=None, 
               rights=None, subtitle=None, title=None, updated=None,
               entry=None, total_results=None, start_index=None,
               items_per_page=None, extension_elements=None,
               extension_attributes=None, text=None):
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
      self.entry.append(_UserEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

def UserFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _UserFeedFromElementTree(element_tree)

_UserFeedFromElementTree = atom._AtomInstanceFromElementTree(
    UserFeed, 'feed', atom.ATOM_NAMESPACE)

class EmailListEntry(gdata.GDataEntry):
  """A Google Apps EmailList flavor of an Atom Entry"""

  def __init__(self, author=None, category=None, content=None,
               atom_id=None, link=None, published=None, 
               title=None, updated=None,
               email_list=None, feed_link=None,
               extended_property=None, 
               extension_elements=None, extension_attributes=None, text=None):

    gdata.GDataEntry.__init__(self, author=author, category=category, 
                              content=content,
                              atom_id=atom_id, link=link, published=published,
                              title=title, updated=updated)
    self.email_list = email_list
    self.feed_link = feed_link or []
    self.extended_property = extended_property or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.email_list:
      self.email_list._BecomeChildElement(element_tree)
    for a_feed_link in self.feed_link:
      a_feed_link._BecomeChildElement(element_tree)
    gdata.GDataEntry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (APPS_NAMESPACE, 'emailList'):
      self.email_list = _EmailListFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'feedLink'):
      self.feed_link.append(gdata._FeedLinkFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

def EmailListEntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _EmailListEntryFromElementTree(element_tree)

_EmailListEntryFromElementTree = atom._AtomInstanceFromElementTree(
  EmailListEntry, 'entry', atom.ATOM_NAMESPACE)

class EmailListFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Apps EmailList feed flavor of an Atom Feed"""

  def __init__(self, author=None, category=None, contributor=None,
               generator=None, icon=None, atom_id=None, link=None, logo=None, 
               rights=None, subtitle=None, title=None, updated=None,
               entry=None, total_results=None, start_index=None,
               items_per_page=None, extension_elements=None,
               extension_attributes=None, text=None):
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
      self.entry.append(_EmailListEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

def EmailListFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _EmailListFeedFromElementTree(element_tree)

_EmailListFeedFromElementTree = atom._AtomInstanceFromElementTree(
    EmailListFeed, 'feed', atom.ATOM_NAMESPACE)

class EmailListRecipientEntry(gdata.GDataEntry):
  """A Google Apps EmailListRecipient flavor of an Atom Entry"""

  def __init__(self, author=None, category=None, content=None,
               atom_id=None, link=None, published=None, 
               title=None, updated=None,
               who=None,
               extended_property=None, 
               extension_elements=None, extension_attributes=None, text=None):

    gdata.GDataEntry.__init__(self, author=author, category=category, 
                              content=content,
                              atom_id=atom_id, link=link, published=published,
                              title=title, updated=updated)
    self.who = who
    self.extended_property = extended_property or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.who:
      self.who._BecomeChildElement(element_tree)
    gdata.GDataEntry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (gdata.GDATA_NAMESPACE, 'who'):
      self.who = _WhoFromElementTree(child)
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

def EmailListRecipientEntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _EmailListRecipientEntryFromElementTree(element_tree)

_EmailListRecipientEntryFromElementTree = atom._AtomInstanceFromElementTree(
  EmailListRecipientEntry, 'entry', atom.ATOM_NAMESPACE)

class EmailListRecipientFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Apps EmailListRecipient feed flavor of an Atom Feed"""

  def __init__(self, author=None, category=None, contributor=None,
               generator=None, icon=None, atom_id=None, link=None, logo=None, 
               rights=None, subtitle=None, title=None, updated=None,
               entry=None, total_results=None, start_index=None,
               items_per_page=None, extension_elements=None,
               extension_attributes=None, text=None):
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
      self.entry.append(_EmailListRecipientEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

def EmailListRecipientFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _EmailListRecipientFeedFromElementTree(element_tree)

_EmailListRecipientFeedFromElementTree = atom._AtomInstanceFromElementTree(
    EmailListRecipientFeed, 'feed', atom.ATOM_NAMESPACE)

class EmailList(atom.AtomBase):
  """The Google Apps EmailList element"""

  def __init__(self, name=None, extension_elements=None,
               extension_attributes=None, text=None):
    self.name = name
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.name:
      element_tree.attrib['name'] = self.name
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = APPS_TEMPLATE % 'emailList'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'name':
      self.name = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
                                                  element_tree)

_EmailListFromElementTree = atom._AtomInstanceFromElementTree(
    EmailList, 'emailList', APPS_NAMESPACE)

class Who(atom.AtomBase):
  """The Google Apps Who element"""

  def __init__(self, rel=None, email=None, extension_elements=None,
               extension_attributes=None, text=None):
    self.rel = rel
    self.email = email
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.email:
      element_tree.attrib['email'] = self.email
    if self.rel:
      element_tree.attrib['rel'] = self.rel
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = gdata.GDATA_TEMPLATE % 'who'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'rel':
      self.rel = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'email':
      self.email = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
                                                  element_tree)

_WhoFromElementTree = atom._AtomInstanceFromElementTree(
    Who, 'who', gdata.GDATA_NAMESPACE)

class Login(atom.AtomBase):
  """The Google Apps Login element"""

  def __init__(self, user_name=None, password=None, suspended=None,
               ip_whitelisted=None, extension_elements=None,
               extension_attributes=None, text=None):
    self.user_name = user_name
    self.password = password
    self.suspended = suspended
    self.ip_whitelisted = ip_whitelisted
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.user_name:
      element_tree.attrib['userName'] = self.user_name
    if self.password:
      element_tree.attrib['password'] = self.password
    if self.suspended:
      element_tree.attrib['suspended'] = self.suspended
    if self.ip_whitelisted:
      element_tree.attrib['ipWhitelisted'] = self.ip_whitelisted
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = APPS_TEMPLATE % 'login'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'userName':
      self.user_name = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'password':
      self.password = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'suspended':
      self.suspended = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'ipWhitelisted':
      self.ip_whitelisted = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
                                                  element_tree)

_LoginFromElementTree = atom._AtomInstanceFromElementTree(
    Login, 'login', APPS_NAMESPACE)

class Quota(atom.AtomBase):
  """The Google Apps Quota element"""

  def __init__(self, limit=None, extension_elements=None,
               extension_attributes=None, text=None):
    self.limit = limit
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.limit:
      element_tree.attrib['limit'] = self.limit
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = APPS_TEMPLATE % 'quota'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'limit':
      self.limit = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
                                                  element_tree)
_QuotaFromElementTree = atom._AtomInstanceFromElementTree(
    Quota, 'quota', APPS_NAMESPACE)

class Name(atom.AtomBase):
  """The Google Apps Name element"""

  def __init__(self, family_name=None, given_name=None,
               extension_elements=None, extension_attributes=None, text=None):
    self.family_name = family_name
    self.given_name = given_name
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.family_name:
      element_tree.attrib['familyName'] = self.family_name
    if self.given_name:
      element_tree.attrib['givenName'] = self.given_name
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = APPS_TEMPLATE % 'name'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'familyName':
      self.family_name = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'givenName':
      self.given_name = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
                                                  element_tree)

_NameFromElementTree = atom._AtomInstanceFromElementTree(
    Name, 'name', APPS_NAMESPACE)

class Nickname(atom.AtomBase):
  """The Google Apps Nickname element"""

  def __init__(self, name=None,
               extension_elements=None, extension_attributes=None, text=None):
    self.name = name
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.name:
      element_tree.attrib['name'] = self.name
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = APPS_TEMPLATE % 'nickname'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'name':
      self.name = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
                                                  element_tree)

_NicknameFromElementTree = atom._AtomInstanceFromElementTree(
    Nickname, 'nickname', APPS_NAMESPACE)
