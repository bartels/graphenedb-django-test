"""
Settings for use in production.
"""
import os
from .defaults import *

DEBUG = False

MANAGERS = list(MANAGERS) + [
    # Add any extra email addresses
]

ALLOWED_HOSTS = (
)

# Temp folders
TEMP_DIR = '/tmp/'
FILE_UPLOAD_TEMP_DIR = TEMP_DIR

# AWS Storage Settings
AWS_STORAGE_BUCKET_NAME = 'graphtest-media-w2'
AWS_S3_HOST = 's3-us-west-2.amazonaws.com'
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = False
AWS_HEADERS = {
    'Cache-Control': 'max-age=864000',
}

# File Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIA_ROOT = os.path.join(TEMP_DIR, 'media')
MEDIA_URL = 'https://graphtest-media-w2.s3-us-west-2.amazonaws.com/'

STATIC_ROOT = root('../../htdocs/static')
STATIC_URL = '/s/'

# This fixes performance problems with sorl-thumbnail when used with s3
THUMBNAIL_FORCE_OVERWRITE = True

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundle/',
        'STATS_FILE': os.path.join(STATIC_ROOT, 'bundle/webpack-stats.json'),
    },
}
