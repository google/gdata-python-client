#!/usr/bin/python2.4
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

"""Sample app for Google Apps Email Migration features.

  EmailMigrationSample: Demonstrates the use of the Email Migration API
"""


__author__ = 'pti@google.com (Prashant Tiwari)'


from optparse import OptionParser
import os
from gdata.apps.migration import service


class EmailMigrationSample(object):
  """Sample application demonstrating use of the Email Migration API."""

  def __init__(self, domain, email, password):
    """Constructor for the EmailMigrationSample object.

    Construct an EmailMigrationSample with the given args.

    Args:
      domain: The domain name ("domain.com")
      email: The email account of the user or the admin ("john@domain.com")
      password: The domain admin's password
    """
    self.service = service.MigrationService(
        email=email,
        password=password,
        domain=domain,
        source='googlecode-migrationsample-v1')
    self.service.ProgrammaticLogin()
    # Sample mail properties
    self.mail_item_properties = ['IS_INBOX', 'IS_UNREAD']
    self.mail_labels = ['EmailMigrationSample']

  def Migrate(self, path):
    """Migrates messages at the given path.
    
    Args:
      path: The file or directory path where messages are stored
    """
    if os.path.isfile(path):
      if os.path.splitext(path)[1] != '.txt':
        print "The input file is not a .txt file"
        return
      self._MigrateOneMail(path)
    elif os.path.isdir(path):
      if path.endswith(os.sep):
        path = path[0: len(path) - 1]
      txt_file_paths = []
      filenames = os.listdir(path)
      for filename in filenames:
        # Filter out the non-txt files in the directory
        filepath = path + os.sep + filename
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1] == '.txt':
          txt_file_paths.append(filepath)
      if not txt_file_paths:
        print "Found no .txt file in the directory"
        return
      elif len(txt_file_paths) == 1:
        # Don't use threading if there's only one txt file in the dir 
        self._MigrateOneMail(txt_file_paths[0])
      else:
        self._MigrateManyMails(txt_file_paths)

  def _MigrateOneMail(self, path):
    """Imports a single message via the ImportMail service. 
    
    Args:
      path: The path of the message file
    """
    print "Attempting to migrate 1 message..."
    content = self._ReadFileAsString(path)
    self.service.ImportMail(user_name=options.username,
                            mail_message=content,
                            mail_item_properties=self.mail_item_properties,
                            mail_labels=self.mail_labels)
    print "Successfully migrated 1 message."

  def _MigrateManyMails(self, paths):
    """Imports several messages via the ImportMultipleMails service. 
    
    Args:
      paths: List of paths of message files
    """
    print "Attempting to migrate %d messages..." % (len(paths))
    for path in paths:
      content = self._ReadFileAsString(path)
      self.service.AddMailEntry(mail_message=content,
                                mail_item_properties=self.mail_item_properties,
                                mail_labels=self.mail_labels,
                                identifier=path)
    success = self.service.ImportMultipleMails(user_name=options.username)
    print "Successfully migrated %d of %d messages." % (success, len(paths))

  def _ReadFileAsString(self, path):
    """Reads the file found at path into a string
    
    Args:
      path: The path of the message file
    
    Returns:
      The file contents as a string
    
    Raises:
      IOError: An error occurred while trying to read the file
    """
    try:
      input_file = open(path, 'r')
      file_str = []
      for eachline in input_file:
        file_str.append(eachline)
      input_file.close()
      return ''.join(file_str)
    except IOError, e:
      raise IOError(e.args[1] + ': ' + path)


def main():
  """Demonstrates the Email Migration API using EmailMigrationSample."""

  usage = 'usage: %prog [options]'
  global options
  parser = OptionParser(usage=usage)
  parser.add_option('-d', '--domain',
                    help="the Google Apps domain, e.g. 'domain.com'")
  parser.add_option('-e', '--email',
                    help="the email account of the user or the admin, \
                    e.g. 'john.smith@domain.com'")
  parser.add_option('-p', '--password',
                    help="the account password")
  parser.add_option('-u', '--username',
                    help="the user account on which to perform operations. for\
                    non-admin users this will be their own account name. \
                    e.g. 'jane.smith'")
  parser.add_option('-f', '--file',
                    help="the system path of an RFC822 format .txt file or\
                    directory containing multiple such files to be migrated")
  (options, args) = parser.parse_args()

  if (options.domain is None
      or options.email is None
      or options.password is None
      or options.username is None
      or options.file is None):
    parser.print_help()
    return

  options.file = options.file.strip()

  if not os.path.exists(options.file):
    print "Invalid file or directory path"
    return

  sample = EmailMigrationSample(domain=options.domain,
                                email=options.email,
                                password=options.password)
  sample.Migrate(options.file)


if __name__ == '__main__':
  main()
