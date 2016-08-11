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
import requests
from backblazeb2 import BackBlazeB2


class common_backup_backblaze_api:
    """
    Class for interfacing with backblaze
    """
    def __init__(self, account_id, app_key):
        self.b2 = BackBlazeB2(account_id, app_key)


    def common_backup_backblaze_bucket_list(self):
        """
        Return list of buckets in Backblaze
        """
        return self.b2.list_buckets()


    def common_backup_backblaze_bucket_create(self, bucket_name):
        """
        Create specified bucket name
        """
        response = self.b2.create_bucket(bucket_name, bucket_type='allPrivate')
        logging.debug("b2 create: %s", response)


    def common_backup_backblaze_upload_file(self, file_name, bucket_name, file_password=None):
        """
        Upload file into specified bucket
        """
        if file_password is None:
            self.b2.upload_file(file_name, bucket_name=bucket_name)
        else:
            self.b2.upload_file(file_name, bucket_name=bucket_name, password=file_password)


    def common_backup_backblaze_upload_directory(self, dir_name, bucket_name, dir_password=None):
        """
        Upload entire directory into specified bucket
        """
        if dir_password is None:
            self.b2.recursive_upload(dir_name, bucket_name=bucket_name, multithread=True)
        else:
            self.b2.recursive_upload(dir_name, bucket_name=bucket_name,\
                    multithread=True, password=dir_password)


    def common_backup_backblaze_download_File(self, file_name, local_file_name, file_password):
        """
        Download specified file
        """
        if file_password is None:
            response = self.b2.download_file_by_name(file_name, local_file_name)
        else:
            response = self.b2.download_file_by_name(file_name, local_file_name,\
                    password=file_password)
        logging.debug("b2 down: %s", response)
