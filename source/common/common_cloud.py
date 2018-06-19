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

from . import common_cloud_aws_s3
from . import common_cloud_dropbox
from . import common_cloud_google_drive
from . import common_cloud_onedrive
from . import common_string

CLOUD_BACKUP_CLASS = (('awss3', 'AWS S3'),
                      ('dropbox', 'Dropbox'),
                      ('google', 'Google Drive'),
                      ('local', 'Local Filesystem'),
                      ('onedrive', 'Microsoft OneDrive'),
                      )


class CommonCloud(object):
    """
    Class for interfacing with aws s3
    """

    def __init__(self, option_config_json):
        self.cloud_awss3 = common_cloud_aws_s3.CommonCloudAWSS3(
            option_config_json)
        self.cloud_dropbox = common_cloud_dropbox.CommonCloudDropbox(
            option_config_json)
        self.cloud_google = common_cloud_google_drive.CommonCloudGoogleDrive(
            option_config_json)
        self.cloud_onedrive = common_cloud_onedrive.CommonCloudOneDrive(
            option_config_json)

    def com_cloud_backup_list(self):
        """
        Get list of all backups
        """
        backup_files = []
        for backup_class in CLOUD_BACKUP_CLASS:
            for backup_cloud in self.com_cloud_file_list(backup_class[0], None, True):
                backup_files.append((backup_cloud.name, backup_class[1],
                                     common_string.com_string_bytes2human(backup_cloud.size)))
        return backup_files

    def com_cloud_file_store(self, cloud_type, file_path_name, file_save_name,
                             backup_bucket=False):
        """
        Store file in cloud
        """
        if cloud_type == "google":
            if self.cloud_google.active:
                pass
        elif cloud_type == "awss3":
            if self.cloud_awss3.active:
                self.cloud_awss3.com_aws_s3_upload(
                    file_path_name, file_save_name, backup_bucket)
        elif cloud_type == "dropbox":
            if self.cloud_dropbox.active:
                self.cloud_dropbox.com_cloud_dropbox_upload(
                    file_path_name, file_save_name)
        elif cloud_type == "onedrive":
            if self.cloud_onedrive.active:
                self.cloud_onedrive.com_cloud_onedrive_update(
                    file_path_name, file_save_name)
        else:
            return None

    def com_cloud_file_delete(self, cloud_type, file_name, backup_bucket=False):
        """
        Delete file in cloud
        """
        if cloud_type == "google":
            if self.cloud_google.active:
                pass
        elif cloud_type == "awss3":
            if self.cloud_awss3.active:
                self.cloud_awss3.com_aws_s3_delete(file_name, backup_bucket)
        elif cloud_type == "dropbox":
            if self.cloud_dropbox.active:
                pass
        elif cloud_type == "onedrive":
            if self.cloud_onedrive.active:
                pass
        else:
            return None

    def com_cloud_file_list(self, cloud_type, file_path=None, backup_bucket=False):
        """
        List files in cloud
        """
        if cloud_type == "google":
            if self.cloud_google.active:
                pass
        elif cloud_type == "awss3":
            if self.cloud_awss3.active:
                return self.cloud_awss3.com_aws_s3_bucket_list(backup_bucket)
        elif cloud_type == "dropbox":
            if self.cloud_dropbox.active:
                return self.cloud_dropbox.com_cloud_dropbox_list(file_path)
        elif cloud_type == "onedrive":
            if self.cloud_onedrive.active:
                pass
        return []

    def com_cloud_file_retrieve(self, cloud_type, file_name, file_location):
        """
        Fetch file from cloud
        """
        if cloud_type == "google":
            if self.cloud_google.active:
                pass
        elif cloud_type == "awss3":
            if self.cloud_awss3.active:
                self.cloud_awss3.com_aws_s3_download(file_name, file_location)
        elif cloud_type == "dropbox":
            if self.cloud_dropbox.active:
                self.cloud_dropbox.com_cloud_dropbox_download(
                    file_name, file_location)
        elif cloud_type == "onedrive":
            if self.cloud_onedrive.active:
                self.cloud_onedrive.com_cloud_onedrive_download(
                    file_name, file_location)
        else:
            return None

    def com_cloud_file_rename(self, cloud_type, file_from, file_to):
        """
        Rename file on cloud
        """
        if cloud_type == "google":
            if self.cloud_google.active:
                pass
        elif cloud_type == "awss3":
            if self.cloud_awss3.active:
                pass
        elif cloud_type == "dropbox":
            if self.cloud_dropbox.active:
                pass
        elif cloud_type == "onedrive":
            if self.cloud_onedrive.active:
                pass
        else:
            return None

    def com_cloud_create_folder(self, cloud_type, dir_name):
        """
        Create directory in cloud
        """
        if cloud_type == "google":
            if self.cloud_google.active:
                pass
        elif cloud_type == "awss3":
            if self.cloud_awss3.active:
                pass
        elif cloud_type == "dropbox":
            if self.cloud_dropbox.active:
                pass
        elif cloud_type == "onedrive":
            if self.cloud_onedrive.active:
                pass
        else:
            return None
