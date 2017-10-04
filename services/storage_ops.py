import os

from google.appengine.api import app_identity

import lib.cloudstorage as gcs

from google.appengine.api import images


def create_stream_in_storage(stream_name):
    bucket = "/hallowed-forge-181415.appspot.com/"
    filename = bucket + str(stream_name) + "/"
    gcs_file = gcs.open(filename, 'w')
    gcs_file.close()
