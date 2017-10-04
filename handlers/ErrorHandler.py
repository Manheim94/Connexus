

import webapp2
from google.appengine.api import users
from config import utils

class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.render()

    def render(self):
        logout_url = users.create_logout_url(utils.raw_logout_url)
        current_user = users.get_current_user().email()
        create_url='/create'

        template_values = {
            'logout_url': logout_url,
            'current_user': current_user,
            'create_url': create_url
        }
        template = utils.JINJA_ENVIRONMENT.get_template('fresh_error.html')
        self.response.write(template.render(template_values))

