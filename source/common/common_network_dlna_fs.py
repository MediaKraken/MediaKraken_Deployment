"""
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
"""

# https://github.com/MediaKraken-Dependancies/fs.dlna
import fs
import fs.dlna


class CommonNetworkDLNAFS:
    """
    For setting up dlna fs read
    """

    def __init__(self):
        yt_fs = fs.open_fs('dlna:///')
        dlna_fs = fs.dlna.DLNAFS(timeout=10)
