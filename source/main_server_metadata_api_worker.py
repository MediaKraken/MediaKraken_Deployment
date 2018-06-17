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

import datetime
import json
import subprocess
import sys

import pika
from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_metadata_limiter
from common import common_string
from common.common_metadata_limiter import *
from guessit import guessit
from metadata import metadata_general
from metadata import metadata_identification


@ratelimited(common_metadata_limiter.API_LIMIT['anidb'][0]
             / common_metadata_limiter.API_LIMIT['anidb'][1])
def anidb(thread_db, download_data):
    """
    Rate limiter for AniDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in anidb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'anidb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['chart_lyrics'][0]
             / common_metadata_limiter.API_LIMIT['chart_lyrics'][1])
def chart_lyrics(thread_db, download_data):
    """
    Rate limiter for Chart Lyrics
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in chart_lyrics rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'chart_lyrics', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['comicvine'][0]
             / common_metadata_limiter.API_LIMIT['comicvine'][1])
def comicvine(thread_db, download_data):
    """
    Rate limiter for ComicVine
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in comicvine rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'comicvine', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['giantbomb'][0]
             / common_metadata_limiter.API_LIMIT['giantbomb'][1])
def giantbomb(thread_db, download_data):
    """
    Rate limiter for GiantBomb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in giantbomb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'giantbomb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['imdb'][0]
             / common_metadata_limiter.API_LIMIT['imdb'][1])
def imdb(thread_db, download_data):
    """
    Rate limiter for IMDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in imdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'imdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['imvdb'][0]
             / common_metadata_limiter.API_LIMIT['imvdb'][1])
def imvdb(thread_db, download_data):
    """
    Rate limiter for IMVdb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in imvdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'imvdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['isbndb'][0]
             / common_metadata_limiter.API_LIMIT['isbndb'][1])
def isbndb(thread_db, download_data):
    """
    Rate limiter for isbndb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in isbndb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'isbndb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['musicbrainz'][0]
             / common_metadata_limiter.API_LIMIT['musicbrainz'][1])
def musicbrainz(thread_db, download_data):
    """
    Rate limiter for MusicBrainz
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in musicbrainz rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'musicbrainz', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['omdb'][0]
             / common_metadata_limiter.API_LIMIT['omdb'][1])
def omdb(thread_db, download_data):
    """
    Rate limiter for OMDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in omdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'omdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['openlibrary'][0]
             / common_metadata_limiter.API_LIMIT['openlibrary'][1])
def openlibrary(thread_db, download_data):
    """
    Rate limiter for openlibrary
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in openlib rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'openlibrary', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['pitchfork'][0]
             / common_metadata_limiter.API_LIMIT['pitchfork'][1])
def pitchfork(thread_db, download_data):
    """
    Rate limiter for Pitchfork
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in pitchfork rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'pitchfork', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['televisiontunes'][0]
             / common_metadata_limiter.API_LIMIT['televisiontunes'][1])
def televisiontunes(thread_db, download_data):
    """
    Rate limiter for Television Tunes
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in televisiontunes rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(
        thread_db, 'televisiontunes', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['theaudiodb'][0]
             / common_metadata_limiter.API_LIMIT['theaudiodb'][1])
def theaudiodb(thread_db, download_data):
    """
    Rate limiter for TheAudioDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in theaudiodb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'theaudiodb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['thegamesdb'][0]
             / common_metadata_limiter.API_LIMIT['thegamesdb'][1])
def thegamesdb(thread_db, download_data):
    """
    Rate limiter for thegamesdb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in thegamesdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'thegamesdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['thelogodb'][0]
             / common_metadata_limiter.API_LIMIT['thelogodb'][1])
def thelogodb(thread_db, download_data):
    """
    Rate limiter for thelogodb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in thelogodb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'thelogodb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['themoviedb'][0]
             / common_metadata_limiter.API_LIMIT['themoviedb'][1])
def themoviedb(thread_db, download_data):
    """
    Rate limiter for theMovieDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in moviedb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'themoviedb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['thesportsdb'][0]
             / common_metadata_limiter.API_LIMIT['thesportsdb'][1])
def thesportsdb(thread_db, download_data):
    """
    Rate limiter for TheSportsDB
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in thesportsdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'thesportsdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['thetvdb'][0]
             / common_metadata_limiter.API_LIMIT['thetvdb'][1])
def thetvdb(thread_db, download_data):
    """
    Rate limiter for theTVdb
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in thetvdb rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'thetvdb', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['tvmaze'][0]
             / common_metadata_limiter.API_LIMIT['tvmaze'][1])
def tvmaze(thread_db, download_data):
    """
    Rate limiter for TVMaze
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in tvmaze rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'tvmaze', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['tv_intros'][0]
             / common_metadata_limiter.API_LIMIT['tv_intros'][1])
def tv_intros(thread_db, download_data):
    """
    Rate limiter for TV Intros
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in tv_intros rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'tv_intros', download_data)


@ratelimited(common_metadata_limiter.API_LIMIT['tvshowtime'][0]
             / common_metadata_limiter.API_LIMIT['tvshowtime'][1])
def tvshowtime(thread_db, download_data):
    """
    Rate limiter for TVShowTime
    """
    common_global.es_inst.com_elastic_index('info', {"here i am in tvshowtime rate":
        datetime.datetime.now().strftime(
            "%H:%M:%S.%f")})
    metadata_general.metadata_process(thread_db, 'tvshowtime', download_data)


def on_message(channel, method_frame, header_frame, body):
    """
    Process pika message
    """
    if body is not None:
        common_global.es_inst.com_elastic_index('info', {"Message body", body})
        json_message = json.loads(body)
        if json_message['Type'] == 'update':
            if content_providers == 'themoviedb':
                subprocess.Popen(['python',
                                  '/mediakraken/subprogram_metadata_tmdb_updates.py'], shell=False)
            elif content_providers == 'thetvdb':
                subprocess.Popen(['python',
                                  '/mediakraken/subprogram_metadata_thetvdb_updates.py'],
                                 shell=False)
            elif content_providers == 'tvmaze':
                subprocess.Popen(['python',
                                  '/mediakraken/subprogram_metadata_tvmaze_updates.py'],
                                 shell=False)
        elif json_message['Type'] == 'collection':
            # this check is just in case there is a tv/etc collection later
            if content_providers == 'themoviedb':
                subprocess.Popen(['python',
                                  '/mediakraken/subprogram_metadata_update_create_collections.py'],
                                 shell=False)
        # TODO add record for activity/etc for the user who ran this
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
    'meta_api_worker_%s' % str(sys.argv[1]).lower())
content_providers = str(sys.argv[1])
common_global.es_inst.com_elastic_index('info', {"worker meta api name":
                                                     content_providers})
# open the database
option_config_json, thread_db = common_config_ini.com_config_read()
# table the class_text into a dict...will lessen the db calls
class_text_dict = {}
for class_data in thread_db.db_media_class_list(None, None):
    class_text_dict[class_data['mm_media_class_guid']
    ] = class_data['mm_media_class_type']

# pika rabbitmq connection
parameters = pika.ConnectionParameters('mkrabbitmq',
                                       credentials=pika.PlainCredentials('guest', 'guest'))
connection = pika.BlockingConnection(parameters)

# setup channels and queue
channel = connection.channel()
exchange = channel.exchange_declare(exchange="mkque_metadata_ex", exchange_type="direct",
                                    durable=True)
queue = channel.queue_declare(queue=content_providers, durable=True)
channel.queue_bind(exchange="mkque_metadata_ex", queue=content_providers)
channel.basic_qos(prefetch_count=1)
# channel.basic_consume(on_message, queue=content_providers, no_ack=False)
# channel.start_consuming(inactivity_timeout=1)

# setup last used id's per thread
metadata_last_id = None
metadata_last_title = None
metadata_last_year = None
while True:
    # common_global.es_inst.com_elastic_index('info', {'stuff':'worker thread before read provider %s', content_providers)
    for row_data in thread_db.db_download_read_provider(content_providers):
        common_global.es_inst.com_elastic_index('info', {"worker meta api row":
                                                             row_data})
        # mdq_id,mdq_download_json
        if content_providers == 'anidb':
            anidb(thread_db, row_data)
        elif content_providers == 'chart_lyrics':
            chart_lyrics(thread_db, row_data)
        elif content_providers == 'comicvine':
            comicvine(thread_db, row_data)
        elif content_providers == 'giantbomb':
            giantbomb(thread_db, row_data)
        elif content_providers == 'imdb':
            imdb(thread_db, row_data)
        elif content_providers == 'imvdb':
            imvdb(thread_db, row_data)
        elif content_providers == 'isbndb':
            isbndb(thread_db, row_data)
        elif content_providers == 'omdb':
            omdb(thread_db, row_data)
        elif content_providers == 'pitchfork':
            pitchfork(thread_db, row_data)
        elif content_providers == 'televisiontunes':
            televisiontunes(thread_db, row_data)
        elif content_providers == 'theaudiodb':
            theaudiodb(thread_db, row_data)
        elif content_providers == 'thegamesdb':
            thegamesdb(thread_db, row_data)
        elif content_providers == 'thelogodb':
            thelogodb(thread_db, row_data)
        elif content_providers == 'themoviedb':
            themoviedb(thread_db, row_data)
        elif content_providers == 'thesportsdb':
            thesportsdb(thread_db, row_data)
        elif content_providers == 'thetvdb':
            thetvdb(thread_db, row_data)
        elif content_providers == 'tv_intros':
            tv_intros(thread_db, row_data)
        elif content_providers == 'tvmaze':
            tvmaze(thread_db, row_data)
        elif content_providers == 'tvshowtime':
            tvshowtime(thread_db, row_data)
        elif content_providers == 'Z':
            common_global.es_inst.com_elastic_index('info', {'worker Z meta api':
                                                                 class_text_dict[row_data[
                                                                     'mdq_download_json'][
                                                                     'ClassID']],
                                                             'row': row_data['mdq_id'],
                                                             'dl json': row_data[
                                                                 'mdq_download_json']})
            metadata_uuid = None
            # check for book/etc
            if class_text_dict[row_data['mdq_download_json']['ClassID']] == 'Book':
                # begin id process
                metadata_uuid = metadata_identification.metadata_identification(thread_db,
                                                                                class_text_dict[
                                                                                    row_data[
                                                                                        'mdq_download_json'][
                                                                                        'ClassID']],
                                                                                row_data[
                                                                                    'mdq_download_json'],
                                                                                row_data['mdq_id'],
                                                                                None)
            else:
                # check for dupes by name/year
                file_name = guessit(row_data['mdq_download_json']['Path'])
                if type(file_name['title']) == list:
                    file_name['title'] = common_string.com_string_guessit_list(file_name['title'])
                common_global.es_inst.com_elastic_index('info', {'worker Z filename':
                                                                     str(file_name)})
                if 'title' in file_name:
                    if 'year' in file_name:
                        if type(file_name['year']) == list:
                            file_name['year'] = file_name['year'][0]
                        if file_name['title'] == metadata_last_title \
                                and file_name['year'] == metadata_last_year:
                            thread_db.db_download_delete(row_data['mdq_id'])
                            metadata_uuid = metadata_last_id
                    elif file_name['title'] == metadata_last_title:
                        thread_db.db_download_delete(row_data['mdq_id'])
                        metadata_uuid = metadata_last_id
                    common_global.es_inst.com_elastic_index('info', {"worker Z meta api uuid":
                                                                         metadata_uuid,
                                                                     'filename': str(file_name)})
                    if metadata_uuid is None:
                        # begin id process
                        metadata_uuid = metadata_identification.metadata_identification(thread_db,
                                                                                        class_text_dict[
                                                                                            row_data[
                                                                                                'mdq_download_json'][
                                                                                                'ClassID']],
                                                                                        row_data[
                                                                                            'mdq_download_json'],
                                                                                        row_data[
                                                                                            'mdq_id'],
                                                                                        file_name)
                    # allow NONE to be set so, unmatched stuff can work for skipping
                    metadata_last_id = metadata_uuid
                    metadata_last_title = file_name['title']
                    try:
                        metadata_last_year = file_name['year']
                    except:
                        metadata_last_year = None
                else:  # invalid guessit guess so set to ZZ to skip for now
                    thread_db.db_download_update_provider(
                        'ZZ', row_data['mdq_id'])
            # update the media row with the json media id AND THE proper NAME!!!
            if metadata_uuid is not None:
                common_global.es_inst.com_elastic_index('info', {"worker Z meta api update":
                                                                     metadata_uuid, 'row':
                                                                     row_data[
                                                                         'mdq_download_json'][
                                                                         'MediaID']})
                thread_db.db_update_media_id(row_data['mdq_download_json']['MediaID'],
                                             metadata_uuid)
    time.sleep(1)
    # grab message from rabbitmq if available
    try:  # since can get connection drops
        method_frame, header_frame, body = channel.basic_get(
            queue=content_providers, no_ack=False)
        on_message(channel, method_frame, header_frame, body)
    except:
        pass
connection.cancel()
thread_db.db_close()
