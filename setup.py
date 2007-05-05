#!/usr/bin/python
#
# Copyright (C) 2006 Google Inc.
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


#from setuptools import setup, find_packages
from distutils.core import setup


setup(
    name='gdata.py',
    version='1.0.2',
    description='Python client library for Google data APIs',
    long_description = """\
The Google data Python client library makes it easy to access data
through the Google data APIs. This library provides data model and
service modules for the Google Calendar data API, Google Spreadsheets
data API, Google Base data API, core Google data API functionality and
the Atom Publishing Protocol.
""",
    author='Jeffrey Scudder',
    author_email='api.jscudder@gmail.com',
    license='Apache 2.0',
    url='http://code.google.com/p/gdata-python-client/',
    packages=['atom', 'gdata', 'gdata.calendar', 'gdata.base',
        'gdata.spreadsheet'],
    package_dir = {'gdata':'src/gdata', 'atom':'src/atom'}
)
