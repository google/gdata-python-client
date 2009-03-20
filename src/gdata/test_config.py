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

import gdata.test_config_template

"""Loads configuration for tests which connect to Google servers.

The test_config_template.py is an example of the settings used in the tests.
Copy the test_config_template and insert your own values if you want to run
the tests which communicate with the servers. Change the import above and 
settings assignment below to use your own test configuration.
"""

settings = gdata.test_config_template
