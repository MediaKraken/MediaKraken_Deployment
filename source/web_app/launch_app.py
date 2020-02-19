# -*- coding: utf-8 -*-


import os
import sys

BASE_DIR = os.path.join(os.path.dirname(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from MediaKraken.app import create_app
from common import common_global
from common import common_logging_elasticsearch

import gevent.monkey
import psycogreen.gevent

gevent.monkey.patch_all()
psycogreen.gevent.patch_psycopg()

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_webapp')
common_global.es_inst.com_elastic_index('info', {'stuff': 'Creating webapp instance'})
application = create_app()
