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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import json
import sys
import signal
import os
import time
import datetime
from metadata import metadata_anime
from metadata import metadata_game
from metadata import metadata_identification
from metadata import metadata_movie
from metadata import metadata_music_video
from metadata import metadata_music
from metadata import metadata_periodicals
from metadata import metadata_person
from metadata import metadata_sports
from metadata import metadata_tv
from common import common_config_ini
from common import common_file
from common import common_hash
from common.common_metadata_limiter import *
from common import common_logging
from common import common_metadata
from common import common_metadata_imvdb
from common import common_metadata_isbndb
from common import common_metadata_limiter
from common import common_metadata_musicbrainz
from common import common_metadata_netflixroulette
from common import common_metadata_omdb
from common import common_metadata_pitchfork
from common import common_metadata_theaudiodb
from common import common_metadata_thegamesdb
from common import common_metadata_thelogodb
from common import common_metadata_thesportsdb
from common import common_metadata_thetvdb
from common import common_metadata_tmdb
from common import common_metadata_tv_intro
from common import common_metadata_tv_theme
from common import common_metadata_tvmaze
from common import common_network
from common import common_thetvdb
from concurrent import futures
import locale
locale.setlocale(locale.LC_ALL, '')


def signal_receive(signum, frame): # pylint: disable=W0613
    """
    Handle signal interupt
    """
    print('CHILD Main Metadata: Received USR1')
    # os.kill(proc_trigger.pid, signal.SIGTERM)
    # cleanup db
    db_connection.db_rollback()
    # log stop
    db_connection.db_activity_insert('MediaKraken_Metadata API Stop', None,\
        'System: Metadata API Stop', 'ServerMetadataAPIStop', None, None, 'System')
    db_connection.db_close()
    sys.stdout.flush()
    sys.exit(0)


# start logging
common_logging.com_logging_start('./log/MediaKraken_Metadata_API')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


db_connection.db_activity_insert('MediaKraken_Metadata API Start', None,\
     'System: Metadata API Start', 'ServerMetadataAPIStart', None, None, 'System')


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c # pylint: disable=E1101
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


@ratelimited(common_metadata_limiter.API_LIMIT['anidb'][0]\
     / common_metadata_limiter.API_LIMIT['anidb'][1])
def anidb(thread_db, download_data):
    """
    Rate limiter for AniDB
    """
    logging.debug("here i am in anidb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['chart_lyrics'][0]\
     / common_metadata_limiter.API_LIMIT['chart_lyrics'][1])
def chart_lyrics(thread_db, download_data):
    """
    Rate limiter for Chart Lyrics
    """
    logging.debug("here i am in chart_lyrics rate %s",\
        datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['comicvine'][0]\
     / common_metadata_limiter.API_LIMIT['comicvine'][1])
def comicvine(thread_db, download_data):
    """
    Rate limiter for ComicVine
    """
    logging.debug("here i am in comicvine rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['giantbomb'][0]\
     / common_metadata_limiter.API_LIMIT['giantbomb'][1])
def giantbomb(thread_db, download_data):
    """
    Rate limiter for GiantBomb
    """
    logging.debug("here i am in giantbomb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['imdb'][0]\
     / common_metadata_limiter.API_LIMIT['imdb'][1])
def imdb(thread_db, download_data):
    """
    Rate limiter for IMDB
    """
    logging.debug("here i am in imdb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['imvdb'][0]\
     / common_metadata_limiter.API_LIMIT['imvdb'][1])
def imvdb(thread_db, download_data):
    """
    Rate limiter for IMVdb
    """
    logging.debug("here i am in imvdb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        metadata_uuid = metadata_music_video.metadata_music_video_lookup()
        if metadata_uuid is None:
            thread_db.db_download_update_provider('theaudiodb', download_data['mdq_id'])


@ratelimited(common_metadata_limiter.API_LIMIT['musicbrainz'][0]\
     / common_metadata_limiter.API_LIMIT['musicbrainz'][1])
def musicbrainz(thread_db, download_data):
    """
    Rate limiter for MusicBrainz
    """
    logging.debug("here i am in musicbrainz rate %s",\
        datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['netflixroulette'][0]\
     / common_metadata_limiter.API_LIMIT['netflixroulette'][1])
def netflixroulette(thread_db, download_data):
    """
    Rate limiter for NetflixRoulette
    """
    logging.debug("here i am in netflixroulette rate %s",\
        datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['omdb'][0]\
     / common_metadata_limiter.API_LIMIT['omdb'][1])
def omdb(thread_db, download_data):
    """
    Rate limiter for OMDB
    """
    logging.debug("here i am in omdb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['pitchfork'][0]\
     / common_metadata_limiter.API_LIMIT['pitchfork'][1])
def pitchfork(thread_db, download_data):
    """
    Rate limiter for Pitchfork
    """
    logging.debug("here i am in pitchfork rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


# they went pay only
#@ratelimited(common_metadata_limiter.API_LIMIT['rotten_tomatoes'][0]\
#     / common_metadata_limiter.API_LIMIT['rotten_tomatoes'][1])
#def rotten_tomatoes(thread_db, download_data):
#    """
#    Rate limiter for Rotten Tomatoes
#    """
#    logging.debug("here i am in rotten_tomatoes rate %s",\
#        datetime.datetime.now().strftime("%H:%M:%S.%f"))
#    if download_data['mdq_download_json']['Status'] == "Search":
#        pass
#    elif download_data['mdq_download_json']['Status'] == "Fetch":
#        pass


@ratelimited(common_metadata_limiter.API_LIMIT['televisiontunes'][0]\
     / common_metadata_limiter.API_LIMIT['televisiontunes'][1])
def televisiontunes(thread_db, download_data):
    """
    Rate limiter for Television Tunes
    """
    logging.debug("here i am in televisiontunes rate %s",\
        datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['theaudiodb'][0]\
     / common_metadata_limiter.API_LIMIT['theaudiodb'][1])
def theaudiodb(thread_db, download_data):
    """
    Rate limiter for TheAudioDB
    """
    logging.debug("here i am in theaudiodb rate %s",\
        datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['thegamesdb'][0]\
    / common_metadata_limiter.API_LIMIT['thegamesdb'][1])
def thegamesdb(thread_db, download_data):
    """
    Rate limiter for thegamesdb
    """
    logging.debug("here i am in thegamesdb rate %s",\
        datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['thelogodb'][0]\
     / common_metadata_limiter.API_LIMIT['thelogodb'][1])
def thelogodb(thread_db, download_data):
    """
    Rate limiter for thelogodb
    """
    logging.debug("here i am in thelogodb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['themoviedb'][0]\
     / common_metadata_limiter.API_LIMIT['themoviedb'][1])
def themoviedb(thread_db, download_data):
    """
    Rate limiter for theMovieDB
    """
    logging.debug("here i am in moviedb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        metadata_uuid = metadata_movie.movie_search_tmdb(thread_db,\
            download_data['mdq_download_json']['Path'])
        if metadata_uuid is None:
            thread_db.db_download_update_provider('omdb', download_data['mdq_id'])
        else:
            thread_db.db_update_media_id(download_data['mdq_download_json']['Media'], metadata_uuid)
            # determine if the metadata is not downloaded
            if thread_db.db_meta_guid_by_tmdb(\
                    download_data['mdq_download_json']['ProviderMetaID']) is None:
                download_data['mdq_download_json'].update({'Status': 'Fetch'})
                thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),\
                    download_data['mdq_id'])
            else:
                thread_db.db_Download_Delete(download_data['mdq_id'])
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        if download_data['mdq_download_json']['ProviderMetaID'][0:2] != 'tt': # imdb id check
            tmdb_id = metadata_movie.movie_fetch_tmdb_imdb(\
                download_data['mdq_download_json']['ProviderMetaID'])
            if tmdb_id is not None:
                download_data['mdq_download_json'].update({'ProviderMetaID': tmdb_id})
                thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),\
                    download_data['mdq_id'])
        else:
            metadata_movie.movie_fetch_save_tmdb(thread_db,\
                download_data['mdq_download_json']['ProviderMetaID'])
            download_data['mdq_download_json'].update({'Status': 'FetchCastCrew'})
            thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),\
                download_data['mdq_id'])
    elif download_data['mdq_download_json']['Status'] == "FetchCastCrew":
        metadata_movie.movie_fetch_save_tmdb_cast_crew(thread_db,\
            download_data['mdq_download_json']['ProviderMetaID'])
        download_data['mdq_download_json'].update({'Status': 'FetchReview'})
        thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),\
            download_data['mdq_id'])
    elif download_data['mdq_download_json']['Status'] == "FetchReview":
        metadata_movie.movie_fetch_save_tmdb_review(thread_db,\
            download_data['mdq_download_json']['ProviderMetaID'])
        thread_db.db_Download_Delete(download_data['mdq_id'])


@ratelimited(common_metadata_limiter.API_LIMIT['thesportsdb'][0]\
     / common_metadata_limiter.API_LIMIT['thesportsdb'][1])
def thesportsdb(thread_db, download_data):
    """
    Rate limiter for TheSportsDB
    """
    logging.debug("here i am in thesportsdb rate %s",\
        datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['thetvdb'][0]\
     / common_metadata_limiter.API_LIMIT['thetvdb'][1])
def thetvdb(thread_db, download_data):
    """
    Rate limiter for theTVdb
    """
    logging.debug("here i am in thetvdb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['tvmaze'][0]\
     / common_metadata_limiter.API_LIMIT['tvmaze'][1])
def tvmaze(thread_db, download_data):
    """
    Rate limiter for TVMaze
    """
    logging.debug("here i am in tvmaze rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['tv_intros'][0]\
     / common_metadata_limiter.API_LIMIT['tv_intros'][1])
def tv_intros(thread_db, download_data):
    """
    Rate limiter for TV Intros
    """
    logging.debug("here i am in tv_intros rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@ratelimited(common_metadata_limiter.API_LIMIT['tvshowtime'][0]\
     / common_metadata_limiter.API_LIMIT['tvshowtime'][1])
def tvshowtime(thread_db, download_data):
    """
    Rate limiter for TVShowTime
    """
    logging.debug("here i am in tvshowtime rate %s",\
        datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


def worker(content_providers):
    """
    Worker thread for limiter
    """
    logging.debug("name: %s", content_providers)
    # open the database
    config_handle, option_config_json, thread_db = common_config_ini.com_config_read()
#    while True:
    for row_data in thread_db.db_download_read_provider(content_providers):
        logging.debug("row: %s", row_data)
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
        elif content_providers == 'netflixroulette':
            netflixroulette(thread_db, row_data)
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
            metadata_uuid = metadata_identification.metadata_identification(thread_db,\
                class_text_dict[row_data['mdq_download_json']['ClassID']],\
                row_data['mdq_download_json']['Path'], row_data['mdq_download_json'],\
                row_data['mdq_id'])
            # update the media row with the json media id AND THE proper NAME!!!
            if metadata_uuid is not None:
                logging.debug("update: %s %s",\
                    row_data['mdq_download_json']['MediaID'], metadata_uuid)
                thread_db.db_update_media_id(row_data['mdq_download_json']['MediaID'],\
                    metadata_uuid)
                thread_db.db_download_delete(row_data['mdq_id'])
    time.sleep(1)
    thread_db.db_commit()
    thread_db.db_close()
    return


# table the class_text into a dict...will lessen the db calls
class_text_dict = {}
for class_data in db_connection.db_media_class_list(None, None):
    class_text_dict[class_data['mm_media_class_guid']] = class_data['mm_media_class_type']


# grab the rate limiting providers and populate threads
with futures.ThreadPoolExecutor(len(common_metadata_limiter.API_LIMIT.keys())) as executor:
    futures = [executor.submit(worker, n) for n in common_metadata_limiter.API_LIMIT.keys()]
    for future in futures:
        logging.debug(future.result())


# log stop
db_connection.db_activity_insert('MediaKraken_Metadata API Stop', None,\
     'System: Metadata API Stop', 'ServerMetadataAPIStop', None, None, 'System')


# commit
db_connection.db_commit()


# close the database
db_connection.db_close()
