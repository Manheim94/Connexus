import json
import os

import ServiceHandlerTwo
import ops
import storage_ops
import webapp2
from google.appengine.api import app_identity
from google.appengine.api import images

import lib.cloudstorage as gcs
import re

import random
import urllib



#from google.storage import speckle
#import cloudstorage as gcs

#from google.cloud import storage



class ManageServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')  # 1 mistake
        if not ops.pigeon_exists(user_id):  # if no such user, return two empty lists
            ops.create_pigeon(user_id)
            owned_stream_list = []
            subed_stream_list = []
        else:
            owned_stream_list = ops.get_self_stream(user_id)
            subed_stream_list = ops.get_sub_stream(user_id)
        return_info = {
            'owned_stream_list': owned_stream_list,
            'subed_stream_list': subed_stream_list
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class ViewAllStreamsServiceHandler(webapp2.RequestHandler):
    def get(self):
        all_stream_list = ops.get_all_stream()
        return_info = {
            'all_stream_list': all_stream_list
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class ViewSingleStreamServiceHandler(webapp2.RequestHandler):
    def get(self):
        stream_id = self.request.get('stream_id')
        page_range = self.request.get('page_range')
        user_id = self.request.get('user_id')

        # get all picts in stream
        all_pict_list = ops.get_single_stream(stream_id)

        # get the owner of the stream from the stream owner dict
        owner = ops.get_stream_owner(stream_id)["Id"]  # It's a dict, need to get the Id
        # check if the user is the owner of the stream
        is_owned = (owner == user_id)

        # get if the user subscribe this stream
        is_subed = ops.is_subscribed(stream_id, user_id)

        return_info = {
            'page_range': min(int(page_range), len(all_pict_list)),
            'pict_list': all_pict_list,
            'is_subed': is_subed,
            'is_owned': is_owned
        }
        self.response.write(json.dumps(return_info))


class SecreteUploadImageServiceHandler(webapp2.RequestHandler):
    def post(self):
        # Secrete handler for web image to upload, shush!
        # only get the img_url
        unicorn_url = self.request.get('img_url')
        img_name = self.request.get('img_name')
        stream_id = self.request.get('stream_id')
        img_comment = "comment"
        lon = float(self.request.get('lon'))
        lat = float(self.request.get('lat'))
        ops.create_image(img_comment, img_name, unicorn_url, stream_id, lon, lat)
        #self.redirect(str("https://pigeonhole-apt.appspot.com/view_single?stream_id=" + str(stream_id)))


class UploadImageServiceHandler(webapp2.RequestHandler):
    def post(self):
        unicorn = self.request.get('img')
        img_name = self.request.get('img_name')
        stream_id = self.request.get('stream_id')

        lon = float(self.request.get('lon'))
        lat = float(self.request.get('lat'))
        img_comment = "comment"

        unicorn = images.resize(unicorn, 500, 500)
        # find the right bucket-stream path
        b = "/pigeonhole-apt.appspot.com/" + str(stream_id)

        # much be post!
        img_real_name = self.request.POST['img'].filename
        pat = "(.+)\.(.+)"
        img_real_type = re.match(pat, str(img_real_name)).group(2)

        # construct a new content_type
        content_type_value = "image/" + str(img_real_type).lower()

        # create such file and write to it
        gcs_file = gcs.open(b + "/" + str(img_name) + "." + str(img_real_type), 'w', content_type=content_type_value)
        gcs_file.write(unicorn)
        gcs_file.close()

        # generate the public url
        # not test yet TODO: test the url
        unicorn_url = "https://storage.googleapis.com/pigeonhole-apt.appspot.com/" \
                      + str(stream_id) + "/" + str(img_name) + "." + str(img_real_type).lower()
        # back to ndb server
        ops.create_image(img_comment, img_name, unicorn_url, stream_id, lon, lat)

        # redirect the user to the view single page
        self.redirect(str("https://pigeonhole-apt.appspot.com/view_single?stream_id=" + str(stream_id)))
        #webapp2.redirect("http://www.facebook.com")


class DeleteStreamServiceHandler(webapp2.RequestHandler):
    def post(self):
        # url request is a list
        delete_stream_string = self.request.get('delete_list')
        delete_stream_list = delete_stream_string.split(',')
        # delete the stream list using map method
        # self.response.out.write(delete_stream_list[1]) error receive a string not a list

        # self.response.out.write(delete_stream_list[0])
        for stream in delete_stream_list:
            ops.delete_stream(str(stream))
            # delete the stream in the google cloud storage
            try:
                stream_path = "/pigeonhole-apt.appspot.com/" + str(stream) + "/"
                gcs.delete(stream_path)
            except gcs.NotFoundError:
                pass
        # map(ops.delete_stream, delete_stream_list)


class UnsubscribeStreamServiceHandler(webapp2.RequestHandler):
    def post(self):
        # unsubscribe_list is a string
        unsubscribe_stream_string = self.request.get('unsubscribe_list')
        # after split, get a list
        unsubscribe_stream_list = unsubscribe_stream_string.split(',')

        user_id = self.request.POST['user_id']

        # unsubscribe needs three parameters, so using for
        for stream in unsubscribe_stream_list:
            ops.delete_subscription(user_id, str(stream))


class SubscribeStreamServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        stream_id = self.request.get('stream_id')
        # only if the user has not subscribed this stream, the sub func can be executed
        if not ops.is_subscribed(stream_id, user_id):
            ops.create_subscription(user_id, stream_id)


class IFeelLuckyServiceHandler(webapp2.RequestHandler):
    def get(self):
        all_stream_list = ops.get_all_stream()
        lucky_stream_num = int(random.random() * len(all_stream_list))
        lucky_stream = all_stream_list[lucky_stream_num]
        return_info = {
            'lucky_stream': lucky_stream
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


class GeoViewServiceHandler(webapp2.RequestHandler):
    def get(self):
        stream_id = self.request.get('stream_id')

        # get all picts information in stream
        all_pict_list = ops.get_geoview_stream(stream_id)

        return_info = {
            'pict_list': all_pict_list,
        }
        self.response.write(json.dumps(return_info))


class ChromeServiceHandler(webapp2.RequestHandler):
    def post(self):
        unicorn_url = self.request.get('img_url')

        pat = "(.+)\.(.+)"
        img_name = re.match(pat, str(unicorn_url)).group(1)

        stream_id = "PigeonFamily"
        img_comment = "comment"
        lon = 0.0
        lat = 0.0
        ops.create_image(img_comment, img_name, unicorn_url, stream_id, lon, lat)


class GPSServiceHandler(webapp2.RequestHandler):
    def get(self):
        return_info = ops.get_gps_list()
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


service = webapp2.WSGIApplication([
    ('/service-manage', ManageServiceHandler),
    ('/service-viewallstreams', ViewAllStreamsServiceHandler),
    ('/service-viewsinglestream', ViewSingleStreamServiceHandler),
    ('/service-uploadimage', UploadImageServiceHandler),
    ('/service-create', ServiceHandlerTwo.CreateStreamServiceHandler),
    ('/service-deletestream', DeleteStreamServiceHandler),
    ('/service-unsubscribestream', UnsubscribeStreamServiceHandler),
    ('/service-search', ServiceHandlerTwo.SearchServiceHandler),
    ('/service-subscribestream', SubscribeStreamServiceHandler),
    ('/service-treanding', ServiceHandlerTwo.TrendingServiceHandler),
    ('/service-cron', ServiceHandlerTwo.CronServiceHandler),
    ('/service-lucky', IFeelLuckyServiceHandler),
    ('/service-setrate', ServiceHandlerTwo.SetDestinationService),
    ('/service-secretupload', SecreteUploadImageServiceHandler),
    ('/service-geoview', GeoViewServiceHandler),
    ('/service-searchSuggestions', ServiceHandlerTwo.GetSearchSuggestionService),
    ('/service-chrome', ChromeServiceHandler),
    ('/service-getgps', GPSServiceHandler)
], debug=True)
