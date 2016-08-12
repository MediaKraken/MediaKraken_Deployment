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


def srv_db_Metadata_Movie_Update_CastCrew(self, tmdb_id, cast_crew_json):
    self.sql3_cursor.execute('select mm_metadata_json from mm_metadata_movie where mm_metadata_media_id->\'TMDB\' ? %s', (tmdb_id,))
    cast_crew_json = self.sql3_cursor.fetchone()['mm_metadata_json'].update({'Cast': cast_crew_json['cast'], 'Crew': cast_crew_json['crew']})
    self.sql3_cursor.execute('update mm_metadata_movie set mm_metadata_json = %s where mm_metadata_guid = %s', (cast_crew_json, metadata_id))
    self.srv_db_Commit()
