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

"""Contains a Sample for Google Apps Admin Settings.

  AdminSettingsSample: shows everything you ever wanted to know about
                       your Google Apps Domain but were afraid to ask.
"""

__author__ = 'jlee@pbu.edu'

import getopt
import getpass
import sys
import time

import gdata.apps.service
import gdata.apps.adminsettings.service

class AdminSettingsSample(object):
  """AdminSettingsSample object demos Admin Settings API."""

  def __init__(self, email, password, domain):
    """Constructor for the AdminSettingsSample object.

    Takes an email and password corresponding to a google apps admin
    account to demon the Admin Settings API.

    Args:
      email: [string] The e-mail address of the account to use for the sample.
      password: [string] The password corresponding to the account specified by
          the email parameter.
      domain: [string] The domain for the Profiles feed
    """
    self.gd_client = gdata.apps.adminsettings.service.AdminSettingsService()
    self.gd_client.domain = domain
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'GoogleInc-AdminSettingsPythonSample-1'
    self.gd_client.ProgrammaticLogin()

  def Run(self):
    #pause 1 sec inbetween calls to prevent quota warning
    print 'Google Apps Domain: ', self.gd_client.domain
    time.sleep(1)
    print 'Default Language: ', self.gd_client.GetDefaultLanguage()
    time.sleep(1)
    print 'Organization Name: ', self.gd_client.GetOrganizationName()
    time.sleep(1)
    print 'Maximum Users: ', self.gd_client.GetMaximumNumberOfUsers()
    time.sleep(1)
    print 'Current Users: ', self.gd_client.GetCurrentNumberOfUsers()
    time.sleep(1)
    print 'Domain is Verified: ',self.gd_client.IsDomainVerified()
    time.sleep(1)
    print 'Support PIN: ',self.gd_client.GetSupportPIN()
    time.sleep(1)
    print 'Domain Edition: ', self.gd_client.GetEdition()
    time.sleep(1)
    print 'Customer PIN: ', self.gd_client.GetCustomerPIN()
    time.sleep(1)
    print 'Domain Creation Time: ', self.gd_client.GetCreationTime()
    time.sleep(1)
    print 'Domain Country Code: ', self.gd_client.GetCountryCode()
    time.sleep(1)
    print 'Admin Secondary Email: ', self.gd_client.GetAdminSecondaryEmail()
    time.sleep(1)
    cnameverificationstatus = self.gd_client.GetCNAMEVerificationStatus()
    print 'CNAME Verification Record Name: ', cnameverificationstatus['recordName']
    print 'CNAME Verification Verified: ', cnameverificationstatus['verified']
    print 'CNAME Verification Method: ', cnameverificationstatus['verificationMethod']
    time.sleep(1)
    mxverificationstatus = self.gd_client.GetMXVerificationStatus()
    print 'MX Verification Verified: ', mxverificationstatus['verified']
    print 'MX Verification Method: ', mxverificationstatus['verificationMethod']
    time.sleep(1)
    ssosettings = self.gd_client.GetSSOSettings()
    print 'SSO Enabled: ', ssosettings['enableSSO']
    print 'SSO Signon Page: ', ssosettings['samlSignonUri']
    print 'SSO Logout Page: ', ssosettings['samlLogoutUri']
    print 'SSO Password Page: ', ssosettings['changePasswordUri']
    print 'SSO Whitelist IPs: ', ssosettings['ssoWhitelist']
    print 'SSO Use Domain Specific Issuer: ', ssosettings['useDomainSpecificIssuer']
    time.sleep(1)
    ssokey = self.gd_client.GetSSOKey()
    print 'SSO Key Modulus: ', ssokey['modulus']
    print 'SSO Key Exponent: ', ssokey['exponent']
    print 'SSO Key Algorithm: ', ssokey['algorithm']
    print 'SSO Key Format: ', ssokey['format']
    print 'User Migration Enabled: ', self.gd_client.IsUserMigrationEnabled()
    time.sleep(1)
    outboundgatewaysettings = self.gd_client.GetOutboundGatewaySettings()
    print 'Outbound Gateway Smart Host: ', outboundgatewaysettings['smartHost']
    print 'Outbound Gateway Mode: ', outboundgatewaysettings['smtpMode']

def main():
  """Demonstrates use of the Admin Settings API using the AdminSettingsSample object."""
  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw=', 'domain='])
  except getopt.error, msg:
    print 'python adminsettings_example.py --user [username] --pw [password]'
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

  while not domain:
    print 'NOTE: Please run these tests only with a test account.'
    domain = raw_input('Please enter your apps domain: ')
  while not user:
    user = raw_input('Please enter a administrator account: ')+'@'+domain
  while not pw:
    pw = getpass.getpass('Please enter password: ')
    if not pw:
      print 'Password cannot be blank.'

  try:
    sample = AdminSettingsSample(user, pw, domain)
  except gdata.service.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  sample.Run()

if __name__ == '__main__':
  main()
