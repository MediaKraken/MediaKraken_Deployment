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
import json
import uuid
import datetime


def srv_db_kodi_user_sync_list_added(self, synctime):
    self.sql3_cursor.execute("select mm_media_guid from mm_media'\
        ' where mm_media_json->>\'DateAdded\' >= %s", (synctime,))
    return self.sql3_cursor.fetchall()


# sync data
def srv_db_kodi_user_sync(self, synctime):
    # title, plot, shortplot, tagline, votecount, rating, writer, year, imdb, sorttitle, runtime, mpaa, genre, director, title, studio, trailer, country, movieid
    #  crew  \'job\': \'Screenplay\' \'name\',
    #  crew  \'job\': \'Director\', \'name\'
    self.sql3_cursor.execute("select mm_media_name, mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'overview\', NULL, mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'tagline\', mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'vote_count\', mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'vote_average\', mm_metadata_json->\'Meta\'->\'TMDB\'->\'Crew\', mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'release_date\', mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'imdb_id\', LOWER(mm_media_name), mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'runtime\', NULL, mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'genres\', mm_metadata_json->\'Meta\'->\'TMDB\'->\'Crew\', mm_media_name, mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'production_companies\', NULL, mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'production_countries\', mm_media_guid from mm_media, mm_metadata_movie where mm_media_metadata_guid = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= %s", (synctime,))
    return self.sql3_cursor.fetchall()
