'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

import json
import os
from datetime import datetime

from elasticsearch import Elasticsearch


class CommonElasticsearch(object):
    """
    Class for interfacing with Elasticsearch
    """

    def __init__(self, index_type='mediakraken', es_host='mkelk', es_port=9200):
        try:
            # doing the try as the environment not set if run from command line
            if os.environ['DEBUG'] == 'True':
                self.debug = True
                self.es_inst = Elasticsearch([{'host': es_host, 'port': es_port}])
                self.es_index = index_type
            else:
                self.debug = False
        except:
            self.debug = False

    def com_elastic_index(self, log_type, body_data):
        if self.debug:
            try:
                self.es_inst.index(index=self.es_index, doc_type='MediaKraken',
                                   body={"text": {"type": log_type, "data": json.dumps(body_data),
                                                  "timestamp": datetime.now()}})
            except:
                print((log_type, body_data))

    def com_elastic_get(self, id):
        self.es_inst.get(index=self.es_index, doc_type='MediaKraken', id=id)
