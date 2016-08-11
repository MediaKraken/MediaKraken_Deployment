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

import gzip
import logging
import time
import sys
import MK_Common_Database_Octmote
import MK_Common_File
import MK_Common_Network
sys.path.append("../../common/lib")
import adba


# http://www.thesportsdb.com/forum/viewtopic.php?f=6&t=5
class MK_Common_Metadata_AniDB_API:
    def __init__(self):
        pass


    def MK_Network_AniDB_Fetch_Titles_File(self, data_type='dat'):
        """
        Fetch the tarball of anime titles
        """
        if data_type == "dat":
            data_file = 'http://anidb.net/api/anime-titles.dat.gz'
        else:
            data_file = 'http://anidb.net/api/anime-titles.xml.gz'
        MK_Common_Network.MK_Network_Fetch_From_URL(data_file, './Temp_AniDB_Titles.gz')


    def MK_Network_AniDB_Save_Title_Data_To_DB(self, title_file):
        """
        Save anidb title data to database
        """
        file_handle = gzip.open(title_file, 'rb')
        file_content = file_handle.read()
        file_handle.close()
        # loop throw the lines
        sql_params_list = []
        for ani_line in file_content.split('\n'):
            if len(ani_line) > 6 and ani_line[0] != '#':
                # not a comment so try to split the file via pipes with a limit of three fields
                sql_fields = ani_line.split('|', 3)
                sql_params_list.append(sql_fields)
        MK_Common_Database_Octmote.MK_Database_Sqlite3_AniDB_Title_Insert(sql_params_list)


    def MK_Network_AniDB_AID_By_Title(self, title_to_search):
        """
        Find AID by title
        """
        # check the local DB
        local_db_result = MK_Common_Database_Octmote.MK_Database_Sqlite3_AniDB_Title_Search(title_to_search)
        if local_db_result is None:
            # check to see if local titles file is older than 24 hours
            if MK_Common_File.MK_Common_File_Modification_Timestamp(title_to_search) \
                    < (time.time() - (1 * 86400)):
                MK_Network_AniDB_Fetch_Titles_File('dat')
                # since new titles file....recheck by title
                MK_Network_AniDB_AID_By_Title(title_to_search)
            else:
                return None
        else:
            return local_db_result


    def MK_Network_AniDB_Connect(self, user_name, user_password):
        """
        Remote api calls
        """
        self.connection = adba.Connection(log=True)
        try:
            self.connection.auth(user_name, user_password)
            pass
        except Exception, e:
            logging.error("exception msg: " + str(e))
        return self.connection


    def MK_Network_AniDB_Logout(self):
        """
        Logout of AniDB
        """
        self.connection.logout()


    def MK_Network_AniDB_Stop(self):
        """
        Close the AniDB connect and stop the thread
        """
        self.connection.stop()


# expericment code
# works MK_Network_AniDB_Fetch_Titles_File('dat')

''' # works
MK_Common_Database_Octmote.MK_Database_Sqlite3_Open()
MK_Network_AniDB_Save_Title_Data_To_DB('./Temp_AniDB_Titles.gz')
MK_Common_Database_Octmote.MK_Database_Sqlite3_Close()
'''
