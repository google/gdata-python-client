__author__ = 'wiktorgworek@google.com (Wiktor Gworek)'

import wsgiref.handlers

import atom
import os
import cgi
import gdata.blogger.service

from oauth import OAuthDanceHandler, OAuthHandler, requiresOAuth
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainHandler(OAuthHandler):
  """Main handler. If user is not logged in via OAuth it will display welcome
  page. In other case user's blogs on Blogger will be displayed."""

  def get(self):
    try:
      template_values = {'logged': self.client.has_access_token()}

      if template_values['logged']:
        feed = self.client.blogger.GetBlogFeed()
        blogs = []
        for entry in feed.entry:
          blogs.append({
            'id': entry.GetBlogId(),
            'title': entry.title.text,
            'link': entry.GetHtmlLink().href,
            'published': entry.published.text,
            'updated': entry.updated.text
          })
        template_values['blogs'] = blogs
    except gdata.service.RequestError, error:
      template_values['logged'] = False

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))


class NewPostHandler(OAuthHandler):
  """Handles AJAX POST request to create a new post on a blog."""

  @requiresOAuth
  def post(self):
    entry = atom.Entry(content=atom.Content(text=self.request.get('body')))
    self.client.blogger.AddPost(entry, blog_id=self.request.get('id'))

def main():
  application = webapp.WSGIApplication([
    (r'/oauth/(.*)', OAuthDanceHandler),
    ('/new_post', NewPostHandler),
    ('/', MainHandler),
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
