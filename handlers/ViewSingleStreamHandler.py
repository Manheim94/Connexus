

import webapp2
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import app_identity

from config import utils
import urllib


class ViewSingleStreamHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.render()

    def render(self):
        appName = app_identity.get_application_id()

        try:
            rpc = urlfetch.create_rpc()
            request={}
            request['user_id']=users.get_current_user().email()
            request['stream_id'] = 'stream1'

            url = 'https://services.' + appName + '.appspot.com?' + urllib.urlencode(request)
            urlfetch.make_fetch_call(rpc, url)
            response = rpc.get_result()

        except Exception:
            self.response.write("General error!<br>")
            self.response.write(Exception)



        logout_url = users.create_logout_url(utils.raw_logout_url)
        template_values = {
            'logout_url': logout_url,
            'current_user': 'haha'
        }
        template = utils.JINJA_ENVIRONMENT.get_template('fresh_manage.html')
        self.response.write(template.render(template_values))

