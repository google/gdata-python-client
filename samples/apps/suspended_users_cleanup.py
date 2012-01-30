#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
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

"""Sample to delete suspended users whose last login date is 6 months old.

Sample to obtain the suspended users and their last login date from the
Reporting API and delete the user if the last login date is older than
6 months using the Provisioning API.
"""

__author__ = 'Shraddha Gupta <shraddhag@google.com>'

import datetime
import getopt
import sys
import gdata.apps.client
import gdata.client
import google.apps.reporting


def Usage():
  print ('Usage: suspended_users_cleanup.py --email=<email> '
         '--password=<password> --domain=<domain> ')


def GetAccountsReport(report_runner):
  """Gets the account report from the Reporting API for current date.

  Args:
    report_runner: An instance of google.apps.reporting.ReportRunner.

  Returns:
    response: String containing accounts report.
  """
  if report_runner.token is None:
    report_runner.Login()
  request = google.apps.reporting.ReportRequest()
  request.token = report_runner.token
  request.domain = report_runner.domain
  request.report_name = 'accounts'
  request.date = report_runner.GetLatestReportDate()
  response = report_runner.GetReportData(request)
  return response


def main():
  """Gets accounts report and deletes old suspended users."""
  try:
    (opts, args) = getopt.getopt(sys.argv[1:], '', ['email=', 'password=',
                                                    'domain='])
  except getopt.GetoptError:
    print 'Error'
    Usage()
    sys.exit(1)
  opts = dict(opts)

  report_runner = google.apps.reporting.ReportRunner()
  email = opts.get('--email')
  report_runner.admin_email = email
  password = opts.get('--password')
  report_runner.admin_password = password
  domain = opts.get('--domain')
  report_runner.domain = domain
  if not email or not password or not domain:
    Usage()
    sys.exit(1)

  # Instantiate a client for Provisioning API
  client = gdata.apps.client.AppsClient(domain=domain)
  client.ClientLogin(email=email, password=password,
                     source='DeleteOldSuspendedUsers')

  # Get accounts report from the Reporting API
  response = GetAccountsReport(report_runner)
  accounts = response.splitlines()
  current_date = datetime.datetime.now()

  # accounts[0] contains the headings for fields, read data starting at index 1
  for i in range(1, len(accounts)):
    account_fields = accounts[i].split(',')
    # Find the suspended users and check if last login date is 180 days old
    if account_fields[3] != 'ACTIVE':
      last_login_date_str = account_fields[10]
      last_login_date = datetime.datetime.strptime(last_login_date_str,
                                                   '%Y%m%d')
      duration = current_date - last_login_date
      days = duration.days
      if days > 180:
        account_id = account_fields[2]
        print 'This user is obsolete: %s' % account_id
        user_name = account_id.split('@')
        delete_flag = raw_input('Do you want to delete the user (y/n)? ')
        if delete_flag == 'y':
          try:
            client.DeleteUser(user_name[0])
            print 'Deleted %s ' % account_id
          except gdata.client.RequestError, e:
            print 'Request Error %s %s %s' % (e.status, e.reason, e.body)


if __name__ == '__main__':
  main()
