"""
  Copyright (C) 2020 Quinn D Granfor <spootdev@gmail.com>

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

import httpx
from common import common_logging_elasticsearch_httpx

from . import common_file


async def mk_network_fetch_from_url_async(url, directory=None):
    """
    Download data from specified url to save in specific directory
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    try:
        async with httpx.AsyncClient() as client:
            datafile = await client.get(url, timeout=3.05)
    except httpx.RequestError as exc:
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
            message_type='error',
            message_text=
            {
                "mk_network_fetch_from_url_async request": str(exc)})
        return False
    except httpx.HTTPStatusError as exc:
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
            message_type='error',
            message_text=
            {
                "mk_network_fetch_from_url_async status": str(exc)})
        return False
    if directory is not None and datafile.status_code == 200:
        try:
            localfile = open(directory, 'wb')
        except:
            # create missing directory structure
            common_file.com_mkdir_p(directory)
            localfile = open(directory, 'wb')
        localfile.write(datafile.content)
        await datafile.aclose()
        localfile.close()
    if directory is None:
        return datafile.content
    return True
