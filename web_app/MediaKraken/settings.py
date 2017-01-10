# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
os_env = os.environ
import sys
sys.path.append('..')
from common import common_file


class Config(object):
    if os.path.exists('web_secret_key.txt'):
        pass
    else:
        data = os.urandom(24).encode('hex')
        common_file.com_file_save_data('web_secret_key.txt', data, False)
    SECRET_KEY = os_env.get('MEDIAKRAKEN_SECRET',\
        common_file.com_file_load_data('web_secret_key.txt', False))
    APP_DIR = os.path.abspath(os.path.dirname(__file__)) # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple' # Can be "memcached", "redis", etc.


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://metamanpg:"\
        + os.environ['POSTGRES_PASSWORD'] + "@mkdatabase/metamandb"
    DEBUG_TB_ENABLED = False # Disable Debug toolbar
