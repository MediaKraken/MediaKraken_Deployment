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

from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime
from elasticsearch import Elasticsearch


class CommonElasticsearch(object):
    """
    Class for interfacing with Elasticsearch
    """

    def __init__(self, index_type='MediaKraken', es_host='mkelk'):
        self.es_inst = Elasticsearch([{'host': es_host, 'port': 9200}])
        self.es_index = index_type

    def com_elastic_index(self, log_type, body_data):
        self.es_inst.index(index=self.es_index, doc_type='MediaKraken',
                           body={"text": {"type": log_type, "data": body_data, "timestamp":
                               datetime.now()}})

    def com_elastic_get(self, id):
        self.es_inst.get(index=self.es_index, doc_type='MediaKraken', id=id)
