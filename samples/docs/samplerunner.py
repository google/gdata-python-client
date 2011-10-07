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

"""Sample running boilerplate."""

__author__ = 'afshar@google.com (Ali Afshar)'


def Run(source_file):
  """Load a source file and run a sample from it."""
  source = open(source_file).read()
  global_dict = {'__file__': source_file}
  exec source in global_dict
  samples = [global_dict[k] for k in global_dict if k.endswith('Sample')]
  lines = source.splitlines()
  for i, sample in enumerate(samples):
    print str(i).rjust(2), sample.__name__, '-', sample.__doc__
  try:
    i = int(raw_input('Select sample: ').strip())
    sample = samples[i]
    print '-' * 80
    print 'def', '%s():' % sample.__name__
    # print each line until a blank one (or eof).
    for line in lines[sample.func_code.co_firstlineno:]:
      if not line:
        break
      print line
    print '-' * 80
    sample()
  except (ValueError, IndexError):
    print 'Bad selection.'
