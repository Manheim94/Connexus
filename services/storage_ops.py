import lib.cloudstorage as gcs
import os
from google.appengine.api import app_identity


def create_stream_in_storage(self, stream_name):
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

def upload_photo_in_storage(self, stream_id, photo):
    bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Demo GCS Application running from Version: '
                        + os.environ['CURRENT_VERSION_ID'] + '\n')
    self.response.write('Using bucket name: ' + bucket_name + '\n\n')
    bucket = '/' + bucket_name
    filename = bucket + '/' + str(stream_id) + "/" + photo

    self.response.write('Creating file %s\n' % filename)
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(filename, 'w',
                        options={'x-goog-meta-foo': 'foo', 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    gcs_file.close()
