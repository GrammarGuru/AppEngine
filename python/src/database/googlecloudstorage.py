import cloudstorage as gcs
import os
from google.appengine.api import app_identity


def store(data, filename):
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(filename, 'w', content_type='text/plain', retry_params=write_retry_params)
    gcs_file.write(data)
    gcs_file.close()

    return data


def get(filename):
    gcs_file = gcs.open(filename)
    contents = gcs_file.read()
    gcs_file.close()
    return contents


def get_filename(filename):
    bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
    return '/{}/{}'.format(bucket_name, filename)
