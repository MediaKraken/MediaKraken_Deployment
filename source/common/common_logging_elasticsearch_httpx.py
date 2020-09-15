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


def com_es_httpx_post(message_type, message_text, index_name=None):
    # this is so only have to pass during START log
    if not hasattr(com_es_httpx_post, "index_ext"):
        # it doesn't exist yet, so initialize it
        # index_name should be populated on first run
        com_es_httpx_post.index_ext = 'httpx_' + index_name.replace(' ', '_')
    response = httpx.post(
        'http://th-elk-1.beaverbay.local:9200/%s/MediaKraken'
        % (com_es_httpx_post.index_ext,),
        data='{"@timestamp": "'
             + datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
             + '", "message": "%s",' % (message_text,)
             + ' "type": "%s",' % (message_type,)
             + ' "user": {"id": "metaman"}}',
        headers={"Content-Type": "application/json"},
        timeout=3.05)
    return response


async def com_es_httpx_post_async(message_type, message_text, index_name=None):
    # this is so only have to pass during START log
    if not hasattr(com_es_httpx_post_async, "index_ext"):
        # it doesn't exist yet, so initialize it
        # index_name should be populated on first run
        com_es_httpx_post_async.index_ext = 'httpx_' + index_name.replace(' ', '_')
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://th-elk-1.beaverbay.local:9200/%s/MediaKraken'
            % (com_es_httpx_post_async.index_ext,),
            data='{"@timestamp": "'
                 + datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                 + '", "message": "%s",' % (message_text,)
                 + ' "type": "%s",' % (message_type,)
                 + ' "user": {"id": "metaman"}}',
            headers={"Content-Type": "application/json"},
            timeout=3.05)
        return response
