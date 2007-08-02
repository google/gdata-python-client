#!/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
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


__author__ = 'api.jfisher (Jeff Fisher)'


import sys
import re
import os.path
import getopt
import getpass
import gdata.docs.service


class DocsSample(object):

  def __init__(self, email, password):
    """Takes an email and password corresponding to a gmail account to
    demonstrate the functionality of the Document List feed."""

    self.gd_client = gdata.docs.service.DocsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'Document List Python Sample'
    self.gd_client.ProgrammaticLogin()

  def _PrintFeed(self, feed):
    """Prints out the contents of a feed to the console."""

    print '\n'
    if not len(feed.entry):
      print 'No entries in feed.\n'
    for i, entry in enumerate(feed.entry):
      print '%s %s\n' % (i+1, entry.title.text.encode('UTF-8'))

  def _GetFileExtension(self, file_name):
    """Returns the three letter file extension for a file in upper case
    characters."""

    match = re.search('.*\.([a-zA-Z]{3}$)',file_name)
    if match:
      return match.group(1).upper()
    else:
      return False

  def _UploadMenu(self):
    """Prompts that enable a user to upload a file to the Document List feed."""

    file_path = ''
    file_path = raw_input('Enter path to file: ')

    if file_path == '':
      return
    elif not os.path.isfile(file_path):
      print 'Not a valid file.'
      return
    
    file_name = os.path.basename(file_path)
    ext = self._GetFileExtension(file_name)

    if not ext or ext not in gdata.docs.service.SUPPORTED_FILETYPES:
      print 'File type not supported. Check the file extension.'
      return
    else:
      content_type = gdata.docs.service.SUPPORTED_FILETYPES[ext]
   
    title = ''
    while title == '':
      title = raw_input('Enter name for document: ')

    try:
      ms = gdata.MediaSource(file_path = file_path, content_type = content_type)
    except IOError:
      print 'Problems reading file. Check permissions.'
      return
   
    if ext in ['CSV','ODS','XLS']:
      print 'Uploading spreadsheet...'
      entry = self.gd_client.UploadSpreadsheet(ms, title)
    else:
      print 'Uploading word processor document...'
      entry = self.gd_client.UploadDocument(ms, title)

    if entry:
      print 'Upload successful!'
      print 'Document now accessible at:', entry.GetAlternateLink().href
    else:
      print 'Upload error.'

  def _ListAllDocuments(self):
    """Retrieves a list of all of a user's documents and displays them."""

    feed = self.gd_client.GetDocumentListFeed()
    self._PrintFeed(feed)

  def _ListAllSpreadsheets(self):
    """Retrieves a list of a user's spreadsheets and displays them."""

    q = gdata.docs.service.DocumentQuery(categories=['spreadsheet'])
    feed = self.gd_client.Query(q.ToUri())
    self._PrintFeed(feed)

  def _ListAllWPDocuments(self):
    """Retrieves a list of a user's word processor documents and displays 
       them."""

    q = gdata.docs.service.DocumentQuery(categories=['document'])
    feed = self.gd_client.Query(q.ToUri())
    self._PrintFeed(feed)

  def _FullTextSearch(self):
    """Provides prompts to search a user's documents and displays the results
    of such a search. The text_query parameter of the DocumentListQuery object
    corresponds to the contents of the q parameter in the feed. Note that this
    parameter searches the content of documents, not just their titles."""

    input = raw_input('Enter search term: ')
    q = gdata.docs.service.DocumentQuery(text_query=input)
    feed = self.gd_client.Query(q.ToUri())
    self._PrintFeed(feed)

  def _PrintMenu(self):
    """Displays a menu of options for the user to choose from."""

    print ('\nDocument List Sample\n'
           '1) List all of your documents.\n'
           '2) List all of your spreadsheets.\n'
           '3) List all of your word processor documents.\n'
           '4) Search your documents.\n'
           '5) Upload a document.\n'
           '6) Exit.\n')

  def _GetMenuChoice(self, max):
    """Retrieves the menu selection from the user."""

    while True:
      input = raw_input('> ')

      try:
        num = int(input)
      except ValueError:
        print 'Invalid choice. Please choose a value between 1 and', max
        continue
      
      if num > max or num < 1:
        print 'Invalid choice. Please choose a value between 1 and', max
      else:
        return num

  def Run(self):
    """Allows the user to pick from various actions which demonstrate uses of
    the Document List feed."""

    try:
      while True:

        self._PrintMenu()

        choice = self._GetMenuChoice(6)

        if choice == 1:
          self._ListAllDocuments()
        elif choice == 2:
          self._ListAllSpreadsheets()
        elif choice == 3:
          self._ListAllWPDocuments()
        elif choice == 4:
          self._FullTextSearch()
        elif choice == 5:
          self._UploadMenu()
        elif choice == 6:
          return

    except KeyboardInterrupt:
      print '\nGoodbye.'
      return


def main():
  """Demonstrates use of the Docs client library extension using the
     DocsSample object."""

  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["user=", "pw="])
  except getopt.error, msg:
    print 'python docsExample.py --user [username] --pw [password] '
    sys.exit(2)

  user = ''
  pw = ''
  key = ''
  # Process options
  for option, arg in opts:
    if option == "--user":
      user = arg
    elif option == "--pw":
      pw = arg

  if user == '':
    print 'NOTE: Please run these tests only with a test account.'
    user = raw_input('Please enter your username: ')
  while pw == '':
    pw = getpass.getpass()
    if pw == '':
      print 'Password cannot be blank.'

  try:
    sample = DocsSample(user, pw)
  except gdata.service.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  sample.Run()


if __name__ == '__main__':
  main()
