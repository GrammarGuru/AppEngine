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


def delete_all(bucket):
    for stat in gcs.listbucket(bucket):
        gcs.delete(stat.filename)


def get_files(bucket):
    stats = gcs.listbucket(bucket)
    result = {}
    for stat in stats:
        pointer = result
        path = stat.filename.split('/')
        title = path[-1]
        for dir in path[2:-1]:
            if dir not in pointer:
                pointer[dir] = {}
            pointer = pointer[dir]

        pointer[title] = True
    return result


def get_filename(filename=None):
    bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
    if filename is not None:
        return '/{}/{}'.format(bucket_name, filename)
    return '/{}'.format(bucket_name)
