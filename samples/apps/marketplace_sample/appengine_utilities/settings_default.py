"""
Copyright (c) 2008, appengine-utilities project
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the appengine-utilities project nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__="jbowman"
__date__ ="$Sep 11, 2009 4:20:11 PM$"


# Configuration settings for the session class.
session = {    
    "COOKIE_NAME": "gaeutilities_session",
    "DEFAULT_COOKIE_PATH": "/",
    "DEFAULT_COOKIE_DOMAIN": False, # Set to False if you do not want this value
                                    # set on the cookie, otherwise put the
                                    # domain value you wish used.
    "SESSION_EXPIRE_TIME": 7200,    # sessions are valid for 7200 seconds
                                    # (2 hours)
    "INTEGRATE_FLASH": True,        # integrate functionality from flash module?
    "SET_COOKIE_EXPIRES": True,     # Set to True to add expiration field to
                                    # cookie
    "WRITER":"datastore",           # Use the datastore writer by default. 
                                    # cookie is the other option.
    "CLEAN_CHECK_PERCENT": 50,      # By default, 50% of all requests will clean
                                    # the datastore of expired sessions
    "CHECK_IP": True,               # validate sessions by IP
    "CHECK_USER_AGENT": True,       # validate sessions by user agent
    "SESSION_TOKEN_TTL": 5,         # Number of seconds a session token is valid
                                    # for.
    "UPDATE_LAST_ACTIVITY": 60,     # Number of seconds that may pass before
                                    # last_activity is updated
}

# Configuration settings for the cache class
cache = {
    "DEFAULT_TIMEOUT": 3600, # cache expires after one hour (3600 sec)
    "CLEAN_CHECK_PERCENT": 50, # 50% of all requests will clean the database
    "MAX_HITS_TO_CLEAN": 20, # the maximum number of cache hits to clean
}

# Configuration settings for the flash class
flash = {
    "COOKIE_NAME": "appengine-utilities-flash",
}

# Configuration settings for the paginator class
paginator = {
    "DEFAULT_COUNT": 10,
    "CACHE": 10,
    "DEFAULT_SORT_ORDER": "ASC",
}

rotmodel = {
    "RETRY_ATTEMPTS": 3,
    "RETRY_INTERVAL": .2,
}
if __name__ == "__main__":
    print "Hello World";

