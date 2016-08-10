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
import sys
import logging
import os
import signal
sys.path.append("../MediaKraken_Common")
sys.path.append("./")  # for db import
import MK_Common_File
import MK_Common_Logging
import MK_Common_Metadata
import MK_Common_Network
import MK_Common_TheLogoDB
import database as database_base


# create the file for pid
pid_file = '../pid/' + str(os.getpid())
MK_Common_File.MK_Common_File_Save_Data(pid_file, 'Logo_Downloader', False, False, None)

def signal_receive(signum, frame):
    print 'CHILD Logo: Received USR1'
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_Logo_Download')       


logo_connection = MK_Common_TheLogoDB.MK_Common_TheLogoDB_API()
total_download_attempts = 0
# main code
def main(argv):
    for channel_info in logo_connection.MK_Common_TheLogoDB_Fetch_Latest()['channels']:
        # fetch and store logo image
        image_file_path = MK_Common_Metadata.MK_Common_Metadata_Image_File_Path(channel_info['strChannel'], 'logo')
        loggin.debug("image: %s", image_file_path)
        MK_Common_Network.MK_Network_Fetch_From_URL(channel_info['strLogoWide'], image_file_path)

# {"idChannel":"6613","strChannel":"Absolute 80s","strPackageIDs":",190,","strLyngsat":null,"strCountry":"United Kingdom","strLyngsatLogo":null,"strLogoWide":"http:\/\/www.thelogodb.com\/images\/media\/logo\/rstxry1453314955.png","strLogoWideBW":null,"strLogoSquare":null,"strLogoSquareBW":null,"strFanart1":null,"strDescription":null,"dateModified":"2016-01-20 18:35:55"}

        total_download_attempts += 1


if __name__ == "__main__":
    print 'Total logo download attempts:', total_download_attempts
    # send notications
#    if total_download_attempts > 0:
#        db.MK_Server_Database_Notification_Insert(locale.format('%d', total_download_attempts, True) + " logo image(s) downloaded.", True)
#    # commit all changes
#    db.MK_Server_Database_Commit()
#    # close DB
#    db.MK_Server_Database_Close()
#    # remove pid
#    os.remove(pid_file)
