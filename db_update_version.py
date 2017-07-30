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
import subprocess
import psycopg2
from common import common_config_ini


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# not really needed if common_version.DB_VERSION == 4:

if db_connection.db_version_check() == 1:
    # add download image que
    proc = subprocess.Popen(['python', './db_create_update.py'], shell=False)
    proc.wait()
    db_connection.db_version_update(2)
    db_connection.db_commit()

if db_connection.db_version_check() == 2:
    # add image for periodical
    db_connection.db_query('ALTER TABLE mm_metadata_book ADD COLUMN mm_metadata_book_image_json jsonb')
    db_connection.db_version_update(3)
    db_connection.db_commit()

if db_connection.db_version_check() == 3:
    # add docker info to options
    option_config_json.update({'Docker': {'Nodes': 0, 'SwarmID': None, 'Instances': 0}})
    db_connection.db_opt_update(option_config_json)
    db_connection.db_version_update(4)
    db_connection.db_commit()

if db_connection.db_version_check() == 4:
    # add cron job
    db_connection.db_cron_insert('Trailer', 'Download new trailers', False, 'Days 1',
        psycopg2.Timestamp(1970, 1, 1, 0, 0, 1), './subprogram_metadata_trailer_download.py')
    db_connection.db_version_update(5)
    db_connection.db_commit()

if db_connection.db_version_check() == 5:
    # drop tvtuners and nas tables
    db_connection.db_drop_table('mm_nas')
    db_connection.db_drop_table('mm_tuner')
    db_connection.db_version_update(6)
    db_connection.db_commit()

if db_connection.db_version_check() == 6:
    # create indexes for pg_trgm
    # su -u postgres psql -d metamandb -c "create extension pg_trgm;"
    db_connection.db_query('CREATE INDEX mm_metadata_tvshow_name_trigram_idx ON mm_metadata_tvshow USING gist(mm_metadata_tvshow_name gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mm_metadata_sports_name_trigram_idx ON mm_metadata_sports USING gist(mm_metadata_sports_name gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mm_metadata_musician_name_trigram_idx ON mm_metadata_musician USING gist(mm_metadata_musician_name gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mm_metadata_album_name_trigram_idx ON mm_metadata_album USING gist(mm_metadata_album_name gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mm_metadata_music_name_trigram_idx ON mm_metadata_music USING gist(mm_metadata_music_name gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mm_media_anime_name_trigram_idx ON mm_metadata_anime USING gist(mm_media_anime_name gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mm_media_name_trigram_idx ON mm_metadata_movie USING gist(mm_media_name gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mm_media_music_video_band_trigram_idx ON mm_metadata_music_video USING gist(mm_media_music_video_band gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mm_media_music_video_song_trigram_idx ON mm_metadata_music_video USING gist(mm_media_music_video_song gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mm_metadata_book_name_trigram_idx ON mm_metadata_book USING gist(mm_metadata_book_name gist_trgm_ops);')
    # since it's json, gist trgm_ops won't work
    #db_connection.db_query('CREATE INDEX mm_metadata_collection_name_trigram_idx ON mm_metadata_collection USING gist(mm_metadata_collection_name gist_trgm_ops);')
    db_connection.db_query('CREATE INDEX mmp_person_name_trigram_idx ON mm_metadata_person USING gist(mmp_person_name gist_trgm_ops);')
    db_connection.db_version_update(7)
    db_connection.db_commit()

# drop trigger table since moving to celery?

# close the database
db_connection.db_close()
