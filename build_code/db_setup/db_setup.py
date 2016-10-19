'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
import uuid
import psycopg2
import json


# media classes
# when adding new classes must update subprogram_match_known_media program as well
base_media_classes = (
    ("Adult", "Video", True),
    ("Anime", "Video", True),
    ("Book", "Publication", True),
    ("Boxset", None, False),
    ("Game CHD", None, False),
    ("Game ISO", None, False),
    ("Game ROM", None, False),
    ("Home Movie", "Video", True),
    ("Magazine", "Publication", True),
    ("Movie", "Video", True),
    ("Movie Extras", "Video", False),
    ("Movie Collection", None, False),
    ("Movie Theme", "Audio", False),
    ("Movie Trailer", "Video", False),
    ("Music", "Audio", True),
    ("Music Album", None, False),
    ("Music Collection", None, False),
    ("Music Lyric", None, False),
    ("Music Video", "Video", True),
    ("Person", None, False),
    ("Picture", "Image", True),
    ("Soundtrack", "Audio", False),
    ("Sports", "Video", True),
    ("Subtitle", None, False),
    ("TV Episode", "Video", False),
    ("TV Extras", "Video", False),
    ("TV Season", None, False),
    ("TV Show", "Video", True),
    ("TV Theme", "Audio", False),
    ("TV Trailer", "Video", False),
    ("Video Game", "Game", True),
    ("Video Game Intro", "Video", True),
    ("Video Game Speedrun", "Video", True),
    ("Video Game Superplay", "Video", True)
    )


# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
sql3_conn = psycopg2.connect("dbname='metamandb' user='metamanpg'"\
    " host='localhost' password='metamanpg'")
sql3_cursor = sql3_conn.cursor()


def db_table_index_check(resource_name):
    sql3_cursor.execute('SELECT to_regclass(\'public.' + resource_name + '\')')
    query_data = sql3_cursor.fetchone()[0]
    return query_data


# create tables for media directories to scan
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_media_dir (mm_media_dir_guid uuid'\
    ' CONSTRAINT mm_media_dir_pk PRIMARY KEY, mm_media_dir_path text,'\
    ' mm_media_dir_class_type uuid, mm_media_dir_last_scanned timestamp,'\
    ' mm_media_dir_status jsonb)')


'''
ALTER TABLE mm_media_dir
ADD CONSTRAINT foreign_book
FOREIGN KEY (book_id) REFERENCES books (id);
'''


# create table for media
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_media (mm_media_guid uuid'\
    ' CONSTRAINT mm_media_pk PRIMARY KEY, mm_media_class_guid uuid,'\
    ' mm_media_metadata_guid uuid, mm_media_path text, mm_media_ffprobe_json jsonb,'\
    ' mm_media_json jsonb)')
if db_table_index_check('mm_media_idxgin_ffprobe') is None:
    sql3_cursor.execute('CREATE INDEX mm_media_idxgin_ffprobe'\
    ' ON mm_media USING gin (mm_media_ffprobe_json)')
if db_table_index_check('mm_media_idx_metadata_uuid') is None:
    sql3_cursor.execute('CREATE INDEX mm_media_idx_metadata_uuid'\
    ' ON mm_media(mm_media_metadata_guid)')
if db_table_index_check('mm_media_idx_path') is None:
    sql3_cursor.execute('CREATE INDEX mm_media_idx_path ON mm_media(mm_media_path)')


# create table for remote media
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_media_remote (mmr_media_guid uuid'\
    ' CONSTRAINT mmr_media_remote_pk PRIMARY KEY, mmr_media_link_id uuid, mmr_media_uuid uuid,'\
    ' mmr_media_class_guid uuid, mmr_media_metadata_guid uuid, mmr_media_ffprobe_json jsonb,'\
    ' mmr_media_json jsonb)')
if db_table_index_check('mmr_media_idxgin_ffprobe') is None:
    sql3_cursor.execute('CREATE INDEX mmr_media_idxgin_ffprobe ON mm_media_remote'\
    ' USING gin (mmr_media_ffprobe_json)')
if db_table_index_check('mmr_media_idx_metadata_uuid') is None:
    sql3_cursor.execute('CREATE INDEX mmr_media_idx_metadata_uuid'\
    ' ON mm_media_remote(mmr_media_metadata_guid)')
if db_table_index_check('mmr_media_idx_link_uuid') is None:
    sql3_cursor.execute('CREATE INDEX mmr_media_idx_link_uuid'\
    ' ON mm_media_remote(mmr_media_link_id)')


# create table for remote server link
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_link (mm_link_guid uuid'\
    ' CONSTRAINT mm_link_guid_pk PRIMARY KEY, mm_link_name text, mm_link_json jsonb)')
if db_table_index_check('mm_link_json_idxgin') is None:
    sql3_cursor.execute('CREATE INDEX mm_link_json_idxgin ON mm_link USING gin (mm_link_json)')
if db_table_index_check('mm_link_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_link_idx_name ON mm_link(mm_link_name)')


# create table for metadata of tvshows (full json w/crew, w/episodes)
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_tvshow (mm_metadata_tvshow_guid uuid'\
    ' CONSTRAINT mm_metadata_tvshow_pk PRIMARY KEY, mm_metadata_media_tvshow_id jsonb,'\
    ' mm_metadata_tvshow_name text, mm_metadata_tvshow_json jsonb,'\
    ' mm_metadata_tvshow_localimage_json jsonb, mm_metadata_tvshow_user_json jsonb)')
if db_table_index_check('mm_metadata_tvshow_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idx_name'\
        ' ON mm_metadata_tvshow(mm_metadata_tvshow_name)')
if db_table_index_check('mm_metadata_tvshow_idx_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idx_name_lower'\
        ' ON mm_metadata_tvshow(lower(mm_metadata_tvshow_name))')
if db_table_index_check('mm_metadata_tvshow_idxgin_media_id') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idxgin_media_id'\
        ' ON mm_metadata_tvshow USING gin (mm_metadata_media_tvshow_id)')
if db_table_index_check('mm_metadata_tvshow_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idxgin_json ON mm_metadata_tvshow'\
        ' USING gin (mm_metadata_tvshow_json)')
if db_table_index_check('mm_metadata_tvshow_idxgin_localimage_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idxgin_localimage_json'\
        ' ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json)')
# yes double parans required
if db_table_index_check('mm_metadata_tvshow_idxgin_media_id_imdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idxgin_media_id_imdb'\
        ' ON mm_metadata_tvshow USING gin ((mm_metadata_media_tvshow_id->\'imdb\'))')
if db_table_index_check('mm_metadata_tvshow_idxgin_media_id_thetvdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdb'\
        ' ON mm_metadata_tvshow USING gin ((mm_metadata_media_tvshow_id->\'thetvdb\'))')
if db_table_index_check('mm_metadata_tvshow_idxgin_media_id_tmdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tmdb'\
        ' ON mm_metadata_tvshow USING gin ((mm_metadata_media_tvshow_id->\'TMDB\'))')
if db_table_index_check('mm_metadata_tvshow_idxgin_media_id_thetvdbseries') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdbseries'\
        ' ON mm_metadata_tvshow USING gin ((mm_metadata_media_tvshow_id->\'thetvdbSeries\'))')
if db_table_index_check('mm_metadata_tvshow_idxgin_media_id_tvmaze') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tvmaze'\
        ' ON mm_metadata_tvshow USING gin ((mm_metadata_media_tvshow_id->\'tvmaze\'))')
if db_table_index_check('mm_metadata_tvshow_idxgin_user_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_tvshow_idxgin_user_json'\
        ' ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_user_json)')


# create table for metadata sports media
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_sports (mm_metadata_sports_guid uuid'\
    ' CONSTRAINT mm_metadata_sports_pk PRIMARY KEY, mm_metadata_media_sports_id jsonb,'\
    ' mm_metadata_sports_name text, mm_metadata_sports_json jsonb,'\
    ' mm_metadata_sports_image_json jsonb)')
if db_table_index_check('mm_metadata_sports_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idx_name'\
        ' ON mm_metadata_sports(mm_metadata_sports_name)')
if db_table_index_check('mm_metadata_sports_idx_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idx_name_lower'\
        ' ON mm_metadata_sports(lower(mm_metadata_sports_name))')
if db_table_index_check('mm_metadata_sports_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idxgin_json ON mm_metadata_sports'\
        ' USING gin (mm_metadata_sports_json)')
if db_table_index_check('mm_metadata_sports_idxgin_media_id') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idxgin_media_id ON mm_metadata_sports'\
        ' USING gin (mm_metadata_media_sports_id)')
# yes double parans required
if db_table_index_check('mm_metadata_sports_idxgin_media_id_imdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idxgin_media_id_imdb'\
        ' ON mm_metadata_sports USING gin ((mm_metadata_media_sports_id->\'imdb\'))')
if db_table_index_check('mm_metadata_sports_idxgin_media_id_thetvdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdb'\
        ' ON mm_metadata_sports USING gin ((mm_metadata_media_sports_id->\'thetvdb\'))')
if db_table_index_check('mm_metadata_sports_idxgin_media_id_tmdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idxgin_media_id_tmdb'\
        ' ON mm_metadata_sports USING gin ((mm_metadata_media_sports_id->\'TMDB\'))')
if db_table_index_check('mm_metadata_sports_idxgin_media_id_thetvdbseries') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdbseries'\
        ' ON mm_metadata_sports USING gin ((mm_metadata_media_sports_id->\'thetvdbSeries\'))')
if db_table_index_check('mm_metadata_sports_idxgin_media_id_tvmaze') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idxgin_media_id_tvmaze'\
        ' ON mm_metadata_sports USING gin ((mm_metadata_media_sports_id->\'tvmaze\'))')
if db_table_index_check('mm_metadata_sports_idxgin_media_id_thesportsdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_sports_idxgin_media_id_thesportsdb'\
        ' ON mm_metadata_sports USING gin ((mm_metadata_media_sports_id->\'thesportsdb\'))')


# setup table for musician
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_musician'\
    ' (mm_metadata_musician_guid uuid CONSTRAINT mm_metadata_musician_pk PRIMARY KEY,'\
    ' mm_metadata_musician_name text, mm_metadata_musician_id jsonb,'\
    ' mm_metadata_musician_json jsonb)')
if db_table_index_check('mm_metadata_musician_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_musician_idx_name'\
        ' ON mm_metadata_musician(mm_metadata_musician_name)')
if db_table_index_check('mm_metadata_musician_idx_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_musician_idx_name_lower'\
        ' ON mm_metadata_musician(lower(mm_metadata_musician_name))')
if db_table_index_check('mm_metadata_musician_idxgin_id_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_musician_idxgin_id_json'\
        ' ON mm_metadata_musician USING gin (mm_metadata_musician_id)')
if db_table_index_check('mm_metadata_musician_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_musician_idxgin_json'\
        ' ON mm_metadata_musician USING gin (mm_metadata_musician_json)')


# setup table for albums
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_album (mm_metadata_album_guid uuid'\
    ' CONSTRAINT mm_metadata_album_pk PRIMARY KEY, mm_metadata_album_name text,'\
    ' mm_metadata_album_id jsonb, mm_metadata_album_json jsonb,'\
    ' mm_metadata_album_musician_guid uuid)')
if db_table_index_check('mm_metadata_album_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_album_idx_name'\
        ' ON mm_metadata_album(mm_metadata_album_name)')
if db_table_index_check('mm_metadata_album_idx_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_album_idx_name_lower'\
        ' ON mm_metadata_album(lower(mm_metadata_album_name))')
if db_table_index_check('mm_metadata_album_idxgin_id_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_album_idxgin_id_json'\
        ' ON mm_metadata_album USING gin (mm_metadata_album_id)')
if db_table_index_check('mm_metadata_album_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_album_idxgin_json'\
        ' ON mm_metadata_album USING gin (mm_metadata_album_json)')
if db_table_index_check('mm_metadata_album_idx_musician') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_album_idx_musician'\
        ' ON mm_metadata_album(mm_metadata_album_musician_guid)')


# create table for metadata of music songs
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_music (mm_metadata_music_guid uuid'\
    ' CONSTRAINT mm_metadata_music_pk PRIMARY KEY, mm_metadata_media_music_id jsonb,'\
    ' mm_metadata_music_name text, mm_metadata_music_json jsonb,'\
    ' mm_metadata_music_album_guid uuid)')
if db_table_index_check('mm_metadata_music_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_music_idx_name'\
        ' ON mm_metadata_music(mm_metadata_music_name)')
if db_table_index_check('mm_metadata_music_idx_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_music_idx_name_lower'\
        ' ON mm_metadata_music(lower(mm_metadata_music_name))')
if db_table_index_check('mm_metadata_music_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_music_idxgin_json ON mm_metadata_music'\
        ' USING gin (mm_metadata_music_json)')
if db_table_index_check('mm_metadata_music_idxgin_media_id') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_music_idxgin_media_id ON mm_metadata_music'\
        ' USING gin (mm_metadata_media_music_id)')
if db_table_index_check('mm_metadata_music_idx_album') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_music_idx_album'\
        ' ON mm_metadata_music(mm_metadata_music_album_guid)')


# create the base media class
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_media_class (mm_media_class_guid uuid'\
    ' CONSTRAINT mm_media_class_pk PRIMARY KEY, mm_media_class_type text,'\
    ' mm_media_class_parent_type text, mm_media_class_display boolean)')
if db_table_index_check('mm_media_class_idx_type') is None:
    sql3_cursor.execute('CREATE INDEX mm_media_class_idx_type'\
        ' ON mm_media_class(mm_media_class_type)')
# add media classes
for media_class in base_media_classes:
    sql3_cursor.execute('select count(*) from mm_media_class where mm_media_class_type = %s',\
                        (media_class[0],))
    if sql3_cursor.fetchone()[0] == 0:
        sql_params = str(uuid.uuid4()), media_class[0], media_class[1], media_class[2]
        sql3_cursor.execute('insert into mm_media_class (mm_media_class_guid,'\
            'mm_media_class_type,mm_media_class_parent_type,mm_media_class_display)'\
            ' values (%s,%s,%s,%s)', sql_params)


# create table for anime metadata
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_anime (mm_metadata_anime_guid uuid'\
    ' CONSTRAINT mm_metadata_anime_pk PRIMARY KEY, mm_metadata_anime_media_id jsonb,'\
    ' mm_media_anime_name text, mm_metadata_anime_json jsonb, mm_metadata_anime_mapping jsonb,'\
    ' mm_metadata_anime_mapping_before text, mm_metadata_anime_localimage_json jsonb,'\
    ' mm_metadata_anime_user_json jsonb)')
if db_table_index_check('mm_metadata_anime_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_anime_idx_name'\
    ' ON mm_metadata_anime(mm_media_anime_name)')
if db_table_index_check('mm_metadata_anime_idx_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_anime_idx_name_lower'\
        ' ON mm_metadata_anime(lower(mm_media_anime_name))')
if db_table_index_check('mm_metadata_anime_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_anime_idxgin_json'\
        ' ON mm_metadata_anime USING gin (mm_metadata_anime_json)')
if db_table_index_check('mm_metadata_aniem_idxgin_media_id') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_aniem_idxgin_media_id'\
        ' ON mm_metadata_anime USING gin (mm_metadata_anime_media_id)')
# yes double paran is required
if db_table_index_check('mm_metadata_anime_idxgin_media_id_anidb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_anime_idxgin_media_id_anidb'\
        ' ON mm_metadata_anime USING gin ((mm_metadata_anime_media_id->\'anidb\'))')
if db_table_index_check('mm_metadata_anime_idxgin_media_id_thetvdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_anime_idxgin_media_id_thetvdb'\
        ' ON mm_metadata_anime USING gin ((mm_metadata_anime_media_id->\'thetvdb\'))')
if db_table_index_check('mm_metadata_anime_idxgin_media_id_tmdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_anime_idxgin_media_id_tmdb'\
        ' ON mm_metadata_anime USING gin ((mm_metadata_anime_media_id->\'TMDB\'))')
if db_table_index_check('mm_metadata_anime_idxgin_media_id_imdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_anime_idxgin_media_id_imdb'\
        ' ON mm_metadata_anime USING gin ((mm_metadata_anime_media_id->\'imdb\'))')
if db_table_index_check('mm_metadata_anime_idxgin_user_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_anime_idxgin_user_json'\
        ' ON mm_metadata_anime USING gin (mm_metadata_anime_user_json)')


# create table for metadata
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_movie (mm_metadata_guid uuid'\
    ' CONSTRAINT mm_metadata_pk PRIMARY KEY, mm_metadata_media_id jsonb, mm_media_name text,'\
    ' mm_metadata_json jsonb, mm_metadata_localimage_json jsonb, mm_metadata_user_json jsonb)')
if db_table_index_check('mm_metadata_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idx_name ON mm_metadata_movie(mm_media_name)')
if db_table_index_check('mm_metadata_idx_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idx_name_lower'\
        ' ON mm_metadata_movie(lower(mm_media_name))')
if db_table_index_check('mm_metadata_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_json'\
        ' ON mm_metadata_movie USING gin (mm_metadata_json)')
if db_table_index_check('mm_metadata_idxgin_media_id') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_media_id'\
        ' ON mm_metadata_movie USING gin (mm_metadata_media_id)')
# yes double paran is required
if db_table_index_check('mm_metadata_idxgin_media_id_thetvdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_media_id_thetvdb'\
        ' ON mm_metadata_movie USING gin ((mm_metadata_media_id->\'thetvdb\'))')
if db_table_index_check('mm_metadata_idxgin_media_id_tmdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_media_id_tmdb'\
        ' ON mm_metadata_movie USING gin ((mm_metadata_media_id->\'TMDB\'))')
if db_table_index_check('mm_metadata_idxgin_media_id_imdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_media_id_imdb'\
        ' ON mm_metadata_movie USING gin ((mm_metadata_media_id->\'imdb\'))')
if db_table_index_check('mm_metadata_idxgin_user_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_user_json'\
        ' ON mm_metadata_movie USING gin (mm_metadata_user_json)')


# create table for metadata
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_music_video'\
    ' (mm_metadata_music_video_guid uuid CONSTRAINT mm_metadata_music_video_pk PRIMARY KEY,'\
    ' mm_metadata_music_video_media_id jsonb, mm_media_music_video_band text,'\
    ' mm_media_music_video_song text, mm_metadata_music_video_json jsonb,'\
    ' mm_metadata_music_video_localimage_json jsonb)')
if db_table_index_check('mm_metadata_idx_band_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idx_band_name'\
        ' ON mm_metadata_music_video(mm_media_music_video_band)')
if db_table_index_check('mm_metadata_idx_band_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idx_band_name_lower'\
        ' ON mm_metadata_music_video(lower(mm_media_music_video_band))')
if db_table_index_check('mm_metadata_idx_song_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idx_song_name'\
        ' ON mm_metadata_music_video(mm_media_music_video_song)')
if db_table_index_check('mm_metadata_idx_song_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idx_song_name_lower'\
        ' ON mm_metadata_music_video(lower(mm_media_music_video_song))')
if db_table_index_check('mm_metadata_idxgin_music_video_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_music_video_json'\
        ' ON mm_metadata_music_video USING gin (mm_metadata_music_video_json)')
if db_table_index_check('mm_metadata_idxgin_music_video_media_id') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_music_video_media_id'\
        ' ON mm_metadata_music_video USING gin (mm_metadata_music_video_media_id)')
# yes double paran is required
if db_table_index_check('mm_metadata_idxgin_music_video_media_id_imvdb') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_music_video_media_id_imvdb'\
        ' ON mm_metadata_music_video USING gin ((mm_metadata_music_video_media_id->\'imvdb\'))')


# create table for metadata for book
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_book (mm_metadata_book_guid uuid'\
    ' CONSTRAINT mm_metadata_book_pk PRIMARY KEY, mm_metadata_book_isbn text,'\
    ' mm_metadata_book_isbn13 text, mm_metadata_book_name text, mm_metadata_book_json jsonb)')
if db_table_index_check('mm_metadata_idx_book_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idx_book_name'\
        ' ON mm_metadata_book(mm_metadata_book_name)')
if db_table_index_check('mm_metadata_idx_book_name_lower') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idx_book_name_lower'\
        ' ON mm_metadata_book(lower(mm_metadata_book_name))')
if db_table_index_check('mm_metadata_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_json'\
        ' ON mm_metadata_book USING gin (mm_metadata_book_json)')
if db_table_index_check('mm_metadata_idxgin_isbn') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_isbn'\
        ' ON mm_metadata_book(mm_metadata_book_isbn)')
if db_table_index_check('mm_metadata_idxgin_isbn13') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_idxgin_isbn13'\
        ' ON mm_metadata_book(mm_metadata_book_isbn13)')


# create user activity table
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_user_activity (mm_activity_guid uuid'\
    ' CONSTRAINT mm_activity_pk PRIMARY KEY, mm_activity_name text, mm_activity_overview text,'\
    ' mm_activity_short_overview text, mm_activity_type text, mm_activity_itemid uuid,'\
    ' mm_activity_userid uuid, mm_activity_datecreated timestamp, mm_activity_log_severity text)')
if db_table_index_check('mm_user_activity_idx_user_guid') is None:
    sql3_cursor.execute('CREATE INDEX mm_user_activity_idx_user_guid'\
        ' ON mm_user_activity(mm_activity_userid)')
if db_table_index_check('mm_user_activity_idx_date') is None:
    sql3_cursor.execute('CREATE INDEX mm_user_activity_idx_date'\
        ' ON mm_user_activity(mm_activity_datecreated)')


# notification table
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_notification (mm_notification_guid uuid'\
    ' CONSTRAINT mm_notification_pk PRIMARY KEY, mm_notification_text text,'\
    ' mm_notification_time timestamp, mm_notification_dismissable bool)')
if db_table_index_check('mm_notification_idx_time') is None:
    sql3_cursor.execute('CREATE INDEX mm_notification_idx_time'\
        ' ON mm_notification(mm_notification_time)')
if db_table_index_check('mm_notification_idx_dismissable') is None:
    sql3_cursor.execute('CREATE INDEX mm_notification_idx_dismissable'\
        ' ON mm_notification(mm_notification_dismissable)')


# create table for user
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_user (id SERIAL PRIMARY KEY,'\
    ' username text, email text, password text, created_at timestamp with time zone,'\
    ' active boolean, is_admin boolean, user_json jsonb, lang text)')
if db_table_index_check('mm_user_idx_username') is None:
    sql3_cursor.execute('CREATE INDEX mm_user_idx_username ON mm_user(username)')


# add table for reviews
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_review (mm_review_guid uuid'\
    ' CONSTRAINT mm_review_pk PRIMARY KEY, mm_review_metadata_id jsonb,'\
    ' mm_review_metadata_guid uuid, mm_review_json jsonb)')
if db_table_index_check('mm_metadata_review_idxgin_media_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_review_idxgin_media_json'\
        ' ON mm_review USING gin (mm_review_metadata_id)')
if db_table_index_check('mm_metadata_review_idx_metadata_uuid') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_review_idx_metadata_uuid'\
        ' ON mm_review(mm_review_metadata_guid)')


# add table to store cd discid's
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_discid (mm_discid_guid uuid'\
    ' CONSTRAINT mm_discid_guid_pk PRIMARY KEY, mm_discid_discid text,'\
    ' mm_discid_media_info jsonb)')
if db_table_index_check('mm_discid_idx_discid') is None:
    sql3_cursor.execute('CREATE INDEX mm_discid_idx_discid ON mm_discid(mm_discid_discid)')


# create table for metadata collections
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_collection'\
    ' (mm_metadata_collection_guid uuid CONSTRAINT mm_metadata_collection_guid_pk PRIMARY KEY,'\
    ' mm_metadata_collection_name jsonb, mm_metadata_collection_media_ids jsonb,'\
    ' mm_metadata_collection_json jsonb, mm_metadata_collection_imagelocal_json jsonb)')
if db_table_index_check('mm_metadata_collection_idxgin_media_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_collection_idxgin_media_json'\
        ' ON mm_metadata_collection USING gin (mm_metadata_collection_media_ids)')
if db_table_index_check('mm_metadata_collection_idxgin_name_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_collection_idxgin_name_json'\
        ' ON mm_metadata_collection USING gin (mm_metadata_collection_name)')
if db_table_index_check('mm_metadata_collection_idxgin_meta_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_collection_idxgin_meta_json'\
        ' ON mm_metadata_collection USING gin (mm_metadata_collection_json)')


# create cron tables
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_cron (mm_cron_guid uuid'\
    ' CONSTRAINT mm_cron_guid_pk PRIMARY KEY, mm_cron_name text, mm_cron_description text,'\
    ' mm_cron_enabled bool, mm_cron_schedule text, mm_cron_last_run timestamp,'\
    ' mm_cron_file_path text)')

base_cron = [
    # game subprograms
    ('Game Audit', 'Scan for new game media', './subprogram_game_audit.py'),
    # media/metadata subprograms
    ('Create Chapter Image', 'Create chapter images for all media', './subprogram_create_chapter_images.py'),
    ('Station Logo Fetch', 'Grab new logos from thelogodb', './subprogram_logo_download.py'),
    ('Anime', 'Match anime via Scudlee data', './subprogram_match_anime_id_scudlee.py'),
    ('Roku Thumb', 'Generate Roku thumbnail images', './subprogram_roku_thumbnail_generate.py'),
    ('Schedules Direct', 'Fetch TV schedules from Schedules Direct', './subprogram_schedules_direct_updates.py'),
    ('Subtitle', 'Download missing subtitles for media', './subprogram_subtitle_downloader.py'),
    ('thetvdb Images', 'Grab missing thetvdb images', './subprogram_thetvdb_images.py'),
    ('thetvdb Update', 'Grab updated thetvdb metadata', './subprogram_thetvdb_updates.py'),
    ('The Movie Database', 'Grab updated movie metadata', './subprogram_tmdb_updates.py'),
    ('tvmaze Images', 'Grab missing tvmaze images', './subprogram_tvmaze_images.py'),
    ('tvmaze Update', 'Grab updated tvmaze metadata', './subprogram_tvmze_updates.py'),
    ('Collections', 'Create and update collection(s)', './subprogram_update_create_collections.py'),
    # normal subprograms
    ('Chromecast', 'Scan for chromecast device(s)', './subprogram_chromecast_discover.py'),
    ('Media Scan', 'Scan for new media', './subprogram_file_scan.py'),
    ('iRadio Scan', 'Scan for iRadio stations', './subprogram_iradio_channels.py'),
    ('Backup', 'Backup Postgresql DB', './subprogram_postgresql_backup.py'),
    ('DB Vacuum', 'Postgresql Vacuum Analyze all tables', './subprogram_postgresql_vacuum.py'),
    ('Sync', 'Sync/transcode media', './subprogram_sync.py'),
    ('Tuner', 'Scan for tuner device(s)', './subprogram_tuner_discover.py'),
    ('ZFS Check', 'Check local ZFS for failed drives', './subprogram_zfs_check.py'),
    ]
# create base cron entries
sql3_cursor.execute('select count(*) from mm_cron')
if sql3_cursor.fetchone()[0] == 0:
    for base_item in base_cron:
        sql_params = str(uuid.uuid4()), base_item[0], base_item[1], False, 'Days 1',\
            psycopg2.Timestamp(1970, 1, 1, 0, 0, 1), base_item[2]
        sql3_cursor.execute('insert into mm_cron (mm_cron_guid, mm_cron_name,'\
            ' mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run,'\
            ' mm_cron_file_path) values (%s,%s,%s,%s,%s,%s,%s)', sql_params)


# create iradio tables
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_radio (mm_radio_guid uuid'\
    ' CONSTRAINT mm_radio_guid_pk PRIMARY KEY, mm_radio_name text,'\
    ' mm_radio_adress text, mm_radio_active bool)')


# create tables for sync
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_sync (mm_sync_guid uuid'\
    ' CONSTRAINT mm_sync_guid_pk PRIMARY KEY, mm_sync_path text, mm_sync_path_to text,'\
    ' mm_sync_options_json jsonb)')
if db_table_index_check('mm_sync_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_sync_idxgin_json'\
        ' ON mm_sync USING gin (mm_sync_options_json)')


# create the table for loaning media
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_loan (mm_loan_guid uuid'\
    ' CONSTRAINT mm_loan_guid_pk PRIMARY KEY, mm_loan_media_id uuid, mm_loan_user_id uuid,'\
    ' mm_load_user_loan_id uuid, mm_loan_time timestamp, mm_loan_return_time timestamp)')


# create the table for "triggers"
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_trigger (mm_trigger_guid uuid'\
    ' CONSTRAINT mm_trigger_guid_pk PRIMARY KEY, mm_trigger_command bytea)')


## create table for country
#sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_country (mm_country_guid uuid CONSTRAINT mm_country_guid_pk PRIMARY KEY, mm_country_name text, mm_country_code text, mm_country_lang_guid uuid)')
#if db_table_index_check('mm_country_idx_name') is None:
#    sql3_cursor.execute('CREATE INDEX mm_country_idx_name ON mm_country(mm_country_name)')
#if db_table_index_check('mm_country_idx_code') is None:
#    sql3_cursor.execute('CREATE INDEX mm_country_idx_code ON mm_country(mm_country_code)')
#if db_table_index_check('mm_country_idx_lang') is None:
#    sql3_cursor.execute('CREATE INDEX mm_country_idx_lang ON mm_country(mm_country_lang_guid)')


# create table for logos
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_metadata_logo (mm_metadata_logo_guid uuid'\
    ' CONSTRAINT mm_metadata_logo_guid_pk PRIMARY KEY, mm_metadata_logo_media_guid jsonb,'\
    ' mm_metadata_logo_image_path text)')
if db_table_index_check('mm_metadata_logo_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_logo_idxgin_json'\
        ' ON mm_metadata_logo USING gin (mm_metadata_logo_media_guid)')


# create table for channels
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_channel (mm_channel_guid uuid'\
    ' CONSTRAINT mm_channel_guid_pk PRIMARY KEY, mm_channel_name text,'\
    ' mm_channel_media_id jsonb, mm_channel_country_guid uuid, mm_channel_logo_guid uuid)')
if db_table_index_check('mm_channel_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_channel_idx_name ON mm_channel(mm_channel_name)')
if db_table_index_check('mm_channel_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_channel_idxgin_json'\
        ' ON mm_channel USING gin (mm_channel_media_id)')
if db_table_index_check('mm_channel_idx_country') is None:
    sql3_cursor.execute('CREATE INDEX mm_channel_idx_country'\
        ' ON mm_channel(mm_channel_country_guid)')
if db_table_index_check('mm_channel_idx_logo') is None:
    sql3_cursor.execute('CREATE INDEX mm_channel_idx_logo ON mm_channel(mm_channel_logo_guid)')


# create table for user groups
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_user_group (mm_user_group_guid uuid'\
    ' CONSTRAINT mm_user_group_guid_pk PRIMARY KEY, mm_user_group_name text,'\
    ' mm_user_group_description text, mm_user_group_rights_json jsonb)')
if db_table_index_check('mm_user_group_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_user_group_idx_name ON mm_user_group(mm_user_group_name)')
sql3_cursor.execute('select count(*) from mm_user_group')
if sql3_cursor.fetchone()[0] == 0:
    base_group = [('Administrator', 'Server administrator',\
        json.dumps({'Admin': True, 'PreviewOnly':False})), ('User', 'General user',\
        json.dumps({'Admin': False, 'PreviewOnly':False})), ('Guest', 'Guest (Preview only)',\
        json.dumps({'Admin': False, 'PreviewOnly':True}))]
    # create base group entries
    for base_item in base_group:
        sql_params = str(uuid.uuid4()), base_item[0], base_item[1], base_item[2]
        sql3_cursor.execute('insert into mm_user_group (mm_user_group_guid,'\
            ' mm_user_group_name, mm_user_group_description, mm_user_group_rights_json)'\
            ' values (%s,%s,%s,%s)', sql_params)


# create table for user profiles
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_user_profile (mm_user_profile_guid uuid'\
    ' CONSTRAINT mm_user_profile_guid_pk PRIMARY KEY, mm_user_profile_name text,'\
    ' mm_user_profile_json jsonb)')
if db_table_index_check('mm_user_profile_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_user_profile_idx_name'\
        ' ON mm_user_profile(mm_user_profile_name)')
sql3_cursor.execute('select count(*) from mm_user_profile')
if sql3_cursor.fetchone()[0] == 0:
    # NC17, R, PG-13, PG, G
    base_user = (
        ('Adult', json.dumps({'Adult': True, 'MaxRating': 5, 'Sync': True, 'MaxBR': 100,\
            'Movie': True, 'Music': True, 'TV': True, 'Sports': True, 'LiveTV': True,\
            'Images': True, 'Games': True, 'Books': True, 'IRadio': True, 'Home': True,\
            '3D': True, 'Internet': True, 'Lang': 'en'})),
        ('Teen', json.dumps({'Adult': False, 'MaxRating': 3, 'Sync': False, 'MaxBR': 50,\
            'Movie': True, 'Music': True, 'TV': True, 'Sports': True, 'LiveTV': True,\
            'Images': True, 'Games': True, 'Books': True, 'IRadio': True, 'Home': True,\
            '3D': True, 'Internet': True, 'Lang': 'en'})),
        ('Child', json.dumps({'Adult': False, 'MaxRating': 0, 'Sync': False, 'MaxBR': 20,\
            'Movie': True, 'Music': True, 'TV': True, 'Sports': True, 'LiveTV': False,\
            'Images': True, 'Games': True, 'Books': True, 'IRadio': False, 'Home': True,\
            '3D': False, 'Internet': False, 'Lang': 'en'}))
        )
    for base_item in base_user:
        sql_params = str(uuid.uuid4()), base_item[0], base_item[1]
        sql3_cursor.execute('insert into mm_user_profile (mm_user_profile_guid,'\
            ' mm_user_profile_name, mm_user_profile_json) values (%s, %s, %s)', sql_params)


# create options and status table
sql3_cursor.execute('CREATE TABLE IF NOT EXISTS mm_options_and_status'\
    ' (mm_options_and_status_guid uuid CONSTRAINT mm_options_and_status_guid_pk PRIMARY KEY,'\
    ' mm_options_json jsonb, mm_status_json jsonb)')
sql3_cursor.execute('select count(*) from mm_options_and_status')
if sql3_cursor.fetchone()[0] == 0:
    sql_params = str(uuid.uuid4()), json.dumps({'Backup':{'BackupType': 'awss3', 'Interval': 0}, 'MaxResumePct': 5,\
    'MediaKrakenServer': {'ListenPort': 8098, 'ImageWeb': 8099, 'FFMPEG': 8900, 'APIPort': 8097,\
        'MetadataImageLocal': '/home/metaman/github/MediaKraken_Deployment/server/web_app/MetaMan/static/meta/images',\
        'BackupLocal': '/home/metaman/github/MediaKraken_Deployment/server/backups/'},\
    'API': {'MediaBrainz': None, 'AniDB': None, 'theTVdb': '147CB43DCA8B61B7',\
        'theMovieDB': 'f72118d1e84b8a1438935972a9c37cac',\
        'TheSportsDB': '4352761817344', 'TheLogoDB': None, 'OpenSubtitles': None,\
        'Google': None, 'GlobalCache': None, 'RottenTomatoes': 'f4tnu5dn9r7f28gjth3ftqaj',\
        'ISBNdb': '25C8IT4I', 'IMVDb': None, 'TVMaze': None},\
    'MediaBrainz': {'Host': '10.0.0.35', 'Port': 5000, 'User': None, 'Password': None,\
        'BrainzDBHost': '10.0.0.35', 'BrainzDBPort': 5432, 'BrainzDBName': 'musicbrainz',\
        'BrainzDBUser': 'musicbrainz', 'BrainzDBPass': 'musicbrainz'},\
    'Transmission': {'Host': '10.0.0.151', 'Port': 9091},\
    'Dropbox': {'APIKey': None, 'APISecret': None},\
    'AWSS3': {'AccessKey': None, 'SecretAccessKey': None, 'Bucket': 'mediakraken',\
        'BackupBucket': 'mkbackup'},\
    'OneDrive': {'ClientID': None, 'SecretKey': None},\
    'GoogleDrive': {'SecretFile': None},\
    'Trakt': {'ApiKey': None, 'ClientID': None, 'SecretKey': None},\
    'SD': {'User': None, 'Password': None},\
    }), json.dumps({'thetvdb_Updated_Epoc':0})
    sql3_cursor.execute('insert into mm_options_and_status (mm_options_and_status_guid,'\
        'mm_options_json,mm_status_json) values (%s,%s,%s)', sql_params)


# create table game_info
sql3_cursor.execute('create table IF NOT EXISTS mm_metadata_game_software_info (gi_id uuid'\
    ' CONSTRAINT gi_id_mpk PRIMARY KEY, gi_system_id uuid, gi_game_info_json jsonb)')
if db_table_index_check('gi_system_id_ndx') is None:
    sql3_cursor.execute('CREATE INDEX gi_system_id_ndx'\
        ' on mm_metadata_game_software_info (gi_system_id);')  # so can match systems quickly
if db_table_index_check('mm_game_info_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_game_info_idxgin_json'\
        ' ON mm_metadata_game_software_info USING gin (gi_game_info_json)')
if db_table_index_check('mm_game_info_idxgin_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_game_info_idxgin_name'\
        ' ON mm_metadata_game_software_info USING gin ((gi_game_info_json->\'@name\'))')


# create table for games systems
sql3_cursor.execute('create table IF NOT EXISTS mm_metadata_game_systems_info (gs_id uuid'\
    ' CONSTRAINT gs_id_pk primary key, gs_game_system_id integer,'\
    ' gs_game_system_name text, gs_game_system_alias text, gs_game_system_json jsonb)')
if db_table_index_check('mm_game_systems_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_game_systems_idxgin_json'\
        ' ON mm_metadata_game_systems_info USING gin (gs_game_system_json)')


# person for bio and image info
sql3_cursor.execute('create table IF NOT EXISTS mm_metadata_person (mmp_id uuid'\
    ' CONSTRAINT mmp_id_pk primary key, mmp_person_media_id jsonb,'\
    ' mmp_person_meta_json jsonb, mmp_person_image jsonb, mmp_person_name text)')
if db_table_index_check('mm_metadata_person_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_person_idx_name'\
        ' ON mm_metadata_person(mmp_person_name)')
if db_table_index_check('mm_metadata_person_idxgin_id_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_person_idxgin_id_json'\
        ' ON mm_metadata_person USING gin (mmp_person_media_id)')
if db_table_index_check('mm_metadata_person_idxgin_meta_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_metadata_person_idxgin_meta_json'\
        ' ON mm_metadata_person USING gin (mmp_person_meta_json)')


# queue
sql3_cursor.execute('create table IF NOT EXISTS mm_download_que (mdq_id uuid'\
    ' CONSTRAINT mdq_id_pk primary key, mdq_provider text, mdq_download_json jsonb)')
if db_table_index_check('mm_download_idx_provider') is None:
    sql3_cursor.execute('CREATE INDEX mm_download_idx_provider ON mm_download_que(mdq_provider)')


# tuners
sql3_cursor.execute('create table IF NOT EXISTS mm_tuner (mm_tuner_id uuid'\
    ' CONSTRAINT mm_tuner_id_pk primary key, mm_tuner_json jsonb)')


# nas
sql3_cursor.execute('create table IF NOT EXISTS mm_nas (mm_nas_id uuid'\
    ' CONSTRAINT mm_nas_id_pk primary key, mm_nas_json jsonb)')


# hardware device
sql3_cursor.execute('create table IF NOT EXISTS mm_device (mm_device_id uuid'\
    ' CONSTRAINT mm_device_id_pk primary key, mm_device_type text, mm_device_json jsonb)')
if db_table_index_check('mm_device_idx_type') is None:
    sql3_cursor.execute('CREATE INDEX mm_device_idx_type ON mm_device(mm_device_type)')
if db_table_index_check('mm_device_idxgin_json') is None:
    sql3_cursor.execute('CREATE INDEX mm_device_idxgin_json'\
        ' ON mm_device USING gin (mm_device_json)')


# tv channel/station
sql3_cursor.execute('create table IF NOT EXISTS mm_tv_stations (mm_tv_stations_id uuid'\
    ' CONSTRAINT mm_tv_stations_id_pk primary key, mm_tv_station_name text,'\
    ' mm_tv_station_id text, mm_tv_station_channel text, mm_tv_station_json jsonb,'\
    ' mm_tv_station_image text)')
if db_table_index_check('mm_tv_stations_idx_station') is None:
    sql3_cursor.execute('CREATE INDEX mm_tv_stations_idx_station'\
        ' ON mm_tv_stations(mm_tv_station_id)')
if db_table_index_check('mm_tv_stations_idx_name') is None:
    sql3_cursor.execute('CREATE INDEX mm_tv_stations_idx_name'\
        ' ON mm_tv_stations(mm_tv_station_name)')


# tv shedules
sql3_cursor.execute('create table IF NOT EXISTS mm_tv_schedule (mm_tv_schedule_id uuid'\
    ' CONSTRAINT mm_tv_schedule_id_pk primary key, mm_tv_schedule_station_id text,'\
    ' mm_tv_schedule_date date, mm_tv_schedule_json jsonb)')
if db_table_index_check('mm_tv_schedule_idx_date') is None:
    sql3_cursor.execute('CREATE INDEX mm_tv_schedule_idx_date'\
        ' ON mm_tv_schedule(mm_tv_schedule_date)')
if db_table_index_check('mm_tv_schedule_idx_station') is None:
    sql3_cursor.execute('CREATE INDEX mm_tv_schedule_idx_station'\
        ' ON mm_tv_schedule(mm_tv_schedule_station_id)')


# tv schedules programs
sql3_cursor.execute('create table IF NOT EXISTS mm_tv_schedule_program'\
    ' (mm_tv_schedule_program_guid uuid CONSTRAINT mm_tv_schedule_program_guid_pk primary key,'\
    ' mm_tv_schedule_program_id text, mm_tv_schedule_program_json jsonb)')
if db_table_index_check('mm_tv_schedule_idx_program') is None:
    sql3_cursor.execute('CREATE INDEX mm_tv_schedule_idx_program'\
        ' ON mm_tv_schedule_program(mm_tv_schedule_program_id)')


sql3_conn.commit()
sql3_conn.close()
