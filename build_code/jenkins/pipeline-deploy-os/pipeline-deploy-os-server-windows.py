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
import os
import shutil


# create dir to throw data into
DIST_LOCAL = 'C:\\Users\\jenkinsbuild\\Documents\\github\\dist\\'
INNO_LOCAL = 'C:\\Users\\jenkinsbuild\\Documents\\github\\inno\\'
try:
    os.makedirs('C:\\Users\\jenkinsbuild\\Documents\\github\\inno')
except:
    pass

# setup inno directory
os.system('robocopy ' + DIST_LOCAL + 'main_server ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'main_server_api ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'main_server_link ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'main_server_metadata_api ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'main_server_trigger ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_broadcast ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_chromecast_discover ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_commercial_strip ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_create_chapter_images ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_cron_checker ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_ffmpeg_process ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_file_scan ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_game_audit ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_game_metadata_giantbomb ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_game_metadata_igdb ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_iradio_channels ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_livestream_downloader ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_logo_download ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_lyrics_downloader ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_match_anime_id_scudlee ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_musicbrainz_sync ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_postgresql_backup ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_postgresql_vacuum ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_reactor_string_weblog ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_reactor_string ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_reactor_web_images ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_roku_thumbnail_generate ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_schedules_direct_updates ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_ssl_keygen ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_subtitle_downloader ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_sync ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_thetvdb_images ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_thetvdb_updates ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_tuner_discover ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_tvmaze_images ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_tvmaze_updates ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_update_create_collections ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_url_checker ' + INNO_LOCAL + ' /E')
os.system('robocopy ' + DIST_LOCAL + 'subprogram_zfs_check ' + INNO_LOCAL + ' /E')
