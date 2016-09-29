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
import logging # pylint: disable=W0611
import gzip
import time
import sys
from . import common_database_octmote
from . import common_file
from . import common_network
sys.path.append("./vault/lib")
import adba


# http://www.thesportsdb.com/forum/viewtopic.php?f=6&t=5
class CommonMetadataANIdb(object):
    """
    Class for interfacing with anidb
    """
    def __init__(self):
        self.adba_connection = None


    def com_net_anidb_fetch_titles_file(self, data_type='dat'):
        """
        Fetch the tarball of anime titles
        """
        if data_type == "dat":
            data_file = 'http://anidb.net/api/anime-titles.dat.gz'
        else:
            data_file = 'http://anidb.net/api/anime-titles.xml.gz'
        common_network.mk_network_fetch_from_url(data_file, './Temp_anidb_Titles.gz')


    def com_net_anidb_save_title_data_to_db(self, title_file):
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
        common_database_octmote.com_db_anidb_title_insert(sql_params_list)


    def com_net_anidb_aid_by_title(self, title_to_search):
        """
        Find AID by title
        """
        # check the local DB
        local_db_result = common_database_octmote.com_db_anidb_title_search(title_to_search)
        if local_db_result is None:
            # check to see if local titles file is older than 24 hours
            if common_file.com_file_modification_timestamp(title_to_search) \
                    < (time.time() - (1 * 86400)):
                self.com_net_anidb_fetch_titles_file('dat')
                # since new titles file....recheck by title
                self.com_net_anidb_aid_by_title(title_to_search)
            else:
                return None
        else:
            return local_db_result


    def com_net_anidb_connect(self, user_name, user_password):
        """
        Remote api calls
        """
        self.adba_connection = adba.Connection(log=True)
        try:
            self.adba_connection.auth(user_name, user_password)
        except Exception, err_code:
            logging.error("exception msg: " + str(err_code))
        return self.adba_connection


    def com_net_anidb_logout(self):
        """
        Logout of anidb
        """
        self.adba_connection.logout()


    def com_net_anidb_stop(self):
        """
        Close the anidb connect and stop the thread
        """
        self.adba_connection.stop()


# expericment code
# works com_net_anidb_Fetch_Titles_File('dat')

''' # works
common_database_octmote.com_db_Open()
com_net_anidb_connect
com_net_anidb_save_title_data_to_db('./Temp_anidb_Titles.gz')
com_net_anidb_logout
common_database_octmote.com_db_Close()
com_net_anidb_stop
'''
