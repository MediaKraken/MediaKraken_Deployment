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

# https://github.com/MediaKraken-Dependancies/xbox
import xbox


class CommonNetworkXboxLive:
    """
    Class for interfacing with xbox
    """

    def __init__(self, email_address, password):
        xbox.client.authenticate(email_address, password)

    def com_net_xboxlive_user(self, gamertag):
        self.gt = xbox.GamerProfile.from_gamertag(gamertag)

    def com_net_xboxlive_gamerscore(self):
        return self.gt.gamerscore

    def com_net_xboxlive_gamerpic(self):
        return self.gt.gamerpic

    def com_net_xboxlive_clips(self):
        '''
        clip.media_url
            'http://gameclipscontent-d2005.xboxlive.com/asset-886c5b78-8876-4823-b31b-fbc77d8caa67/GameClip-Original.MP4?sv=2012-02-12&st=2014-09-03T22%3A40%3A58Z&se=2014-09-03T23%3A45%3A58Z&sr=c&sp=r&sig=Q5qvyDvFRM2Bn2tztJ%2F%2BEf9%2FQOpkTPuFniByvE%2Bc9cc%3D&__gda__=1409787958_f22b516f9d29da56911b7cac03f15d05'
        clip.views
        clip.state
        clip.duration
        clip.thumbnails.large
        '''
        return self.gt.clips()
