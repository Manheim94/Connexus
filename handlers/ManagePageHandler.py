import webapp2
from google.appengine.api import users
from config import utils
from services.TestServiceHandler import TestServiceHandler
import json

from google.appengine.api import urlfetch
from google.appengine.api import app_identity
import urllib

class ManagePageHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.render()

    def render(self):

        appName = app_identity.get_application_id()
        current_user = users.get_current_user().email()
        logout_url = users.create_logout_url(utils.raw_logout_url)

        try:
            rpc = urlfetch.create_rpc()
            request = {}
            request['user_id'] = current_user
            request['stream_id'] = 'stream1'

            url = 'https://services.' + appName + '.appspot.com?' + urllib.urlencode(request)
            urlfetch.make_fetch_call(rpc, url)
            response = rpc.get_result()

        except Exception:
            self.response.write("General error!<br>")
            self.response.write(Exception)
        '''
        instance= TestServiceHandler()
        data= json.loads(instance.getJson())
        owned_stream_list= data['owned_stream_list']
        '''
        data= json.loads(response)
        owned_stream_list=data['owned_stream_list']

        template_values = {
            'logout_url': logout_url,
            'current_user': current_user,
            'owned_stream_list': owned_stream_list
        }

        template = utils.JINJA_ENVIRONMENT.get_template('fresh_manage.html')
        self.response.write(template.render(template_values))
