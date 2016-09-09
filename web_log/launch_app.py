# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import sys
import os

BASE_DIR = os.path.join(os.path.dirname(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from WebLog.app import create_app
from common import common_logging

# start logging
common_logging.com_logging_start('../log_debug/WebLog_WebApp')
logging.info('Creating weblog instance')
# defaults to PROD config
application = create_app()
