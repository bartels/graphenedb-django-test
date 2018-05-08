"""
Default settings for graphtest project
"""
import environ

DEBUG = False

ADMINS = (
    ('Eric Bartels', 'ebartels@gmail.com'),
)
MANAGERS = ADMINS

# Project paths
root = environ.Path(__file__) - 2
BASE_DIR = BASE_PATH = root()

# Apps
INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader',
    'rest_framework',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'graphtest.urls'

WSGI_APPLICATION = 'graphtest.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/s/'
STATIC_ROOT = root('../../htdocs/static')
STATICFILES_DIRS = (
    root('../static'),
)

# Uploaded media & files
MEDIA_URL = '/m/'
MEDIA_ROOT = root('../../htdocs/media')
FILE_UPLOAD_PERMISSIONS = 0o664

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates'),
            # cms_root('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                # 'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

# Headers used by http proxy middleware
PROXY_HOST_HEADER = 'HTTP_X_FORWARDED_FOR'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'regular': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}

# Auth & Profiles
AUTHENTICATION_BACKENDS = (
    # uncomment to use Email as login
    # 'django.contrib.auth.backends.ModelBackend',
)

# DRF settings
REST_FRAMEWORK = {
    # 'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
}

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_ERRORS': False
}
