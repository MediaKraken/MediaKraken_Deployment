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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import uuid


def db_review_count(self, metadata_id):
    """
    # count reviews for media
    """
    self.db_cursor.execute('select count(*) from mm_review where mm_review_metadata_guid = %s',\
        (metadata_id,))
    return self.db_cursor.fetchone()[0]


def db_review_list_by_tmdb_guid(self, metadata_id):
    """
    # grab reviews for metadata
    """
    self.db_cursor.execute('select mm_review_guid,mm_review_json from mm_review'\
        ' where mm_review_metadata_id->\'TMDB\' ? %s', (metadata_id,))
    return self.db_cursor.fetchall()


def db_review_insert(self, metadata_id, review_json):
    """
    # insert record
    """
    self.db_cursor.execute('insert into mm_review (mm_review_guid, mm_review_metadata_id,'\
        ' mm_review_json) values (%s,%s,%s)', (str(uuid.uuid4()), metadata_id, review_json))
