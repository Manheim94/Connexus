
import webapp2
from google.appengine.api import users
from config import utils
from google.appengine.api import urlfetch
import json
import urllib

class SearchStreamHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.render()

    def render(self):
        data = {}
        logout_url = users.create_logout_url(utils.raw_logout_url)
        current_user = users.get_current_user().email()
        searchword=self.request.get('searchword')
        if(searchword!=""):
            try:
                rpc = urlfetch.create_rpc()
                request = {}
                request['user_id'] = current_user
                request['searchword'] = searchword
                url= 'https://services-dot-hallowed-forge-181415.appspot.com/service-search?' + urllib.urlencode(request)

                urlfetch.make_fetch_call(rpc, url)
                response = rpc.get_result()
                data = json.loads(response.content)

            except Exception:
                self.response.write("Error!<br>")
                self.response.write(Exception)

            stream_list=data['stream_list']
        else:
            stream_list=""

        logout_url = users.create_logout_url(utils.raw_logout_url)
        search_send_request_handler_url= "/search" #"/search_send_request_handler_url"

        template_values = {
            'logout_url': logout_url,
            'current_user': current_user,
            'stream_list':stream_list,
            'searchword': searchword,
            'search_send_request_handler_url':search_send_request_handler_url
        }


        template = utils.JINJA_ENVIRONMENT.get_template('fresh_search_streams.html')
        self.response.write(template.render(template_values))

class SearchSendRequestHandler(webapp2.RequestHandler):
    def get(self):
        pass
