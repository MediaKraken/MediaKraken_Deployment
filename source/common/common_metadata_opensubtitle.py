'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File


class CommonMetadataOpenSubtitles:
    """
    Class for interfacing with Opensubtitles
    """

    def __init__(self, user_name, user_password):
        self.opensubtitles_inst = OpenSubtitles()
        self.token = self.opensubtitles_inst.login(user_name, user_password)

    def com_meta_opensub_search(self, file_name):
        f = File(file_name)
        return self.opensubtitles_inst.search_subtitles([{'sublanguageid': 'all',
                                                          'moviehash': f.get_hash(),
                                                          'moviebytesize': f.size}])

    def com_meta_opensub_ping(self):
        self.opensubtitles_inst.no_operation()

    def com_meta_opensub_logoff(self):
        self.opensubtitles_inst.logout()
