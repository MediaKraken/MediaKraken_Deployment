"""
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
"""

import inspect

from common import common_logging_elasticsearch_httpx
from common import common_network_async

# https://openlibrary.org/developers/api

class CommonMetadataOpenLibrary:
    """
    Class for interfacing with OpenLibrary
    """

    def __init__(self):
        pass

    async def com_meta_openlibrary_fetch_cover(self, isbn_id, image_path):
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        await common_network_async.mk_network_fetch_from_url_async(
            'http://covers.openlibrary.org/b/isbn/'
            + isbn_id + '-L.jpg', image_path)
