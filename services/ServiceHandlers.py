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
            owned_stream_list = [1, 2, 3]
            subed_stream_list = [4, 5, 6]
            # owned_stream_list = ops.get_self_stream(user_id)
            # subed_stream_list = ops.get_sub_stream(user_id)
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
        all_pict_list = ops.get_single_stream(stream_id)
        pict_list = []
        for i in range(min(page_range, len(all_pict_list))):
            pict_list[i] = all_pict_list[i]
        return_info = {
            'page_range': min(page_range, len(all_pict_list)),
            'pict_list': pict_list
        }
        self.response.write(json.dumps(return_info))


class UploadImageServiceHandler(webapp2.RequestHandler):
    def post(self):

        unicorn = self.request.get('img')
        img_name = self.request.get('img_name')
        stream_id = self.request.get('stream_id')
        img_comment = self.request.get('img_comment')

        unicorn = images.resize(unicorn, 500, 500)
        # find the right bucket-stream path
        b = "/hallowed-forge-181415.appspot.com/" + str(stream_id)

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
        unicorn_url = "https://storage.googleapis.com/hallowed-forge-181415.appspot.com/" \
                      + str(stream_id) + "/" + str(img_name) + ".png"
        # back to ndb server
        ops.create_image(img_comment, img_name, unicorn_url, stream_id)

        # redirect the user to the view single page
        self.redirect("https://www.pornhub.com")
        #webapp2.redirect("http://www.facebook.com")


class DeleteStreamServiceHandler(webapp2.RequestHandler):
    def post(self):
        delete_stream_list = self.request.POST['delete_list']
        # delete the stream list using map method
        map(ops.delete_stream, delete_stream_list)


class UnsubscribeStreamServiceHandler(webapp2.RequestHandler):
    def post(self):
        unsubscribe_stream_list = self.request.POST['unsubscribe_list']
        user_id = self.request.POST['']
        # unsubscribe needs three parameters, so using for
        for stream in unsubscribe_stream_list:
            ops.delete_subscription(user_id, stream)


service = webapp2.WSGIApplication([
    ('/service-manage', ManageServiceHandler),
    ('/service-viewallstreams', ViewAllStreamsServiceHandler),
    ('/service-viewsinglestream', ViewSingleStreamServiceHandler),
    ('/service-uploadimage', UploadImageServiceHandler),
    ('/service-create', ServiceHandlerTwo.CreateStreamServiceHandler),
    ('/service-createstream', CreateStreamServiceHandler),
    ('/service-deletestream', DeleteStreamServiceHandler),
    ('/service-unsubscribestream', UnsubscribeStreamServiceHandler)
], debug=True)
