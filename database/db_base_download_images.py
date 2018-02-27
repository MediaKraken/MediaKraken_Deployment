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


def db_download_image_insert(self, provider, down_json):
    """
    Create/insert a download into the que
    """
    logging.info('dl image insert: %s', down_json)
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_download_image_que (mdq_image_id,mdq_image_provider,'
                           'mdq_image_download_json) values (%s,%s,%s)',
                           (new_guid, provider, down_json))
    self.db_commit()
    return new_guid


def db_download_image_read(self):
    """
    Read the downloads
    """
    self.db_cursor.execute('select mdq_image_id,mdq_image_download_json'
                           ' from mm_download_image_que')
    return self.db_cursor.fetchall()


def db_download_image_delete(self, guid):
    """
    Remove download
    """
    self.db_cursor.execute('delete from mm_download_image_que where mdq_image_id = %s',
                           (guid,))
    self.db_commit()
