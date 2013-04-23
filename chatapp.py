import jinja2
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.ext.webapp import template

import models


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class MainPage(webapp2.RequestHandler):
    def get(self):
        name = None
        count = 0
        while models.User.check(name):
          prefix = models.Prefix.get()
          body = models.Body.get()
          suffix = models.Suffix.get()

          name = prefix + body + suffix
          count = count + 1
          if count > 100:
              count = 0
              models.User.reset()
              
        template_values = {'name': name}            
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class DisconnectHandler(webapp2.RequestHandler):
  def post(self):
    # In the handler for _ah/channel/disconnected/
    client_id = self.request.get('from')
    models.User.set(client_id, False)
    self.response.out.write('none')

class SendChatLog(webapp2.RequestHandler):
    def post(self):
        log = self.request.get('log')
        librarian = "UIUC Librarian <michaelkanglu@gmail.com>"
        title = "Your Chat History with UIUC Library"
        patron = "Patron <mengyalan@gmail.com>"
        # email = self.request.get('email')
        # nickname = self.request.get('nickname')
        # patron = nickname + ' <' + email + '>'
        message = mail.EmailMessage(sender=librarian, subject=title)
        
        message.to = patron
        message.html = log
        
        message.send()
        self.redirect('/')
        
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/disconnect/', DisconnectHandler),
    ('/email', SendChatLog)
], debug=True)
