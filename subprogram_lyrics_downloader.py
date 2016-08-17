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
import logging
import sys
import os
import signal
sys.path.append("../common")
sys.path.append("../server")
from common import common_file
from common import common_chart_lyrics
import common_logging
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

# create the file for pid
pid_file = '../pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'Sub_Lyrics_Downloader', False, False, None)

def signal_receive(signum, frame):
    print('CHILD Lyrics: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_rollback()
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Lyrics_Download')


total_download_attempts = 0
# main code
def main(argv):
    global total_download_attempts
    # parse arguments
    sub_lang = "en"
    # search the directory for filter files
    for media_row in common_file.common_file_Dir_List():
        logging.debug(media_row)


if __name__ == "__main__":
    print('Total lyrics download attempts: %s', total_download_attempts)
    # send notications
    if total_download_attempts > 0:
        db.srv_db_Notification_Insert(locale.format('%d',\
            total_download_attempts, True) + " lyric(s) downloaded.", True)
    # commit all changes
    db.srv_db_commit()
    # close DB
    db.srv_db_close()
    # remove pid
    os.remove(pid_file)
