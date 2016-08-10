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

import requests
import logging
from backblazeb2 import BackBlazeB2


class MK_Common_Backup_Backblaze_API:
    def __init__(self, account_id, app_key):
        self.b2 = BackBlazeB2(account_id, app_key)


    def MK_Common_Backup_Backblaze_Bucket_List(self):
        return self.b2.list_buckets()


    def MK_Common_Backup_Backblaze_Bucket_Create(self, bucket_name):
        response = self.b2.create_bucket(bucket_name, bucket_type='allPrivate')
        logging.debug("b2 create: %s", response)


    def MK_Common_Backup_Backblaze_Upload_File(self, file_name, bucket_name, file_password=None):
        if file_password is None:
            self.b2.upload_file(file_name, bucket_name=bucket_name)
        else:
            self.b2.upload_file(file_name, bucket_name=bucket_name, password=file_password)


    def MK_Common_Backup_Backblaze_Upload_Directory(self, dir_name, bucket_name, dir_password=None):
        if dir_password is None:
            self.b2.recursive_upload(dir_name, bucket_name=bucket_name, multithread=True)
        else:
            self.b2.recursive_upload(dir_name, bucket_name=bucket_name, multithread=True, password=dir_password)


    def MK_Common_Backup_Backblaze_Download_File(self, file_name, local_file_name, file_password):
        if file_password is None:
            response = self.b2.download_file_by_name(file_name, local_file_name)
        else:
            response = self.b2.download_file_by_name(file_name, local_file_name, password=file_password)
        logging.debug("b2 down: %s", response)
