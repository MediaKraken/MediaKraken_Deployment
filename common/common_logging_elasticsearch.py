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

    def __init__(self, index_type='MediaKraken'):
        self.es_inst = Elasticsearch([{'host': 'mkelk', 'port': 9200}])
        self.es_index = index_type
        self.id = 0

    def com_elastic_index(self, doc_type, body_data):
        self.id += 1
        self.es_inst.index(index=self.es_index, doc_type=doc_type, id=self.id,
                           body={"log": body_data, "timestamp": datetime.now()})

    def com_elastic_get(self, doc_type, id):
        self.es_inst.get(index=self.es_index, doc_type=doc_type, id=id)
