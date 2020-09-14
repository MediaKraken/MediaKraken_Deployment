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

from datetime import datetime

import httpx


def com_es_httpx_post(index_name, message_type, message_text):
    response = httpx.post(
        'http://th-elk-1.beaverbay.local:9200/%s/MediaKraken' % (index_name,),
        data='{"@timestamp": "'
             + datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
             + '", "message": "%s",' % (message_text,)
             + ' "type": "%s",' % (message_type,)
             + ' "user": {"id": "metaman"}}',
        headers={"Content-Type": "application/json"},
        timeout=3.05)
    return response


async def com_es_httpx_post_async(index_name, message_type, message_text):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://th-elk-1.beaverbay.local:9200/%s/MediaKraken' % (index_name,),
            data='{"@timestamp": "'
                 + datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                 + '", "message": "%s",' % (message_text,)
                 + ' "type": "%s",' % (message_type,)
                 + ' "user": {"id": "metaman"}}',
            headers={"Content-Type": "application/json"},
            timeout=3.05)
        return response
