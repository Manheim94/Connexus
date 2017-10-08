import webapp2
from google.appengine.api import urlfetch

class CallCron(webapp2.RequestHandler):
    def get(self):
        rpc = urlfetch.create_rpc()
        url = 'services-dot-pigeonhole-apt.appspot.com/service-cron'
        urlfetch.make_fetch_call(rpc, url)
