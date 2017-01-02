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
import logging # pylint: disable=W0611
import uuid
import json


def db_meta_book_list(self, offset=None, records=None):
    """
    book list
    """
    if offset is None:
        self.db_cursor.execute('select mm_metadata_book_guid,mm_metadata_book_name '\
            'from mm_metadata_book order by mm_metadata_book_name')
    else:
        self.db_cursor.execute('select mm_metadata_book_guid,mm_metadata_book_name '\
            'from mm_metadata_book order by mm_metadata_book_name '\
            'offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def db_meta_book_guid_by_isbn(self, isbn_uuid, isbn13_uuid):
    """
    # metadata guid by isbm id
    """
    self.db_cursor.execute('select mm_metadata_book_guid from mm_metadata_book'\
        ' where mm_metadata_book_isbn = %s or mm_metadata_book_isbn13 = %s',\
        (isbn_uuid, isbn13_uuid))
    try:
        return self.db_cursor.fetchone()['mm_metadata_book_guid']
    except:
        return None


def db_meta_book_guid_by_name(self, book_name):
    """
    # metadata guid by name
    """
    self.db_cursor.execute('select mm_metadata_book_guid from mm_metadata_book'\
        ' where mm_metadata_book_name =  %s', (book_name,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_book_guid']
    except:
        return None


def db_meta_book_insert(self, json_data):
    """
    # insert metadata json from isbndb
    """
    #json_data = json.dumps(json_data)
    logging.info('book insert %s', json_data)
    logging.info('book insert data %s', json_data['data'])
    insert_uuid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_book (mm_metadata_book_guid,'\
        ' mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name,'\
        ' mm_metadata_book_json) values (%s,%s,%s,%s,%s)',\
        (insert_uuid, json_data['data'][0]['isbn10'], json_data['data'][0]['isbn13'], \
         json_data['data'][0]['title'], json.dumps(json_data['data'][0])))
    return insert_uuid


def db_meta_book_by_uuid(self, book_uuid):
    """
    grab book by uuid
    """
    self.db_cursor.execute('select mm_metadata_book_json from mm_metadata_book '\
                           'where mm_metadata_book_guid = %s', book_uuid)
    try:
        return self.db_cursor.fetchone()
    except:
        return None
