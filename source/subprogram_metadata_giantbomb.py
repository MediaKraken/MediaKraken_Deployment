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

from common import common_config_ini
from common import common_internationalization
from common import common_signal

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# set signal exit breaks
common_signal.com_signal_set_break()

total_download_attempts = 0


# main code
def main(argv):
    global total_download_attempts

    # search the directory for filter files


# TODO this should go thru the limiter
if __name__ == "__main__":
    print(('bomb game info download attempts: %s' % total_download_attempts))
    # send notifications
    if total_download_attempts > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(
                total_download_attempts)
            + " Giant Bomb game info downloaded.", True)
    # commit all changes
    db_connection.db_commit()
    # close DB
    db_connection.db_close()
