import webapp2
from google.appengine.api import users
from config import utils
from services.TestServiceHandler import TestServiceHandler
import json

from google.appengine.api import urlfetch
from google.appengine.api import app_identity
import urllib
import logging

class ManagePageHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.render()

    def render(self):

        #appName = app_identity.get_application_id()
        current_user = users.get_current_user().email()
        logout_url = users.create_logout_url(utils.raw_logout_url)
        data={}
        try:
            rpc = urlfetch.create_rpc()
            request = {}
            request['user_id'] = current_user
            url= 'https://services-dot-hallowed-forge-181415.appspot.com/service-manage?' + urllib.urlencode(request)

            #url = 'https://services-dot-' + appName + '.appspot.com?' + urllib.urlencode(request)
            urlfetch.make_fetch_call(rpc, url)
            response = rpc.get_result()
            data = json.loads(response.content)

        except Exception:
            self.response.write("Error!<br>")
            self.response.write(Exception)

        owned_stream_list=data['owned_stream_list']
        subed_stream_list=data['subed_stream_list']
        delete_owned_stream_handler_url="/delete_owned_stream_handler_url"
        unsubscribe_stream_handler_url="/unsubscribe_stream_handler_url"

        for stream in owned_stream_list:
            stream['url']="/view_single?stream_id="+ stream['Name']

        for stream in subed_stream_list:
            stream['url']="/view_single?stream_id="+ stream['Name']

        template_values = {
            'logout_url': logout_url,
            'current_user': current_user,
            'owned_stream_list': owned_stream_list,
            'subed_stream_list':subed_stream_list,
            'delete_owned_stream_handler_url': delete_owned_stream_handler_url,
            'unsubscribe_stream_handler_url': unsubscribe_stream_handler_url
        }

        template = utils.JINJA_ENVIRONMENT.get_template('fresh_manage.html')
        self.response.write(template.render(template_values))

class ManagePageDeleteHandler(webapp2.RequestHandler):
    #form_fields={}
    def post(self):

        delete_list=self.request.get_all('delete_owned')

        delete_pass_str=""
        for stream_name in delete_list:
            delete_pass_str+=stream_name
            delete_pass_str+=","
        delete_pass_str=delete_pass_str[:-1]

        form_fields={
            'delete_list': delete_pass_str
        }


        try:
            form_data = urllib.urlencode(form_fields)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            result = urlfetch.fetch(
                url='https://services-dot-hallowed-forge-181415.appspot.com/service-deletestream',
                payload=form_data,
                method=urlfetch.POST,
                headers=headers)
            self.response.write(result.content)
            self.redirect('/manage')

        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

class ManagePageUnsubscribeHandler(webapp2.RequestHandler):
    def post(self):
        current_user = users.get_current_user().email()
        unsubscribe_list= self.request.get_all('unsubscribe')

        unsubscribe_pass_str = ""
        for stream_name in unsubscribe_list:
            unsubscribe_pass_str += stream_name
            unsubscribe_pass_str += ","
            unsubscribe_pass_str = unsubscribe_pass_str[:-1]

        
        form_fields={
            'unsubscribe_list': unsubscribe_pass_str,
            'user_id': current_user
        }
        try:
            form_data = urllib.urlencode(form_fields)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            result = urlfetch.fetch(
                url='https://services-dot-hallowed-forge-181415.appspot.com/service-unsubscribestream', #need changing
                payload=form_data,
                method=urlfetch.POST,
                headers=headers)
            self.response.write(result.content)
            self.redirect('/manage')


        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
