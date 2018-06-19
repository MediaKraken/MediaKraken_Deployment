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


def db_version_check(self):
    """
    query db version
    """
    self.db_cursor.execute('select mm_version_no from mm_version')
    return self.db_cursor.fetchone()[0]


def db_version_update(self, version_no):
    """
    update db version
    """
    self.db_cursor.execute(
        'update mm_version set mm_version_no = %s', (version_no,))
