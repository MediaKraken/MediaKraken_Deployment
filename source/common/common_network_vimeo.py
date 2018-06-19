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

import vimeo


class CommonNetworkVimeo(object):
    """
    Class for interfacing with Vimeo
    """

    def __init__(self, option_config_json):
        self.vimeo_instance = vimeo.VimeoClient(
            token=option_config_json['Vimeo']['AccessToken'],
            key=option_config_json['Vimeo']['ClientID'],
            secret=option_config_json['Vimeo']['ClientSecret'])
