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
import json
import sys
import time

from . import common_file
from . import common_global
from . import common_network

sys.path.append(".")
import adba


class CommonMetadataANIdb:
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
        # check to see if local titles file is older than 24 hours
        if common_file.com_file_modification_timestamp('./cache/anidb_titles.gz') \
                < (time.time() - 86400):
            common_network.mk_network_fetch_from_url('http://anidb.net/api/anime-titles.xml.gz',
                                                     './cache/anidb_titles.gz')
            return True  # new file
        return False

    def com_net_anidb_save_title_data_to_db(self, title_file='./cache/anidb_titles.gz'):
        """
        Save anidb title data to database
        """
        common_global.es_inst.com_elastic_index('info', {'stuff': 'start'})
        file_handle = gzip.open(title_file, 'rb')
        # file_handle = gzip.open(title_file, 'rt', encoding='utf-8') # python 3.3+
        anime_aid = None
        anime_title = None
        anime_title_ja = None
        for file_line in file_handle.readlines():
            # common_global.es_inst.com_elastic_index('info',
            # {'stuff':'line: %s', file_line.decode('utf-8'))
            if file_line.decode('utf-8').find('<anime aid="') != -1:
                anime_aid = file_line.decode(
                    'utf-8').split('"', 1)[1].rsplit('"', 1)[0]
                # common_global.es_inst.com_elastic_index('info',
                # {'stuff':'aid: %s', anime_aid)
            elif file_line.decode('utf-8').find('title xml:lang="ja"') != -1:
                anime_title_ja = file_line.decode(
                    'utf-8').split('>', 1)[1].rsplit('<', 1)[0]
                # common_global.es_inst.com_elastic_index('info',
                # {'stuff':'title: %s', anime_title_ja)
            elif file_line.decode('utf-8').find('title xml:lang="en"') != -1:
                anime_title = file_line.decode(
                    'utf-8').split('>', 1)[1].rsplit('<', 1)[0]
                # common_global.es_inst.com_elastic_index('info',
                # {'stuff':'title: %s', anime_title)
            elif file_line.decode('utf-8').find('</anime>') != -1:
                if self.db_connection.db_meta_anime_meta_by_id(anime_aid) is None:
                    if anime_title is None:
                        anime_title = anime_title_ja
                    self.db_connection.db_meta_anime_title_insert(
                        json.dumps({'anidb': anime_aid}), anime_title,
                        None, None, None, None, None)
                # reset each time to handle ja when this doesn't exist
                anime_title = None
                # common_global.es_inst.com_elastic_index('info', {'stuff':'end insert')
        file_handle.close()
        common_global.es_inst.com_elastic_index('info', {'stuff': 'end'})

    def com_net_anidb_aid_by_title(self, title_to_search):
        """
        Find AID by title
        """
        # check the local DB
        local_db_result = self.db_connection.db_meta_anime_title_search(
            title_to_search)
        if local_db_result is None:
            # check to see if local titles file is older than 24 hours
            if self.com_net_anidb_fetch_titles_file():
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
        except Exception as err_code:
            common_global.es_inst.com_elastic_index('error', {"exception msg":
                                                                  err_code})
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
