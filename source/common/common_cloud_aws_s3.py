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

import time

import boto
from boto.s3.key import Key


class CommonCloudAWSS3(object):
    """
    Class for interfacing with aws s3
    """

    def __init__(self, option_config_json):
        # set active false so if following falls
        self.active = False
        if option_config_json['AWSS3']['AccessKey'] is not None:
            self.aws_access_key_id = option_config_json['AWSS3']['AccessKey']
            self.aws_secret_access_key = option_config_json['AWSS3']['SecretAccessKey']
            self.aws_bucket_name = option_config_json['AWSS3']['Bucket']
            self.aws_bucket_backup_name = option_config_json['AWSS3']['BackupBucket']
            # setup connection and buckets for later use
            conn = boto.connect_s3(
                self.aws_access_key_id, self.aws_secret_access_key)
            self.bucket = conn.get_bucket(self.aws_bucket_name)
            self.bucket_backup = conn.get_bucket(self.aws_bucket_backup_name)
            self.active = True

    def com_aws_s3_upload(self, source_path, destination_filename, backup_bucket=False):
        """
        Upload file to S3
        """
        if not backup_bucket:
            k = Key(self.bucket)
        else:
            k = Key(self.bucket_backup)
        k.key = destination_filename
        k.set_contents_from_filename(source_path)

    def com_aws_s3_download(self, source_key, destination_filename, backup_bucket=False):
        """
        Download from s3
        """
        if not backup_bucket:
            k = Key(self.bucket)
        else:
            k = Key(self.bucket_backup)
        k.key = source_key
        k.get_contents_to_filename(destination_filename)

    def com_aws_s3_delete(self, key, backup_bucket=False):
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
            timestamp = time.strptime(
                key.last_modified, '%Y-%m-%dT%H:%M:%S.%fZ')
            if timestamp < days_to_keep:
                self.bucket_backup.delete_key(key)

    def com_aws_s3_bucket_list(self, backup_bucket=False):
        """
        Bucket list (ha)
        """
        if not backup_bucket:
            return self.bucket.list()
        else:
            return self.bucket_backup.list()
