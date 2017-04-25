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
import sys
import os
import uuid
from . import common_file
from . import common_system


def com_emby_installed_directory(dir_name=None):
    """
    Determine install directory
    """
    if dir_name is None:
        # windows
        if str.upper(sys.platform[0:3]) == 'WIN' \
        or str.upper(sys.platform[0:3]) == 'CYG':
            if os.path.isdir("C:/Users/" + db_username_dir + "/AppData/Roaming/Emby-Server/"):
                dir_name = "C:/Users/" + db_username_dir + "/AppData/Roaming/Emby-Server/"
            elif os.path.isdir("C:/Users/" + db_username_dir\
                + "/AppData/Roaming/MediaBrowser-Server/"):
                dir_name = "C:/Users/" + db_username_dir + "/AppData/Roaming/MediaBrowser-Server/"
        # mac
        elif str.upper(sys.platform[0:3]) == 'DAR':
            if os.path.isdir("/Users/" + db_username_dir + "/EmbyServer/ProgramData-Server/"):
                dir_name = "/Users/" + db_username_dir + "/EmbyServer/ProgramData-Server/"
            elif os.path.isdir("/Users/" + db_username_dir + "/MediaBrowser/ProgramData-Server/"):
                dir_name = "/Users/" + db_username_dir + "/MediaBrowser/ProgramData-Server/"
        else:
            # xubuntu
            if os.path.isdir("/var/lib/emby-server"):
                dir_name = "/var/lib/emby-server/"
            elif os.path.isdir("/var/lib/mediabrowser/"):
                dir_name = "/var/lib/mediabrowser/"
            else:
                # centos 6.x
                if os.path.isdir("/var/opt/MediaBrowser/MediaBrowserServer/"):
                    dir_name = '/var/opt/MediaBrowser/MediaBrowserServer/'
    return dir_name


def com_emby_library_list(dir_name=None):
    """
    Fetch library list
    """
    if dir_name is None:
        dir_name = os.path.join(com_emby_installed_directory(), 'root', 'default')
    # grab dir and files
    library_list = {}
    if dir_name is not None:
        for dir_path in common_file.com_file_dir_list(dir_name, None, False, False):
            logging.info("main dir: %s", dir_path)
            lib_file_path = []
            for file_list in common_file.com_file_dir_list(os.path.join(dir_name, dir_path,
                    None, False, False)):
                logging.info("file: %s", file_list)
                if file_list.endswith('.mblink'): # only grab "link" files for path
                    lib_file_path.append(common_file.com_file_load_data(os.path.join(dir_name,
                        dir_path, file_list), False))
            library_list[dir_path] = lib_file_path
    return library_list


def com_emby_check_instance():
    """
    Check for running instance
    """
    name_check = 'emby-server'
    if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
        name_check += '.exe'
    if common_system.com_process_list(name_check):
        logging.critical("Please shutdown Emby server first")
        sys.exit(-1)


def com_emby_guid_to_uuid(emby_guid):
    """
    C# guid to text
    """
    return uuid.UUID(bytes=emby_guid)


def com_emby_uuid_to_guid(emby_guid):
    """
    Text uuid to C# guid
    """
    return emby_guid.bytes
