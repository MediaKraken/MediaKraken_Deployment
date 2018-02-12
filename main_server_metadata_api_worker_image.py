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
import time
from common import common_config_ini
from common import common_logging
from common import common_network
from common import common_signal

# set signal exit breaks
common_signal.com_signal_set_break()


def main():
    # open the database
    option_config_json, thread_db = common_config_ini.com_config_read()
    while True:
        for row_data in thread_db.db_download_image_read():
            common_network.mk_network_fetch_from_url(row_data['mdq_image_download_json']['url'],
                                                     row_data['mdq_image_download_json']['local'])
            thread_db.db_download_image_delete(row_data['mdq_image_id'])
            # thread_db.db_commit() - commit done in delete function above
        time.sleep(1)
    #        break # TODO for now testing.......
    thread_db.db_close()


if __name__ == "__main__":
    # start logging
    common_logging.com_logging_start('./log/MediaKraken_Metadata_API_Worker_Images')
    main()
