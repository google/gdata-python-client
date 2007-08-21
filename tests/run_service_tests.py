#!/usr/bin/python

import sys
import unittest
import module_test_runner
import getopt
import getpass
# Modules whose tests we will run.
import atom_tests.service_test
import gdata_tests.service_test
import gdata_tests.apps.service_test
import gdata_tests.base.service_test
import gdata_tests.calendar.service_test
import gdata_tests.docs.service_test
import gdata_tests.spreadsheet.service_test


def RunAllTests(username, password, spreadsheet_key, worksheet_key, domain):
  test_runner = module_test_runner.ModuleTestRunner()
  test_runner.modules = [atom_tests.service_test, 
                         gdata_tests.service_test, 
                         gdata_tests.apps.service_test,
                         gdata_tests.base.service_test, 
                         gdata_tests.calendar.service_test,
                         gdata_tests.docs.service_test, 
                         gdata_tests.spreadsheet.service_test]
  test_runner.settings = {'username':username, 'password':password, 
                          'test_image_location':'testimage.jpg',
                          'ss_key':spreadsheet_key,
                          'ws_key':worksheet_key,
                          'domain':domain}
  test_runner.RunAllTests()

def GetValuesForTestSettingsAndRunAllTests():
  username = ''
  password = ''
  spreadsheet_key = ''
  worksheet_key = ''
  domain = ''
  
  print ('NOTE: Please run these tests only with a test account. ' 
         'The tests may delete or update your data.')
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['username=', 'password=',
                                                  'ss_key=', 'ws_key=', 
                                                  'domain='])
    for o, a in opts:
      if o == '--username':
        username = a
      elif o == '--password':
        password = a
      elif o == '--ss_key':
        spreadsheet_key = a
      elif o == '--ws_key':
        worksheet_key = a
      elif o == '--domain':
        domain = a
  except getopt.GetoptError:
    pass

  if username == '' and password == '':
    print ('Missing --user and --pw command line arguments, '  
           'prompting for credentials.')
  if username == '':
    username = raw_input('Please enter your username: ')
  if password == '':
    password = getpass.getpass()
  if spreadsheet_key == '':
    spreadsheet_key = raw_input(
        'Please enter the key for the test spreadsheet: ')
  if worksheet_key == '':
    worksheet_key = raw_input(
        'Please enter the id for the worksheet to be edited: ')
  if domain == '':
    domain = raw_input('Please enter the domain for the Google Apps account: ')
  RunAllTests(username, password, spreadsheet_key, worksheet_key, domain)

if __name__ == '__main__':
  GetValuesForTestSettingsAndRunAllTests()
