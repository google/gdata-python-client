#!/usr/bin/python
#
# Copyright (C) 2007, 2009 Google Inc.
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

__author__ = 'Gunjan Sharma <gunjansharma@google.com>'

import getopt
import getpass
import sys
import time
import atom
import atom.data
import gdata.apps.multidomain.client
import gdata.apps.organization.service
import gdata.apps.service
import gdata.client
import gdata.contacts.client
import gdata.contacts.data
import gdata.contacts.service
import gdata.sites.client
import gdata.sites.data

#The title for the site
ORG_SITE_TITLE = 'Organization Hierarchy'
#Title for the users site
USER_SITE_TITLE = 'Users'
#The template URI for a site
URI = 'https://sites.google.com/a/%s/%s/'
#Description for the sites
DESCRIPTION = 'Under Construction'
#Theme for the sites
THEME = 'slate'
#Header for the new webpages
HTML_HEADER = ('<html:div xmlns:html="http://www.w3.org/1999/xhtml">'
               '<html:table cellspacing="0" class='
               '"sites-layout-name-one-column sites-layout-hbox"><html:tbody>'
               '<html:tr><html:td class="sites-layout-tile '
               'sites-tile-name-content-1">')
#Footer for the new webpages
HTML_FOOTER = '</html:td></html:tr></html:tbody></html:table></html:div>'
#The template string for each user's html page
TEMPLATE_USER_HTML = ('<h2>Name:</h2><p>%s</p><h2>Gender:</h2><p> %s</p>'
                      '<h2>Address:</h2><p>%s</p><h2>Email:</h2><p>%s</p>')


class OrgUnitAddressBook(object):
  """Creates organization unit sites from the domain."""

  def __init__(self, email, password, domain):
    """Constructor for the OrgUnitSites object.

    Takes an email, password and domain to create a site map corresponding
    to the organization units in the domain.

    Args:
      email: [string] The email address of the admin.
      password: [string] The password corresponding to the admin account.
      domain: [string] The domain for which sites are to be made.

    Returns:
      A OrgUnitSites object used to run the site making.
    """
    source = 'Making sites corresponding to org units'
    self.domain = domain
    # Create sites object
    self.sites_client = gdata.sites.client.SitesClient(source=source,
                                                       domain=domain)
    self.sites_client.ClientLogin(email, password, self.sites_client.source);
    #Get the sites feed
    self.all_site_feed = self.sites_client.GetSiteFeed()
    
    # Create google contacts object
    self.profiles_client = gdata.contacts.client.ContactsClient(domain=domain)
    self.profiles_client.client_login(email, password, 'cp', service='cp')

    # Create an Organization Unit Client
    self.org_unit_client = gdata.apps.organization.service.OrganizationService(
                                 email=email, domain=domain, password=password)
    self.org_unit_client.ProgrammaticLogin()
    customer_id_set = self.org_unit_client.RetrieveCustomerId()
    self.customer_id = customer_id_set['customerId']

  def _GetSiteName(self, site_title):
    """Returns the corresponding site_name. This is needed since the site name
       isn't the same as the title.

    Args:
      site_title: [string] The title for a site.

    Returns:
      A string which is the corresponding site_name.
    """
    site_name = site_title.replace(' ', '-')
    site_name = site_name.lower()
    return site_name
  
  def _GetSiteURI(self, site_title):
    """Returns the corresponding uri to the site.
       Needed to get the link to a particular user page.

    Args:
      site_title: [string] The title for a site.

    Returns:
      A string which is the corresponding site's URI.
    """
    uri = URI % (self.domain, self._GetSiteName(site_title))
    return uri
    
  def _CreateSite(self, site_title, description=DESCRIPTION, theme=THEME):
    """Creates a site with the site_title, if it not already exists.

    Args:
      site_title: [string] The title for a site.
      description: [string] The description for the site.
      theme: [string] The theme that should be set for the site.

    Returns:
      A Content feed object for the created site.
    """
    site_entry = None
    site_found = False
    site_name = self._GetSiteName(site_title)    
    for site in self.all_site_feed.entry:
      if site.site_name.text == site_name:
        site_found = True
        site_entry = site
        break
    if site_found == False:
      try:
        site_entry = self.sites_client.CreateSite(site_title,
                          description=description, theme=theme)
      except gdata.client.RequestError, error:
        print error
    self.sites_client.site = site_name
    return site_entry

  def _DeleteAllPages(self):
    '''Deletes all the pages in a site except home'''
    feed_uri = self.sites_client.make_content_feed_uri()
    while feed_uri:
      feed = self.sites_client.GetContentFeed()
      for entry in feed.entry:
        if entry.page_name.text != 'home':
          self.sites_client.Delete(entry)
      feed_uri = feed.FindNextLink()

  def _GetUsersProfileFeed(self):
    """Retrieves all the user's profile.

    Returns:
      A Dictionary of email address to ContentEntry objects
    """    
    profiles = []
    feed_uri = self.profiles_client.GetFeedUri('profiles')
    while feed_uri:
      feed = self.profiles_client.GetProfilesFeed(uri=feed_uri)
      profiles.extend(feed.entry)
      feed_uri = feed.FindNextLink()
    
    profiles_dict = {}
    for profile in profiles:
      for email in profile.email:
        if email.primary and email.primary == 'true':
          profiles_dict[email.address] = profile
          break
          
    return profiles_dict
    
  def _CreateUserPageHTML(self, profile):
    """Creates HTML for a user profile.

    Args:
      profile: [gdata.contacts.data.ProfileEntry] It is the profile of the user
                                                  whose HTML has to be created.

    Returns:
      A String which is the HTML code.
    """    
    address_string = ''
    email_string = ''
    for address in profile.structured_postal_address:
      address_string = '%s<li>%s</li><br />' % (address_string, address)
    for email in profile.email:
      if email.primary and email.primary == 'true':
        email_string = '%s<li>%s</li><br />' % (email_string, email.address)
    
    new_html = TEMPLATE_USER_HTML % (profile.name.full_name.text,
                         str(profile.gender), address_string, email_string)
    
    return HTML_HEADER + new_html + HTML_FOOTER

  def _GetUserPageName(self, user_email):
    """Creates a page name for a particular user depending on the
       email address.

    Args:
      user_email: [string] The email address of the user.

    Returns:
      A String which defines the user page name.
    """
    user_page_name = user_email.replace('@', '-')
    user_page_name = user_page_name.replace('.', '_')
    user_page_name = user_page_name.lower()
    return user_page_name

  def _CreateUserPages(self):
    """Makes all the user pages"""
    
    entry = self._CreateSite(USER_SITE_TITLE)

    #Delete all the pages 
    self._DeleteAllPages()
    
    users_profile = self._GetUsersProfileFeed()
    users = self.org_unit_client.RetrieveAllOrgUsers(self.customer_id)
    for user in users:
      user_email = user['orgUserEmail']
      user_profile = users_profile[user_email]
      new_html = self._CreateUserPageHTML(user_profile)  
      user_page_name = self._GetUserPageName(user_email)
      
      self.sites_client.CreatePage('webpage', user_profile.name.full_name.text,
                                   html=new_html, page_name=user_page_name)
  
  def _GetOrgUnitPageHTML(self, path):
    """Creates HTML for a Org Unit Page.

    Args:
      profile: [string] Path of the Org Unit.

    Returns:
      A String which is the HTML code.
    """
    
    domain_users = self.org_unit_client.RetrieveOrgUnitUsers(self.customer_id,
                                                             path)
    new_html = '<p>'
    for user in domain_users:
      user_email = user['orgUserEmail']
      user_page_name = self._GetUserPageName(user_email)
      site_uri = self._GetSiteURI(USER_SITE_TITLE)
      new_html = '%s<li><a href="%s">%s</a></li><br />' % (new_html,
                                         site_uri + user_page_name, user_email)
    new_html = new_html + '</p>'
    return HTML_HEADER + new_html + HTML_FOOTER
  
  def _SetOrgSiteHomePage(self):
    """Sets up the home page for Org Unit Site"""
    new_html = self._GetOrgUnitPageHTML('/')
    home_path = self._GetUnitPath()
    home_feed = self.sites_client.GetContentFeed(uri=home_path)
    home_feed.entry[0].title.text = self.domain
    home_feed.entry[0].content.html = new_html
    self.sites_client.Update(home_feed.entry[0])
  
  def _GetUnitPath(self, path=None):
    """Returns path to the parent unit

    Args:
      parent_path: [string] Path of the Parent Org Unit.

    Returns:
      A String which is the path to the parent.
    """
    path_uri = '%s?path=/%s'
    if path:
      path = path.replace('+', '-')
      path = path.lower()
      path = 'home/' + path
    else:
      path = 'home'
  
    uri = path_uri % (self.sites_client.MakeContentFeedUri(), path)
    return uri
  
  def _CreateOrgUnitPages(self):
    """Creates all the org unit pages"""
    
    entry = self._CreateSite(ORG_SITE_TITLE)    
    #Delete all the pages 
    self._DeleteAllPages()
    
    self._SetOrgSiteHomePage()
    
    orgUnits = self.org_unit_client.RetrieveAllOrgUnits(self.customer_id)
    for unit in orgUnits:
      parent_uri = self._GetUnitPath(unit['parentOrgUnitPath'])      
      parent_feed = self.sites_client.GetContentFeed(uri=parent_uri)
  
      new_html = self._GetOrgUnitPageHTML(unit['orgUnitPath'])      
      self.sites_client.CreatePage('webpage', unit['name'], html=new_html,
                                   parent=parent_feed.entry[0])

  def Run(self):
    """Controls the entire flow of the sites making process"""
    
    print 'Starting the process. This may take few minutes.'
    print 'Creating user pages...'
    self._CreateUserPages()
    print 'User pages created'
    print 'Creating Organization Unit Pages'
    self._CreateOrgUnitPages()
    print 'Your website is ready, visit it at: %s' % (self._GetSiteURI(
                                                      ORG_SITE_TITLE))


def main():
  """Runs the site making module using an instance of OrgUnitAddressBook"""
  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['email=', 'pw=', 'domain='])
  except getopt.error, msg:
    print ('python org_unit_sites.py --email [emailaddress] --pw [password]'
           ' --domain [domain]')
    sys.exit(2)

  email = ''
  password = ''
  domain = ''
  # Parse options
  for option, arg in opts:
    if option == '--email':
      email = arg
    elif option == '--pw':
      password = arg
    elif option == '--domain':
      domain = arg

  while not email:
    email = raw_input('Please enter admin email address (admin@example.com): ')
  while not password:
    sys.stdout.write('Admin Password: ')
    password = getpass.getpass()
    if not password:
      print 'Password cannot be blank.'
  while not domain:
    username, domain = email.split('@', 1)
    choice = raw_input('You have not given us the domain name. ' +
                        'Is it %s? (y/n)' % (domain))
    if choice == 'n':
      domain = raw_input('Please enter domain name (domain.com): ')

  try:
    org_unit_address_book = OrgUnitAddressBook(email, password, domain)
  except gdata.service.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  org_unit_address_book.Run()


if __name__ == '__main__':
  main()
