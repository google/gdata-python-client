#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""A sample app for Google Apps Email Settings features.

  EmailSettingsSample: demonstrates getting and setting/updating email settings
"""

__author__ = 'Prashant Tiwari <pti@google.com>'

from gdata.apps.emailsettings.client import EmailSettingsClient
from optparse import OptionParser

#defaults for sendAs alias settings
SEND_AS_NAME = 'test-alias'
#update SEND_AS_ADDRESS to a valid account on your domain
SEND_AS_ADDRESS = 'johndoe@domain.com'
SEND_AS_REPLY_TO = 'replyto@example.com'
SEND_AS_MAKE_DEFAULT = False

#defaults for label settings
LABEL_NAME = 'label'

#defaults for forwarding settings
#update FORWARD_TO to a valid account on your domain
FORWARD_TO = 'account@domain.com'
FORWARDING_ACTION = 'ARCHIVE'

#defaults for pop settings
POP_ENABLE_FOR = 'MAIL_FROM_NOW_ON'
POP_ACTION = 'ARCHIVE'

#defaults for signature settings
SIGNATURE = "<Insert witty signature here>"

#defaults for vacation settings
VACATION_SUBJECT = "On vacation"
VACATION_MESSAGE = "I'm on vacation, will respond when I return."
VACATION_CONTACTS_ONLY = True

#defaults for filter settings
FILTER_FROM = 'me@domain.com'
FILTER_TO = 'you@domain.com'
FILTER_SUBJECT = 'subject'
FILTER_HAS_THE_WORD = 'has'
FILTER_DOES_NOT_HAVE_THE_WORD = 'no'
FILTER_HAS_ATTACHMENT = True
FILTER_SHOULD_MARK_AS_READ = True
FILTER_SHOULD_ARCHIVE = True
FILTER_LABEL = 'label'

#defaults for general settings
GENERAL_PAGE_SIZE = '50'
GENERAL_ENABLE_SHORTCUTS = True
GENERAL_ENABLE_ARROWS = True
GENERAL_ENABLE_SNIPPETS = True
GENERAL_ENABLE_UNICODE = True

#defaults for language settings
LANGUAGE = 'en-US'

parser = None
options = None

class EmailSettingsSample(object):
  """EmailsSettingsSample object demos the Email Settings API."""
  
  def __init__(self, domain, email, password, app):
    """Constructor for the EmailSettingsSample object.

    Takes an email, password and an app id corresponding to a google apps admin
    account to demo the Email Settings API.

    Args:
      domain: [string] The domain name (e.g. domain.com)
      email: [string] The e-mail address of a domain admin account.
      password: [string] The domain admin's password.
      app: [string] The app name of the form 
          companyName-applicationName-versionID
    """
    self.client = EmailSettingsClient(domain=domain)
    self.client.ClientLogin(email=email, password=password,
                            source=app)
    
  def run(self, username, setting, method):
    """Method that invokes the EmailSettingsClient services
    
    Args:
      username: [string] The name of the account for whom to get/set settings
      setting: [string] The email setting to be got/set/updated
      method: [string] Specifies the get or set method
    """
    if setting == 'label':
      if method == 'get':
        print "getting labels for %s...\n" % (username)
        print self.client.RetrieveLabels(username=username)
      else:
        print "creating label for %s...\n" % (username)
        print self.client.CreateLabel(username=username, name=LABEL_NAME)
    elif setting == 'forwarding':
      if method == 'get':
        print "getting forwarding for %s...\n" % (username)
        print self.client.RetrieveForwarding(username)
      else:
        print "updating forwarding settings for %s...\n" % (username)
        print self.client.UpdateForwarding(username=username, 
                                           enable=not(options.disable),
                                           forward_to=FORWARD_TO,
                                           action=FORWARDING_ACTION)
    elif setting == 'sendas':
      if method == 'get':
        print "getting sendAs alias for %s...\n" % (username)
        print self.client.RetrieveSendAs(username=username)
      else:
        print "creating sendAs alias for %s...\n" % (username)
        print self.client.CreateSendAs(username=username, name=SEND_AS_NAME, 
                                       address=SEND_AS_ADDRESS,
                                       reply_to=SEND_AS_REPLY_TO, 
                                       make_default=SEND_AS_MAKE_DEFAULT)
    elif setting == 'pop':
      if method == 'get':
        print "getting pop settings for %s...\n" % (username)
        print self.client.RetrievePop(username=username)
      else:
        print "updating pop settings for %s...\n" % (username)
        print self.client.UpdatePop(username=username, 
                                    enable=not(options.disable), 
                                    enable_for=POP_ENABLE_FOR,
                                    action=POP_ACTION)
    elif setting == 'signature':
      if method == 'get':
        print "getting signature for %s...\n" % (username)
        print self.client.RetrieveSignature(username=username)
      else:
        print "updating signature for %s...\n" % (username)
        print self.client.UpdateSignature(username=username, 
                                          signature=SIGNATURE)
    elif setting == 'vacation':
      if method == 'get':
        print "getting vacation settings for %s...\n" % (username)
        print self.client.RetrieveVacation(username=username)
      else:
        print "updating vacation settings for %s...\n" % (username)
        print self.client.UpdateVacation(username=username, 
                                         enable=not(options.disable),
                                         subject=VACATION_SUBJECT, 
                                         message=VACATION_MESSAGE,
                                         contacts_only=VACATION_CONTACTS_ONLY)
    elif setting == 'imap':
      if method == 'get':
        print "getting imap settings for %s...\n" % (username)
        print self.client.RetrieveImap(username)
      else:
        print "updating imap settings for %s...\n" % (username)
        print self.client.UpdateImap(username=username, 
                                     enable=not(options.disable))
    elif setting == 'filter':
      if method == 'get':
        print "getting email filters is not yet possible\n"
        parser.print_help()
      else:
        print "creating an email filter for %s...\n" % (username)
        print self.client.CreateFilter(username=username, 
                                       from_address=FILTER_FROM, 
                                       to_address=FILTER_TO,
                                       subject=FILTER_SUBJECT, 
                                       has_the_word=FILTER_HAS_THE_WORD,
                                       does_not_have_the_word=
                                          FILTER_DOES_NOT_HAVE_THE_WORD,
                                       has_attachments=FILTER_HAS_ATTACHMENT, 
                                       label=FILTER_LABEL,
                                       mark_as_read=FILTER_SHOULD_MARK_AS_READ,
                                       archive=FILTER_SHOULD_ARCHIVE)
    elif setting == 'general':
      if method == 'get':
        print "getting general email settings is not yet possible\n"
        parser.print_help()
      else:
        print "updating general settings for %s...\n" % (username)
        print self.client.UpdateGeneralSettings(username=username, 
                                                page_size=GENERAL_PAGE_SIZE,
                                                shortcuts=
                                                    GENERAL_ENABLE_SHORTCUTS,
                                                arrows=
                                                    GENERAL_ENABLE_ARROWS,
                                                snippets=
                                                    GENERAL_ENABLE_SNIPPETS,
                                                use_unicode=
                                                    GENERAL_ENABLE_UNICODE)
    elif setting == 'language':
      if method == 'get':
        print "getting language settings is not yet possible\n"
        parser.print_help()
      else:
        print "updating language for %s...\n" % (username)
        print self.client.UpdateLanguage(username=username, language=LANGUAGE)
    elif setting == 'webclip':
      if method == 'get':
        print "getting webclip settings is not yet possible\n"
        parser.print_help()
      else:
        print "updating webclip settings for %s...\n" % (username)
        print self.client.UpdateWebclip(username=username, 
                                        enable=not(options.disable))
    else:
      parser.print_help()

def main():
  """Demos the Email Settings API using the EmailSettingsSample object."""
  
  usage = 'usage: %prog [options]'
  global parser
  global options
  parser = OptionParser(usage=usage)
  parser.add_option('--domain',
                    help="The Google Apps domain, e.g. 'domain.com'.")
  parser.add_option('--email',
                    help="The admin's email account, e.g. 'admin@domain.com'.")
  parser.add_option('--password',
                    help="The admin's password.")
  parser.add_option('--app',
                    help="The name of the app.")
  parser.add_option('--username',
                    help="The user account on which to perform operations.")
  parser.add_option('--setting',
                    choices=['filter', 'label', 'forwarding', 'sendas', 'pop', 
                             'signature', 'vacation', 'imap', 'general', 
                             'language', 'webclip'],
                    help="The email setting to use. Choose from filter, label, \
                    forwarding, sendas, pop, signature, vacation, imap, \
                    general, language, webclip.")
  parser.add_option('--method',
                     default='get',
                     help="Specify whether to get or set/update a setting. \
                     Choose between get (default) and set.")
  parser.add_option('--disable',
                    action="store_true",
                    default=False,
                    dest="disable",
                    help="Disable a setting when using the set method with the\
                     --disable option. The default is to enable the setting.")
  (options, args) = parser.parse_args()
  
  if (options.domain == None or options.email == None or options.password == 
      None or options.username == None or options.app == None or 
      options.setting == None):
    parser.print_help()
    return
  
  sample = EmailSettingsSample(options.domain, options.email, options.password,
                               options.app)
  sample.run(options.username, options.setting, options.method)

if __name__ == '__main__':
  main()
