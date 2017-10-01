import ops
import webapp2
import json


class ManageServiceHandler(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')  # 1 mistake
        if not ops.pigeon_exists(user_id):  # if no such user, return two empty lists
            ops.create_pigeon(user_id)
            owned_stream_list = []
            subed_stream_list = []
        else:  # if
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
        # TODO: a new method to return all streams and their cover photo list of dict
        all_stream_list = ops.get_all_stream()
        return_info = {
            'all_stream_list': all_stream_list
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))


# class ViewSingleStreamServiceHandler(webapp2.RequestHandler):
#     def get(self):
#         stream_id



service = webapp2.WSGIApplication([
    ('/service-manage', ManageServiceHandler),
    ('/service-viewallstreams', ViewAllStreamsServiceHandler),
    ('/service-viewsinglestream', ViewSingleStreamServiceHandler)
], debug=True)
