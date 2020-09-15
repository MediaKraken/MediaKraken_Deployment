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

from bs4 import BeautifulSoup
from common import common_logging_elasticsearch_httpx

from . import common_network
from . import common_string


def com_tvtheme_download(media_name):
    """
    Try to grab theme from tvtunes
    """
    data = BeautifulSoup(common_network.mk_network_fetch_from_url(
        "http://www.televisiontunes.com/"
        + common_string.com_string_title(media_name).replace(' ', '_')
        + ".html", None)).find(id="download_song")
    if data is not None:
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'href': data['href']})
        common_network.mk_network_fetch_from_url("http://www.televisiontunes.com"
                                                 + data['href'], 'theme.mp3')
        return True  # success
    return False  # no match

# com_tvtheme_download("V")
