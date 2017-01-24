# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
os_env = os.environ
import sys
sys.path.append('..')
from common import common_file


class Config(object):
    if os.path.exists('web_secret_key_debug.txt'):
        pass
    else:
        data = os.urandom(24).encode('hex')
        common_file.com_file_save_data('web_secret_key_debug.txt', data, False)
    SECRET_KEY = os_env.get('WEBLOG_SECRET',
        common_file.com_file_load_data('web_secret_key_debug.txt', False))
    APP_DIR = os.path.abspath(os.path.dirname(__file__)) # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple' # Can be "memcached", "redis", etc.


#class DevConfig(Config): # for flipping to debug
class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'\
        + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'user.db')
    DEBUG_TB_ENABLED = False # Disable Debug toolbar


#class ProdConfig(Config): # for flipping to debug
class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'\
        + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'user.db')
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True # Don't bundle/minify static assets
    CACHE_TYPE = 'simple' # Can be "memcached", "redis", etc.
