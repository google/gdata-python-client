#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


__author__ = 'Claudio Cherubino <ccherubino@google.com>'


import unittest
import gdata.client
import gdata.data
import gdata.gauth
import gdata.apps.emailsettings.client
import gdata.apps.emailsettings.data
import gdata.test_config as conf


conf.options.register_option(conf.APPS_DOMAIN_OPTION)
conf.options.register_option(conf.TARGET_USERNAME_OPTION)


class EmailSettingsClientTest(unittest.TestCase):

  def setUp(self):
    self.client = gdata.apps.emailsettings.client.EmailSettingsClient(
        domain='example.com')
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.apps.emailsettings.client.EmailSettingsClient(
          domain=conf.options.get_value('appsdomain'))
      if conf.options.get_value('ssl') == 'true':
        self.client.ssl = True
      conf.configure_client(self.client, 'EmailSettingsClientTest',
          self.client.auth_service, True)
      self.username = conf.options.get_value('appsusername').split('@')[0]

  def tearDown(self):
    conf.close_client(self.client)

  def testClientConfiguration(self):
    self.assertEqual('apps-apis.google.com', self.client.host)
    self.assertEqual('2.0', self.client.api_version)
    self.assertEqual('apps', self.client.auth_service)
    self.assertEqual(
        ('http://www.google.com/a/feeds/',
         'https://www.google.com/a/feeds/',
         'http://apps-apis.google.com/a/feeds/',
         'https://apps-apis.google.com/a/feeds/'), self.client.auth_scopes)
    if conf.options.get_value('runlive') == 'true':
      self.assertEqual(self.client.domain, conf.options.get_value('appsdomain'))
    else:
      self.assertEqual(self.client.domain, 'example.com')

  def testMakeEmailSettingsUri(self):
    self.assertEqual('/a/feeds/emailsettings/2.0/%s/%s/%s' % (self.client.domain,
        'abc', 'label'),
        self.client.MakeEmailSettingsUri('abc', 'label'))

  def testCreateLabel(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testCreateLabel')

    new_label = self.client.CreateLabel(
        username=conf.options.get_value('targetusername'),
        name='status updates')

    self.assert_(isinstance(new_label,
        gdata.apps.emailsettings.data.EmailSettingsLabel))
    self.assertEqual(new_label.name, 'status updates')

  def testCreateFilter(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testCreateFilter')

    new_filter = self.client.CreateFilter(
        username=conf.options.get_value('targetusername'),
        from_address='alice@gmail.com',
        has_the_word='project proposal', mark_as_read=True)

    self.assert_(isinstance(new_filter,
        gdata.apps.emailsettings.data.EmailSettingsFilter))
    self.assertEqual(new_filter.from_address, 'alice@gmail.com')
    self.assertEqual(new_filter.has_the_word, 'project proposal')
    self.assertEqual(new_filter.mark_as_read, 'True')

    new_filter = self.client.CreateFilter(
        username=conf.options.get_value('targetusername'),
        to_address='announcements@example.com',
        label="announcements")

    self.assert_(isinstance(new_filter,
        gdata.apps.emailsettings.data.EmailSettingsFilter))
    self.assertEqual(new_filter.to_address, 'announcements@example.com')
    self.assertEqual(new_filter.label, 'announcements')

    new_filter = self.client.CreateFilter(
        username=conf.options.get_value('targetusername'),
        subject='urgent',
        does_not_have_the_word='spam',
        has_attachments=True,
        archive=True)

    self.assert_(isinstance(new_filter,
        gdata.apps.emailsettings.data.EmailSettingsFilter))
    self.assertEqual(new_filter.subject, 'urgent')
    self.assertEqual(new_filter.does_not_have_the_word, 'spam')
    self.assertEqual(new_filter.has_attachments, 'True')
    self.assertEqual(new_filter.archive, 'True')

  def testCreateSendAs(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testCreateSendAs')

    new_sendas = self.client.CreateSendAs(
        username=conf.options.get_value('targetusername'),
        name='Sales', address=conf.options.get_value('appsusername'),
        reply_to='abc@gmail.com',
        make_default=True)

    self.assert_(isinstance(new_sendas,
        gdata.apps.emailsettings.data.EmailSettingsSendAsAlias))
    self.assertEqual(new_sendas.name, 'Sales')
    self.assertEqual(new_sendas.address,
        conf.options.get_value('appsusername'))
    self.assertEqual(new_sendas.reply_to, 'abc@gmail.com')
    self.assertEqual(new_sendas.make_default, 'True')

  def testUpdateWebclip(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUpdateWebclip')

    new_webclip = self.client.UpdateWebclip(
        username=conf.options.get_value('targetusername'),
        enable=True)

    self.assert_(isinstance(new_webclip,
        gdata.apps.emailsettings.data.EmailSettingsWebClip))
    self.assertEqual(new_webclip.enable, 'True')

    new_webclip = self.client.UpdateWebclip(
        username=conf.options.get_value('targetusername'),
        enable=False)

    self.assert_(isinstance(new_webclip,
        gdata.apps.emailsettings.data.EmailSettingsWebClip))
    self.assertEqual(new_webclip.enable, 'False')

  def testUpdateForwarding(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUpdateForwarding')

    new_forwarding = self.client.UpdateForwarding(
        username=conf.options.get_value('targetusername'),
        enable=True,
        forward_to=conf.options.get_value('appsusername'),
        action='KEEP')

    self.assert_(isinstance(new_forwarding,
        gdata.apps.emailsettings.data.EmailSettingsForwarding))
    self.assertEqual(new_forwarding.enable, 'True')
    self.assertEqual(new_forwarding.forward_to,
        conf.options.get_value('appsusername'))
    self.assertEqual(new_forwarding.action, 'KEEP')

    new_forwarding = self.client.UpdateForwarding(
        username=conf.options.get_value('targetusername'),
        enable=False)

    self.assert_(isinstance(new_forwarding,
        gdata.apps.emailsettings.data.EmailSettingsForwarding))
    self.assertEqual(new_forwarding.enable, 'False')

  def testUpdatePop(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUpdatePop')

    new_pop = self.client.UpdatePop(
        username=conf.options.get_value('targetusername'),
        enable=True, enable_for='MAIL_FROM_NOW_ON', action='KEEP')

    self.assert_(isinstance(new_pop,
        gdata.apps.emailsettings.data.EmailSettingsPop))
    self.assertEqual(new_pop.enable, 'True')
    self.assertEqual(new_pop.enable_for, 'MAIL_FROM_NOW_ON')
    self.assertEqual(new_pop.action, 'KEEP')

    new_pop = self.client.UpdatePop(
        username=conf.options.get_value('targetusername'),
        enable=False)

    self.assert_(isinstance(new_pop,
        gdata.apps.emailsettings.data.EmailSettingsPop))
    self.assertEqual(new_pop.enable, 'False')

  def testUpdateImap(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUpdateImap')

    new_imap = self.client.UpdateImap(
        username=conf.options.get_value('targetusername'),
        enable=True)

    self.assert_(isinstance(new_imap,
        gdata.apps.emailsettings.data.EmailSettingsImap))
    self.assertEqual(new_imap.enable, 'True')

    new_imap = self.client.UpdateImap(
        username=conf.options.get_value('targetusername'),
        enable=False)

    self.assert_(isinstance(new_imap,
        gdata.apps.emailsettings.data.EmailSettingsImap))
    self.assertEqual(new_imap.enable, 'False')

  def testUpdateVacation(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUpdateVacation')

    new_vacation = self.client.UpdateVacation(
        username=conf.options.get_value('targetusername'),
        enable=True, subject='Out of office',
        message='If urgent call me at 555-5555.',
        contacts_only=True)

    self.assert_(isinstance(new_vacation,
        gdata.apps.emailsettings.data.EmailSettingsVacationResponder))
    self.assertEqual(new_vacation.enable, 'True')
    self.assertEqual(new_vacation.subject, 'Out of office')
    self.assertEqual(new_vacation.message, 'If urgent call me at 555-5555.')
    self.assertEqual(new_vacation.contacts_only, 'True')

    new_vacation = self.client.UpdateVacation(
        username=conf.options.get_value('targetusername'),
        enable=False)

    self.assert_(isinstance(new_vacation,
        gdata.apps.emailsettings.data.EmailSettingsVacationResponder))
    self.assertEqual(new_vacation.enable, 'False')

  def testUpdateSignature(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUpdateSignature')

    new_signature = self.client.UpdateSignature(
        username=conf.options.get_value('targetusername'),
        signature='Regards, Joe')

    self.assert_(isinstance(new_signature,
        gdata.apps.emailsettings.data.EmailSettingsSignature))
    self.assertEqual(new_signature.signature_value, 'Regards, Joe')

    new_signature = self.client.UpdateSignature(
        username=conf.options.get_value('targetusername'),
        signature='')

    self.assert_(isinstance(new_signature,
        gdata.apps.emailsettings.data.EmailSettingsSignature))
    self.assertEqual(new_signature.signature_value, '')

  def testUpdateLanguage(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUpdateLanguage')

    new_language = self.client.UpdateLanguage(
        username=conf.options.get_value('targetusername'),
        language='es')

    self.assert_(isinstance(new_language,
        gdata.apps.emailsettings.data.EmailSettingsLanguage))
    self.assertEqual(new_language.language_tag, 'es')

  def testUpdateGeneral(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUpdateGeneral')

    new_general = self.client.UpdateGeneralSettings(
        username=conf.options.get_value('targetusername'),
        page_size=25, arrows=True)

    self.assert_(isinstance(new_general,
        gdata.apps.emailsettings.data.EmailSettingsGeneral))
    self.assertEqual(new_general.page_size, '25')
    self.assertEqual(new_general.arrows, 'True')

    new_general = self.client.UpdateGeneralSettings(
        username=conf.options.get_value('targetusername'),
        shortcuts=False, snippets=True, use_unicode=False)

    self.assert_(isinstance(new_general,
        gdata.apps.emailsettings.data.EmailSettingsGeneral))
    self.assertEqual(new_general.shortcuts, 'False')
    self.assertEqual(new_general.snippets, 'True')
    self.assertEqual(new_general.use_unicode, 'False')


def suite():
  return conf.build_suite([EmailSettingsClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
