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

# import modules
from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import sys
import os
import signal
from common import common_config_ini
from common import common_file
from common import common_logging
from common import common_metadata
from common import common_network
from common import common_metadata_thelogodb


# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'Logo_Downloader', False, False, None)

def signal_receive(signum, frame):
    print('CHILD Logo: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db_connection.db_rollback()
    db_connection.db_close()
    sys.stdout.flush()
    sys.exit(0)

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Logo_Download')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read(True)


logo_connection = com_thelogodb.com_thelogodb_API()
total_download_attempts = 0
# main code
def main(argv):
    for channel_info in logo_connection.com_thelogodb_Fetch_Latest()['channels']:
        # fetch and store logo image
        image_file_path = com_metadata.com_meta_image_file_path(channel_info['strChannel'], 'logo')
        loggin.debug("image: %s", image_file_path)
        common_network.mk_network_fetch_from_url(channel_info['strLogoWide'], image_file_path)

# {"idChannel":"6613","strChannel":"Absolute 80s","strPackageIDs":",190,",
#"strLyngsat":null,"strCountry":"United Kingdom","strLyngsatLogo":null,
#"strLogoWide":"http:\/\/www.thelogodb.com\/images\/media\/logo\/rstxry1453314955.png","strLogoWideBW":null,"strLogoSquare":null,"strLogoSquareBW":null,"strFanart1":null,"strDescription":null,"dateModified":"2016-01-20 18:35:55"}

        total_download_attempts += 1


if __name__ == "__main__":
    print('Total logo download attempts: %s', total_download_attempts)
    # send notications
#    if total_download_attempts > 0:
#        db_connection.db_notification_insert(locale.format('%d', total_download_attempts, True) + " logo image(s) downloaded.", True)
#    # commit all changes
#    db_connection.db_commit()
#    # close DB
#    db_connection.db_close()
#    # remove pid
#    os.remove(pid_file)
