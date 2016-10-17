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


PIPELINE_APP_LIST = [
    'bulk_gamesdb_netfetch',
    'main_octmote',
    'main_server_api',
    'main_server_link',
    'main_server_metadata_api',
    'main_server_slave',
    'main_server_trigger',
    'main_server_weblog',
    'main_server',
    'main_theater',
    'subprogram_broadcast',
    'subprogram_commercial_strip',
    'subprogram_create_chapter_images',
    'subprogram_cron_checker',
    'subprogram_file_scan',
    'subprogram_game_audit',
    'subprogram_hardware_chromecast_discover',
    'subprogram_hardware_tuner_discover',
    'subprogram_iradio_channels',
    'subprogram_match_anime_id_scudlee',
    'subprogram_metadata_anidb_updates',
    'subprogram_metadata_giantbomb',
    'subprogram_metadata_igdb',
    'subprogram_metadata_logo_download',
    'subprogram_metadata_lyrics_downloader',
    'subprogram_metadata_musicbrainz_sync',
    'subprogram_metadata_subtitle_downloader',
    'subprogram_metadata_thetvdb_images',
    'subprogram_metadata_thetvdb_updates',
    'subprogram_metadata_tmdb_updates',
    'subprogram_metadata_tvmaze_images',
    'subprogram_metadata_tvmaze_updates',
    'subprogram_metadata_update_create_collections',
    'subprogram_postgresql_backup',
    'subprogram_postgresql_vacuum',
    'subprogram_reactor_string_weblog',
    'subprogram_reactor_string',
    'subprogram_reactor_web_images',
    'subprogram_roku_thumbnail_generate',
    'subprogram_schedules_direct_updates',
    'subprogram_ssl_keygen',
    'subprogram_streamlink',
    'subprogram_sync',
    'subprogram_watchdog',
    'subprogram_zfs_check',
    ]
