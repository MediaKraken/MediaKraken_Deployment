"""
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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

import uuid

from common import common_logging_elasticsearch_httpx

def db_download_read_provider(self, provider_name):
    """
    Read the downloads by provider
    """
    self.db_cursor.execute('select mdq_id,'
                           ' mdq_que_type,'
                           ' mdq_new_uuid,'
                           ' mdq_provider_id,'
                           ' mdq_status'
                           ' from mm_download_que'
                           ' where mdq_provider = %s'
                           ' order by mdq_que_type limit 25',
                           (provider_name,))
    return self.db_cursor.fetchall()


def db_download_delete(self, guid):
    """
    Remove download
    """
    self.db_cursor.execute('delete from mm_download_que'
                           ' where mdq_id = %s', (guid,))
    self.db_commit()


def db_download_update_provider(self, provider_name, guid):
    """
    Update provider
    """
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        'download update provider': provider_name,
        'guid': guid})
    self.db_cursor.execute('update mm_download_que set mdq_provider = %s'
                           ' where mdq_id = %s',
                           (provider_name, guid))


def db_download_update(self, guid, status, provider_guid=None):
    """
    Update download que record
    """
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        'download update': status,
        'que': provider_guid, 'guid': guid})
    if provider_guid is not None:
        self.db_cursor.execute('update mm_download_que set mdq_status = %s,'
                               ' mdq_provider_id = %s'
                               ' where mdq_id = %s',
                               (status, provider_guid, guid))
    else:
        self.db_cursor.execute('update mm_download_que set mdq_status = %s'
                               ' where mdq_id = %s', (status, guid))
