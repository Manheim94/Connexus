#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

from handlers.ManagePageHandler import ManagePageHandler
from handlers.CreateNewStreamHandler import  CreateNewStreamPageHandler
from handlers.SearchStreamHandler import SearchStreamHandler
from handlers.ViewSingleStreamHandler import ViewSingleStreamHandler
from handlers.ViewAllStreamsHandler import ViewAllStreamsHandler
from handlers.ViewTrendingStreamHandler import ViewTrendingStreamHandler
from handlers.ErrorHandler import ErrorHandler
from handlers.ManagePageHandler import ManagePageDeleteHandler
from handlers.ManagePageHandler import ManagePageUnsubscribeHandler
from handlers.CreateNewStreamHandler import CreateNewStreamRequestHandler
from handlers.ViewSingleStreamHandler import UploadImageHandler

from config import utils
from google.appengine.api import users



class MainPage(webapp2.RequestHandler):
    def get(self):

        if users.get_current_user():
            login_url = '/manage'
            self.redirect(login_url)
        else:
            login_url = users.create_login_url('/manage')

        template_values = {
            'login_url': login_url,
        }

        template = utils.JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/manage', ManagePageHandler),
    ('/create', CreateNewStreamPageHandler),
    ('/view_single', ViewSingleStreamHandler),
    ('/view_all', ViewAllStreamsHandler),
    ('/search', SearchStreamHandler),
    ('/view_trending', ViewTrendingStreamHandler),
    ('/error', ErrorHandler),
    ('/delete_owned_stream_handler_url', ManagePageDeleteHandler),
    ('/unsubscribe_stream_handler_url',ManagePageUnsubscribeHandler),
    ('/create_stream_url',CreateNewStreamRequestHandler),
    ('/upload_image_handler_url',UploadImageHandler)

], debug=True)

def main():
    app.run()


if __name__ == '__main__':
    main()