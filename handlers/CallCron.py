import webapp2
from google.appengine.api import urlfetch

class CallCron(webapp2.RequestHandler):
    def get(self):
        rpc = urlfetch.create_rpc()
        url = 'https://services-dot-hallowed-forge-181415.appspot.com/service-cron'
        urlfetch.make_fetch_call(rpc, url)
