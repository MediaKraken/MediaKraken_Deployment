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

import json
import uuid

from common import common_global


def db_meta_book_list_count(self, search_value=None):
    """
    book list count
    """
    if search_value is not None:
        self.db_cursor.execute('select count(*) '
                               'from mm_metadata_book where mm_metadata_book_name %% %s',
                               (search_value,))
    else:
        self.db_cursor.execute('select count(*) from mm_metadata_book')
    return self.db_cursor.fetchone()[0]


def db_meta_book_list(self, offset=0, records=None, search_value=None):
    """
    book list
    """
    # TODO sort by release date
    if search_value is not None:
        self.db_cursor.execute('select mm_metadata_book_guid,mm_metadata_book_name '
                               'from mm_metadata_book where mm_metadata_book_name %% %s'
                               ' order by mm_metadata_book_name '
                               'offset %s limit %s', (search_value, offset, records))
    else:
        self.db_cursor.execute('select mm_metadata_book_guid,mm_metadata_book_name '
                               'from mm_metadata_book order by mm_metadata_book_name '
                               'offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def db_meta_book_guid_by_isbn(self, isbn_uuid, isbn13_uuid):
    """
    # metadata guid by isbm id
    """
    self.db_cursor.execute('select mm_metadata_book_guid from mm_metadata_book'
                           ' where mm_metadata_book_isbn = %s or mm_metadata_book_isbn13 = %s',
                           (isbn_uuid, isbn13_uuid))
    try:
        return self.db_cursor.fetchone()['mm_metadata_book_guid']
    except:
        return None


def db_meta_book_guid_by_name(self, book_name):
    """
    # metadata guid by name
    """
    # TODO can be more than one by name
    # TODO sort by release date
    self.db_cursor.execute('select mm_metadata_book_guid from mm_metadata_book'
                           ' where mm_metadata_book_name =  %s', (book_name,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_book_guid']
    except:
        return None


def db_meta_book_insert(self, json_data):
    """
    # insert metadata json from isbndb
    """
    # json_data = json.dumps(json_data)
    common_global.es_inst.com_elastic_index('info', {'book insert': json_data})
    common_global.es_inst.com_elastic_index('info', {'book insert data': json_data['data']})
    insert_uuid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_book (mm_metadata_book_guid,'
                           ' mm_metadata_book_isbn, mm_metadata_book_isbn13,'
                           ' mm_metadata_book_name, mm_metadata_book_json)'
                           ' values (%s,%s,%s,%s,%s)',
                           (insert_uuid, json_data['data'][0]['isbn10'],
                            json_data['data'][0]['isbn13'], json_data['data'][0]['title'],
                            json.dumps(json_data['data'][0])))
    self.db_commit()
    return insert_uuid


def db_meta_book_by_uuid(self, book_uuid):
    """
    grab book by uuid
    """
    self.db_cursor.execute('select mm_metadata_book_json from mm_metadata_book '
                           'where mm_metadata_book_guid = %s', (book_uuid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_book_image_random(self, return_image_type='Cover'):
    """
    Find random book image
    """
    self.db_cursor.execute('select mm_metadata_book_image_json->\'Images\'->\'themoviedb\'->>\''
                           + return_image_type + '\' as image_json,mm_metadata_book_guid'
                                                 ' from mm_media,mm_metadata_book'
                                                 ' where mm_media_metadata_guid = mm_metadata_book_guid'
                                                 ' and (mm_metadata_book_image_json->\'Images\'->\'themoviedb\'->>\''
                           + return_image_type + '\'' + ')::text != \'null\''
                                                        ' order by random() limit 1')
    try:
        # then if no results.....a None will except which will then pass None, None
        image_json, metadata_id = self.db_cursor.fetchone()
        return image_json, metadata_id
    except:
        return None, None
