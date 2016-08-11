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

import logging
import pitchfork


class MK_Common_Pitchfork_API:
    def __init__(self):
        pass


    def MK_Common_Pitchfork_Search(self, artist_name, album_title):
        self.pitchfork_api = pitchfork.search(artist_name, album_title)


    def MK_Common_Pitchfork_Album_Title(self):
        return self.pitchfork_api.album()


    def MK_Common_Pitchfork_Album_Label(self):
        return self.pitchfork_api.label()


    def MK_Common_Pitchfork_Album_Review(self):
        return self.pitchfork_api.editorial()


    def MK_Common_Pitchfork_Album_Cover_Art_Link(self):
        return self.pitchfork_api.cover()


    def MK_Common_Pitchfork_Album_Review_Score(self):
        return self.pitchfork_api.score()
