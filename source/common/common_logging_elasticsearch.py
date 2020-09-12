"""
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
"""

import os
import sys
import time
from datetime import datetime

from elasticsearch import AsyncElasticsearch
from elasticsearch import Elasticsearch


class CommonElasticsearch:
    """
    Class for interfacing with Elasticsearch or docker logging directly
    """

    def __init__(self, index_type='mediakraken', es_host='th-elk-1.beaverbay.local',
                 es_port=9200, debug_override=None, async_mode=False):
        self.async_mode = async_mode
        if 'DEBUG' in os.environ and debug_override is None:
            self.debug = os.environ['DEBUG'].lower()
            if self.debug == 'es':
                if self.async_mode:
                    self.es_inst = AsyncElasticsearch([{'host': es_host, 'port': es_port}])
                else:
                    self.es_inst = Elasticsearch([{'host': es_host, 'port': es_port}])
                self.es_index = index_type
        else:
            self.debug = debug_override

    async def com_elastic_index(self, log_type, body_data):
        # do this first for speed
        if self.debug is None:
            pass
        # write log to elk
        elif self.debug == 'es':
            # leave the try....as I don't want the container to fail if mkelk not accepting
            try:
                if self.async_mode:
                    await self.es_inst.index(index=self.es_index, doc_type='MediaKraken',
                                             body={"type": log_type,
                                                   "data": str(body_data),
                                                   "timestamp": datetime.now()})
                else:
                    self.es_inst.index(index=self.es_index, doc_type='MediaKraken',
                                       body={"type": log_type,
                                             "data": str(body_data),
                                             "timestamp": datetime.now()})
            except:
                print((log_type, body_data), flush=True)
        # write log to host syslog
        elif self.debug == 'sys':
            sys.stdout.write(str({"type": log_type,
                                  "data": str(body_data),
                                  "timestamp": time.strftime("%Y%m%d%H%M%S")}))
        # write log to host syslog
        elif self.debug == 'print':
            print(str({"type": log_type,
                       "data": str(body_data),
                       "timestamp": time.strftime("%Y%m%d%H%M%S")}), flush=True)

    async def com_elastic_get(self, id):
        if self.async_mode:
            await self.es_inst.get(index=self.es_index, doc_type='MediaKraken', id=id)
        else:
            self.es_inst.get(index=self.es_index, doc_type='MediaKraken', id=id)
