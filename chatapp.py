import os
import webapp2

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext.webapp import template

import models


class MainPage(webapp2.RequestHandler):
    RESET_COUNT = 100
    
    def get(self):
        # Called when the app is loaded. Randomly generates
        # a username from the combination of values available
        # in the database and if the resulting name is
        # not in use, templates it to the app.
        nickname = None
        count = 0
        
        while models.User.isNotAvailable(nickname):
          prefix = models.Prefix.getRandom()
          body = models.Body.getRandom()
          suffix = models.Suffix.getRandom()

          nickname = prefix + body + suffix
          count = count + 1
          
          # If 100 instances are called unsuccessfully
          # reset the User datastore and deal with the
          # consequences. 
          if count > RESET_COUNT:
              models.User.reset()
              count = 0
        
        # Claim the name and return templated html      
        models.User.claim(nickname)      
        template_values = {'nickname': nickname}            
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class DisconnectHandler(webapp2.RequestHandler):
  def post(self):
    # Called when any instance of the chatapp is "unloaded".
    # The username the app was using gets flagged as false
    # to show that it is available.
    nickname = self.request.get('from')
    models.User.release(nickname)
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