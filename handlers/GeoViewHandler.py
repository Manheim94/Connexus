
from datetime import timedelta, datetime
import random
import webapp2
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import urlfetch
import urllib
from config import utils
import json

class GeoViewHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            url = "/geo_view?stream_id=" + self.request.get("stream_id")
            self.redirect(users.create_login_url(url))
        else:
            self.render()

    def render(self):
        logout_url = users.create_logout_url(utils.raw_logout_url)
        current_user = users.get_current_user().email()
        image_info = self.getGeoViewImageInfo()

        template_values = {
            'logout_url': logout_url,
            'current_user': current_user,
            'image_info': image_info
        }

        template = utils.JINJA_ENVIRONMENT.get_template('geo_view.html')
        self.response.write(template.render(template_values))

    def getGeoViewImageInfo(self):
        data={}
        current_user = users.get_current_user().email()
        stream_id = self.request.get('stream_id')
        images_info = []
        currentTime = datetime.now()
        aYearAgo = currentTime - timedelta(days=365)
        try:
            rpc = urlfetch.create_rpc()
            request = {}
            request['user_id'] = current_user
            request['stream_id'] = stream_id
            request['page_range'] = 1
            url = 'https://services-dot-pigeonhole-apt.appspot.com/service-geoview?' + urllib.urlencode(request)
            urlfetch.make_fetch_call(rpc, url)
            response = rpc.get_result()
            data = json.loads(response.content)

        except Exception:
            self.response.write("Error!<br>")
            self.response.write(Exception)

        pict_list=data['pict_list']

        #self.response.write(pict_list)

        for image in pict_list:
            #createTime = str(image.upload_date)[:10] + 'T' + str(image.upload_date)[11:] + 'Z'

            createTime=str(image['img_date'])+'T'+'00:00:00Z'
            #self.response.write(createTime)

            lat = - 57.32652122521709 + 114.65304245043419 * random.random()
            lon = - 123.046875 + 246.09375 * random.random()

            # if aYearAgo <= date_object:
            images_info.append({
                "url": str(image['img_url']),
                "lon": lon,
                "lat": lat,
                "createTime": createTime
            })

        return images_info

