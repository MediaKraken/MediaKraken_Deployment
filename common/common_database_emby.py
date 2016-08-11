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

import logging
import sqlite3
import json
import sys
import os
import MK_Common_Emby


class MK_Common_Database_Emby:
    def __init__(self):
        pass

    def MK_Database_Sqlite3_Attach_Emby(self, dir_path):
        """
        Attach rest of databases so I can query them
        """
        # user activity - start/stop, errors and info
        self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/activitylog.db' as 'activitylog'")
        # access tokens for devices
        #self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/authentication.db' as 'authentication'")
        #drwxrwxr-x.   2 MediaBrowserServer media      4096 Mar 29  2015 camerauploads
        # frame/time/path information for media chapters - no longer in BETA version
        #self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/chapters.db' as 'chapters'")
        #drwxrwxr-x. 134 MediaBrowserServer media     12288 Oct 26 03:47 collections
        #drwxrwxr-x    2 MediaBrowserServer media    249856 Nov  2 12:43 critic-reviews
        #drwxrwxr-x.  65 MediaBrowserServer media      4096 Nov  5 10:29 devices
        # eh?
        #self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/displaypreferences.db' as 'displaypreferences'")
        # blank db!
        #self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/fileorganization.db' as 'fileorganization'")
        # imagesizes.json
        # data about media, codecs, lang, channels, bitrate, path, etc - no longer in BETA version
        #self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/mediainfo.db' as 'mediainfo'")
        # notifications/spam etc from Emby team
        self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/notifications.db' as 'notifications'")
        #drwxrwxr-x.   2 MediaBrowserServer media      4096 Mar 29  2015 playlists
        # metadata status such as when it was refreshed last
        #self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/refreshinfo.db' as 'refreshinfo'")
        # remotenotifications.json
        #drwxrwxr-x.   2 MediaBrowserServer media      4096 May 28  2015 ScheduledTasks
        # blank db!
        #self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/shares.db' as 'shares'")
        # contains info on sync jobs
        self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/sync14.db' as 'sync14'")
        # user info for favs, played, etc
        self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/userdata_v2.db' as 'userdata_v2'")
        # list of users along with json info
        self.sql3_emby_cursor.execute("ATTACH DATABASE '" + dir_path + "/users.db' as 'users'")


    def MK_Database_Sqlite3_Open_Emby(self, db_file_name = None, db_username_dir = os.environ.get("USERNAME"), attach_other_db = False):
        """
        Open database and pull in config from sqlite and create db if not exist
        """
        # if not specified....then try to find the default
        if db_file_name is None:
            # windows
            db_file_name = os.join(MK_Common_Emby.MK_Common_Emby_Installed_Directory, '/data/library.db')
        # verify it found a file
        if db_file_name is None:
            logging.critical("Cannot find database file.  Exiting.")
            sys.exit()
        try:
            self.sql3_emby_conn = sqlite3.connect(db_file_name)
            self.sql3_emby_cursor = self.sql3_emby_conn.cursor()
            self.sql3_emby_conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
            if attach_other_db:
                MK_Database_Sqlite3_Attach_Emby(db_file_name.replace('/library.db', ''))
        except:
            logging.critical("Unable to open db file(s): %s", db_file_name)
            sys.exit()


    def MK_Database_Sqlite3_Close_Emby(self):
        """
        Close connection to emby database
        """
        self.sql3_emby_conn.close()


    def MK_Database_Sqlite3_Movie_List_Emby(self, offset = None, records = None):
        """
        Grab all movies in emby database
        """
        if offset is None:
            self.sql3_emby_cursor.execute('select * from TypedBaseItems where type = "MediaBrowser.Controller.Entities.Movies.Movie"')
        else:
            self.sql3_emby_cursor.execute('select * from TypedBaseItems where type = "MediaBrowser.Controller.Entities.Movies.Movie" limit ? offset ?', (records, offset))
        return self.sql3_emby_cursor.fetchall()


    def MK_Database_Sqlite3_Movie_List_Emby_Count(self):
        """
        Grab all movies in emby database count
        """
        self.sql3_emby_cursor.execute('select count(*) from TypedBaseItems where type = "MediaBrowser.Controller.Entities.Movies.Movie"')
        return self.sql3_emby_cursor.fetchone()[0]


    def MK_Database_Sqlite3_TV_List_Emby(self, offset = None, records = None):
        """
        Grab all the tv episodes in the emby database
        """
        if offset is None:
            self.sql3_emby_cursor.execute('select * from TypedBaseItems where type = "MediaBrowser.Controller.Entities.TV.Episode"')
        else:
            self.sql3_emby_cursor.execute('select * from TypedBaseItems where type = "MediaBrowser.Controller.Entities.TV.Episode" limit ? offset ?', (records, offset))
        return self.sql3_emby_cursor.fetchall()


    def MK_Database_Sqlite3_TV_List_Emby_Count(self):
        """
        Grab all the tv episodes in the emby database count
        """
        self.sql3_emby_cursor.execute('select count(*) from TypedBaseItems where type = "MediaBrowser.Controller.Entities.TV.Episode"')
        return self.sql3_emby_cursor.fetchone()[0]


    def MK_Database_Sqlite3_TV_Movie_List_Emby(self, offset = None, records = None):
        """
        Grab all the tv episodes and movies in the emby database
        """
        if offset is None:
            self.sql3_emby_cursor.execute('select * from TypedBaseItems where type IN ("MediaBrowser.Controller.Entities.TV.Episode" "MediaBrowser.Controller.Entities.Movies.Movie")')
        else:
            self.sql3_emby_cursor.execute('select * from TypedBaseItems where type IN ("MediaBrowser.Controller.Entities.TV.Episode" "MediaBrowser.Controller.Entities.Movies.Movie") limit ? offset ?', (records, offset))
        return self.sql3_emby_cursor.fetchall()


    def MK_Database_Sqlite3_TV_Movie_List_Emby_Count(self):
        """
        Grab all the tv episodes and movies in the emby database count
        """
        self.sql3_emby_cursor.execute('select count(*) from TypedBaseItems where type IN ("MediaBrowser.Controller.Entities.TV.Episode" "MediaBrowser.Controller.Entities.Movies.Movie")')
        return self.sql3_emby_cursor.fetchone()[0]


    def MK_Database_Sqlite3_Users_List(self, offset = None, records = None, play_stats = None):
        """
        Grab all users from database
        """
        if play_stats is None:
            if offset is None:
                self.sql3_emby_cursor.execute('select users.users.guid, users.users.data from users.users')
            else:
                self.sql3_emby_cursor.execute('select users.users.guid, users.users.data from users.users limit ? offset ?', (records, offset))
        else:
            if offset is None:
                self.sql3_emby_cursor.execute('select users.users.guid, users.users.data, sum(userdata_v2.userdata.playCount), max(userdata_v2.userdata.lastPlayedDate) from users.users join userdata_v2.userdata on users.users.guid = userdata_v2.userdata.userId union select users.users.guid, users.users.data, 0, NULL from users.users left join userdata_v2.userdata on users.users.guid = userdata_v2.userdata.userId where userdata_v2.userdata.userId IS NULL')
            else:
                self.sql3_emby_cursor.execute('select users.users.guid, users.users.data, sum(userdata_v2.userdata.playCount), max(userdata_v2.userdata.lastPlayedDate) from users.users join userdata_v2.userdata on users.users.guid = userdata_v2.userdata.userId union select users.users.guid, users.users.data, 0, NULL from users.users left join userdata_v2.userdata on users.users.guid = userdata_v2.userdata.userId where userdata_v2.userdata.userId IS NULL limit ? offset ?', (records, offset))
        return self.sql3_emby_cursor.fetchall()


    def MK_Database_Sqlite3_Users_List_Count(self):
        """
        Grab count of all users
        """
        self.sql3_emby_cursor.execute('select count(*) from users.users')
        return self.sql3_emby_cursor.fetchone()[0]


    def MK_Database_Sqlite3_User_Last_IP(self, user_id):
        """
        Grab last IP
        """
        self.sql3_emby_cursor.execute('select ShortOverview from ActivityLogEntries where UserId = ? and ShortOverview LIKE \'Ip address%\' order by DateCreated desc limit 1', (user_id,))
        row_data = self.sql3_emby_cursor.fetchone() # don't auto [0] since could be None
        if row_data is None:
            return 'NA'
        else:
            return row_data[0].split(':')[1].strip()


    def MK_Database_Sqlite3_Media_In_Dir(self, dir_name):
        """
        Get all the media files that match directory
        """
        # query by video will grab "home videos" type
        self.sql3_emby_cursor.execute('select * from TypedBaseItems where type = "MediaBrowser.Controller.Entities.Video"')
        file_in_path = []
        for media_row in self.sql3_emby_cursor:
            json_data = json.loads(str(media_row[2]))
            # begins with the dir_name specified in parameter
            try:
                if json_data["Path"].find(dir_name) == 0:
                    file_in_path.append(media_row)
            except:
                pass
        return file_in_path


    def MK_Database_Sqlite3_Emby_Activity_List(self, offset = None, records = None):
        """
        Grab all activity data
        """
        if offset is None:
            self.sql3_emby_cursor.execute('select * from ActivityLogEntries')
        else:
            self.sql3_emby_cursor.execute('select * from ActivityLogEntries limit ? offset ?',\
                    (records, offset))
        return self.sql3_emby_cursor.fetchall()


    def MK_Database_Sqlite3_Emby_Activity_List_Count(self):
        """
        Grab all activity data count
        """
        self.sql3_emby_cursor.execute('select count(*) from ActivityLogEntries')
        return self.sql3_emby_cursor.fetchone()[0]


    def MK_Databas_Sqlite3_Emby_Notification_List(self, offset = None, records = None):
        """
        Grab all notifications
        """
        if offset is None:
            self.sql3_emby_cursor.execute('select * from Notifications')
        else:
            self.sql3_emby_cursor.execute('select * from Notifications limit ? offset ?',\
                    (records, offset))
        return self.sql3_emby_cursor.fetchall()


    def MK_Database_Sqlite3_Emby_Notification_List_Count(self):
        """
        Grab notification  data count
        """
        self.sql3_emby_cursor.execute('select count(*) from Notifications')
        return self.sql3_emby_cursor.fetchone()[0]


    def MK_Database_Sqlite3_Emby_Sync_List(self, offset = None, records = None):
        """
        Grab all notifications
        """
        if offset is None:
            self.sql3_emby_cursor.execute('select * from SyncJobs')
        else:
            self.sql3_emby_cursor.execute('select * from SyncJobs limit ? offset ?',\
                    (records, offset))
        return self.sql3_emby_cursor.fetchall()


    def MK_Database_Sqlite3_Emby_Sync_List_Count(self):
        """
        Grab notification  data count
        """
        self.sql3_emby_cursor.execute('select count(*) from SyncJobs')
        return self.sql3_emby_cursor.fetchone()[0]


    def MK_Database_Sqlite3_Media_By_Guid(self, guid):
        """
        Get id to lookup from metadata
        """
        self.sql3_emby_cursor.execute('select * from TypedBaseItems where guid = ?', (guid,))
        try:
            return self.sql3_cursor.fetchone()[0]
        except:
            return None


    def MK_Database_Sqlite3_User_Play_Data(self):
        """
        All data from users for playback
        """
        self.sql3_emby_cursor.execute('select * from userdata')
        return self.sql3_emby_cursor.fetchall()
