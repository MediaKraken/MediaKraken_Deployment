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


def db_nas_count(self):
    """
    # count nas
    """
    self.db_cursor.execute('select count(*) from mm_nas')
    return self.db_cursor.fetchone()[0]


def db_nas_list(self):
    """
    # read nas
    """
    self.db_cursor.execute('select mm_nas_id, mm_nas_json from mm_nas')
    return self.db_cursor.fetchall()


def db_nas_insert(self, nas_json):
    """
    # insert record
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_nas (mm_nas_id, mm_nas_json) values (%s,%s)',
                           (new_guid, nas_json))
    self.db_commit()
    return new_guid


def db_nas_update(self, guid, nas_json):
    """
    # update record
    """
    self.db_cursor.execute('update mm_nas set mm_nas_json = %s where mm_nas_id = %s',
                           (nas_json, guid))
    self.db_commit()


def db_nas_delete(self, guid):
    """
    # delete record
    """
    self.db_cursor.execute('delete from mm_nas where mm_nas_id = %s', (guid,))
    self.db_commit()


def db_nas_read(self, guid):
    """
    # find details by nas
    """
    self.db_cursor.execute('select mm_nas_json from mm_nas where mm_nas_id = %s', (guid,))
    try:
        return self.db_cursor.fetchone()['mm_nas_json']
    except:
        return None
