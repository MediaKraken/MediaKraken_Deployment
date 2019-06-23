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
from common import common_network_youtube


# fetch video via youtube-dl
# def com_meta_youtube_fetch_video_by_url(url_location, file_name):


class TestCommonYoutube:

    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def teardown_class(self):
        pass

    def test_com_net_yt_trending(self):
        common_network_youtube.com_net_yt_trending()

    # @pytest.mark.parametrize(("search_string", "max_files"), [
    #     ('die hard trailer', 5),
    #     ('flask programming', 25)])
    # def test_com_meta_youtube_fetch_video_list(self, search_string, max_files):
    #     """
    #     Test function
    #     """
    #     common_network_youtube.com_net_yt_search(search_string, max_files)
