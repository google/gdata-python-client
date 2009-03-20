#!/usr/bin/env python


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


"""Fill in this module with configuration data to use in tests.

See comments in the source code for explanations of the settings.
"""


# To actually run the tests which use this configuration information you must
# change RUN_LIVE_TESTS to True.
RUN_LIVE_TESTS = False


# If set to True, the client will save responses from the server and reuse
# them in future runs of the test.
CACHE_RESPONSES = True


GOOGLE_ACCOUNT_EMAIL = '<your email>'
GOOGLE_ACCOUNT_PASSWORD = '<your password>'


def blogger_email():
  """Provides email to log into the test Blogger account.
  
  By default uses GOOGLE_ACCOUNT_EMAIL, so edit this function if you have
  a Blogger-specific test account.
  """
  return GOOGLE_ACCOUNT_EMAIL


def blogger_password():
  """Provides password to log into the test Blogger account.
  
  By default uses GOOGLE_ACCOUNT_PASSWORD, so edit this function if you have
  a Blogger-specific test account.
  """
  return GOOGLE_ACCOUNT_PASSWORD


BLOGGER_CONFIG = {'title': 'A Test Post',
                  'content': 'This is a <b>test</b>.',
                  'blog_id': '<your test blog\'s id>',
                  'auth_token': None,
                  }
