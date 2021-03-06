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
import urllib.error
import urllib.parse
import urllib.request
import httpx
import requests
from common import common_hash
from common import common_logging_elasticsearch_httpx
from common import common_version


class CommonMetadataTheSubDB:
    url = 'http://api.thesubdb.com/'
    headers = {
        "User-Agent": ("MediaKraken/1.0 "
                       "(MediaKraken/%s; http://www.mediakraken.org)"
                       % common_version.APP_VERSION)
    }

    async def com_meta_thesubdb_search(self, filename, langs):
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        filehash = common_hash.com_hash_thesubdb(filename)
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url,
                                        params={'action': 'search', 'hash': filehash},
                                        headers=self.headers,
                                        timeout=3.05)
        if response.status_code == 404:
            # no subtitle found
            return []
        subtitles = []
        for lang in response.text.splitlines()[0].split(','):
            if lang in langs:
                sublink = '%s?%s' % (self.url,
                                     urllib.parse.urlencode({'action': 'download',
                                                             'hash': filehash,
                                                             'language': lang}))
                subtitles.append({'lang': lang, 'link': sublink})
        return subtitles

    async def com_meta_thesubdb_download(self, subtitle, stream):
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            response = await client.get(subtitle["link"], headers=self.headers, timeout=5)
        stream.write(response.content)
