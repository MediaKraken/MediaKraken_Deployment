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

import sys

sys.path.append('.')
from common import common_config_ini
from common import common_metadata_musicbrainz


class TestCommonMusicbrainz:

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.musicbrainz_connection = common_metadata_musicbrainz.CommonMetadataMusicbrainz(
            option_config_json)

    @classmethod
    def teardown_class(self):
        pass

    # def show_release_details(self, rel):

    # search by artist and album name
    # def com_Mediabrainz_Get_Releases(self, disc_id=None, artist_name=None, artist_recording=None, return_limit=5, strict_flag=False):

    # search by artist and song name
    # def com_Mediabrainz_Get_Recordings(self, artist_name=None, release_name=None, song_name=None, return_limit=5, strict_flag=False):
