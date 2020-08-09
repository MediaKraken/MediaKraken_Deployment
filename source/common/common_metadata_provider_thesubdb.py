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

import urllib.error
import urllib.parse
import urllib.request

import requests
from common import common_hash
from common import common_version


class CommonMetadataTheSubDB:
    url = 'http://api.thesubdb.com/'
    headers = {
        "User-Agent": ("MediaKraken/1.0 "
                       "(MediaKraken/%s; http://www.mediakraken.org)"
                       % common_version.APP_VERSION)
    }

    def com_meta_thesubdb_search(self, filename, langs):
        filehash = common_hash.com_hash_thesubdb(filename)
        response = requests.get(self.url, params={'action': 'search', 'hash': filehash},
                                headers=self.headers)
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

    def com_meta_thesubdb_download(self, subtitle, stream):
        response = requests.get(subtitle["link"], headers=self.headers)
        stream.write(response.content)
