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

import logging
import MK_Common_Cloud_AWS_S3
import MK_Common_Cloud_Dropbox
import MK_Common_Cloud_Google_Drive
import MK_Common_Cloud_OneDrive
import MK_Common_String


cloud_backup_class = (('awss3', 'AWS S3'),
    ('dropbox', 'Dropbox'),
    ('google', 'Google Drive'),
    ('local', 'Local Filesystem'),
    ('onedrive', 'Microsoft OneDrive')
    )


awss3 = MK_Common_Cloud_AWS_S3.MK_Common_AWS_S3_API()
dropbox = MK_Common_Cloud_Dropbox.MK_Common_DropBox_API()
google = MK_Common_Cloud_Google_Drive.MK_Common_Google_Drive_API()
onedrive = MK_Common_Cloud_OneDrive.MK_Common_OneDrive_API()


# get list of all backups
def MK_Common_Cloud_Backup_List():
    backup_files = []
    for backup_class in cloud_backup_class:    
        for backup_cloud in MK_Common_Cloud_File_List(backup_class[0], None, True):
            loggging.debug("cloud back: %s",backup_cloud)
            backup_files.append((backup_cloud.name, backup_class[1], MK_Common_String.bytes2human(backup_cloud.size)))
    return backup_files


# store file in cloud
def MK_Common_Cloud_File_Store(cloud_type, file_path_name, file_save_name, backup_bucket=False):
    if cloud_type == "google":
        if google.active:
            pass
    elif cloud_type == "awss3":
        if awss3.active:
            awss3.MK_Common_AWS_S3_Upload(file_path_name, file_save_name, backup_bucket)
    elif cloud_type == "dropbox":
        if dropbox.active:
            MK_Common_Cloud_Dropbox.dropbox_upload(file_path_name, file_save_name)
    elif cloud_type == "onedrive":
        if onedrive.active:
            MK_Common_Cloud_OneDrive.MK_OneDrive_Update(file_path_name, file_save_name)
    else:
        return None


# delete file in cloud
def MK_Common_Cloud_File_Delete(cloud_type, file_name, backup_bucket=False):
    if cloud_type == "google":
        if google.active:
            pass
    elif cloud_type == "awss3":
        if awss3.active:
            awss3.MK_Common_AWS_S3_Delete(file_name, backup_bucket)
    elif cloud_type == "dropbox":
        if dropbox.active:
            pass
    elif cloud_type == "onedrive":
        if onedrive.active:
            pass
    else:
        return None


# list files in cloud
def MK_Common_Cloud_File_List(cloud_type, file_path=None, backup_bucket=False):
    if cloud_type == "google":
        if google.active:
            pass
    elif cloud_type == "awss3":
        if awss3.active:
            return awss3.MK_Common_AWS_S3_Bucket_List(backup_bucket)
    elif cloud_type == "dropbox":
        if dropbox.active:
            return MK_Common_Cloud_Dropbox.dropbox_list(file_path)
    elif cloud_type == "onedrive":
        if onedrive.active:
            pass
    return []


# fetch file from cloud
def MK_Common_Cloud_File_Retrieve(cloud_type, file_name, file_location):
    if cloud_type == "google":
        if google.active:
            pass
    elif cloud_type == "awss3":
        if awss3.active:
            awss3.MK_Common_AWS_S3_Download(file_name, file_location)
    elif cloud_type == "dropbox":
        if dropbox.active:
            MK_Common_Cloud_Dropbox.dropbox_download(file_name, file_location)
    elif cloud_type == "onedrive":
        if onedrive.active:
            MK_Common_Cloud_OneDrive.MK_OneDrive_Download(file_name, file_location)
    else:
        return None


# rename file on cloud
def MK_Common_Cloud_File_Rename(cloud_type, file_from, file_to):
    if cloud_type == "google":
        if google.active:
            pass
    elif cloud_type == "awss3":
        if awss3.active:
            pass
    elif cloud_type == "dropbox":
        if dropbox.active:
            pass
    elif cloud_type == "onedrive":
        if onedrive.active:
            pass
    else:
        return None


# create direcgtory in cloud
def MK_Common_Cloud_Create_Folder(cloud_type, dir_name):
    if cloud_type == "google":
        if google.active:
            pass
    elif cloud_type == "awss3":
        if awss3.active:
            pass
    elif cloud_type == "dropbox":
        if dropbox.active:
            pass
    elif cloud_type == "onedrive":
        if onedrive.active:
            pass
    else:
        return None
