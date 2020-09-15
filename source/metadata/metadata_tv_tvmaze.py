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

import json

import pika
from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_string
from guessit import guessit


# # setup the tvmaze class
# TVMAZE_CONNECTION = common_metadata_provider_tvmaze.CommonMetadatatvmaze()


async def tv_search_tvmaze(db_connection, file_name, lang_code='en'):
    """
    # tvmaze search
    """
    file_name = guessit(file_name)
    if type(file_name['title']) == list:
        file_name['title'] = common_string.com_string_guessit_list(file_name['title'])
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text={
        "meta tv search tvmaze": str(file_name)})
    metadata_uuid = None
    tvmaze_id = None
    if TVMAZE_CONNECTION is not None:
        if 'year' in file_name:
            tvmaze_id = str(TVMAZE_CONNECTION.com_meta_tvmaze_widesearch(file_name['title'],
                                                                         file_name['year']))
        else:
            tvmaze_id = str(TVMAZE_CONNECTION.com_meta_tvmaze_widesearch(file_name['title'],
                                                                         None))
        common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                             message_text={'response': tvmaze_id})
        if tvmaze_id is not None:
            #            # since there has been NO match whatsoever.....can "wipe" out everything
            #            media_id_json = json.dumps({'tvmaze_id': tvmaze_id})
            #            common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text= {'stuff':"dbjson: %s", media_id_json)
            # check to see if metadata exists for tvmaze id
            metadata_uuid = await db_connection.db_metatv_guid_by_tvmaze(tvmaze_id)
            common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text={
                "db result": metadata_uuid})
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text={
        'meta tv uuid': metadata_uuid,
        'tvmaze': tvmaze_id})
    return metadata_uuid, tvmaze_id


async def tv_fetch_save_tvmaze(db_connection, tvmaze_id):
    """
    Fetch show data from tvmaze
    """
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text={
        "meta tv tvmaze save fetch": tvmaze_id})
    metadata_uuid = None
    result_data = TVMAZE_CONNECTION.com_meta_tvmaze_show_by_id(
        tvmaze_id,
        imdb_id=None,
        tvdb_id=None,
        embed_info=True)
    try:
        result_json = json.loads(result_data)
    except:
        result_json = None
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                         message_text={"tvmaze full": result_json})
    if result_json is not None and result_json['status'] != 404:
        show_full_json = ({'Meta': {'tvmaze': result_json}})
        show_detail = show_full_json['Meta']['tvmaze']
        common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                             message_text={"detail": show_detail})
        tvmaze_name = show_detail['name']
        common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                             message_text={"name": tvmaze_name})
        try:
            thetvdb_id = str(show_detail['externals']['thetvdb'])
        except KeyError:
            thetvdb_id = None
        try:
            imdb_id = str(show_detail['externals']['imdb'])
        except KeyError:
            imdb_id = None
        series_id_json = json.dumps({'tvmaze': str(tvmaze_id),
                                     'imdb': imdb_id,
                                     'thetvdb': thetvdb_id})
        metadata_uuid = await db_connection.db_meta_tvmaze_insert(series_id_json, tvmaze_name,
                                                                  json.dumps(
                                                                      show_full_json),
                                                                  json.dumps({'Images': {'tvmaze': {
                                                                      'Characters': {},
                                                                      'Episodes': {},
                                                                      "Redo": True}}}))
        # store person info
        if 'cast' in show_full_json['Meta']['tvmaze']['_embedded'] \
                and len(show_full_json['Meta']['tvmaze']['_embedded']['cast']) > 0:
            await db_connection.db_meta_person_insert_cast_crew('tvmaze',
                                                                show_full_json['Meta']['tvmaze'][
                                                                    '_embedded']['cast'])
        if 'crew' in show_full_json['Meta']['tvmaze']['_embedded'] \
                and len(show_full_json['Meta']['tvmaze']['_embedded']['crew']) > 0:
            await db_connection.db_meta_person_insert_cast_crew('tvmaze',
                                                                show_full_json['Meta']['tvmaze'][
                                                                    '_embedded']['crew'])
        # save rows for episode image fetch
        for episode_info in show_detail['_embedded']['episodes']:
            if episode_info['image'] is not None:
                # tvmaze image
                # This is the SAVE path.  Do NOT shorten the path to static.
                # This is the SAVE path.  Do NOT shorten the path to static.
                channel.basic_publish(exchange='mkque_download_ex',
                                      routing_key='mkdownload',
                                      body=json.dumps(
                                          {'Type': 'download', 'Subtype': 'image',
                                           'url': episode_info['image']['original'],
                                           'local': common_global.static_data_directory
                                                    + '/meta/images/episodes/'
                                                    + str(episode_info['id']) + '.jpg'}),
                                      properties=pika.BasicProperties(content_type='text/plain',
                                                                      delivery_mode=2))
        await db_connection.db_commit()
    return metadata_uuid
