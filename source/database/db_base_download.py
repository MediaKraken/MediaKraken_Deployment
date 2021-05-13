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


def db_download_insert(self, provider, que_type, down_json, down_new_uuid):
    """
    Create/insert a download into the que
    """
    new_guid = uuid.uuid4()
    self.db_cursor.execute('insert into mm_download_que (mdq_id,'
                           ' mdq_provider,'
                           ' mdq_que_type,'
                           ' mdq_new_uuid,'
                           ' mdq_provider_id,'
                           ' mdq_status)'
                           ' values (%s,%s,%s,%s,%s,%s,%s)',
                           (new_guid, provider, que_type, down_new_uuid,
                            down_json['ProviderMetaID'], down_json['Status']))
    self.db_commit()
    return new_guid


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


def db_download_que_exists(self, download_que_uuid, download_que_type,
                           provider_name, provider_id,
                           exists_only=False):
    """
    See if download que record exists for provider and id and type
        still need this as records could be from different threads or not in order
        and themoviedb "reuses" media id records for tv/movie
    """
    # include search to find OTHER records besides the row that's
    # doing the query itself
    # this should now catch anything that's Fetch+, there should also technically
    # only ever be one Fetch+, rest should be search or null
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        'db_download_que_exists': download_que_uuid,
        'name': provider_name,
        'id': provider_id})
    if exists_only:
        return self.db_cursor.execute('select exists(select 1'
                                      ' from mm_download_que'
                                      ' where mdq_provider = $1'
                                      ' and mdq_que_type = $2'
                                      ' and mdq_provider_id = $3'
                                      ' limit 1) limit 1',
                                      provider_name, download_que_type, provider_id)
    else:
        # que type is movie, tv, etc as those numbers could be reused
        self.db_cursor.execute('select mdq_new_uuid'
                               ' from mm_download_que'
                               ' where mdq_provider = %s'
                               ' and mdq_que_type = %s'
                               ' and mdq_provider_id = %s limit 1',
                               (provider_name, download_que_type, provider_id))
    # if no data, send none back
    try:
        return self.db_cursor.fetchone()[0]
    except:
        return None
