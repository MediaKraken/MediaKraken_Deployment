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
import json
import xmltodict
from . import common_file
from . import common_network
sys.path.append("./vault/lib")
import adba


class CommonMetadataANIdb(object):
    """
    Class for interfacing with anidb
    """
    def __init__(self, db_connection):
        self.adba_connection = None
        self.db_connection = db_connection


    def com_net_anidb_fetch_titles_file(self):
        """
        Fetch the tarball of anime titles
        """
        common_network.mk_network_fetch_from_url('http://anidb.net/api/anime-titles.xml.gz',\
            './cache/anidb_titles.gz')


    def com_net_anidb_save_title_data_to_db(self, title_file='./cache/anidb_titles.gz'):
        """
        Save anidb title data to database
        """
        file_handle = gzip.open(title_file, 'rb')
        file_content = file_handle.read()
        file_handle.close()
        # loop through titles
        for anime_title in xmltodict.parse(file_content)['animetitles']:
            logging.debug('ani title: %s', anime_title)
            self.db_connection.db_meta_anime_title_insert(\
                json.dumps({'anidb': anime_title['anime aid']}),\
                anime_title['title type="official" xml:lang="en"'],\
                json.dumps(anime_title), None, None)


    def com_net_anidb_aid_by_title(self, title_to_search):
        """
        Find AID by title
        """
        # check the local DB
        local_db_result = self.db_connection.db_meta_anime_title_search(title_to_search)
        if local_db_result is None:
            # check to see if local titles file is older than 24 hours
            if common_file.com_file_modification_timestamp(title_to_search) \
                    < (time.time() - 86400):
                self.com_net_anidb_fetch_titles_file()
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
            logging.error("exception msg: %s", err_code)
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
