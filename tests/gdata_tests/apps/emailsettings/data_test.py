#!/usr/bin/python
#
# Copyright (C) 2010 Google Inc.
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


__author__ = 'Claudio Cherubino <ccherubino@google.com>'


import unittest
import gdata.apps.emailsettings.data
import gdata.test_config as conf


class EmailSettingsLabelTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsLabel()

  def testName(self):
    self.entry.name = 'test label'
    self.assertEquals(self.entry.name, 'test label')


class EmailSettingsFilterTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsFilter()

  def testFrom(self):
    self.entry.from_address = 'abc@example.com'
    self.assertEquals(self.entry.from_address, 'abc@example.com')

  def testTo(self):
    self.entry.to_address = 'to@example.com'
    self.assertEquals(self.entry.to_address, 'to@example.com')

  def testFrom(self):
    self.entry.from_address = 'abc@example.com'
    self.assertEquals(self.entry.from_address, 'abc@example.com')

  def testSubject(self):
    self.entry.subject = 'Read me'
    self.assertEquals(self.entry.subject, 'Read me')

  def testHasTheWord(self):
    self.entry.has_the_word = 'important'
    self.assertEquals(self.entry.has_the_word, 'important')

  def testDoesNotHaveTheWord(self):
    self.entry.does_not_have_the_word = 'spam'
    self.assertEquals(self.entry.does_not_have_the_word, 'spam')

  def testHasAttachments(self):
    self.entry.has_attachments = True
    self.assertEquals(self.entry.has_attachments, True)

  def testLabel(self):
    self.entry.label = 'Trip reports'
    self.assertEquals(self.entry.label, 'Trip reports')

  def testMarkHasRead(self):
    self.entry.mark_has_read = True
    self.assertEquals(self.entry.mark_has_read, True)

  def testArchive(self):
    self.entry.archive = True
    self.assertEquals(self.entry.archive, True)


class EmailSettingsSendAsAliasTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsSendAsAlias()

  def testName(self):
    self.entry.name = 'Sales'
    self.assertEquals(self.entry.name, 'Sales')

  def testAddress(self):
    self.entry.address = 'sales@example.com'
    self.assertEquals(self.entry.address, 'sales@example.com')

  def testReplyTo(self):
    self.entry.reply_to = 'support@example.com'
    self.assertEquals(self.entry.reply_to, 'support@example.com')

  def testMakeDefault(self):
    self.entry.make_default = True
    self.assertEquals(self.entry.make_default, True)


class EmailSettingsWebClipTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsWebClip()

  def testEnable(self):
    self.entry.enable = True
    self.assertEquals(self.entry.enable, True)


class EmailSettingsForwardingTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsForwarding()

  def testEnable(self):
    self.entry.enable = True
    self.assertEquals(self.entry.enable, True)

  def testForwardTo(self):
    self.entry.forward_to = 'fred@example.com'
    self.assertEquals(self.entry.forward_to, 'fred@example.com')

  def testAction(self):
    self.entry.action = 'KEEP'
    self.assertEquals(self.entry.action, 'KEEP')


class EmailSettingsPopTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsPop()

  def testEnable(self):
    self.entry.enable = True
    self.assertEquals(self.entry.enable, True)

  def testForwardTo(self):
    self.entry.enable_for = 'ALL_MAIL'
    self.assertEquals(self.entry.enable_for, 'ALL_MAIL')

  def testAction(self):
    self.entry.action = 'KEEP'
    self.assertEquals(self.entry.action, 'KEEP')


class EmailSettingsImapTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsImap()

  def testEnable(self):
    self.entry.enable = True
    self.assertEquals(self.entry.enable, True)


class EmailSettingsVacationResponderTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsVacationResponder()

  def testEnable(self):
    self.entry.enable = True
    self.assertEquals(self.entry.enable, True)

  def testSubject(self):
    self.entry.subject = 'On vacation!'
    self.assertEquals(self.entry.subject, 'On vacation!')

  def testMessage(self):
    self.entry.message = 'See you on September 1st'
    self.assertEquals(self.entry.message, 'See you on September 1st')

  def testContactsOnly(self):
    self.entry.contacts_only = True
    self.assertEquals(self.entry.contacts_only, True)


class EmailSettingsSignatureTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsSignature()

  def testValue(self):
    self.entry.signature_value = 'Regards, Joe'
    self.assertEquals(self.entry.signature_value, 'Regards, Joe')


class EmailSettingsLanguageTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsLanguage()

  def testLanguage(self):
    self.entry.language_tag = 'es'
    self.assertEquals(self.entry.language_tag, 'es')


class EmailSettingsGeneralTest(unittest.TestCase):

  def setUp(self):
    self.entry = gdata.apps.emailsettings.data.EmailSettingsGeneral()

  def testPageSize(self):
    self.entry.page_size = 25
    self.assertEquals(self.entry.page_size, 25)

  def testShortcuts(self):
    self.entry.shortcuts = True
    self.assertEquals(self.entry.shortcuts, True)

  def testArrows(self):
    self.entry.arrows = True
    self.assertEquals(self.entry.arrows, True)

  def testSnippets(self):
    self.entry.snippets = True
    self.assertEquals(self.entry.snippets, True)

  def testUnicode(self):
    self.entry.use_unicode = True
    self.assertEquals(self.entry.use_unicode, True)


def suite():
  return conf.build_suite([EmailSettingsLabelTest, EmailSettingsFilterTest,
      EmailSettingsSendAsAliasTest, EmailSettingsWebClipTest,
      EmailSettingsForwardingTest, EmailSettingsPopTest,
      EmailSettingsImapTest, EmailSettingsVacationResponderTest,
      EmailSettingsSignatureTest, EmailSettingsLanguageTest,
      EmailSettingsGeneralTest])


if __name__ == '__main__':
  unittest.main()
