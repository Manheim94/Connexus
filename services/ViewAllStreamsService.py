from services import ops
import webapp2
import json


class ViewAllStreamsServiceHandler(webapp2.RequestHandler):
    def get(self):
        # TODO: a new method to return all streams and their cover photo list of dict
        all_stream_list = ops.get_all_stream()
        return_info = {
            'all_stream_list': all_stream_list
        }
        self.response.content_type = 'text/html'
        self.response.write(json.dumps(return_info))
