"""
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
"""

import os
import socket

import smbclient
from smb.SMBConnection import SMBConnection

from . import common_logging_elasticsearch_httpx


# has v3 support
class CommonNetworkCIFS:
    def __init__(self, server_name, share_name, username='guest', password=None, encrypt=False):
        if password is None:
            smbclient.register_session(server_name,
                                       username=username,
                                       encrypt=encrypt,
                                       )
        else:
            smbclient.register_session(server_name,
                                       username=username,
                                       password=password,
                                       encrypt=encrypt,
                                       )
        self.server_name = server_name
        self.share_name = share_name

    def com_cifs_delete(self, file_name):
        # smbclient.remove(r"\\server\share\file.txt")
        smbclient.remove(file_name)

    def com_cifs_delete_directory(self, dir_name):
        smbclient.rmdir(dir_name)

    def com_cifs_stat(self, file_name):
        return smbclient.stat(file_name)

    def com_cifs_write(self, file_name, file_mode='w'):  # w write, a append
        with smbclient.open_file(file_name, mode=file_mode) as fd:
            fd.write(u"content")

    def com_cifs_read(self, file_name, file_mode=None):
        if file_name is None:
            with smbclient.open_file(file_name) as fd:
                return fd.read()
        else:
            with smbclient.open_file(file_name, mode="rb") as fd:
                return fd.read()

    def com_cifs_directory_create(self, dir_path):
        smbclient.mkdir(dir_path)

    def com_cifs_directory_file_list(self, dir_path):
        return smbclient.listdir(dir_path)

    def com_cifs_file_walk(self, dir_path):
        for file_info in smbclient.scandir(dir_path):
            file_inode = file_info.inode()
            if file_info.is_file():
                print("File: %s %d" % (file_info.name, file_inode))
            elif file_info.is_dir():
                print("Dir: %s %d" % (file_info.name, file_inode))
            else:
                print("Symlink: %s %d" % (file_info.name, file_inode))


# only does v1 and v2
# class CommonNetworkCIFSShareURL:
#     """
#     Handle CIFS shares
#     """
#
#     def __init__(self):
#         pass
#
#     def com_cifs_url_director(self, connect_string):
#         """
#         Create director for CIFS management
#         """
#         self.director = urllib.request.build_opener(SMBHandler)
#
#     def com_cifs_url_download(self, connect_string):
#         """
#         Grab file from CIFS
#         """
#         # For paths/files with unicode characters, simply pass in the URL as an unicode string
#         file_con = self.director.open(
#             'smb://myuserID:mypassword@192.168.1.1/sharedfolder/waffle.dat')
#         # Process file_con like a file-like object and then close it.
#         file_con.close()
#
#     def com_cifs_url_upload(self, file_path, connect_string):
#         """
#         Post file via CIFS
#         """
#         file_con = self.director.open(
#             'smb://myuserID:mypassword@192.168.1.1/sharedfolder/upload_file.dat',
#             data=open(file_path, 'rb'))
#         file_con.close()


# only does v1 and v2
class CommonCIFSShare:
    """
    Handle CIFS shares
    """

    def __init__(self):
        self.smb_conn = None

    def com_cifs_open(self, ip_addr, user_name='guest', user_password=''):
        self.smb_conn = SMBConnection(user_name, user_password, 'My Computer', 'Server',
                                      use_ntlm_v2=True)
        try:
            self.smb_conn.connect(ip_addr, 139)
        except socket.gaierror:
            # TODO send notification that it failed
            return False
        return True

    def com_cifs_share_list_by_connection(self):
        """
        List shares
        """
        share_names = []
        for row_data in self.smb_conn.listShares():
            share_names.append(row_data.name)
        return share_names

    def com_cifs_share_file_list_by_share(self, share_name, path_text='/'):
        """
        List files in share
        """
        file_names = []
        for row_data in self.smb_conn.listPath(share_name, path_text):
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                 message_text={
                                                                     'stuff': row_data.filename})
            file_names.append(row_data.filename)
        return file_names

    def com_cifs_share_directory_check(self, share_name, dir_path):
        """
        Verify smb directory
        """
        # try due to fact invalid file/path freaks out the connection
        try:
            return self.smb_conn.getAttributes(share_name, dir_path).isDirectory
        except:
            pass
        return False

    def com_cifs_share_file_dir_info(self, share_name, file_path):
        """
        Get specific path/file info
        """
        return self.smb_conn.getAttributes(share_name, file_path)

    def com_cifs_share_file_upload(self, file_path):
        """
        Upload file to smb
        """
        self.smb_conn.storeFile(os.path.join(
            self.sharename, file_path), open(file_path, 'rb'))

    def com_cifs_share_file_download(self, file_path):
        """
        Download from smb
        """
        self.smb_conn.retrieveFile(self.sharename, open(file_path, 'wb'))

    def com_cifs_share_file_delete(self, share_name, file_path):
        """
        Delete from smb
        """
        self.smb_conn.deleteFiles(os.path.join(share_name, file_path))

    def com_cifs_close(self):
        """
        Close connection
        """
        self.smb_conn.close()

    def com_cifs_walk(self, share_name, file_path='/'):
        """
        cifs directory walk
        """
        dirs, nondirs = [], []
        for name in self.smb_conn.listPath(share_name, file_path):
            if name.isDirectory:
                if name.filename not in ['.', '..']:
                    dirs.append(name.filename)
            else:
                nondirs.append(name.filename)
        yield file_path, dirs, nondirs
        for name in dirs:
            #           new_path = file_path + '\\' + name
            #            for ndx in self.com_cifs_walk(share_name, new_path):
            for ndx in self.com_cifs_walk(share_name, os.path.join(file_path, name)):
                yield ndx
        return dirs, nondirs
#    ans = com_cifs_Walk(conn, 'SHARE_FOLDER',file_path= '/')
