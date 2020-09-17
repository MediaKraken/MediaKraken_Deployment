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

import pornhub


# https://github.com/MediaKraken-Dep/pornhub-api

class CommonMetadataPornhub:
    """
    Class for interfacing with pornhub
    """

    def __init__(self, proxy_ip=None, proxy_port=None):
        if proxy_ip is None:
            self.pornhub_inst = pornhub.PornHub()
        else:
            self.pornhub_inst = pornhub.PornHub(proxy_ip, proxy_port)

    def com_meta_pornhub_stars(self, star_limit):
        return self.pornhub_inst.getStars(star_limit)

    def com_meta_pornhub_search(self, search_keywords, quantity, page):
        self.pornhub_inst = pornhub.PornHub(search_keywords)
        return self.pornhub_inst.getVideos(quantity, page=page)
