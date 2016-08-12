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
import pitchfork


class CommonPitchfork(object):
    """
    Class for interfacing with pitchfork
    """
    def __init__(self):
        pass


    def com_pitchfork_search(self, artist_name, album_title):
        self.pitchfork_api = pitchfork.search(artist_name, album_title)


    def com_pitchfork_album_title(self):
        return self.pitchfork_api.album()


    def com_pitchfork_album_label(self):
        return self.pitchfork_api.label()


    def com_pitchfork_album_review(self):
        return self.pitchfork_api.editorial()


    def com_pitchfork_album_cover_art_link(self):
        return self.pitchfork_api.cover()


    def com_pitchfork_album_review_score(self):
        return self.pitchfork_api.score()
