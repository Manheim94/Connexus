

import webapp2
from google.appengine.api import users
from support import settings

class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.render()

    def render(self):
        logout_url = users.create_logout_url(settings.raw_logout_url)
        template_values = {
            'logout_url': logout_url,
            'current_user': 'haha'
        }
        template = settings.JINJA_ENVIRONMENT.get_template('manage.html')
        self.response.write(template.render(template_values))

