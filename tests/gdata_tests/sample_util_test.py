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


__author__ = 'j.s@google.com (Jeff Scudder)'


import unittest
import sys
import gdata.sample_util


class SettingsUtilTest(unittest.TestCase):

  def setUp(self):
    self.settings = gdata.sample_util.SettingsUtil()

  def test_get_param(self):
    self.assert_(self.settings.get_param('missing', ask=False) is None)
    self.settings.prefs['x'] = 'something'
    self.assertEqual(self.settings.get_param('x'), 'something')
  
  def test_get_param_from_command_line_arg(self):
    self.assert_('x' not in self.settings.prefs)
    self.assert_(self.settings.get_param('x', ask=False) is None)
    sys.argv.append('--x=something')
    self.assertEqual(self.settings.get_param('x'), 'something')
    self.assert_('x' not in self.settings.prefs)
    self.assert_('y' not in self.settings.prefs)
    self.assert_(self.settings.get_param('y', ask=False) is None)
    sys.argv.append('--y')
    sys.argv.append('other')
    self.assertEqual(self.settings.get_param('y', reuse=True), 'other')
    self.assertEqual(self.settings.prefs['y'], 'other')


def suite():
  return conf.build_suite([SettingsUtilTest])


if __name__ == '__main__':
  unittest.main()
