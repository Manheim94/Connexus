from services import ops
import webapp2
import json


class ManageServiceHandler(webapp2.RequestHandler):
    def get(self, user_id):
        if not ops.pigeon_exists(user_id):  # if no such user, return two empty lists
            ops.add_new_user(user_id)  # TODO: construct a new method to add new user
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
