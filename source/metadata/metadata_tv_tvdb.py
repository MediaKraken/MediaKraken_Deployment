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
from common import common_metadata_provider_thetvdb
from common import common_string
from common import common_thetvdb
from guessit import guessit

# # pika rabbitmq connection
# parameters = pika.ConnectionParameters('mkstack_rabbitmq', socket_timeout=30,
#                                        credentials=pika.PlainCredentials('guest', 'guest'))
# connection = pika.BlockingConnection(parameters)
# # setup channels and queue
# channel = connection.channel()
# exchange = channel.exchange_declare(exchange="mkque_download_ex", exchange_type="direct",
#                                     durable=True)
# queue = channel.queue_declare(queue='mkdownload', durable=True)
# channel.queue_bind(exchange="mkque_download_ex", queue='mkdownload')
# channel.basic_qos(prefetch_count=1)
#
# THETVDB_CONNECTION = common_thetvdb.CommonTheTVDB(option_config_json)
# # tvshow xml downloader and general api interface
# THETVDB_API = common_metadata_provider_thetvdb.CommonMetadataTheTVDB(option_config_json)


def tv_search_tvdb(db_connection, file_name, lang_code='en'):
    """
    # tvdb search
    """
    file_name = guessit(file_name)
    if type(file_name['title']) == list:
        file_name['title'] = common_string.com_string_guessit_list(file_name['title'])
    common_global.es_inst.com_elastic_index('info', {"meta tv search tvdb": str(file_name)})
    metadata_uuid = None
    tvdb_id = None
    if THETVDB_CONNECTION is not None:
        if 'year' in file_name:
            tvdb_id = str(THETVDB_CONNECTION.com_thetvdb_search(file_name['title'],
                                                                file_name['year'], lang_code, True))
        else:
            tvdb_id = str(THETVDB_CONNECTION.com_thetvdb_search(file_name['title'],
                                                                None, lang_code, True))
        common_global.es_inst.com_elastic_index('info', {"response": tvdb_id})
        if tvdb_id is not None:
            #            # since there has been NO match whatsoever.....can "wipe" out everything
            #            media_id_json = json.dumps({'thetvdb': tvdb_id})
            #            common_global.es_inst.com_elastic_index('info', {'stuff':"dbjson: %s", media_id_json)
            # check to see if metadata exists for TVDB id
            metadata_uuid = db_connection.db_metatv_guid_by_tvdb(tvdb_id)
            common_global.es_inst.com_elastic_index('info', {"db result": metadata_uuid})
    common_global.es_inst.com_elastic_index('info', {'meta tv uuid': metadata_uuid,
                                                     'tvdb': tvdb_id})
    return metadata_uuid, tvdb_id


def tv_fetch_save_tvdb(db_connection, tvdb_id):
    """
    # tvdb data fetch
    """
    common_global.es_inst.com_elastic_index('info', {"meta tv tvdb save fetch": tvdb_id})
    metadata_uuid = None
    # fetch XML zip file
    xml_show_data, xml_actor_data, xml_banners_data \
        = THETVDB_API.com_meta_thetvdb_get_zip_by_id(tvdb_id)
    common_global.es_inst.com_elastic_index('info', {'tv fetch save tvdb show': xml_show_data})
    if xml_show_data is not None:
        common_global.es_inst.com_elastic_index('info', {'stuff': 'insert'})
        # insert
        image_json = {'Images': {'thetvdb': {
            'Characters': {}, 'Episodes': {}, "Redo": True}}}
        series_id_json = json.dumps({'imdb': xml_show_data['Data']['Series']['IMDB_ID'],
                                     'thetvdb': str(tvdb_id),
                                     'zap2it': xml_show_data['Data']['Series']['zap2it_id']})
        common_global.es_inst.com_elastic_index('info', {'stuff': 'insert 2'})
        metadata_uuid = db_connection.db_metatvdb_insert(series_id_json,
                                                         xml_show_data['Data']['Series'][
                                                             'SeriesName'],
                                                         json.dumps({'Meta': {'thetvdb':
                                                                                  {'Meta':
                                                                                       xml_show_data[
                                                                                           'Data'],
                                                                                   'Cast': xml_actor_data,
                                                                                   'Banner': xml_banners_data}}}),
                                                         json.dumps(image_json))
        common_global.es_inst.com_elastic_index('info', {'stuff': 'insert 3'})
        # insert cast info
        if xml_actor_data is not None:
            db_connection.db_meta_person_insert_cast_crew('thetvdb',
                                                          xml_actor_data['Actor'])
        common_global.es_inst.com_elastic_index('info', {'stuff': 'insert 4'})
        # save rows for episode image fetch
        if 'Episode' in xml_show_data['Data']:
            # checking id instead of filename as id should always exist
            try:
                print(('len %s', len(xml_show_data['Data']['Episode'][0]['id'])), flush=True)
                if len(xml_show_data['Data']['Episode'][0]['id']) > 1:
                    # thetvdb is Episode
                    for episode_info in xml_show_data['Data']['Episode']:
                        common_global.es_inst.com_elastic_index('info', {'eps info': episode_info})
                        if episode_info['filename'] is not None:
                            # thetvdb
                            channel.basic_publish(exchange='mkque_download_ex',
                                                  routing_key='mkdownload',
                                                  body=json.dumps(
                                                      {'Type': 'download', 'Subtype': 'image',
                                                       'url': 'https://thetvdb.com/banners/'
                                                              + episode_info['filename'],
                                                       'local': '/mediakraken/web_app_sanic/MediaKraken/static/meta/images/'
                                                                + episode_info['filename']}),
                                                  properties=pika.BasicProperties(
                                                      content_type='text/plain',
                                                      delivery_mode=2))
                else:
                    if xml_show_data['Data']['Episode']['filename'] is not None:
                        # thetvdb
                        channel.basic_publish(exchange='mkque_download_ex',
                                              routing_key='mkdownload',
                                              body=json.dumps(
                                                  {'Type': 'download', 'Subtype': 'image',
                                                   'url': 'https://thetvdb.com/banners/'
                                                          + xml_show_data['Data']['Episode'][
                                                              'filename'],
                                                   'local': '/mediakraken/web_app_sanic/MediaKraken/static/meta/images/'
                                                            + xml_show_data['Data']
                                                            ['Episode']['filename']}),
                                              properties=pika.BasicProperties(
                                                  content_type='text/plain',
                                                  delivery_mode=2))
            except:
                if xml_show_data['Data']['Episode']['filename'] is not None:
                    # thetvdb
                    channel.basic_publish(exchange='mkque_download_ex',
                                          routing_key='mkdownload',
                                          body=json.dumps(
                                              {'Type': 'download', 'Subtype': 'image',
                                               'url': 'https://thetvdb.com/banners/'
                                                      + xml_show_data['Data'][
                                                          'Episode']['filename'],
                                               'local': '/mediakraken/web_app_sanic/MediaKraken/static/meta/images/'
                                                        + xml_show_data['Data']
                                                        ['Episode']['filename']}),
                                          properties=pika.BasicProperties(content_type='text/plain',
                                                                          delivery_mode=2))
        db_connection.db_commit()
    return metadata_uuid
