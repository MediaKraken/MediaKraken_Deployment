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

import discogs_client
from common import common_version


class CommonMetadataDiscogs(object):
    """
    Class for interfacing with discogs
    """

    def __init__(self):
        self.discogs_inst = discogs_client.Client(
            'MediaKraken/%s' % common_version.APP_VERSION)

    def com_meta_discogs_search(self, title):
        return self.discogs_inst.search(title, type='release')

    def com_meta_discogs_by_id(self, release_id):
        return self.discogs_inst.release(release_id)
