'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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
'''

import json
import pika
from guessit import guessit

from common import common_config_ini
from common import common_global
from common import common_metadata_tmdb
from common import common_string

option_config_json, db_connection = common_config_ini.com_config_read()

# pika rabbitmq connection
parameters = pika.ConnectionParameters('mkrabbitmq', socket_timeout=30,
                                       credentials=pika.PlainCredentials('guest', 'guest'))
connection = pika.BlockingConnection(parameters)
# setup channels and queue
channel = connection.channel()
exchange = channel.exchange_declare(exchange="mkque_download_ex", exchange_type="direct",
                                    durable=True)
queue = channel.queue_declare(queue='mkdownload', durable=True)
channel.queue_bind(exchange="mkque_download_ex", queue='mkdownload')
channel.basic_qos(prefetch_count=1)

# verify themoviedb key exists
if option_config_json['API']['themoviedb'] is not None:
    # setup the thmdb class
    TMDB_CONNECTION = common_metadata_tmdb.CommonMetadataTMDB(option_config_json)
else:
    TMDB_CONNECTION = None


def tv_fetch_save_tmdb(db_connection, tmdb_id):
    """
    # tmdb data fetch for tv
    """
    common_global.es_inst.com_elastic_index('info', {"meta tv themoviedb save fetch": tmdb_id})
    metadata_uuid = None
    result_json = TMDB_CONNECTION.com_tmdb_metadata_tv_by_id(tmdb_id)
    common_global.es_inst.com_elastic_index('info', {'tv fetch save themoviedb show': result_json})
    if result_json is not None:
        common_global.es_inst.com_elastic_index('info', {'stuff': 'insert'})
        # store the cast and crew
        db_connection.db_meta_person_insert_cast_crew('themoviedb', result_json['credits']['cast'])
        db_connection.db_meta_person_insert_cast_crew('themoviedb', result_json['credits']['crew'])


        # # insert
        # image_json = {'Images': {'themoviedb': {
        #     'Characters': {}, 'Episodes': {}, "Redo": True}}}
        # series_id_json = json.dumps({'imdb': xml_show_data['Data']['Series']['IMDB_ID'],
        #                              'themoviedb': str(tmdb_id),
        #                              'zap2it': xml_show_data['Data']['Series']['zap2it_id']})
        # common_global.es_inst.com_elastic_index('info', {'stuff': 'insert 2'})
        # metadata_uuid = db_connection.db_metatmdb_insert(series_id_json,
        #                                                  xml_show_data['Data']['Series'][
        #                                                      'SeriesName'],
        #                                                  json.dumps({'Meta': {'themoviedb':
        #                                                                           {'Meta':
        #                                                                                xml_show_data[
        #                                                                                    'Data'],
        #                                                                            'Cast': xml_actor_data,
        #                                                                            'Banner': xml_banners_data}}}),
        #                                                  json.dumps(image_json))
        # common_global.es_inst.com_elastic_index('info', {'stuff': 'insert 4'})
        # # save rows for episode image fetch
        # if 'Episode' in xml_show_data['Data']:
        #     # checking id instead of filename as id should always exist
        #     try:
        #         common_global.es_inst.com_elastic_index('info',
        #                                                 {len(xml_show_data['Data']['Episode'][0][
        #                                                          'id'])})
        #         if len(xml_show_data['Data']['Episode'][0]['id']) > 1:
        #             # thetmdb is Episode
        #             for episode_info in xml_show_data['Data']['Episode']:
        #                 common_global.es_inst.com_elastic_index('info', {'eps info': episode_info})
        #                 if episode_info['filename'] is not None:
        #                     # tmdb
        #                     channel.basic_publish(exchange='mkque_download_ex',
        #                                           routing_key='mkdownload',
        #                                           body=json.dumps(
        #                                               {'Type': 'download', 'Subtype': 'image',
        #                                                'url': 'https://thetmdb.com/banners/'
        #                                                       + episode_info['filename'],
        #                                                'local': '/mediakraken/web_app/MediaKraken/static/meta/images/'
        #                                                         + episode_info['filename']}),
        #                                           properties=pika.BasicProperties(
        #                                               content_type='text/plain',
        #                                               delivery_mode=2))
        #         else:
        #             if xml_show_data['Data']['Episode']['filename'] is not None:
        #                 # tmdb
        #                 channel.basic_publish(exchange='mkque_download_ex',
        #                                       routing_key='mkdownload',
        #                                       body=json.dumps(
        #                                           {'Type': 'download', 'Subtype': 'image',
        #                                            'url': 'https://thetmdb.com/banners/'
        #                                                   + xml_show_data['Data']['Episode'][
        #                                                       'filename'],
        #                                            'local': '/mediakraken/web_app/MediaKraken/static/meta/images/'
        #                                                     + xml_show_data['Data']
        #                                                     ['Episode']['filename']}),
        #                                       properties=pika.BasicProperties(
        #                                           content_type='text/plain',
        #                                           delivery_mode=2))
        #     except:
        #         if xml_show_data['Data']['Episode']['filename'] is not None:
        #             # tmdb
        #             channel.basic_publish(exchange='mkque_download_ex',
        #                                   routing_key='mkdownload',
        #                                   body=json.dumps(
        #                                       {'Type': 'download', 'Subtype': 'image',
        #                                        'url': 'https://thetmdb.com/banners/'
        #                                               + xml_show_data['Data'][
        #                                                   'Episode']['filename'],
        #                                        'local': '/mediakraken/web_app/MediaKraken/static/meta/images/'
        #                                                 + xml_show_data['Data']
        #                                                 ['Episode']['filename']}),
        #                                   properties=pika.BasicProperties(content_type='text/plain',
        #                                                                   delivery_mode=2))
        db_connection.db_commit()
    return metadata_uuid
