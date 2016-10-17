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


# nuke previous pyinstaller directories to start fresh
try:
    shutil.rmtree('C:\\Users\\jenkinsbuild\\Documents\\github\\build')
except:
    pass
try:
    shutil.rmtree('C:\\Users\\jenkinsbuild\\Documents\\github\\dist')
except:
    pass


# start building python "app"
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\main_server.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\main_server_api.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\main_server_link.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\main_server_metadata_api.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\main_server_slave.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\main_server_trigger.py')

# start building the subprograms
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_broadcast.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_chromecast_discover.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_commercial_strip.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_create_chapter_images.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_cron_checker.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_file_scan.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_game_audit.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_game_metadata_giantbomb.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_game_metadata_igdb.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_iradio_channels.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_livestream_downloader.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_logo_download.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_lyrics_downloader.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_match_anime_id_scudlee.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_metadata_musicbrainz_sync.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_postgresql_backup.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_postgresql_vacuum.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_reactor_string_weblog.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_reactor_string.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_reactor_web_images.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_roku_thumbnail_generate.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_schedules_direct_updates.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_ssl_keygen.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_metadata_subtitle_downloader.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_sync.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_metadata_thetvdb_images.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_metadata_thetvdb_updates.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_tuner_discover.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_metadata_tvmaze_images.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_metadata_tvmaze_updates.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_metadata_update_create_collections.py')
os.system('pyinstaller --clean'\
    ' C:\\Users\\jenkinsbuild\\Documents\\github\\subprogram_zfs_check.py')
