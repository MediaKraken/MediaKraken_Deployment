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
import logging
import boto
from boto.s3.key import Key


class CommonAWSS3(object):
    """
    Class for interfacing with aws s3
    """
    def __init__(self):
        import os
        # set active false so if following falls
        self.active = False
        # pull in the ini file config
        import ConfigParser
        Config = ConfigParser.ConfigParser()
        if os.path.isfile("MediaKraken.ini"):
            Config.read("MediaKraken.ini")
        else:
            Config.read("../MediaKraken.ini")
        if Config.get('AWSS3', 'AccessKey').strip() != 'None':
            # Amazon S3 settings.
            self.AWS_ACCESS_KEY_ID = Config.get('AWSS3', 'AccessKey').strip()
            self.AWS_SECRET_ACCESS_KEY = Config.get('AWSS3', 'SecretAccessKey').strip()
            self.AWS_BUCKET_NAME = Config.get('AWSS3', 'Bucket').strip()
            self.AWS_BUCKET_BACKUP_NAME = Config.get('AWSS3', 'BackupBucket').strip()
            # setup connection and buckets for later use
            conn = boto.connect_s3(self.AWS_ACCESS_KEY_ID, self.AWS_SECRET_ACCESS_KEY)
            self.bucket = conn.get_bucket(self.AWS_BUCKET_NAME)
            self.bucket_backup = conn.get_bucket(self.AWS_BUCKET_BACKUP_NAME)
            self.active = True


    def com_aws_s3_upload(self, source_path, destination_filename, backup_bucket = False):
        """
        Upload file to S3
        """
        if not backup_bucket:
            k = Key(self.bucket)
        else:
            k = Key(self.bucket_backup)
        k.key = destination_filename
        k.set_contents_from_filename(source_path)


    def com_aws_s3_download(self, source_key, destination_filename, backup_bucket = False):
        """
        Download from s3
        """
        if not backup_bucket:
            k = Key(self.bucket)
        else:
            k = Key(self.bucket_backup)
        k.key = source_key
        k.get_contents_to_filename(destination_filename)


    def com_aws_s3_delete(self, key, backup_bucket = False):
        """
        Delete
        """
        if not backup_bucket:
            self.bucket.delete_key(key)
        else:
            self.bucket_backup.delete_key(key)


    def com_aws_s3_backup_purge(self, days_to_keep):
        """
        Remove old database backups
        """
        # Delete files older than days to keep.
        for key in self.bucket_backup.list():
            timestamp = datetime.strptime(key.last_modified, '%Y-%m-%dT%H:%M:%S.%fZ')
            if timestamp < days_to_keep:
                self.bucket_backup.delete_key(key)


    def com_aws_s3_bucket_list(self, backup_bucket = False):
        """
        Bucket list (ha)
        """
        if not backup_bucket:
            return self.bucket.list()
        else:
            return self.bucket_backup.list()
