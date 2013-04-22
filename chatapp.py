import jinja2
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class MainPage(webapp2.RequestHandler):
    def get(self):
        username = 'placeholder'
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(username=username))

        

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
    ('/email', SendChatLog)
], debug=True)
