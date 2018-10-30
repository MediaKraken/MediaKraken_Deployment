'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
import uuid


def db_collection_list_count(self, search_value=None):
    if search_value is not None:
        self.db_cursor.execute('select count(*)'
                               ' from mm_metadata_collection'
                               ' where mm_metadata_collection_name %% %s',
                               (search_value, ))
    else:
        self.db_cursor.execute('select count(*)'
                               ' from mm_metadata_collection')
    return self.db_cursor.fetchone()[0]


def db_collection_list(self, offset=None, records=None, search_value=None):
    """
    Return collections list from the database
    """
    if offset is None:
        if search_value is not None:
            self.db_cursor.execute('select mm_metadata_collection_guid,'
                                   'mm_metadata_collection_name,'
                                   'mm_metadata_collection_imagelocal_json'
                                   ' from mm_metadata_collection'
                                   ' where mm_metadata_collection_name %% %s'
                                   ' order by mm_metadata_collection_name',
                                   (search_value,))
        else:
            self.db_cursor.execute('select mm_metadata_collection_guid,'
                                   'mm_metadata_collection_name,'
                                   'mm_metadata_collection_imagelocal_json'
                                   ' from mm_metadata_collection'
                                   ' order by mm_metadata_collection_name')
    else:
        if search_value is not None:
            self.db_cursor.execute('select mm_metadata_collection_guid,'
                                   'mm_metadata_collection_name,'
                                   'mm_metadata_collection_imagelocal_json'
                                   ' from mm_metadata_collection'
                                   ' where mm_metadata_collection_guid'
                                   ' in (select mm_metadata_collection_guid'
                                   ' from mm_metadata_collection'
                                   ' where mm_metadata_collection_name %% %s'
                                   ' order by mm_metadata_collection_name'
                                   ' offset %s limit %s) order by mm_metadata_collection_name',
                                   (search_value, offset, records))
        else:
            self.db_cursor.execute('select mm_metadata_collection_guid,'
                                   'mm_metadata_collection_name,'
                                   'mm_metadata_collection_imagelocal_json'
                                   ' from mm_metadata_collection'
                                   ' where mm_metadata_collection_guid'
                                   ' in (select mm_metadata_collection_guid'
                                   ' from mm_metadata_collection'
                                   ' order by mm_metadata_collection_name'
                                   ' offset %s limit %s) order by mm_metadata_collection_name',
                                   (offset, records))
    return self.db_cursor.fetchall()


def db_media_collection_scan(self):
    """
    Returns a list of movies that belong in a collection specifified by tmdb
    """
    self.db_cursor.execute('select mm_metadata_guid, mm_metadata_json from mm_metadata_movie'
                           ' where mm_metadata_json->\'Meta\'->\'themoviedb\'->\'Meta\'->>\'belongs_to_collection\'::text'
                           ' <> \'{}\'::text'
                           ' order by mm_metadata_json->\'Meta\'->\'themoviedb\'->\'Meta\'->>\'belongs_to_collection\'')
    return self.db_cursor.fetchall()


def db_collection_guid_by_name(self, collection_name):
    """
    Return uuid from collection name
    """
    self.db_cursor.execute('select mm_metadata_collection_guid from mm_metadata_collection'
                           ' where mm_metadata_collection_name->>\'name\' = %s',
                           (collection_name,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_collection_guid']
    except:
        return None


def db_collection_by_tmdb(self, tmdb_id):
    """
    Return uuid via tmdb id
    """
    self.db_cursor.execute('select mm_metadata_collection_guid from mm_metadata_collection'
                           ' where mm_metadata_collection_json @> \'{"id":%s}\'', (tmdb_id,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_collection_guid']
    except:
        return None


def db_collection_insert(self, collection_name, guid_json, metadata_json,
                         localimage_json):
    """
    Insert collection into the database
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_collection (mm_metadata_collection_guid,'
                           ' mm_metadata_collection_name, mm_metadata_collection_media_ids,'
                           ' mm_metadata_collection_json, mm_metadata_collection_imagelocal_json)'
                           ' values (%s,%s,%s,%s,%s)', (new_guid, json.dumps(collection_name),
                                                        json.dumps(guid_json),
                                                        json.dumps(
                                                            metadata_json),
                                                        json.dumps(localimage_json)))
    return new_guid


def db_collection_update(self, collection_guid, guid_json):
    """
    Update the ids listed within a collection
    """
    self.db_cursor.execute('update mm_metadata_collection'
                           ' set mm_metadata_collection_media_ids = %s,'
                           ' mm_metadata_collection_json = %s'
                           ' where mm_metadata_collection_guid = %s',
                           (json.dumps(guid_json), collection_guid))


def db_collection_read_by_guid(self, media_uuid):
    """
    Collection details
    """
    self.db_cursor.execute('select mm_metadata_collection_json,'
                           'mm_metadata_collection_imagelocal_json from mm_metadata_collection'
                           ' where mm_metadata_collection_guid = %s', (media_uuid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None
