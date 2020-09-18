"""
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
"""

import inspect

from common import common_logging_elasticsearch_httpx
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File


class CommonMetadataOpenSubtitles:
    """
    Class for interfacing with Opensubtitles
    """

    def __init__(self, user_name, user_password):
        self.opensubtitles_inst = OpenSubtitles()
        self.token = self.opensubtitles_inst.login(user_name, user_password)

    async def com_meta_opensub_search(self, file_name):
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        f = File(file_name)
        return self.opensubtitles_inst.search_subtitles([{'sublanguageid': 'all',
                                                          'moviehash': f.get_hash(),
                                                          'moviebytesize': f.size}])

    async def com_meta_opensub_ping(self):
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        self.opensubtitles_inst.no_operation()

    async def com_meta_opensub_logoff(self):
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        self.opensubtitles_inst.logout()
