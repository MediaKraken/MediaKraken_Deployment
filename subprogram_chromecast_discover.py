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
import logging
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import sys
sys.path.append("../MediaKraken_Common")
sys.path.append("../MediaKraken_Server")
import MK_Common_Chromecast
import MK_Common_File
import MK_Common_Logging
import MK_Common_String
import os
import json
import signal
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')
#lock = threading.Lock()


# create the file for pid
pid_file = './pid/' + str(os.getpid())
MK_Common_File.MK_Common_File_Save_Data(pid_file, 'Chromecast_Scan', False, False, None)


def signal_receive(signum, frame):
    global global_end_program
    global_end_program = True
    print 'CHILD Tuner Scan: Received USR1'
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_Chromecast_Discovery')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server Chromecast Scan Start', None, u'System: Server Chromecast Scan Start', u'ServerChromecastScanStart', None, None, u'System')


# grab some dirs to scan and thread out the scans
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


devices_added = 0


# look for devices
chrome = MK_Common_Chromecast.MK_Common_Chromecast_API()
logging.debug("Chrome: %s", chrome)
for row_data in chrome.MK_Chromecast_Discover_Dict():
    logging.debug("Dict: %s", row_data)
    chrome.MK_Chromecast_Connect_By_Name(row_data)
    logging.debug("Connected!")
    cast_json = chrome.MK_Chromecast_Info()
    logging.debug("Cast: %s", cast_json)
    print "status:", chrome.MK_Chromecast_Status()
    db.MK_Server_Database_Device_Insert('cast', json.dumps({cast_json}))


if devices_added > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', devices_added, True) + " Chromecast added.", True)


# log end
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server Chromecast Scan Stop', None, u'System: Server Chromecast Scan Stop', u'ServerChromecastScanStop', None, None, u'System')

# commit
db.MK_Server_Database_Commit()

# close the database
db.MK_Server_Database_Close()

# remove pid
os.remove(pid_file)
