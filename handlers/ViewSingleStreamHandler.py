

import webapp2
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import app_identity

from config import utils
import urllib
import json
import logging


class ViewSingleStreamHandler(webapp2.RequestHandler):
    stream_id=""
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            global stream_id
            stream_id = self.request.get('stream_id')
            self.increase_view_count()
            self.render()

    def increase_view_count(self): #do i need this?
        pass

    def render(self):
        #appName = app_identity.get_application_id()
        current_user = users.get_current_user().email()
        logout_url = users.create_logout_url(utils.raw_logout_url)
        data = {}

        try:
            rpc = urlfetch.create_rpc()
            request = {}
            request['user_id'] = current_user
            request['stream_id'] = ViewSingleStreamHandler.stream_id
            url= 'https://services-dot-hallowed-forge-181415.appspot.com/service-viewsinglestream?' + urllib.urlencode(request)

            urlfetch.make_fetch_call(rpc, url)
            response = rpc.get_result()
            data = json.loads(response.content)

        except Exception:
            self.response.write("Error!<br>")
            self.response.write(Exception)

        pict_list=data['pict_list']
        page_range=data['page_range']
        logout_url = users.create_logout_url(utils.raw_logout_url)
        upload_image_handler_url='/upload_image_handler_url'
        upload_image_servic_url='https://services-dot-hallowed-forge-181415.appspot.com/service-test'

        template_values = {
            'logout_url': logout_url,
            'current_user': current_user,
            'pict_list':pict_list,
            'page_range':page_range,
            'upload_image_handler_url':upload_image_servic_url
        }


        template = utils.JINJA_ENVIRONMENT.get_template('fresh_view_single_stream.html')
        self.response.write(template.render(template_values))

class UploadImageHandler(webapp2.RequestHandler):
    def post(self):
        current_user = users.get_current_user().email()
        img=self.request.get('img')
        img_comment=""
        img_name=self.request.get('img_name')
        form_fields = {
            'img': img,
            'img_comment':img_comment,
            'img_name':img_name,
            'user_id': current_user,
            'stream_id': ViewSingleStreamHandler.stream_id
        }
        try:
            form_data = urllib.urlencode(form_fields)
            headers = {}#{'Content-Type': 'multipart/form-data'}
            #headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            result = urlfetch.fetch(
                url='https://services-dot-hallowed-forge-181415.appspot.com/service-test',  # need changing
                payload=form_data,
                method=urlfetch.POST)
                #,headers=headers)
            self.response.write(result.content)
            self.redirect('/view_single')


        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
