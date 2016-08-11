# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
os_env = os.environ
import sys
sys.path.append('./MediaKraken_Common')
sys.path.append('../MediaKraken_Common')
sys.path.append('../../MediaKraken_Common')
import MK_Common_File

# pull in the ini file config
import ConfigParser
ConfigFile = ConfigParser.ConfigParser()
ConfigFile.read("../MediaKraken.ini")

class Config(object):
    if os.path.exists('web_secret_key.txt'):
        pass
    else:
        data = os.urandom(24).encode('hex')
        MK_Common_File.MK_Common_File_Save_Data('web_secret_key.txt', data, False)
    SECRET_KEY = os_env.get('METAMAN_SECRET', MK_Common_File.MK_Common_File_Load_Data('web_secret_key.txt', False))
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


#class DevConfig(Config):
class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://' + ConfigFile.get('DB Connections','PostDBUser') + ':' + ConfigFile.get('DB Connections','PostDBPass').strip() + '@' + ConfigFile.get('DB Connections','PostDBHost').strip() + '/' + ConfigFile.get('DB Connections','PostDBName').strip()
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


#class ProdConfig(Config):
class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://' + ConfigFile.get('DB Connections','PostDBUser') + ':' + ConfigFile.get('DB Connections','PostDBPass').strip() + '@' + ConfigFile.get('DB Connections','PostDBHost').strip() + '/' + ConfigFile.get('DB Connections','PostDBName').strip()
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
