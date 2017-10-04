

import webapp2
from google.appengine.api import users
from config import utils
import urllib
from google.appengine.api import urlfetch
import logging
import json

class CreateNewStreamPageHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.render()

    def render(self):
        current_user = users.get_current_user().email()
        logout_url = users.create_logout_url(utils.raw_logout_url)
        create_stream_url="/create_stream_url"
        template_values = {
            'logout_url': logout_url,
            'current_user': current_user,
            'create_stream_url':create_stream_url
        }
        template = utils.JINJA_ENVIRONMENT.get_template('fresh_create_stream.html')
        self.response.write(template.render(template_values))

class CreateNewStreamRequestHandler(webapp2.RequestHandler):
    form_fields={}
    def post(self):
        current_user = users.get_current_user().email()
        name= self.request.get('stream_name')
        cover_url= self.request.get('cover_url')
        subscribers = self.request.get('subscribers')
        message = self.request.get('message')
        tags = self.request.get('tags')

        form_fields={
            'user_id':current_user,
            'name': name,
            'cover_url':cover_url,
            'subscribers': subscribers,
            'message': message,
            'tags': tags
        }

        try:
            form_data = urllib.urlencode(form_fields)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            result = urlfetch.fetch(
                url='https://services-dot-hallowed-forge-181415.appspot.com/service-create', #need changing
                payload=form_data,
                method=urlfetch.POST,
                headers=headers)
            #self.response.write(type(result.content))
            returnvalue=json.loads(result.content)
            status=returnvalue['status']
            if(status==True):
                self.redirect('/view_single?stream_id='+name)
            else:
                self.redirect('')


        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
