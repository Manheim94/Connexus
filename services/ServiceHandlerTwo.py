from google.appengine.api import mail
import re
import ops
import webapp2
import json
from google.appengine.api import users


class CreateStreamServiceHandler(webapp2.RequestHandler):
    def post(self):
        user_id = self.request.get('user_id')  # from Zhangyi 'current_user' exactly
        name = self.request.get('name')  # from page
        cover_url = self.request.get('cover_url')  # from page    can be empty!
        subscribers = self.request.get('subscribers')  # from page
        message = self.request.get('message')  # from page
        tags = self.request.get('tags')  # from page

        '''stream already exits, return false'''
        if ops.stream_exists(name):
            return_info = {
                'status': False,
            }
            self.response.write(json.dumps(return_info))
            return

        tag_list = re.findall(r'#\w+', tags)
        sub_list = re.findall(r'[\w\.-]+@[\w\.-]+', subscribers)  # a list of emails

        '''send email'''
        mail.send_mail(sender=user_id,
                       to=sub_list,
                       subject='You have subscribed the stream: ' + name,
                       body=message
                       )

        '''create stream'''
        ops.create_stream(user_id, name, cover_url, sub_list, tag_list)
        return_info = {
            'status': True,
        }
        self.response.write(json.dumps(return_info))