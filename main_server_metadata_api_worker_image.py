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
import time
import sys
from common import common_config_ini
from common import common_logging
from common import common_metadata_tvmaze
from common import common_network
from common import common_signal


# set signal exit breaks
common_signal.com_signal_set_break()


def main():
    # open the database
    option_config_json, thread_db = common_config_ini.com_config_read()
    # table the class_text into a dict...will lessen the db calls
    while True:
        for row_data in thread_db.db_download_read_provider(content_providers):
            logging.info("worker meta api row: %s", row_data)
            # mdq_id,mdq_download_json
            if content_providers == 'anidb':
                anidb(thread_db, row_data)
            elif content_providers == 'chart_lyrics':
                chart_lyrics(thread_db, row_data)
            elif content_providers == 'comicvine':
                comicvine(thread_db, row_data)
            elif content_providers == 'tvshowtime':
                tvshowtime(thread_db, row_data)
            elif content_providers == 'Z':
                logging.info('worker Z meta api: class: %s rowid: %s json: %s',\
                    class_text_dict[row_data['mdq_download_json']['ClassID']],\
                    row_data['mdq_id'], row_data['mdq_download_json'])
                metadata_uuid = None
                # check for dupes by name/year
                file_name = guessit(row_data['mdq_download_json']['Path'])
                logging.info('worker Z filename: %s', file_name)
        thread_db.db_commit()
        time.sleep(1)
#        break # TODO for now testing.......
    thread_db.db_close()


if __name__ == "__main__":
    # start logging
    common_logging.com_logging_start('./log/MediaKraken_Metadata_API_Worker_Images')
    main()
