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

"""Sample app for Google Apps Calendar Resource features.

  CalendarResourceSample: Demonstrates the use of the Calendar Resource API
"""


__author__ = 'pti@google.com (Prashant Tiwari)'


import getpass
from gdata.calendar_resource.client import CalendarResourceClient


class CalendarResourceSample(object):
  def __init__(self, domain, email, password):
    """Constructor for the CalendarResourceSample object.

    Construct a CalendarResourceSample with the given args.

    Args:
      domain: The domain name ("domain.com")
      email: The email account of the user or the admin ("john@domain.com")
      password: The domain admin's password
    """
    self.client = CalendarResourceClient(domain=domain)
    self.client.ClientLogin(email=email, password=password,
                            source='googlecode-calendarresourcesample-v1')


  def create(self, resource_properties):
    """Creates a calendar resource with the given resource_properties
    
    Args:
      resource_properties: A dictionary of calendar resource properties
    """
    print 'Creating a new calendar resource with id %s...' % (
        resource_properties['resource_id'])
    print self.client.CreateResource(
        resource_id=resource_properties['resource_id'],
        resource_common_name=resource_properties['resource_name'],
        resource_description=resource_properties['resource_description'],
        resource_type=resource_properties['resource_type'])

  def get(self, resource_id=None):
    """Retrieves the calendar resource with the given resource_id
    
    Args:
      resource_id: The optional calendar resource identifier
    """
    if resource_id:
      print 'Retrieving the calendar resource with id %s...' % (resource_id)
      print self.client.GetResource(resource_id=resource_id)
    else:
      print 'Retrieving all calendar resources...'
      print self.client.GetResourceFeed()

  def update(self, resource_properties):
    """Updates the calendar resource with the given resource_properties
    
    Args:
      resource_properties: A dictionary of calendar resource properties
    """
    print 'Updating the calendar resource with id %s...' % (
        resource_properties['resource_id'])
    print self.client.UpdateResource(
        resource_id=resource_properties['resource_id'],
        resource_common_name=resource_properties['resource_name'],
        resource_description=resource_properties['resource_description'],
        resource_type=resource_properties['resource_type'])

  def delete(self, resource_id):
    """Deletes the calendar resource with the given resource_id
    
    Args:
      resource_id: The unique calendar resource identifier
    """
    print 'Deleting the calendar resource with id %s...' % (resource_id)
    self.client.DeleteResource(resource_id)
    print 'Calendar resource successfully deleted.'


def main():
  """Demonstrates the Calendar Resource API using CalendarResourceSample."""
  domain = None
  admin_email = None
  admin_password = None
  do_continue = 'y'
  print("Google Apps Calendar Resource API Sample\n\n")
  while not domain:
    domain = raw_input('Google Apps domain: ')
  while not admin_email:
    admin_email = '%s@%s' % (raw_input('Administrator username: '), domain)
  while not admin_password:
    admin_password = getpass.getpass('Administrator password: ')

  sample = CalendarResourceSample(domain=domain, email=admin_email,
                                  password=admin_password)

  while do_continue.lower() != 'n':
    do_continue = call_service(sample)


def call_service(sample):
  """Calls the service methods on the user input"""
  operation = None

  while operation not in ['c', 'C', 'g', 'G', 'u', 'U', 'd', 'D', 'q', 'Q']:
    operation = raw_input('Do [c=create|g=get|u=update|d=delete|q=quit]: ')

  operation = operation.lower()

  if operation == 'q':
    return 'n'

  resource_properties = get_input(operation)

  if operation == 'c':
    sample.create(resource_properties)
  elif operation == 'g':
    sample.get(resource_properties['resource_id'])
  elif operation == 'u':
    sample.update(resource_properties)
  elif operation == 'd':
    sample.delete(resource_properties['resource_id'])

  do_continue = None
  while do_continue not in ['', 'y', 'Y', 'n', 'N']:
    do_continue = raw_input('Want to continue (Y/n): ')

  if do_continue == '':
    do_continue = 'y'

  return do_continue.lower()


def get_input(operation):
  """Gets user input from console"""
  resource_id = None
  resource_name = None
  resource_description = None
  resource_type = None

  if operation == 'g':
    resource_id = raw_input('Resource id (leave blank to get all resources): ')
  else:
    while not resource_id:
      resource_id = raw_input('Resource id: ')

  if operation == 'c':
    resource_name = raw_input('Resource common name (recommended): ')
    resource_description = raw_input('Resource description (recommended): ')
    resource_type = raw_input('Resource type (recommended): ')
  elif operation == 'u':
    resource_name = raw_input(
        'New resource common name (leave blank if no change): ')
    resource_description = raw_input(
        'New resource description (leave blank if no change): ')
    resource_type = raw_input('New resource type (leave blank if no change): ')

  resource_properties = {'resource_id': resource_id,
                         'resource_name': resource_name,
                         'resource_description': resource_description,
                         'resource_type': resource_type}
  return resource_properties


if __name__ == '__main__':
  main()
