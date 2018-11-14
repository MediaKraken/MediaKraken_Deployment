'''
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
'''

import json

import pika
from common import common_config_ini
from common import common_global
from common import common_metadata_thetvdb
from common import common_metadata_tvmaze
from common import common_string
from common import common_thetvdb
from guessit import guessit

from . import metadata_nfo_xml

option_config_json, db_connection = common_config_ini.com_config_read()

# pika rabbitmq connection
parameters = pika.ConnectionParameters('mkrabbitmq',
                                       credentials=pika.PlainCredentials('guest', 'guest'))
connection = pika.BlockingConnection(parameters)
# setup channels and queue
channel = connection.channel()
exchange = channel.exchange_declare(exchange="mkque_cloud_ex", exchange_type="direct",
                                    durable=True)
queue = channel.queue_declare(queue='mkcloud', durable=True)
channel.queue_bind(exchange="mkque_cloud_ex", queue='mkcloud')
channel.basic_qos(prefetch_count=1)

# verify thetvdb key exists for search
if option_config_json['API']['thetvdb'] is not None:
    THETVDB_CONNECTION = common_thetvdb.CommonTheTVDB(option_config_json)
    # tvshow xml downloader and general api interface
    THETVDB_API = common_metadata_thetvdb.CommonMetadataTheTVDB(option_config_json)
else:
    THETVDB_CONNECTION = None

# setup the tvmaze class
# if option_config_json['API']['tvmaze'] is not None:
TVMAZE_CONNECTION = common_metadata_tvmaze.CommonMetadatatvmaze()
# else:
#    TVMAZE_CONNECTION = None


def tv_search_tvmaze(db_connection, file_name, lang_code='en'):
    """
    # tvmaze search
    """
    file_name = guessit(file_name)
    if type(file_name['title']) == list:
        file_name['title'] = common_string.com_string_guessit_list(file_name['title'])
    common_global.es_inst.com_elastic_index('info', {"meta tv search tvmaze": str(file_name)})
    metadata_uuid = None
    tvmaze_id = None
    if TVMAZE_CONNECTION is not None:
        if 'year' in file_name:
            tvmaze_id = str(TVMAZE_CONNECTION.com_meta_tvmaze_widesearch(file_name['title'],
                                                                         file_name['year']))
        else:
            tvmaze_id = str(TVMAZE_CONNECTION.com_meta_tvmaze_widesearch(file_name['title'],
                                                                         None))
        common_global.es_inst.com_elastic_index('info', {'response': tvmaze_id})
        if tvmaze_id is not None:
            #            # since there has been NO match whatsoever.....can "wipe" out everything
            #            media_id_json = json.dumps({'tvmaze_id': tvmaze_id})
            #            common_global.es_inst.com_elastic_index('info', {'stuff':"dbjson: %s", media_id_json)
            # check to see if metadata exists for tvmaze id
            metadata_uuid = db_connection.db_metatv_guid_by_tvmaze(tvmaze_id)
            common_global.es_inst.com_elastic_index('info', {"db result": metadata_uuid})
    common_global.es_inst.com_elastic_index('info', {'meta tv uuid': metadata_uuid,
                                                     'tvbmaze': tvmaze_id})
    return metadata_uuid, tvmaze_id


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
                print(('len %s', len(xml_show_data['Data']['Episode'][0]['id'])))
                if len(xml_show_data['Data']['Episode'][0]['id']) > 1:
                    # thetvdb is Episode
                    for episode_info in xml_show_data['Data']['Episode']:
                        common_global.es_inst.com_elastic_index('info', {'eps info': episode_info})
                        if episode_info['filename'] is not None:
                            # thetvdb
                            channel.basic_publish(exchange='mkque_cloud_ex',
                                                  routing_key='mkcloud',
                                                  body=json.dumps(
                                                      {'Type': 'download', 'Subtype': 'image',
                                                       'url': 'https://thetvdb.com/banners/'
                                                              + episode_info['filename'],
                                                       'local': '/mediakraken/web_app/MediaKraken/static/meta/images/'
                                                                + episode_info['filename']}),
                                                  properties=pika.BasicProperties(
                                                      content_type='text/plain',
                                                      delivery_mode=1))
                else:
                    if xml_show_data['Data']['Episode']['filename'] is not None:
                        # thetvdb
                        channel.basic_publish(exchange='mkque_cloud_ex',
                                              routing_key='mkcloud',
                                              body=json.dumps(
                                                  {'Type': 'download', 'Subtype': 'image',
                                                   'url': 'https://thetvdb.com/banners/'
                                                          + xml_show_data['Data']['Episode'][
                                                              'filename'],
                                                   'local': '/mediakraken/web_app/MediaKraken/static/meta/images/'
                                                            + xml_show_data['Data']
                                                            ['Episode']['filename']}),
                                              properties=pika.BasicProperties(
                                                  content_type='text/plain',
                                                  delivery_mode=1))
            except:
                if xml_show_data['Data']['Episode']['filename'] is not None:
                    # thetvdb
                    channel.basic_publish(exchange='mkque_cloud_ex',
                                          routing_key='mkcloud',
                                          body=json.dumps(
                                              {'Type': 'download', 'Subtype': 'image',
                                               'url': 'https://thetvdb.com/banners/'
                                                      + xml_show_data['Data'][
                                                          'Episode']['filename'],
                                               'local': '/mediakraken/web_app/MediaKraken/static/meta/images/'
                                                        + xml_show_data['Data']
                                                        ['Episode']['filename']}),
                                          properties=pika.BasicProperties(content_type='text/plain',
                                                                          delivery_mode=1))
        db_connection.db_commit()
    return metadata_uuid


def tv_fetch_save_tvmaze(db_connection, tvmaze_id):
    """
    Fetch show data from tvmaze
    """
    common_global.es_inst.com_elastic_index('info', {"meta tv tvmaze save fetch": tvmaze_id})
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
    common_global.es_inst.com_elastic_index('info', {"tvmaze full": result_json})
    if result_json is not None and result_json['status'] != 404:
        show_full_json = ({'Meta': {'tvmaze': result_json}})
        show_detail = show_full_json['Meta']['tvmaze']
        common_global.es_inst.com_elastic_index('info', {"detail": show_detail})
        tvmaze_name = show_detail['name']
        common_global.es_inst.com_elastic_index('info', {"name": tvmaze_name})
        try:
            thetvdb_id = str(show_detail['externals']['thetvdb'])
        except:
            thetvdb_id = None
        try:
            imdb_id = str(show_detail['externals']['imdb'])
        except:
            imdb_id = None
        series_id_json = json.dumps({'tvmaze': str(tvmaze_id),
                                     'imdb': imdb_id,
                                     'thetvdb': thetvdb_id})
        image_json = {'Images': {'tvmaze': {
            'Characters': {}, 'Episodes': {}, "Redo": True}}}
        metadata_uuid = db_connection.db_meta_tvmaze_insert(series_id_json, tvmaze_name,
                                                            json.dumps(
                                                                show_full_json),
                                                            json.dumps(image_json))
        # store person info
        if 'cast' in show_full_json['Meta']['tvmaze']['_embedded'] \
                and len(show_full_json['Meta']['tvmaze']['_embedded']['cast']) > 0:
            db_connection.db_meta_person_insert_cast_crew('tvmaze',
                                                          show_full_json['Meta']['tvmaze'][
                                                              '_embedded']['cast'])
        if 'crew' in show_full_json['Meta']['tvmaze']['_embedded'] \
                and len(show_full_json['Meta']['tvmaze']['_embedded']['crew']) > 0:
            db_connection.db_meta_person_insert_cast_crew('tvmaze',
                                                          show_full_json['Meta']['tvmaze'][
                                                              '_embedded']['crew'])
        # save rows for episode image fetch
        for episode_info in show_detail['_embedded']['episodes']:
            if episode_info['image'] is not None:
                # tvmaze image
                channel.basic_publish(exchange='mkque_cloud_ex',
                                      routing_key='mkcloud',
                                      body=json.dumps(
                                          {'Type': 'download', 'Subtype': 'image',
                                           'url': episode_info['image']['original'],
                                           'local': '/mediakraken/web_app/MediaKraken/static/meta/images/episodes/'
                                                    + str(episode_info['id']) + '.jpg'}),
                                      properties=pika.BasicProperties(content_type='text/plain',
                                                                      delivery_mode=1))
        db_connection.db_commit()
    return metadata_uuid


def metadata_tv_lookup(db_connection, media_file_path, download_que_json, download_que_id,
                       file_name):
    """
    Lookup tv metadata
    """
    # don't bother checking title/year as the main_server_metadata_api_worker does it already
    if not hasattr(metadata_tv_lookup, "metadata_last_id"):
        # it doesn't exist yet, so initialize it
        metadata_tv_lookup.metadata_last_id = None
        metadata_tv_lookup.metadata_last_imdb = None
        metadata_tv_lookup.metadata_last_tvdb = None
        metadata_tv_lookup.metadata_last_rt = None
    metadata_uuid = None  # so not found checks verify later
    common_global.es_inst.com_elastic_index('info', {'metadata_tv_lookup': str(file_name)})
    # determine provider id's from nfo/xml if they exist
    nfo_data, xml_data = metadata_nfo_xml.nfo_xml_file_tv(media_file_path)
    imdb_id, tvdb_id, rt_id = metadata_nfo_xml.nfo_xml_id_lookup_tv(nfo_data, xml_data)
    common_global.es_inst.com_elastic_index('info', {"tv look": imdb_id, 'tbdb': tvdb_id,
                                                     'rtid': rt_id})
    # if same as last, return last id and save lookup
    # check these dupes as the nfo/xml files might not exist to pull the metadata id from
    if imdb_id is not None and imdb_id == metadata_tv_lookup.metadata_last_imdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_tv_lookup.metadata_last_id
    if tvdb_id is not None and tvdb_id == metadata_tv_lookup.metadata_last_tvdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_tv_lookup.metadata_last_id
    if rt_id is not None and rt_id == metadata_tv_lookup.metadata_last_rt:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_tv_lookup.metadata_last_id
    # if ids from nfo/xml, query local db to see if exist
    if tvdb_id is not None:
        metadata_uuid = db_connection.db_metatv_guid_by_tvdb(tvdb_id)
    if imdb_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_metatv_guid_by_imdb(imdb_id)
    if rt_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_metatv_guid_by_rt(rt_id)
    # if ids from nfo/xml on local db
    common_global.es_inst.com_elastic_index('info', {"meta tv metadata_uuid A": metadata_uuid})
    if metadata_uuid is not None:
        db_connection.db_download_delete(download_que_id)
        # fall through here to set last name/year id's
    else:
        # id is known from nfo/xml but not in db yet so fetch data
        if tvdb_id is not None or imdb_id is not None:
            if tvdb_id is not None:
                dl_meta = db_connection.db_download_que_exists(download_que_id, 0,
                                                               'thetvdb', str(tvdb_id))
                if dl_meta is None:
                    metadata_uuid = download_que_json['MetaNewID']
                    download_que_json.update(
                        {'Status': 'Fetch', 'ProviderMetaID': str(tvdb_id)})
                    db_connection.db_download_update(json.dumps(download_que_json),
                                                     download_que_id)
                    # set provider last so it's not picked up by the wrong thread too early
                    db_connection.db_download_update_provider(
                        'thetvdb', download_que_id)
                else:
                    db_connection.db_download_delete(download_que_id)
                    metadata_uuid = dl_meta
            else:
                dl_meta = db_connection.db_download_que_exists(download_que_id, 0,
                                                               'thetvdb', imdb_id)
                if dl_meta is None:
                    metadata_uuid = download_que_json['MetaNewID']
                    download_que_json.update(
                        {'Status': 'Fetch', 'ProviderMetaID': imdb_id})
                    db_connection.db_download_update(json.dumps(download_que_json),
                                                     download_que_id)
                    # set provider last so it's not picked up by the wrong thread too early
                    db_connection.db_download_update_provider(
                        'thetvdb', download_que_id)
                else:
                    db_connection.db_download_delete(download_que_id)
                    metadata_uuid = dl_meta
    common_global.es_inst.com_elastic_index('info', {"meta tv metadata_uuid B": metadata_uuid})
    if metadata_uuid is None:
        # no ids found on the local database so begin name/year searches
        common_global.es_inst.com_elastic_index('info', {'stuff': "tv db lookup", 'file': str(
            file_name)})
        # db lookup by name and year (if available)
        if 'year' in file_name:
            metadata_uuid = db_connection.db_metatv_guid_by_tvshow_name(file_name['title'],
                                                                        file_name['year'])
        else:
            metadata_uuid = db_connection.db_metatv_guid_by_tvshow_name(
                file_name['title'], None)
        common_global.es_inst.com_elastic_index('info', {"tv db meta": metadata_uuid})
        if metadata_uuid is not None:
            # match found by title/year on local db so purge dl record
            db_connection.db_download_delete(download_que_id)
        else:
            # no matches by name/year
            # search tvmaze since not matched above via DB or nfo/xml
            download_que_json.update({'Status': 'Search'})
            # save the updated status
            db_connection.db_download_update(json.dumps(download_que_json),
                                             download_que_id)
            # set provider last so it's not picked up by the wrong thread
            db_connection.db_download_update_provider(
                'tvmaze', download_que_id)
    # set last values to negate lookups for same show
    metadata_tv_lookup.metadata_last_id = metadata_uuid
    metadata_tv_lookup.metadata_last_imdb = imdb_id
    metadata_tv_lookup.metadata_last_tvdb = tvdb_id
    metadata_tv_lookup.metadata_last_rt = rt_id
    return metadata_uuid
