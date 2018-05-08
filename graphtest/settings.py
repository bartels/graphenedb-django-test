"""
Project settings file for graphtest

This is the bootstrap settings file. settings below are configurable using
environment variables. Most settings changes should not be made here but
instead in one of the proper settings files in the "config" directory.

config directory files:

    config/defaults.py:      base settings
    config/dev.py:           settings overrides for development
    config/production.py     settings overrides for production/deployment
    config/tests.py          settings overrides for test runner
    config/local.py          Not to be checked into version control, use for
                             private settings (e.g. passwords, SECRET_KEY, etc)

"""
from __future__ import absolute_import
import os
import environ
from django.core.exceptions import ImproperlyConfigured


# read environment vars from .env files
root = environ.Path(__file__) - 1
env_paths = [root('../../.env'), root('../.env')]
for env_path in env_paths:
    if os.path.exists(root(env_path)):
        environ.Env.read_env(env_path)

# import either production or dev settings
# Set environment variable DJANGO_ENV (defaults to dev)
# e.g. export DJANGO_ENV=production
ENVIRONMENT = environ.Env()('DJANGO_ENV', default='dev')
if ENVIRONMENT == 'dev':
    from .config.dev import *
else:
    from .config.production import *

# import any local settings
for config in ('local',):
    config_path = root('config/{0}.py'.format(config))
    try:
        exec(open(config_path).read())
    except IOError:
        pass

# Default environment settings
env = environ.Env(
        DEBUG=(bool, DEBUG),
        GRAPHENEDB_USER=(str, locals().get('GRAPHENEDB_USER', '')),
        GRAPHENEDB_PASS=(str, locals().get('GRAPHENEDB_PASS', '')),
    )

# deubg
DEBUG = env("DEBUG")

# secret key
try:
    SECRET_KEY = env('SECRET_KEY')
except ImproperlyConfigured:
    SECRET_KEY = locals().get('SECRET_KEY', None)
    if SECRET_KEY is None:
        if ENVIRONMENT == 'dev':
            SECRET_KEY = '__SECRET_KEY__'
        else:
            raise

# Databases
try:
    DATABASES = {
        'default': env.db()
    }
except ImproperlyConfigured:
    if locals().get('DATABASES') is None:
        raise

# Caches
try:
    default_cache = env.cache()
    if locals().get('CACHES'):
        for key, val in default_cache.items():
            if val:
                if key == 'OPTIONS' and key in CACHES['default']:
                    CACHES['default'][key].update({key: val})
                else:
                    CACHES['default'][key] = val
    else:
        CACHES = {
            'default': default_cache
        }
except ImproperlyConfigured:
    if locals().get('CACHES') is None:
        raise


# AWS credientials
GRAPHENEDB_USER = env('GRAPHENEDB_USER')
GRAPHENEDB_PASS = env('GRAPHENEDB_PASS')
