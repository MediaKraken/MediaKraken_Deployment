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

# https://github.com/MediaKraken-Dep/pysmb
import os
import urllib.error
import urllib.parse
import urllib.request

from smb.SMBConnection import SMBConnection
from smb.SMBHandler import SMBHandler

from . import common_global


class CommonNetworkCIFSShareURL:
    """
    Handle CIFS shares
    """

    def __init__(self):
        pass

    def com_cifs_url_director(self, connect_string):
        """
        Create director for CIFS management
        """
        self.director = urllib.request.build_opener(SMBHandler)

    def com_cifs_url_download(self, connect_string):
        """
        Grab file from CIFS
        """
        # For paths/files with unicode characters, simply pass in the URL as an unicode string
        file_con = self.director.open(
            'smb://myuserID:mypassword@192.168.1.1/sharedfolder/waffle.dat')
        # Process file_con like a file-like object and then close it.
        file_con.close()

    def com_cifs_url_upload(self, file_path, connect_string):
        """
        Post file via CIFS
        """
        file_con = self.director.open(
            'smb://myuserID:mypassword@192.168.1.1/sharedfolder/upload_file.dat',
            data=open(file_path, 'rb'))
        file_con.close()


class CommonCIFSShare:
    """
    Handle CIFS shares
    """

    def __init__(self):
        self.smb_conn = None

    def com_cifs_connect(self, ip_addr, user_name='guest', user_password=''):
        """
        Connect to share
        """
        server_name = 'Server'
        client_name = 'My Computer'
        self.smb_conn = SMBConnection(user_name, user_password, client_name, server_name,
                                      use_ntlm_v2=True)
        self.smb_conn.connect(ip_addr, 139)

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
            common_global.es_inst.com_elastic_index('info', {'stuff': row_data.filename})
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

#    ans = com_cifs_Walk(conn, 'SHARE_FOLDER',file_path= '/')
