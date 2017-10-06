
import webapp2
from google.appengine.api import users
from config import utils
from google.appengine.api import urlfetch
import urllib
import json

class ViewTrendingStreamHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.render()

    def render(self):
        data = {}
        logout_url = users.create_logout_url(utils.raw_logout_url)
        current_user = users.get_current_user().email()

        try:
            rpc = urlfetch.create_rpc()
            request = {}
            request['user_id'] = current_user
            #request['stream_id'] = stream_id
            url= 'https://services-dot-hallowed-forge-181415.appspot.com/service-treanding?' + urllib.urlencode(request)

            urlfetch.make_fetch_call(rpc, url)
            response = rpc.get_result()
            data = json.loads(response.content)

        except Exception:
            self.response.write("Error!<br>")
            self.response.write(Exception)

        stream_list=data['trending']
        ratenum= data['rate']
        ratedict = {-1: "no", 1: "5min", 12: "1hour", 288: "1day"}
        rate = ratedict[ratenum]

        for stream in stream_list:
            stream['url']="/view_single?stream_id="+stream['Name']
        logout_url = users.create_logout_url(utils.raw_logout_url)
        view_trending_update_rate_handler_url="/view_trending_update_rate_handler_url"

        template_values = {
            'logout_url': logout_url,
            'current_user': current_user,
            'stream_list':stream_list,
            'view_trending_update_rate_handler_url':view_trending_update_rate_handler_url,
            'rate':rate
        }


        template = utils.JINJA_ENVIRONMENT.get_template('fresh_trending_streams.html')
        self.response.write(template.render(template_values))

class ViewTrendingUpdateRateHandler(webapp2.RequestHandler):
    def get(self):
        rate=self.request.get('rate')

        current_user = users.get_current_user().email()
        data={}
        try:
            rpc = urlfetch.create_rpc()
            request = {}
            request['user_id'] = current_user
            request['rate'] = rate
            url = 'https://services-dot-hallowed-forge-181415.appspot.com/service-cron?' + urllib.urlencode(request)
            urlfetch.make_fetch_call(rpc, url)
            #response = rpc.get_result()
            #data = json.loads(response.content)

        except Exception:
            self.response.write("Error!<br>")
            self.response.write(Exception)

        self.redirect('/view_trending')