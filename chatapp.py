import os
import webapp2

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext.webapp import template

import models


class MainPage(webapp2.RequestHandler):
    def get(self):
        nickname = None
        count = 0
        while models.User.check(nickname):
          prefix = models.Prefix.get()
          body = models.Body.get()
          suffix = models.Suffix.get()

          nickname = prefix + body + suffix
          count = count + 1
          if count > 100:
              count = 0
              models.User.reset()
              
        template_values = {'nickname': nickname}            
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class DisconnectHandler(webapp2.RequestHandler):
  def post(self):
    # In the handler for _ah/channel/disconnected/
    nickname = self.request.get('from')
    models.User.set(nickname, False)
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
