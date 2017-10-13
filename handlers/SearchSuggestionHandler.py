import webapp2
from google.appengine.api import urlfetch
import urllib
import logging
import json

class SearchSuggetionHandler(webapp2.RequestHandler):
    def get(self):
        try:

            data={}
            rpc = urlfetch.create_rpc()
            request = {}
            request['searchContent'] = self.request.get('searchContent')
            url = 'https://services-dot-pigeonhole-apt.appspot.com/service-searchSuggestions?' + urllib.urlencode(request)


            #url = 'https://services-dot-' + appName + '.appspot.com?' + urllib.urlencode(request)
            urlfetch.make_fetch_call(rpc, url)
            response = rpc.get_result()

            #data = json.loads(response.content)

            self.response.write(response.content)


        except Exception:
            self.response.write("Error!<br>")
            self.response.write(Exception)
        return