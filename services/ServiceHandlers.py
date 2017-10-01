import ops
import webapp2
import json
from google.appengine.api import images


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
        unicore_name = self.request.get('img_name')
        unicore_comment = self.request.get('img_comment')
        unicore = self.request.get('img')
        unicore = images.resize(unicore, 40, 40)  # all uploaded images have same size!
        unicore_url = "TODO: Gloud Storage Store the image and return a url"
        # ops.create_image(unicore_comment, unicore_name, unicore_url, stream_id)





service = webapp2.WSGIApplication([
    ('/service-manage', ManageServiceHandler),
    ('/service-viewallstreams', ViewAllStreamsServiceHandler),
    ('/service-viewsinglestream', ViewSingleStreamServiceHandler),
    ('/service-uploadimage', UploadImageServiceHandler)
], debug=True)
