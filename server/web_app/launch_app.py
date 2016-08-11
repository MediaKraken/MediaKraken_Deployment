# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import sys
import os

BASE_DIR = os.path.join(os.path.dirname(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from MediaKraken.app import create_app

sys.path.append("../../MediaKraken_Common")
import MK_Common_Logging

# start logging
MK_Common_Logging.MK_Common_Logging_Start('../log/MediaKraken_WebApp')
logging.info('Creating webapp instance')
# defaults to PROD config
application = create_app()
