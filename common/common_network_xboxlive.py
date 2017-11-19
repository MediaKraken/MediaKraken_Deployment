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

from __future__ import absolute_import, division, print_function, unicode_literals
from common import common_logging
import xbox


class CommonNetworkXboxLive(object):
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
