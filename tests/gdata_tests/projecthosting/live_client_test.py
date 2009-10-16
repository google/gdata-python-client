#!/usr/bin/env python
#
# Copyright (C) 2009 Google Inc.
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


# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


__author__ = 'jlapenna@google.com (Joe LaPenna)'


import unittest
import gdata.projecthosting.client
import gdata.projecthosting.data
import gdata.gauth
import gdata.client
import atom.http_core
import atom.mock_http_core
import atom.core
import gdata.data
import gdata.test_config as conf


conf.options.register_option(conf.PROJECT_NAME_OPTION)
conf.options.register_option(conf.ISSUE_ASSIGNEE_OPTION)


class ProjectHostingClientTest(unittest.TestCase):

  def setUp(self):
    self.client = None
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.projecthosting.client.ProjectHostingClient()
      conf.configure_client(self.client, 'ProjectHostingClientTest', 'code')

    self.project_name = conf.options.get_value('project_name')
    self.assignee = conf.options.get_value('issue_assignee')
    self.owner = conf.options.get_value('username')

  def tearDown(self):
    conf.close_client(self.client)

  def create_issue(self):
    # Add an issue
    created = self.client.add_issue(
        self.project_name,
        'my title',
        'my summary',
        self.owner,
        labels=['label0'])

    self.assertEqual(created.title.text, 'my title')
    self.assertEqual(created.content.text, 'my summary')

    self.assertEqual(len(created.label), 1)
    self.assertEqual(created.label[0].text, 'label0')

    return created

  def test_create_update_close(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_create_update_delete')

    # Create the issue:
    created = self.create_issue()

    # Change the issue we just added.
    issue_id = created.id.text.split('/')[-1]
    update_response = self.client.update_issue(
        self.project_name,
        issue_id,
        self.owner,
        comment='My comment here.',
        summary='New Summary',
        status='Accepted',
        owner=self.assignee,
        labels=['-label0', 'label1'],
        ccs=[self.owner])

    updates = update_response.updates
    # Make sure it changed our status, summary, and added the comment.
    self.assertEqual(update_response.content.text, 'My comment here.')
    self.assertEqual(updates.summary.text, 'New Summary')
    self.assertEqual(updates.status.text, 'Accepted')

    # Make sure it got all our label change requests.
    self.assertEquals(len(updates.label), 2)
    self.assertEquals(updates.label[0].text, '-label0')
    self.assertEquals(updates.label[1].text, 'label1')

    # Be sure it saw our CC change. We can't check the specific values (yet)
    # because ccUpdate and ownerUpdate responses are mungled.
    self.assertEquals(len(updates.ccUpdate), 1)
    self.assert_(updates.ownerUpdate.text)

  def test_get_issues(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_create_update_delete')

    # Create an issue so we have something to look up.
    created = self.create_issue()

    # The fully qualified id is a url, we just want the number.
    issue_id = created.id.text.split('/')[-1]

    # Get the specific issue in our issues feed. You could use label,
    # canned_query and others just the same.
    query = gdata.projecthosting.client.Query(label='label0')
    feed = self.client.get_issues(self.project_name, query=query)

    # Make sure we at least find the entry we created with that label.
    self.assert_(len(feed.entry) > 0)

    for issue in feed.entry:
      label_texts = [label.text for label in issue.label]
      self.assert_('label0' in label_texts, 'Issue does not have label label0')

  def test_get_comments(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_create_update_delete')

    # Create an issue so we have something to look up.
    created = self.create_issue()

    # The fully qualified id is a url, we just want the number.
    issue_id = created.id.text.split('/')[-1]

    # Now lets add two comments to that issue.
    for i in range(2):
      update_response = self.client.update_issue(
          self.project_name,
          issue_id,
          self.owner,
          comment='My comment here %s' % i)

    # We have an issue that has several comments. Lets get them.
    comments_feed = self.client.get_comments(self.project_name, issue_id)

    # It has 2 comments.
    self.assertEqual(2, len(comments_feed.entry))


class ProjectHostingDocExamplesTest(unittest.TestCase):

  def setUp(self):
    self.project_name = conf.options.get_value('project_name')
    self.assignee = conf.options.get_value('issue_assignee')
    self.owner = conf.options.get_value('username')
    self.password = conf.options.get_value('password')

  def test_doc_examples(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    issues_client = gdata.projecthosting.client.ProjectHostingClient()

    self.authenticating_client(issues_client, self.owner, self.password)

    issue = self.creating_issues(issues_client, self.project_name, self.owner)
    issue_id = issue.id.text.split('/')[-1]

    self.retrieving_all_issues(issues_client, self.project_name)
    self.retrieving_issues_using_query_parameters(
        issues_client,
        self.project_name)
    self.modifying_an_issue_or_creating_issue_comments(
        issues_client,
        self.project_name,
        issue_id,
        self.owner,
        self.assignee)
    self.retrieving_issues_comments_for_an_issue(
        issues_client,
        self.project_name,
        issue_id)

  def authenticating_client(self, client, username, password):
    return client.client_login(
        username,
        password,
        source='your-client-name',
        service='code')

  def creating_issues(self, client, project_name, owner):
    """Create an issue."""
    return client.add_issue(
        project_name,
        'my title',
        'my summary',
        owner,
        labels=['label0'])

  def retrieving_all_issues(self, client, project_name):
    """Retrieve all the issues in a project."""
    feed = client.get_issues(project_name)
    for issue in feed.entry:
      self.assert_(issue.title.text is not None)

  def retrieving_issues_using_query_parameters(self, client, project_name):
    """Retrieve a set of issues in a project."""
    query = gdata.projecthosting.client.Query(label='label0', max_results=1000)
    feed = client.get_issues(project_name, query=query)
    for issue in feed.entry:
      self.assert_(issue.title.text is not None)
    return feed

  def retrieving_issues_comments_for_an_issue(self, client, project_name,
                                              issue_id):
    """Retrieve all issue comments for an issue."""
    comments_feed = client.get_comments(project_name, issue_id)
    for comment in comments_feed.entry:
      self.assert_(comment.content is not None)
    return comments_feed

  def modifying_an_issue_or_creating_issue_comments(self, client, project_name,
                                                    issue_id, owner, assignee):
    """Add a comment and update metadata in an issue."""
    return client.update_issue(
        project_name,
        issue_id,
        owner,
        comment='My comment here.',
        summary='New Summary',
        status='Accepted',
        owner=assignee,
        labels=['-label0', 'label1'],
        ccs=[owner])


def suite():
  return conf.build_suite([ProjectHostingClientTest,
                           ProjectHostingDocExamplesTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
