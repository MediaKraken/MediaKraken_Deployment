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
import json


def db_meta_movie_update_castcrew(self, cast_crew_json, metadata_id):
    """
    Update the cast/crew for selected media
    """
    logging.debug('upt castcrew: %s', metadata_id)
    self.db_cursor.execute('select mm_metadata_json from mm_metadata_movie'\
        ' where mm_metadata_guid = %s', (metadata_id,))

    cast_crew_json_row = self.db_cursor.fetchone()
    logging.debug('row: %s', cast_crew_json_row)
    if 'cast' in cast_crew_json:
        cast_crew_json_row['mm_metadata_json'].update({'Cast': cast_crew_json['cast']})
    if 'crew' in cast_crew_json:
        cast_crew_json_row['mm_metadata_json'].update({'Crew': cast_crew_json['crew']})

    logging.debug('upt: %s', cast_crew_json_row)
    self.db_cursor.execute('update mm_metadata_movie set mm_metadata_json = %s'\
        ' where mm_metadata_guid = %s', (json.dumps(cast_crew_json_row), metadata_id))
    self.db_commit()
