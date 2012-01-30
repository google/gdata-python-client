import Cookie
import os

from common.appengine_utilities import sessions


class SessionMiddleware(object):
    TEST_COOKIE_NAME = 'testcookie'
    TEST_COOKIE_VALUE = 'worked'

    def process_request(self, request):
        """
        Check to see if a valid session token exists, if not,
        then use a cookie only session. It's up to the application
        to convert the session to a datastore session. Once this
        has been done, the session will continue to use the datastore
        unless the writer is set to "cookie".

        Setting the session to use the datastore is as easy as resetting
        request.session anywhere if your application.

        Example:
            from common.appengine_utilities import sessions
            request.session = sessions.Session()
        """
        self.request = request
        if sessions.Session.check_token():
            request.session = sessions.Session()
        else:
            request.session = sessions.Session(writer="cookie")
        request.session.set_test_cookie = self.set_test_cookie
        request.session.test_cookie_worked = self.test_cookie_worked
        request.session.delete_test_cookie = self.delete_test_cookie
        request.session.save = self.save
        return None

    def set_test_cookie(self):
        string_cookie = os.environ.get('HTTP_COOKIE', '')

        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)
        self.cookie[self.TEST_COOKIE_NAME] = self.TEST_COOKIE_VALUE
        print self.cookie

    def test_cookie_worked(self):
        string_cookie = os.environ.get('HTTP_COOKIE', '')

        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)

        return self.cookie.get(self.TEST_COOKIE_NAME)

    def delete_test_cookie(self):
        string_cookie = os.environ.get('HTTP_COOKIE', '')

        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)
        self.cookie[self.TEST_COOKIE_NAME] = ''
        self.cookie[self.TEST_COOKIE_NAME]['path'] = '/'
        self.cookie[self.TEST_COOKIE_NAME]['expires'] = 0

    def save(self):
        self.request.session = sessions.Session()

    def process_response(self, request, response):
        if hasattr(request, "session"):
            response.cookies= request.session.output_cookie
        return response
