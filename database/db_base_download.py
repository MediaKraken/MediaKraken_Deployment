'''
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
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging  # pylint: disable=W0611
import uuid


def db_download_insert(self, provider, que_type, down_json):
    """
    Create/insert a download into the que
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_download_que (mdq_id,mdq_provider,mdq_que_type,'
                           'mdq_download_json) values (%s,%s,%s,%s)',
                           (new_guid, provider, que_type, down_json))
    self.db_commit()
    return new_guid


def db_download_read_provider(self, provider_name):
    """
    Read the downloads by provider
    """
    self.db_cursor.execute('select mdq_id,mdq_que_type,mdq_download_json from mm_download_que'
                           ' where mdq_provider = %s', (provider_name,))
    return self.db_cursor.fetchall()


def db_download_delete(self, guid):
    """
    Remove download
    """
    self.db_cursor.execute(
        'delete from mm_download_que where mdq_id = %s', (guid,))
    self.db_commit()


def db_download_update_provider(self, provider_name, guid):
    """
    Update provider
    """
    logging.info('download update provider: %s %s', provider_name, guid)
    self.db_cursor.execute('update mm_download_que set mdq_provider = %s where mdq_id = %s',
                           (provider_name, guid))
    self.db_commit()


def db_download_update(self, update_json, guid, update_que_id=None):
    """
    Update download que record
    """
    logging.info('download update: %s %s %s', update_json, update_que_id, guid)
    if update_que_id is not None:
        self.db_cursor.execute('update mm_download_que set mdq_download_json = %s,'
                               ' mdq_que_type = %s where mdq_id = %s',
                               (update_json, update_que_id, guid))
    else:
        self.db_cursor.execute('update mm_download_que set mdq_download_json = %s'
                               ' where mdq_id = %s', (update_json, guid))
    self.db_commit()


def db_download_que_exists(self, download_que_uuid, download_que_type,
                           provider_name, provider_id):
    """
    See if download que record exists for provider and id and type
    """
    # include search to find OTHER records besides the row that's
    # doing the query itself
    # this should now catch anything that's Fetch+, there should also technically
    # only ever be one Fetch+, rest should be search or null
    logging.info('db que exits: %s %s %s', download_que_uuid,
                 provider_name, provider_id)
    if download_que_uuid is not None:
        self.db_cursor.execute('select mdq_download_json->\'MetaNewID\' from mm_download_que'
                               ' where mdq_provider = %s and mdq_que_type = %s'
                               ' and mdq_download_json->\'ProviderMetaID\' ? %s'
                               ' and mdq_download_json->>\'Status\' <> \'Search\' limit 1',
                               (provider_name, download_que_type, provider_id,))
    # why do I care about the download que id?
    #            ' and mdq_id <> %s and mdq_download_json->>\'Status\' <> \'Search\' limit 1',
    #            (provider_name, download_que_type, provider_id, download_que_uuid))
    else:
        self.db_cursor.execute('select mdq_download_json->\'MetaNewID\' from mm_download_que'
                               ' where mdq_provider = %s and mdq_que_type = %s'
                               ' and mdq_download_json->\'ProviderMetaID\' ? %s limit 1',
                               (provider_name, download_que_type, provider_id))
    # if no data, send none back
    try:
        return self.db_cursor.fetchone()[0]
    except:
        return None
