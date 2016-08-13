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


def srv_db_nas_count(self):
    """
    # count nass
    """
    self.sql3_cursor.execute('select count(*) from mm_nas')
    return self.sql3_cursor.fetchone()[0]


def srv_db_nas_list(self):
    """
    # read nas
    """
    self.sql3_cursor.execute('select mm_nas_id, mm_nas_json from mm_nas')
    return self.sql3_cursor.fetchall()


def srv_db_nas_insert(self, nas_json):
    """
    # insert record
    """
    self.sql3_cursor.execute('insert into mm_nas (mm_nas_id, mm_nas_json) values (%s,%s)',\
        (str(uuid.uuid4()), nas_json))


def srv_db_nas_update(self, guid, nas_json):
    """
    # update record
    """
    self.sql3_cursor.execute('update mm_nas set mm_nas_json = %s where mm_nas_id = %s',\
        (nas_json, guid))


def srv_db_nas_delete(self, guid):
    """
    # delete record
    """
    self.sql3_cursor.execute('delete from mm_nas where mm_nas_id = %s', (guid,))


def srv_db_nas_read(self, guid):
    """
    # find detials by nas
    """
    self.sql3_cursor.execute('select mm_nas_json from mm_nas where mm_nas_id = %s', (guid,))
    try:
        return self.sql3_cursor.fetchone()['mm_nas_json']
    except:
        return None
