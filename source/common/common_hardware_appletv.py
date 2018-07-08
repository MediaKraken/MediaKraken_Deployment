'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

# https://github.com/postlund/pyatv
import asyncio

LOOP = asyncio.get_event_loop()


@asyncio.coroutine
def com_hard_atv_what_is_playing(atv):
    playing = yield from atv.metadata.playing()
    return playing


def com_hard_atv_discover():
    atvs = await pyatv.scan_for_apple_tvs(loop, timeout=5)
    if not atvs:
        return False
    print('Connecting to {0}'.format(atvs[0].address))


class CommonHardwareAppleTV(object):
    """
    Class for interfacing with apple tv
    """

    def __init__(self, ip_addr, loop):
        self.atv_inst = pyatv.connect_to_apple_tv(atvs[0], loop)

    def com_hard_atv_logout(self):
        await self.atv_inst.logout()

# helpers.auto_connect(com_hard_atv_what_is_playing)
