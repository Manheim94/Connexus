# Database information should be put in here

import os
import jinja2

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)

raw_logout_url = '/'