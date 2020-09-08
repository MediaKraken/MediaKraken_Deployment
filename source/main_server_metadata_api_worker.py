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

import asyncio
import datetime
import json
import subprocess
import sys

import aio_pika
from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_metadata_limiter
from common import common_metadata_provider_anidb
from common import common_metadata_provider_imvdb
from common import common_metadata_provider_isbndb
from common import common_metadata_provider_musicbrainz
from common import common_metadata_provider_thegamesdb
from common import common_metadata_provider_themoviedb
from common import common_metadata_provider_thesportsdb
from common import common_signal
from common import common_string
from common.common_metadata_limiter import *
from guessit import guessit
from metadata import metadata_general
from metadata import metadata_identification


@ratelimited(common_metadata_limiter.API_LIMIT['anidb'][0]
             / common_metadata_limiter.API_LIMIT['anidb'][1])
def anidb(db_connection, download_data):
    """
    Rate limiter for AniDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in anidb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'anidb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['chart_lyrics'][0]
             / common_metadata_limiter.API_LIMIT['chart_lyrics'][1])
def chart_lyrics(db_connection, download_data):
    """
    Rate limiter for Chart Lyrics
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in chart_lyrics rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'chart_lyrics', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['comicvine'][0]
             / common_metadata_limiter.API_LIMIT['comicvine'][1])
def comicvine(db_connection, download_data):
    """
    Rate limiter for ComicVine
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in comicvine rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'comicvine', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['giantbomb'][0]
             / common_metadata_limiter.API_LIMIT['giantbomb'][1])
def giantbomb(db_connection, download_data):
    """
    Rate limiter for GiantBomb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in giantbomb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'giantbomb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['imdb'][0]
             / common_metadata_limiter.API_LIMIT['imdb'][1])
def imdb(db_connection, download_data):
    """
    Rate limiter for IMDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in imdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'imdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['imvdb'][0]
             / common_metadata_limiter.API_LIMIT['imvdb'][1])
def imvdb(db_connection, download_data):
    """
    Rate limiter for IMVdb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in imvdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'imvdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['isbndb'][0]
             / common_metadata_limiter.API_LIMIT['isbndb'][1])
def isbndb(db_connection, download_data):
    """
    Rate limiter for isbndb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in isbndb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'isbndb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['musicbrainz'][0]
             / common_metadata_limiter.API_LIMIT['musicbrainz'][1])
def musicbrainz(db_connection, download_data):
    """
    Rate limiter for MusicBrainz
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in musicbrainz rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'musicbrainz', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['omdb'][0]
             / common_metadata_limiter.API_LIMIT['omdb'][1])
def omdb(db_connection, download_data):
    """
    Rate limiter for OMDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in omdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'omdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['openlibrary'][0]
             / common_metadata_limiter.API_LIMIT['openlibrary'][1])
def openlibrary(db_connection, download_data):
    """
    Rate limiter for openlibrary
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in openlib rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'openlibrary', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['pitchfork'][0]
             / common_metadata_limiter.API_LIMIT['pitchfork'][1])
def pitchfork(db_connection, download_data):
    """
    Rate limiter for Pitchfork
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in pitchfork rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'pitchfork', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['pornhub'][0]
             / common_metadata_limiter.API_LIMIT['pornhub'][1])
def pornhub(db_connection, download_data):
    """
    Rate limiter for pornhub
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in pornhub rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'pornhub', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['televisiontunes'][0]
             / common_metadata_limiter.API_LIMIT['televisiontunes'][1])
def televisiontunes(db_connection, download_data):
    """
    Rate limiter for Television Tunes
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in televisiontunes rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(
        db_connection, 'televisiontunes', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['theaudiodb'][0]
             / common_metadata_limiter.API_LIMIT['theaudiodb'][1])
def theaudiodb(db_connection, download_data):
    """
    Rate limiter for TheAudioDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in theaudiodb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'theaudiodb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['thegamesdb'][0]
             / common_metadata_limiter.API_LIMIT['thegamesdb'][1])
def thegamesdb(db_connection, download_data):
    """
    Rate limiter for thegamesdb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in thegamesdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'thegamesdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['themoviedb'][0]
             / common_metadata_limiter.API_LIMIT['themoviedb'][1])
def themoviedb(db_connection, download_data):
    """
    Rate limiter for theMovieDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in moviedb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'themoviedb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['thesportsdb'][0]
             / common_metadata_limiter.API_LIMIT['thesportsdb'][1])
def thesportsdb(db_connection, download_data):
    """
    Rate limiter for TheSportsDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in thesportsdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'thesportsdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['tv_intros'][0]
             / common_metadata_limiter.API_LIMIT['tv_intros'][1])
def tv_intros(db_connection, download_data):
    """
    Rate limiter for TV Intros
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in tv_intros rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(db_connection, 'tv_intros', download_data)


# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
    'meta_api_worker_%s' % str(sys.argv[1]).lower())

# set signal exit breaks
common_signal.com_signal_set_break()

content_providers = str(sys.argv[1])
common_global.es_inst.com_elastic_index('info', {"worker meta api name":
                                                     content_providers})


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        common_global.es_inst.com_elastic_index('info', {"Message body", message.body})
        json_message = json.loads(message.body)
        if json_message['Type'] == 'Update Metadata':
            # this check is just in case there is a tv/etc collection later
            if content_providers == 'themoviedb':
                # TODO verify it isn't already running!
                subprocess.Popen(['python3', json_message['JSON']['program']],
                                 stdout=subprocess.PIPE, shell=False)
        elif json_message['Type'] == 'Update Collection':
            # this check is just in case there is a tv/etc collection later
            if content_providers == 'themoviedb':
                # TODO verify it isn't already running!
                subprocess.Popen(['python3', json_message['JSON']['program']],
                                 stdout=subprocess.PIPE, shell=False)
        # TODO add record for activity/etc for the user who ran this
        await aio_pika.IncomingMessage.ack()
        await asyncio.sleep(1)


async def main(loop):
    # open the database
    option_config_json, db_connection = common_config_ini.com_config_read(loop=loop,
                                                                          async_mode=True)
    # rabbitmq connection

    # parameters = pika.ConnectionParameters('mkstack_rabbitmq',
    #                                        socket_timeout=60,
    #                                        heartbeat=600,
    #                                        blocked_connection_timeout=300)
    # connection = pika.BlockingConnection(parameters)
    # # setup channels and queue
    # channel = connection.channel()
    # exchange = channel.exchange_declare(exchange="mkque_metadata_ex",
    #                                     exchange_type="direct",
    #                                     durable=True)
    # queue = channel.queue_declare(queue=content_providers,
    #                               durable=True)
    # channel.queue_bind(exchange="mkque_metadata_ex",
    #                    queue=content_providers)
    # channel.basic_qos(prefetch_count=1)

    # Perform connection
    connection = await aio_pika.connect("amqp://guest:guest@mkstack_rabbitmq/", loop=loop)
    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    # Declaring queue
    queue = await channel.declare_queue(content_providers,
                                        durable=True)
    # Start listening
    await queue.consume(on_message)

    # connection = await aio_pika.connect_robust("amqp://guest:guest@mkstack_rabbitmq/", loop=loop)
    # # Creating channel
    # channel = await connection.channel()
    # # Declaring exchange
    # exchange = await channel.declare_exchange("direct", durable=True)
    # # Declaring queue
    # queue = await channel.declare_queue(queue_name, durable=True)
    # # Binding queue
    # await queue.bind(exchange, routing_key)

    # setup the api key instances, if needed
    if content_providers == 'anidb':
        common_global.api_instance = common_metadata_provider_anidb.CommonMetadataANIdb(
            option_config_json)
    elif content_providers == 'imvdb':
        common_global.api_instance = common_metadata_provider_imvdb.CommonMetadataIMVdb(
            option_config_json)
    elif content_providers == 'isbndb':
        common_global.api_instance = common_metadata_provider_isbndb.CommonMetadataISBNdb(
            option_config_json)
    elif content_providers == 'musicbrainz':
        common_global.api_instance = common_metadata_provider_musicbrainz.CommonMetadataMusicbrainz(
            option_config_json)
    elif content_providers == 'thegamesdb':
        common_global.api_instance = common_metadata_provider_thegamesdb.CommonMetadataGamesDB(
            option_config_json)
    elif content_providers == 'themoviedb':
        common_global.api_instance = common_metadata_provider_themoviedb.CommonMetadataTMDB(
            option_config_json)
    elif content_providers == 'thesportsdb':
        common_global.api_instance = common_metadata_provider_thesportsdb.CommonMetadataTheSportsDB(
            option_config_json)
    # setup last used id's per thread
    metadata_last_id = None
    metadata_last_title = None
    metadata_last_year = None
    while True:
        # grab new batch of records to process by content provider
        for row_data in db_connection.db_download_read_provider(content_providers):
            common_global.es_inst.com_elastic_index('info', {"worker meta api row": row_data})
            # checking each provider like this to send through the limiter decorator
            if content_providers == 'anidb':
                anidb(db_connection, row_data)
            elif content_providers == 'chart_lyrics':
                chart_lyrics(db_connection, row_data)
            elif content_providers == 'comicvine':
                comicvine(db_connection, row_data)
            elif content_providers == 'giantbomb':
                giantbomb(db_connection, row_data)
            elif content_providers == 'imdb':
                imdb(db_connection, row_data)
            elif content_providers == 'imvdb':
                imvdb(db_connection, row_data)
            elif content_providers == 'isbndb':
                isbndb(db_connection, row_data)
            elif content_providers == 'musicbrainz':
                musicbrainz(db_connection, row_data)
            elif content_providers == 'omdb':
                omdb(db_connection, row_data)
            elif content_providers == 'pitchfork':
                pitchfork(db_connection, row_data)
            elif content_providers == 'pornhub':
                pornhub(db_connection, row_data)
            elif content_providers == 'televisiontunes':
                televisiontunes(db_connection, row_data)
            elif content_providers == 'theaudiodb':
                theaudiodb(db_connection, row_data)
            elif content_providers == 'thegamesdb':
                thegamesdb(db_connection, row_data)
            elif content_providers == 'themoviedb':
                themoviedb(db_connection, row_data)
            elif content_providers == 'thesportsdb':
                thesportsdb(db_connection, row_data)
            elif content_providers == 'tv_intros':
                tv_intros(db_connection, row_data)
            # Z records are the start of all lookups
            elif content_providers == 'Z':
                common_global.es_inst.com_elastic_index('info', {'worker Z meta api':
                                                                     row_data['mdq_download_json'][
                                                                         'ClassID'],
                                                                 'row': row_data['mdq_id'],
                                                                 'dl json': row_data[
                                                                     'mdq_download_json']})
                metadata_uuid = None
                # check for dupes by name/year
                file_name = guessit(row_data['mdq_download_json']['Path'])
                if type(file_name['title']) == list:
                    file_name['title'] = common_string.com_string_guessit_list(file_name['title'])
                common_global.es_inst.com_elastic_index('info',
                                                        {'worker Z filename': str(file_name)})
                if 'title' in file_name:
                    if 'year' in file_name:
                        if type(file_name['year']) == list:
                            file_name['year'] = file_name['year'][0]
                        if file_name['title'].lower() == metadata_last_title \
                                and file_name['year'] == metadata_last_year:
                            # matches last media scanned, so set with that metadata id
                            metadata_uuid = metadata_last_id
                    elif file_name['title'].lower() == metadata_last_title:
                        # matches last media scanned, so set with that metadata id
                        metadata_uuid = metadata_last_id
                    common_global.es_inst.com_elastic_index('info',
                                                            {
                                                                "worker Z meta api uuid": metadata_uuid,
                                                                'filename': str(file_name)})
                    # doesn't match the last file, so set the file to be id'd
                    if metadata_uuid is None:
                        # begin id process
                        metadata_uuid = await metadata_identification.metadata_identification(
                            db_connection,
                            row_data['mdq_download_json']['ClassID'],
                            row_data['mdq_download_json'],
                            row_data['mdq_id'],
                            row_data['mdq_que_type'],
                            file_name)
                    # allow NONE to be set so, unmatched stuff can work for skipping
                    metadata_last_id = metadata_uuid
                    metadata_last_title = file_name['title'].lower()
                    try:
                        metadata_last_year = file_name['year']
                    except KeyError:
                        metadata_last_year = None
                else:  # invalid guessit guess so set to ZZ to skip for now
                    await db_connection.db_download_update_provider('ZZ', row_data['mdq_id'])
                    await db_connection.db_commit()
                # update the media row with the json media id AND THE proper NAME!!!
                if metadata_uuid is not None:
                    common_global.es_inst.com_elastic_index('info', {"worker Z meta api update":
                                                                         metadata_uuid, 'row':
                                                                         row_data[
                                                                             'mdq_download_json'][
                                                                             'MediaID']})
                    await db_connection.db_begin()
                    await db_connection.db_update_media_id(row_data['mdq_download_json']['MediaID'],
                                                           metadata_uuid)
                    await db_connection.db_download_delete(row_data['mdq_id'])
                    await db_connection.db_commit()
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()
