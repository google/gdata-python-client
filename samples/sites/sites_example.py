#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.
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


__author__ = 'e.bidelman (Eric Bidelman)'

import getopt
import mimetypes
import os.path
import sys

import gdata.sample_util
import gdata.sites.client
import gdata.sites.data


SOURCE_APP_NAME = 'googleInc-GoogleSitesAPIPythonLibSample-v1.1'
MAIN_MENU = ['1)  List site content',
             '2)  List recent activity',
             '3)  List revision history',
             '4)  Create webpage',
             '5)  Create web attachment',
             '6)  Upload attachment',
             '7)  Download attachment',
             '8)  Delete item',
             '9)  List sites',
             '10)  Create a new site',
             "11) List site's sharing permissions",
             '12) Change settings',
             '13) Exit']
SETTINGS_MENU = ['1) Change current site.',
                 '2) Change domain.']


class SitesExample(object):
  """Wrapper around the Sites API functionality."""

  def __init__(self, site_name=None, site_domain=None, ssl=False, debug=False):
    if site_domain is None:
      site_domain = self.PromptDomain()

    if site_name is None:
      site_name = self.PromptSiteName()

    mimetypes.init()

    self.client = gdata.sites.client.SitesClient(
        source=SOURCE_APP_NAME, site=site_name, domain=site_domain)
    self.client.http_client.debug = debug
    self.client.ssl = ssl

    try:
      gdata.sample_util.authorize_client(
          self.client, service=self.client.auth_service, source=SOURCE_APP_NAME,
          scopes=['http://sites.google.com/feeds/',
                  'https://sites.google.com/feeds/'])
    except gdata.client.BadAuthentication:
      exit('Invalid user credentials given.')
    except gdata.client.Error:
      exit('Login Error')

  def PrintMainMenu(self):
    """Displays a menu of options for the user to choose from."""
    print '\nSites API Sample'
    print '================================'
    print '\n'.join(MAIN_MENU)
    print '================================\n'

  def PrintSettingsMenu(self):
    """Displays a menu of settings for the user change."""
    print '\nSites API Sample > Settings'
    print '================================'
    print '\n'.join(SETTINGS_MENU)
    print '================================\n'

  def GetMenuChoice(self, menu):
    """Retrieves the menu selection from the user.

    Args:
      menu: list The menu to get a selection from.

    Returns:
      The integer of the menu item chosen by the user.
    """
    max_choice = len(menu)
    while True:
      user_input = raw_input(': ')

      try:
        num = int(user_input)
      except ValueError:
        continue

      if num <= max_choice and num > 0:
        return num

  def PromptSiteName(self):
    site_name = ''
    while not site_name:
      site_name = raw_input('site name: ')
      if not site_name:
        print 'Please enter the name of your Google Site.'
    return site_name

  def PromptDomain(self):
    return raw_input(('If your Site is hosted on a Google Apps domain, '
                      'enter it (e.g. example.com): ')) or 'site'

  def GetChoiceSelection(self, feed, message):
    for i, entry in enumerate(feed.entry):
      print '%d.) %s' % (i + 1, entry.title.text)
    choice = 0
    while not choice or not 0 <= choice <= len(feed.entry):
      choice = int(raw_input(message))
    print
    return choice

  def PrintEntry(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    if entry.page_name:
      print ' page name:\t%s' % entry.page_name.text
    if entry.content:
      print ' content\t%s...' % str(entry.content.html)[0:100]

  def PrintListItem(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    for col in entry.field:
      print ' %s %s\t%s' % (col.index, col.name, col.text)

  def PrintListPage(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    for col in entry.data.column:
      print ' %s %s' % (col.index, col.name)

  def PrintFileCabinetPage(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    print ' page name:\t%s' % entry.page_name.text
    print ' content\t%s...' % str(entry.content.html)[0:100]

  def PrintAttachment(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    if entry.summary is not None:
      print ' description:\t%s' % entry.summary.text
    print ' content\t%s, %s' % (entry.content.type, entry.content.src)

  def PrintWebAttachment(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    if entry.summary.text is not None:
      print ' description:\t%s' % entry.summary.text
    print ' content src\t%s' % entry.content.src

  def Run(self):
    """Executes the demo application."""

    try:
      while True:
        self.PrintMainMenu()
        choice = self.GetMenuChoice(MAIN_MENU)

        if choice == 1:
          kind_choice = raw_input('What kind (all|%s)?: ' % '|'.join(
              gdata.sites.data.SUPPORT_KINDS))
          if kind_choice in gdata.sites.data.SUPPORT_KINDS:
            uri = '%s?kind=%s' % (self.client.make_content_feed_uri(),
                                  kind_choice)
            feed = self.client.GetContentFeed(uri=uri)
          else:
            feed = self.client.GetContentFeed()

          print "\nFetching content feed of '%s'...\n" % self.client.site

          for entry in feed.entry:
            kind = entry.Kind()

            if kind == 'attachment':
              self.PrintAttachment(entry)
            elif kind == 'webattachment':
              self.PrintWebAttachment(entry)
            elif kind == 'filecabinet':
              self.PrintFileCabinetPage(entry)
            elif kind == 'listitem':
              self.PrintListItem(entry)
            elif kind == 'listpage':
              self.PrintListPage(entry)
            else:
              self.PrintEntry(entry)

            print ' revision:\t%s' % entry.revision.text
            print ' updated:\t%s' % entry.updated.text

            parent_link = entry.FindParentLink()
            if parent_link:
              print ' parent link:\t%s' % parent_link

            if entry.GetAlternateLink():
              print ' view in Sites:\t%s' % entry.GetAlternateLink().href

            if entry.feed_link:
              print ' feed of items:\t%s' % entry.feed_link.href

            if entry.IsDeleted():
              print ' deleted:\t%s' % entry.IsDeleted()

            if entry.in_reply_to:
              print ' in reply to:\t%s' % entry.in_reply_to.href

            print

        elif choice == 2:
          print "\nFetching activity feed of '%s'..." % self.client.site
          feed = self.client.GetActivityFeed()
          for entry in feed.entry:
            print '  %s [%s on %s]' % (entry.title.text, entry.Kind(),
                                       entry.updated.text)

        elif choice == 3:
          print "\nFetching content feed of '%s'...\n" % self.client.site

          feed = self.client.GetContentFeed()
          try:
            selection = self.GetChoiceSelection(
                feed, 'Select a page to fetch revisions for: ')
          except TypeError:
            continue
          except ValueError:
            continue

          feed = self.client.GetRevisionFeed(
              feed.entry[selection - 1].GetNodeId())
          for entry in feed.entry:
            print entry.title.text
            print '  new version on:\t%s' % entry.updated.text
            print '  view changes:\t%s' % entry.GetAlternateLink().href
            print '  current version:\t%s...' % str(entry.content.html)[0:100]
            print

        elif choice == 4:
          print "\nFetching content feed of '%s'...\n" % self.client.site

          feed = self.client.GetContentFeed()
          try:
            selection = self.GetChoiceSelection(
                feed, 'Select a parent to upload to (or hit ENTER for none): ')
          except ValueError:
            selection = None

          page_title = raw_input('Enter a page title: ')

          parent = None
          if selection is not None:
            parent = feed.entry[selection - 1]

          new_entry = self.client.CreatePage(
              'webpage', page_title, '<b>Your html content</b>',
              parent=parent)
          if new_entry.GetAlternateLink():
            print 'Created. View it at: %s' % new_entry.GetAlternateLink().href

        elif choice == 5:
          print "\nFetching filecabinets on '%s'...\n" % self.client.site

          uri = '%s?kind=%s' % (self.client.make_content_feed_uri(),
                                'filecabinet')
          feed = self.client.GetContentFeed(uri=uri)

          selection = self.GetChoiceSelection(
              feed, 'Select a filecabinet to create the web attachment on: ')

          url = raw_input('Enter the URL of the attachment: ')
          content_type = raw_input("Enter the attachment's mime type: ")
          title = raw_input('Enter a title for the web attachment: ')
          description = raw_input('Enter a description: ')

          parent_entry = None
          if selection is not None:
            parent_entry = feed.entry[selection - 1]

          self.client.CreateWebAttachment(url, content_type, title,
                                          parent_entry, description=description)
          print 'Created!'

        elif choice == 6:
          print "\nFetching filecainets on '%s'...\n" % self.client.site

          uri = '%s?kind=%s' % (self.client.make_content_feed_uri(),
                                'filecabinet')
          feed = self.client.GetContentFeed(uri=uri)

          selection = self.GetChoiceSelection(
              feed, 'Select a filecabinet to upload to: ')

          filepath = raw_input('Enter a filename: ')
          page_title = raw_input('Enter a title for the file: ')
          description = raw_input('Enter a description: ')

          filename = os.path.basename(filepath)
          file_ex = filename[filename.rfind('.'):]
          if not file_ex in mimetypes.types_map:
            content_type = raw_input(
                'Unrecognized file extension. Please enter the mime type: ')
          else:
            content_type = mimetypes.types_map[file_ex]

          entry = None
          if selection is not None:
            entry = feed.entry[selection - 1]

          new_entry = self.client.UploadAttachment(
              filepath, entry, content_type=content_type, title=page_title,
              description=description)
          print 'Uploaded. View it at: %s' % new_entry.GetAlternateLink().href

        elif choice == 7:
          print "\nFetching all attachments on '%s'...\n" % self.client.site

          uri = '%s?kind=%s' % (self.client.make_content_feed_uri(),
                                'attachment')
          feed = self.client.GetContentFeed(uri=uri)

          selection = self.GetChoiceSelection(
              feed, 'Select an attachment to download: ')

          filepath = raw_input('Save as: ')

          entry = None
          if selection is not None:
            entry = feed.entry[selection - 1]

          self.client.DownloadAttachment(entry, filepath)
          print 'Downloaded.'

        elif choice == 8:
          print "\nFetching content feed of '%s'...\n" % self.client.site

          feed = self.client.GetContentFeed()
          selection = self.GetChoiceSelection(feed, 'Select a page to delete: ')

          entry = None
          if selection is not None:
            entry = feed.entry[selection - 1]

          self.client.Delete(entry)
          print 'Removed!'

        elif choice == 9:
          print ('\nFetching your list of sites for domain: %s...\n'
                 % self.client.domain)

          feed = self.client.GetSiteFeed()
          for entry in feed.entry:
            print entry.title.text
            print '  site name: ' + entry.site_name.text
            if entry.summary.text:
              print '  summary: ' + entry.summary.text
            if entry.FindSourceLink():
              print '  copied from site: ' + entry.FindSourceLink()
            print '  acl feed: %s\n' % entry.FindAclLink()

        elif choice == 10:
          title = raw_input('Enter a title: ')
          summary = raw_input('Enter a description: ')
          theme = raw_input('Theme name (ex. "default"): ')

          new_entry = self.client.CreateSite(
              title, description=summary, theme=theme)
          print 'Site created! View it at: ' + new_entry.GetAlternateLink().href

        elif choice == 11:
          print "\nFetching acl permissions of '%s'...\n" % self.client.site

          feed = self.client.GetAclFeed()
          for entry in feed.entry:
            print '%s (%s) - %s' % (entry.scope.value, entry.scope.type,
                                    entry.role.value)

        elif choice == 12:
          self.PrintSettingsMenu()
          settings_choice = self.GetMenuChoice(SETTINGS_MENU)

          if settings_choice == 1:
            self.client.site = self.PromptSiteName()
          elif settings_choice == 2:
            self.client.domain = self.PromptDomain()

        elif choice == 13:
          print 'Later!\n'
          return

    except gdata.client.RequestError, error:
      print error
    except KeyboardInterrupt:
      return


def main():
  """The main function runs the SitesExample application."""

  print 'NOTE: Please run these tests only with a test account.\n'

  try:
    opts, args = getopt.getopt(sys.argv[1:], '',
                               ['site=', 'domain=', 'ssl', 'debug'])
  except getopt.error, msg:
    print """python sites_sample.py --site [sitename]
                                    --domain [domain or "site"]
                                    --ssl [enables https if set]
                                    --debug [prints debug info if set]"""
    sys.exit(2)

  site = None
  domain = None
  debug = False
  ssl = False

  for option, arg in opts:
    if option == '--site':
      site = arg
    elif option == '--domain':
      domain = arg
    elif option == '--ssl':
      ssl = True
    elif option == '--debug':
      debug = True

  sample = SitesExample(site, domain, ssl=ssl, debug=debug)
  sample.Run()


if __name__ == '__main__':
  main()
