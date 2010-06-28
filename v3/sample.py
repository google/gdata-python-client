# Copyright (C) 2010 Google Inc.
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

import apiclient
import oauth_wrap


def main():
  http = oauth_wrap.get_wrapped_http()
  p = apiclient.build('buzz', '1.0', http = http)
  activitylist = p.activities().list(scope='@self', userId='@me')
  print activitylist['items'][0]['title']


if __name__ == '__main__':
  main()
