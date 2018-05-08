"""
Settings for use in development environment.
"""
import environ
from .defaults import *

DEBUG = True

# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS = (
    '.localhost',
)

# Temp folders
TEMP_DIR = root('../tmp')
FILE_UPLOAD_TEMP_DIR = TEMP_DIR

# Cache Setup
CACHE_TIMEOUT = 60 * 10
CACHE_PREFIX = 'GRAPHTEST'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'graphtest-cache',
        'KEY_PREFIX': CACHE_PREFIX,
        'TIMEOUT': CACHE_TIMEOUT,
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
        },
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
CACHE_MIDDLEWARE_SECONDS = CACHE_TIMEOUT
CACHE_MIDDLEWARE_KEY_PREFIX = CACHE_PREFIX

# dummy images for sorl
THUMBNAIL_DUMMY = True
THUMBNAIL_DUMMY_SOURCE = 'http://placeholder.pics/svg/%(width)sx%(height)s/FFF/AAA'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = environ.Path(TEMP_DIR)('emails')
DEFAULT_FROM_EMAIL = '<ebartels@gmail.com>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# logging
LOGGING['loggers'].update({
    'graphtest': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
    },
})

# webpack
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundle/',
        'STATS_FILE': root('../static/bundle/webpack-stats.json'),
    },
}
