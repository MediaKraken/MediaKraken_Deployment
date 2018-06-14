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

import uuid


def db_link_list_count(self, search_value=None):
    """
    Return count of linked servers
    """
    if search_value is not None:
        self.db_cursor.execute('select count(*) from mm_link where mm_link_name %% %s',
                               (search_value,))
    else:
        self.db_cursor.execute('select count(*) from mm_link')
    return self.db_cursor.fetchone()[0]


def db_link_list(self, offset=None, records=None, search_value=None):
    """
    Return list of linked server
    Complete list for admins
    """
    if offset is None:
        if search_value is not None:
            self.db_cursor.execute('select mm_link_guid, mm_link_name, mm_link_json'
                                   ' from mm_link where mm_link_name %% %s', (search_value,))
        else:
            self.db_cursor.execute(
                'select mm_link_guid, mm_link_name, mm_link_json from mm_link')
    else:
        if search_value is not None:
            self.db_cursor.execute('select mm_link_guid, mm_link_name, mm_link_json from mm_link'
                                   ' where mm_link_guid in (select mm_link_guid'
                                   ' from mm_link where mm_link_name %% %s offset %s limit %s)',
                                   (search_value, offset, records))
        else:
            self.db_cursor.execute('select mm_link_guid, mm_link_name, mm_link_json from mm_link'
                                   ' where mm_link_guid in (select mm_link_guid from mm_link'
                                   ' offset %s limit %s)', (offset, records))
    return self.db_cursor.fetchall()


def db_link_insert(self, link_json):
    """
    Insert linked server
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_link (mm_link_guid, mm_link_json)'
                           ' values (%s, %s)', (new_guid, link_json))
    self.db_commit()
    return new_guid


def db_link_delete(self, sync_guid):
    """
    Delete server link
    """
    self.db_cursor.execute(
        'delete from mm_link where mm_link_guid = %s', (sync_guid,))
    self.db_commit()
