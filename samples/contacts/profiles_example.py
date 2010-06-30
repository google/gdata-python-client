#!/usr/bin/env python
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

"""Contains a Sample for Google Profiles.

  ProfilesSample: demonstrates operations with the Profiles feed.
"""

__author__ = 'jtoledo (Julian Toledo)'


import getopt
import getpass
import sys

import gdata.contacts
import gdata.contacts.service


class ProfilesSample(object):
  """ProfilesSample object demonstrates operations with the Profiles feed."""

  def __init__(self, email, password, domain):
    """Constructor for the ProfilesSample object.

    Takes an email and password corresponding to a gmail account to
    demonstrate the functionality of the Profiles feed.

    Args:
      email: [string] The e-mail address of the account to use for the sample.
      password: [string] The password corresponding to the account specified by
          the email parameter.
      domain: [string] The domain for the Profiles feed
    """
    self.gd_client = gdata.contacts.service.ContactsService(
        contact_list=domain)
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'GoogleInc-ProfilesPythonSample-1'
    self.gd_client.ProgrammaticLogin()

  def PrintFeed(self, feed, ctr=0):
    """Prints out the contents of a feed to the console.

    Args:
      feed: A gdata.profiles.ProfilesFeed instance.
      ctr: [int] The number of entries in this feed previously printed. This
          allows continuous entry numbers when paging through a feed.

    Returns:
      The number of entries printed, including those previously printed as
      specified in ctr. This is for passing as an ar1gument to ctr on
      successive calls to this method.
    """
    if not feed.entry:
      print '\nNo entries in feed.\n'
      return 0
    for entry in feed.entry:
      self.PrintEntry(entry)
    return len(feed.entry) + ctr

  def PrintEntry(self, entry):
    """Prints out the contents of a single Entry to the console.

    Args:
      entry: A gdata.contacts.ProfilesEntry
    """
    print '\n%s' % (entry.title.text)    
    for email in entry.email:
      if email.primary == 'true':
        print 'Email: %s (primary)' % (email.address)
      else:
        print 'Email: %s' % (email.address)
    if entry.nickname:
      print 'Nickname: %s' % (entry.nickname.text)
    if entry.occupation:
      print 'Occupation: %s' % (entry.occupation.text)
    if entry.gender:
      print 'Gender: %s' % (entry.gender.value)
    if entry.birthday:
      print 'Birthday: %s' % (entry.birthday.when)
    for relation in entry.relation:
      print 'Relation: %s %s' % (relation.rel, relation.text)
    for user_defined_field in entry.user_defined_field:
      print 'UserDefinedField: %s %s' % (user_defined_field.key,
                                         user_defined_field.value)
    for website in entry.website:
      print 'Website: %s %s' % (website.href, website.rel)
    for phone_number in entry.phone_number:
      print 'Phone Number: %s' % phone_number.text
    for organization in entry.organization:
      print 'Organization:'
      if organization.org_name:
        print ' Name: %s' % (organization.org_name.text)
      if organization.org_title:
        print ' Title: %s' % (organization.org_title.text)
      if organization.org_department:
        print ' Department: %s' % (organization.org_department.text)
      if organization.org_job_description:
        print ' Job Desc: %s' % (organization.org_job_description.text)

  def PrintPaginatedFeed(self, feed, print_method):
    """Print all pages of a paginated feed.

    This will iterate through a paginated feed, requesting each page and
    printing the entries contained therein.

    Args:
      feed: A gdata.contacts.ProfilesFeed instance.
      print_method: The method which will be used to print each page of the
    """
    ctr = 0
    while feed:
      # Print contents of current feed
      ctr = print_method(feed=feed, ctr=ctr)
      # Prepare for next feed iteration
      next = feed.GetNextLink()
      feed = None
      if next:
        if self.PromptOperationShouldContinue():
          # Another feed is available, and the user has given us permission
          # to fetch it
          feed = self.gd_client.GetProfilesFeed(next.href)
        else:
          # User has asked us to terminate
          feed = None

  def PromptOperationShouldContinue(self):
    """Display a "Continue" prompt.

    This give is used to give users a chance to break out of a loop, just in
    case they have too many profiles/groups.

    Returns:
      A boolean value, True if the current operation should continue, False if
      the current operation should terminate.
    """
    while True:
      key_input = raw_input('Continue [Y/n]? ')
      if key_input is 'N' or key_input is 'n':
        return False
      elif key_input is 'Y' or key_input is 'y' or key_input is '':
        return True

  def ListAllProfiles(self):
    """Retrieves a list of profiles and displays name and primary email."""
    feed = self.gd_client.GetProfilesFeed()
    self.PrintPaginatedFeed(feed, self.PrintFeed)

  def SelectProfile(self):
    username = raw_input('Please enter your username for the profile: ')
    entry_uri = self.gd_client.GetFeedUri('profiles')+'/'+username
    try:
      entry = self.gd_client.GetProfile(entry_uri)
      self.PrintEntry(entry)
    except gdata.service.RequestError:
      print 'Invalid username for the profile.'

  def PrintMenu(self):
    """Displays a menu of options for the user to choose from."""
    print ('\nProfiles Sample\n'
           '1) List all of your Profiles.\n'
           '2) Get a single Profile.\n'
           '3) Exit.\n')

  def GetMenuChoice(self, maximum):
    """Retrieves the menu selection from the user.

    Args:
      maximum: [int] The maximum number of allowed choices (inclusive)

    Returns:
      The integer of the menu item chosen by the user.
    """
    while True:
      key_input = raw_input('> ')

      try:
        num = int(key_input)
      except ValueError:
        print 'Invalid choice. Please choose a value between 1 and', maximum
        continue

      if num > maximum or num < 1:
        print 'Invalid choice. Please choose a value between 1 and', maximum
      else:
        return num

  def Run(self):
    """Prompts the user to choose funtionality to be demonstrated."""
    try:
      while True:
        self.PrintMenu()
        choice = self.GetMenuChoice(3)
        if choice == 1:
          self.ListAllProfiles()
        elif choice == 2:
          self.SelectProfile()
        elif choice == 3:
          return

    except KeyboardInterrupt:
      print '\nGoodbye.'
      return


def main():
  """Demonstrates use of the Profiles using the ProfilesSample object."""
  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw=', 'domain='])
  except getopt.error, msg:
    print 'python profiles_example.py --user [username] --pw [password]'
    print ' --domain [domain]'
    sys.exit(2)

  user = ''
  pw = ''
  domain = ''

  # Process options
  for option, arg in opts:
    if option == '--user':
      user = arg
    elif option == '--pw':
      pw = arg
    elif option == '--domain':
      domain = arg

  while not user:
    print 'NOTE: Please run these tests only with a test account.'
    user = raw_input('Please enter your email: ')
  while not pw:
    pw = getpass.getpass('Please enter password: ')
    if not pw:
      print 'Password cannot be blank.'
  while not domain:
    domain = raw_input('Please enter your Apps domain: ')

  try:
    sample = ProfilesSample(user, pw, domain)
  except gdata.service.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  sample.Run()

if __name__ == '__main__':
  main()
