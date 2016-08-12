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
import logging
import uuid
import json


# metadata guid by isbm id
def srv_db_MetadataBook_GUID_By_ISBN(self, isbn_uuid, isbn13_uuid):
    self.sql3_cursor.execute('select mm_metadata_book_guid from mm_metadata_book where mm_metadata_book_isbn = %s or mm_metadata_book_isbn13 = %s', (isbn_uuid, isbn13_uuid))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_book_guid']
    except:
        return None


# metadata guid by name
def srv_db_MetadataBook_GUID_By_Name(self, book_name):
    self.sql3_cursor.execute('select mm_metadata_book_guid from mm_metadata_book where mm_metadata_book_name =  %s', (book_name,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_book_guid']
    except:
        return None


# insert metadata json from isbndb
def srv_db_MetadataBook_Book_Insert(self, json_data):
    json_data = json.dumps(json_data)
    insert_uuid = str(uuid.uuid4())
    self.sql3_cursor.execute('insert into mm_metadata_book (mm_metadata_book_guid, mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name, mm_metadata_book_json) values (%s,%s,%s,%s,%s)', (insert_uuid, json_data['isbn10'], json_data['isbn13'], json_data['title'], json_data))
    return insert_uuid
