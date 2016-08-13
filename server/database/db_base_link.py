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
#import logging
import uuid


def srv_db_link_list_vount(self):
    """
    Return count of linked servers
    """
    self.sql3_cursor.execute('select count(*) from mm_link')
    return self.sql3_cursor.fetchone()[0]


def srv_db_link_list(self, offset=None, records=None):
    """
    Return list of linked server
    Complete list for admins
    """
    if offset is None:
        self.sql3_cursor.execute('select mm_link_guid, mm_link_name, mm_link_json from mm_link')
    else:
        self.sql3_cursor.execute('select mm_link_guid, mm_link_name, mm_link_json from mm_link'\
            ' where mm_link_guid in (select mm_link_guid from mm_link offset %s limit %s)',\
            (offset, records))
    return self.sql3_cursor.fetchall()


def srv_db_link_insert(self, link_json):
    """
    Insert linked server
    """
    self.sql3_cursor.execute('insert into mm_link (mm_link_guid, mm_link_options_json)'\
        ' values (%s, %s)', (str(uuid.uuid4()), link_json))


def srv_db_link_delete(self, sync_guid):
    """
    Delete server link
    """
    self.sql3_cursor.execute('delete from mm_link where mm_link_guid = %s', (sync_guid,))
