"""
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
"""

import gzip
import inspect
import json
import time

from common import common_file
from common import common_logging_elasticsearch_httpx
from common import common_network_async


class CommonMetadataANIdb:
    """
    Class for interfacing with anidb
    """

    def __init__(self, db_connection):
        self.adba_connection = None
        self.db_connection = db_connection

    async def com_net_anidb_fetch_titles_file(self):
        """
        Fetch the tarball of anime titles
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        # check to see if local titles file is older than 24 hours
        if common_file.com_file_modification_timestamp('./cache/anidb_titles.gz') \
                < (time.time() - 86400):
            await common_network_async.mk_network_fetch_from_url_async(
                'http://anidb.net/api/anime-titles.xml.gz',
                './cache/anidb_titles.gz')
            return True  # new file
        return False

    async def com_net_anidb_save_title_data_to_db(self, title_file='./cache/anidb_titles.gz'):
        """
        Save anidb title data to database
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        file_handle = gzip.open(title_file, 'rb')
        # file_handle = gzip.open(title_file, 'rt', encoding='utf-8') # python 3.3+
        anime_aid = None
        anime_title = None
        anime_title_ja = None
        for file_line in file_handle.readlines():
            # common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
            # {'stuff':'line: %s', file_line.decode('utf-8'))
            if file_line.decode('utf-8').find('<anime aid="') != -1:
                anime_aid = file_line.decode(
                    'utf-8').split('"', 1)[1].rsplit('"', 1)[0]
                # common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
                # {'stuff':'aid: %s', anime_aid)
            elif file_line.decode('utf-8').find('title xml:lang="ja"') != -1:
                anime_title_ja = file_line.decode(
                    'utf-8').split('>', 1)[1].rsplit('<', 1)[0]
                # common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
                # {'stuff':'title: %s', anime_title_ja)
            elif file_line.decode('utf-8').find('title xml:lang="en"') != -1:
                anime_title = file_line.decode(
                    'utf-8').split('>', 1)[1].rsplit('<', 1)[0]
                # common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
                # {'stuff':'title: %s', anime_title)
            elif file_line.decode('utf-8').find('</anime>') != -1:
                if self.db_connection.db_meta_anime_meta_by_id(anime_aid) is None:
                    if anime_title is None:
                        anime_title = anime_title_ja
                    self.db_connection.db_meta_anime_title_insert(
                        {'anidb': anime_aid}, anime_title,
                        None, None, None, None, None)
                # reset each time to handle ja when this doesn't exist
                anime_title = None
        file_handle.close()
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'stuff': 'end'})

    async def com_net_anidb_aid_by_title(self, title_to_search):
        """
        Find AID by title
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
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

    async def com_net_anidb_connect(self, user_name, user_password):
        """
        Remote api calls
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        self.adba_connection = adba.Connection(log=True)
        try:
            self.adba_connection.auth(user_name, user_password)
        except Exception as err_code:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='error',
                                                                 message_text={"exception msg":
                                                                                   err_code})
        return self.adba_connection

    async def com_net_anidb_logout(self):
        """
        Logout of anidb
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        self.adba_connection.logout()

    async def com_net_anidb_stop(self):
        """
        Close the anidb connect and stop the thread
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        self.adba_connection.stop()
