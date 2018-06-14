# -*- coding: utf-8 -*-

import os

os_env = os.environ
import sys

sys.path.append('..')
from common import common_file


class Config(object):
    if os.path.exists('/mediakraken/key/web_secret_key.txt'):
        pass
    else:
        common_file.com_file_save_data('/mediakraken/key/web_secret_key.txt',
                                       os.urandom(24).encode('hex'), False)
    SECRET_KEY = os_env.get('MEDIAKRAKEN_SECRET',
                            common_file.com_file_load_data('/mediakraken/key/web_secret_key.txt',
                                                           False))
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://" + os.environ['POSTGRES_USER'] + ":" \
                              + os.environ['POSTGRES_PASSWORD'] + "@mkpgbounce:6432/" \
                              + os.environ['POSTGRES_DB']
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    FLASK_PIKA_PARAMS = {
        'host': 'mkrabbitmq',  # amqp.server.com
        'username': 'guest',  # convenience param for username
        'password': 'guest',  # convenience param for password
        'port': 5672  # amqp server port
    }
    FLASK_PIKA_POOL_PARAMS = {
        'pool_size': 8,
        'pool_recycle': 600
    }
