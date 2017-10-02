import ops
import storage_ops
import webapp2
import json
from google.appengine.api import images
import ServiceHandlerTwo
import os
from google.appengine.api import app_identity
import lib.cloudstorage as gcs
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
    def get(self):
        stream_id = self.request.get('stream_id')
        unicorn_name = self.request.get('img_name')
        unicorn_comment = self.request.get('img_comment')
        unicorn = self.request.get('img')
        unicorn = images.resize(unicorn, 40, 40)  # all uploaded images have same size!

        unicorn_url = storage_ops.upload_photo_in_storage(stream_id, unicorn)
        ops.create_image(unicorn_comment, unicorn_name, unicorn_url, stream_id)


class CreateStreamServiceHandler(webapp2.RequestHandler):
    def get(self):
        stream_name = self.request.get('name')
        user_id = self.request.get('user_id')
        cover_url = self.request.get('cover_url')
        tag_list = self.request.get('tag_list')
        sub_list = self.request.get('sub_list')
        ops.create_stream(user_id, stream_name, cover_url, sub_list, tag_list)
        self.create_file(stream_name)

    def create_file(self, stream_name):
        bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Demo GCS Application running from Version: '
                            + os.environ['CURRENT_VERSION_ID'] + '\n')
        self.response.write('Using bucket name: ' + bucket_name + '\n\n')
        bucket = '/' + bucket_name
        filename = bucket + '/' + str(stream_name) + "/"

        self.response.write('Creating file %s\n' % filename)
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename, 'w',
                            options={'x-goog-meta-foo': 'foo', 'x-goog-meta-bar': 'bar'},
                            retry_params=write_retry_params)
        gcs_file.close()


class TestHandler(webapp2.RequestHandler):
    def get(self):
        stream_name = 'The_Shanghai_Photos'
        self.delete_file(stream_name)

    def create_file(self, stream_name):
        bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Demo GCS Application running from Version: '
                            + os.environ['CURRENT_VERSION_ID'] + '\n')
        self.response.write('Using bucket name: ' + bucket_name + '\n\n')
        bucket = '/' + bucket_name
        filename = bucket + '/' + str(stream_name) + "/"

        self.response.write('Creating file %s\n' % filename)
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename, 'w',
                            options={'x-goog-meta-foo': 'foo', 'x-goog-meta-bar': 'bar'},
                            retry_params=write_retry_params)
        gcs_file.close()

    def read_file(self, filename):
        self.response.write('Abbreviated file content (first line and last 1K):\n')

        gcs_file = gcs.open(filename)
        self.response.write(gcs_file.readline())
        gcs_file.seek(-1024, os.SEEK_END)
        self.response.write(gcs_file.read())
        gcs_file.close()


class DeleteStreamServiceHandler(webapp2.RequestHandler):
    def post(self):
        delete_stream_list = self.request.POST['delete_list']
        self.response.out.write("Yeah!")


service = webapp2.WSGIApplication([
    ('/service-manage', ManageServiceHandler),
    ('/service-viewallstreams', ViewAllStreamsServiceHandler),
    ('/service-viewsinglestream', ViewSingleStreamServiceHandler),
    ('/service-uploadimage', UploadImageServiceHandler),
    ('/service-create', ServiceHandlerTwo.CreateStreamServiceHandler)
    #('/service-uploadimage', UploadImageServiceHandler),
    ('/service-test', TestHandler),
    ('/service-createstream', CreateStreamServiceHandler),
    #('/service-deletestream', DeleteStreamServiceHandler)
    ('/service-deletestream', DeleteStreamServiceHandler)
], debug=True)
