import webapp2
from google.appengine.api import users
from config import utils
from services.TestServiceHandler import TestServiceHandler
import json

class ManagePageHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.render()

    def render(self):
        instance= TestServiceHandler()
        data= json.loads(instance.getJson())
        owned_stream_list= data['owned_stream_list']

        logout_url = users.create_logout_url(utils.raw_logout_url)

        current_user = users.get_current_user().email()

        template_values = {
            'logout_url': logout_url,
            'current_user': current_user,
            'owned_stream_list': owned_stream_list
        }

        template = utils.JINJA_ENVIRONMENT.get_template('fresh_manage.html')
        self.response.write(template.render(template_values))
