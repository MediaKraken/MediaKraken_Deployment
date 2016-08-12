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
import logging
# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import json
import uuid
import sys
import subprocess
import signal
import os
import time
import datetime
try:
    import cPickle as pickle
except:
    import pickle
sys.path.append("./common")
sys.path.append("./server")
sys.path.append("./server/metadata")
import database as database_base
import metadata_anime
import metadata_game
import metadata_identification
import metadata_movie
import metadata_music_video
import metadata_music
import metadata_periodicals
import metadata_person
import metadata_sports
import metadata_tv
import common_file
import common_Hash
import common_ISBNdb
from com_Metadata_Limiter import *
import common_logging
import common_Metadata
import common_Metadata_IMVDb
import common_Metadata_Limiter
import common_Metadata_MusicBrainz
import common_metadata_netflixroulette
import common_metadata_omdb
import common_Metadata_Pitchfork
import common_Metadata_TheAudioDB
import common_Metadata_TheGamesDB
import common_Metadata_TheLogoDB
import common_Metadata_TheSportsDB
import common_Metadata_TheTVDB
import common_metadata_tmdb
import common_Metadata_TV_Intro
import common_Metadata_TV_Theme
import common_Metadata_TVMaze
import common_network
import common_system
import common_TheTVDB
from concurrent import futures
import locale
locale.setlocale(locale.LC_ALL, '')


def signal_receive(signum, frame):
    print('CHILD Main Metadata: Received USR1')
    # os.kill(proc_trigger.pid, signal.SIGTERM)
    # cleanup db
    db.srv_db_Rollback()
    # log stop
    db.srv_db_Activity_Insert('MediaKraken_Metadata API Stop', None,\
        'System: Metadata API Stop', 'ServerMetadataAPIStop', None, None, 'System')
    db.srv_db_Close()
    sys.stdout.flush()
    sys.exit(0)


# store pid for initd
pid = os.getpid()
op = open("/var/mm_server_metadata_api.pid", "w")
op.write("%s" % pid)
op.close()


# start logging
common_logging.common_logging_Start('./log/MediaKraken_Metadata_API')


# open the database
db = database_base.MK_Server_Database()
db.srv_db_Open(Config.get('DB Connections', 'PostDBHost').strip(),\
    Config.get('DB Connections', 'PostDBPort').strip(),\
    Config.get('DB Connections', 'PostDBName').strip(),\
    Config.get('DB Connections', 'PostDBUser').strip(),\
    Config.get('DB Connections', 'PostDBPass').strip())


db.srv_db_Activity_Insert('MediaKraken_Metadata API Start', None,\
     'System: Metadata API Start', 'ServerMetadataAPIStart', None, None, 'System')


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


@RateLimited(com_Metadata_Limiter.API_Limit['AniDB'][0] / com_Metadata_Limiter.API_Limit['AniDB'][1])
def AniDB(thread_db, download_data):
    logging.debug("here i am in AniDB rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['Chart_Lyrics'][0] / com_Metadata_Limiter.API_Limit['Chart_Lyrics'][1])
def Chart_Lyrics(thread_db, download_data):
    logging.debug("here i am in Chart_Lyrics rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['ComicVine'][0] / com_Metadata_Limiter.API_Limit['ComicVine'][1])
def ComicVine(thread_db, download_data):
    logging.debug("here i am in ComicVine rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['GiantBomb'][0] / com_Metadata_Limiter.API_Limit['GiantBomb'][1])
def GiantBomb(thread_db, download_data):
    logging.debug("here i am in GiantBomb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['IMDB'][0] / com_Metadata_Limiter.API_Limit['IMDB'][1])
def IMDB(thread_db, download_data):
    logging.debug("here i am in IMDB rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['IMVDb'][0] / com_Metadata_Limiter.API_Limit['IMVDb'][1])
def IMVDb(thread_db, download_data):
    logging.debug("here i am in IMVDb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        metadata_uuid = metadata_music_video.metadata_music_video_lookup()
        if metadata_uuid is None:
            thread_db.srv_db_Download_Update_Provider('TheAudioDB', download_data['mdq_id'])


@RateLimited(com_Metadata_Limiter.API_Limit['MusicBrainz'][0] / com_Metadata_Limiter.API_Limit['MusicBrainz'][1])
def MusicBrainz(thread_db, download_data):
    logging.debug("here i am in MusicBrainz rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['NetflixRoulette'][0] / com_Metadata_Limiter.API_Limit['NetflixRoulette'][1])
def NetflixRoulette(thread_db, download_data):
    logging.debug("here i am in NetflixRoulette rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['OMDb'][0] / com_Metadata_Limiter.API_Limit['OMDb'][1])
def OMDb(thread_db, download_data):
    logging.debug("here i am in OMDb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['Pitchfork'][0] / com_Metadata_Limiter.API_Limit['Pitchfork'][1])
def Pitchfork(thread_db, download_data):
    logging.debug("here i am in Pitchfork rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['Rotten_Tomatoes'][0] / com_Metadata_Limiter.API_Limit['Rotten_Tomatoes'][1])
def Rotten_Tomatoes(thread_db, download_data):
    logging.debug("here i am in Rotten_Tomatoes rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['televisiontunes'][0] / com_Metadata_Limiter.API_Limit['televisiontunes'][1])
def televisiontunes(thread_db, download_data):
    logging.debug("here i am in televisiontunes rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['TheAudioDB'][0] / com_Metadata_Limiter.API_Limit['TheAudioDB'][1])
def TheAudioDB(thread_db, download_data):
    logging.debug("here i am in TheAudioDB rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['TheGamesDB'][0] / com_Metadata_Limiter.API_Limit['TheGamesDB'][1])
def TheGamesDB(thread_db, download_data):
    logging.debug("here i am in TheGamesDB rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['TheLogoDB'][0] / com_Metadata_Limiter.API_Limit['TheLogoDB'][1])
def TheLogoDB(thread_db, download_data):
    logging.debug("here i am in TheLogoDB rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['theMovieDB'][0] / com_Metadata_Limiter.API_Limit['theMovieDB'][1])
def theMovieDB(thread_db, download_data):
    logging.debug("here i am in moviedb rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        metadata_uuid = metadata_movie.movie_search_tmdb(thread_db, download_data['mdq_download_json']['Path'])
        if metadata_uuid is None:
            thread_db.srv_db_Download_Update_Provider('OMDb', download_data['mdq_id'])
        else:
            thread_db.srv_db_Update_Media_ID(download_data['mdq_download_json']['Media'], metadata_uuid)
            # determine if the metadata is not downloaded
            if thread_db.srv_db_Metadata_GUID_By_TMDB(download_data['mdq_download_json']['ProviderMetaID']) is None:
                download_data['mdq_download_json'].update({'Status': 'Fetch'})
                thread_db.srv_db_Download_Update(json.dumps(download_data['mdq_download_json']), download_data['mdq_id'])
            else:
                thread_db.srv_db_Download_Delete(download_data['mdq_id'])
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        if download_data['mdq_download_json']['ProviderMetaID'][0:2] != 'tt': # imdb id check
            tmdb_id = metadata_movie.movie_fetch_tmdb_imdb(download_data['mdq_download_json']['ProviderMetaID'])
            if tmdb_id is not None:
                download_data['mdq_download_json'].update({'ProviderMetaID': tmdb_id})
                thread_db.srv_db_Download_Update(json.dumps(download_data['mdq_download_json']), download_data['mdq_id'])
        else:
            metadata_movie.movie_fetch_save_tmdb(thread_db, download_data['mdq_download_json']['ProviderMetaID'])
            download_data['mdq_download_json'].update({'Status': 'FetchCastCrew'})
            thread_db.srv_db_Download_Update(json.dumps(download_data['mdq_download_json']), download_data['mdq_id'])
    elif download_data['mdq_download_json']['Status'] == "FetchCastCrew":
        metadata_movie.movie_fetch_save_tmdb_cast_crew(thread_db, download_data['mdq_download_json']['ProviderMetaID'])
        download_data['mdq_download_json'].update({'Status': 'FetchReview'})
        thread_db.srv_db_Download_Update(json.dumps(download_data['mdq_download_json']), download_data['mdq_id'])
    elif download_data['mdq_download_json']['Status'] == "FetchReview":
        metadata_movie.movie_fetch_save_tmdb_review(thread_db, download_data['mdq_download_json']['ProviderMetaID'])
        thread_db.srv_db_Download_Delete(download_data['mdq_id'])


@RateLimited(com_Metadata_Limiter.API_Limit['TheSportsDB'][0] / com_Metadata_Limiter.API_Limit['TheSportsDB'][1])
def TheSportsDB(thread_db, download_data):
    logging.debug("here i am in TheSportsDB rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['theTVDB'][0] / com_Metadata_Limiter.API_Limit['theTVDB'][1])
def theTVDB(thread_db, download_data):
    logging.debug("here i am in theTVDB rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['TVMaze'][0] / com_Metadata_Limiter.API_Limit['TVMaze'][1])
def TVMaze(thread_db, download_data):
    logging.debug("here i am in TVMaze rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['tv_intros'][0] / com_Metadata_Limiter.API_Limit['tv_intros'][1])
def tv_intros(thread_db, download_data):
    logging.debug("here i am in tv_intros rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


@RateLimited(com_Metadata_Limiter.API_Limit['tvshowtime'][0] / com_Metadata_Limiter.API_Limit['tvshowtime'][1])
def tvshowtime(thread_db, download_data):
    logging.debug("here i am in tvshowtime rate %s", datetime.datetime.now().strftime("%H:%M:%S.%f"))
    if download_data['mdq_download_json']['Status'] == "Search":
        pass
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        pass


def worker(content_providers):
    """
    Worker thread for limiter
    """
    logging.debug("name: %s", content_providers)
    thread_db = database_base.MK_Server_Database()
    thread_db.srv_db_Open(Config.get('DB Connections', 'PostDBHost').strip(),\
        Config.get('DB Connections', 'PostDBPort').strip(),\
        Config.get('DB Connections', 'PostDBName').strip(),\
        Config.get('DB Connections', 'PostDBUser').strip(),\
        Config.get('DB Connections', 'PostDBPass').strip())
#    while True:
    for row_data in thread_db.srv_db_Download_Read_By_Provider(content_providers):
        logging.debug("row: %s", row_data)
        # mdq_id,mdq_download_json
        if content_providers == 'AniDB':
            AniDB(thread_db, row_data)
        elif content_providers == 'Chart_Lyrics':
            Chart_Lyrics(thread_db, row_data)
        elif content_providers == 'ComicVine':
            ComicVine(thread_db, row_data)
        elif content_providers == 'GiantBomb':
            GiantBomb(thread_db, row_data)
        elif content_providers == 'IMDB':
            IMDB(thread_db, row_data)
        elif content_providers == 'IMVDb':
            IMVDb(thread_db, row_data)
        elif content_providers == 'NetflixRoulette':
            NetflixRoulette(thread_db, row_data)
        elif content_providers == 'OMDb':
            OMDb(thread_db, row_data)
        elif content_providers == 'Pitchfork':
            Pitchfork(thread_db, row_data)
        elif content_providers == 'televisiontunes':
            televisiontunes(thread_db, row_data)
        elif content_providers == 'TheAudioDB':
            TheAudioDB(thread_db, row_data)
        elif content_providers == 'TheGamesDB':
            TheGamesDB(thread_db, row_data)
        elif content_providers == 'TheLogoDB':
            TheLogoDB(thread_db, row_data)
        elif content_providers == 'theMovieDB':
            theMovieDB(thread_db, row_data)
        elif content_providers == 'TheSportsDB':
            TheSportsDB(thread_db, row_data)
        elif content_providers == 'theTVDB':
            theTVDB(thread_db, row_data)
        elif content_providers == 'tv_intros':
            tv_intros(thread_db, row_data)
        elif content_providers == 'TVMaze':
            TVMaze(thread_db, row_data)
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
                thread_db.srv_db_Update_Media_ID(row_data['mdq_download_json']['MediaID'], metadata_uuid)
                thread_db.srv_db_Download_Delete(row_data['mdq_id'])
    time.sleep(1)
    thread_db.srv_db_Commit()
    thread_db.srv_db_Close()
    return


# table the class_text into a dict...will lessen the db calls
class_text_dict = {}
for class_data in db.srv_db_Media_Class_List(None, None):
    class_text_dict[class_data['mm_media_class_guid']] = class_data['mm_media_class_type']


# grab the rate limiting providers and populate threads
with futures.ThreadPoolExecutor(len(com_Metadata_Limiter.API_Limit.keys())) as executor:
    futures = [executor.submit(worker, n) for n in com_Metadata_Limiter.API_Limit.keys()]
    for future in futures:
        logging.debug(future.result())


# log stop
db.srv_db_Activity_Insert('MediaKraken_Metadata API Stop', None,\
     'System: Metadata API Stop', 'ServerMetadataAPIStop', None, None, 'System')


# commit
db.srv_db_Commit()


# close the database
db.srv_db_Close()
