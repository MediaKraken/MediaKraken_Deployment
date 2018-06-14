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

import soundcloud


class CommonNetworkSoundcloud(object):
    """
    Class for interfacing with Soundcloud
    """

    def __init__(self, access_token):
        self.soundcloud_inst = soundcloud.Client(access_token=access_token)

    def com_net_soundcloud_follow(self, user_id_to_follow):
        self.soundcloud_inst.put('/me/followings/%d' % user_id_to_follow)

    def com_net_soundcloud_desc(self, description):
        self.soundcloud_inst.put('/me', user={'description': description})

    def com_net_soundcloud_upload(self, track_title, file_name):
        track = self.soundcloud_inst.post('/tracks', track={
            'title': track_title,
            'sharing': 'private',
            'asset_data': open(file_name, 'rb')})
