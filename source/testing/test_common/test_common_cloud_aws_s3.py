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

import os
import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_cloud_aws_s3
from common import common_config_ini


class TestCommonCloudAWSS3(object):

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.awss3 = common_cloud_aws_s3.CommonCloudAWSS3(option_config_json)

    @classmethod
    def teardown_class(self):
        pass

    # upload file to S3
    @pytest.mark.parametrize(("source_path", "destination_filename", "backup_bucket"), [
        ("./cache/HashCalc.txt", "HashCalc.txt", False),
        ("./cache/HashCalc.txt", "HashCalc.txt", True),
        ("./cache/HashCalcfake.txt", "HashCalc.txt", False),
        ("./cache/HashCalcfake.txt", "HashCalc.txt", True)])
    def test_com_aws_s3_upload(self, source_path, destination_filename,
                               backup_bucket):
        """
        Test function
        """
        self.awss3.com_aws_s3_upload(
            source_path, destination_filename, backup_bucket)

    # download from s3
    # def com_AWS_S3_Download(self, source_key, destination_filename, backup_bucket = False):
    @pytest.mark.parametrize(("source_key", "destination_filename", "backup_bucket"), [
        ("HashCalc.txt", "./cache/HashCalcDown.txt", False),
        ("HashCalc.txt", "./cache/HashCalcDown2.txt", True)])
    def test_com_aws_s3_download(self, source_key, destination_filename, backup_bucket):
        """
        Test function
        """
        self.awss3.com_aws_s3_download(
            source_key, destination_filename, backup_bucket)
        os.remove("./cache/HashCalcDown.txt")
        os.remove("./cache/HashCalcDown2.txt")

    # delete
    @pytest.mark.parametrize(("key", "backup_bucket"), [
        ("HashCalc.txt", False),
        ("HashCalc.txt", True)])
    def test_com_aws_s3_delete(self, key, backup_bucket):
        """
        Test function
        """
        self.awss3.com_aws_s3_delete(key, backup_bucket)

    # remove old database backups
    @pytest.mark.parametrize(("days_to_keep"), [
        (7),
        (400)])
    def test_com_aws_s3_backup_purge(self, days_to_keep):
        """
        Test function
        """
        self.awss3.com_aws_s3_backup_purge(days_to_keep)

    # bucket list (ha)
    @pytest.mark.parametrize(("backup_bucket"), [
        (True),
        (False)])
    def test_com_aws_s3_bucket_list(self, backup_bucket):
        """
        Test function
        """
        self.awss3.com_aws_s3_bucket_list(backup_bucket)
