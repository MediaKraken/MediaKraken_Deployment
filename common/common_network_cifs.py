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
import os
import urllib2
from smb.SMBConnection import SMBConnection


class MK_Common_CIFS_Share_URL_API:
    def __init__(self):
        pass


    def MK_Common_CIFS_URL_Director(self, connect_string):
        self.director = urllib2.build_opener(SMBHandler)


    def MK_Common_CIFS_URL_Download(self, connect_string):
        # For paths/files with unicode characters, simply pass in the URL as an unicode string
        file_con = self.director.open('smb://myuserID:mypassword@192.168.1.1/sharedfolder/waffle.dat')
        # Process file_con like a file-like object and then close it.
        file_con.close()


    def MK_Common_CIFS_URL_Upload(self, file_path, connect_string):
        file_con = self.director.open('smb://myuserID:mypassword@192.168.1.1/sharedfolder/upload_file.dat', data = open(file_path, 'rb'))
        file_con.close()


class MK_Common_CIFS_Share_API:
    def __init__(self):
        pass


    def MK_Common_CIFS_Connect(self, ip_addr, user_name='guest', user_password=''):
        """
        Connect to share
        """
        server_name = 'Server'
        client_name = 'My Computer'
        self.smb_conn = SMBConnection(user_name, user_password, client_name, server_name, use_ntlm_v2 = True)
        self.smb_conn.connect(ip_addr, 139)


    def MK_Common_CIFS_Share_List_By_Connection(self):
        """
        List shares
        """
        share_names = []
        for row_data in self.smb_conn.listShares():
            share_names.append(row_data.name)
        return share_names


    def MK_Common_CIFS_Share_File_List_By_Share(self, share_name, path_text='/'):
        """
        List files in share
        """
        file_names = []
        for row_data in self.smb_conn.listPath(share_name, path_text):
            logging.debug(row_data.filename)
            file_names.append(row_data.filename)
        return file_names


    def MK_Common_CIFS_Share_Directory_Check(self, share_name, dir_path):
        """
        Verify smb directory
        """
        # try due to fact invalid file/path freaks out the connection
        try:
            return self.smb_conn.getAttributes(share_name, dir_path).isDirectory
        except:
            pass
        return False


    def MK_Common_CIFS_Share_File_Dir_Info(self, share_name, file_path):
        """
        Get specific path/file info
        """
        return self.smb_conn.getAttributes(share_name, file_path)


    def MK_Common_CIFS_Share_File_Upload(self, file_path):
        """
        Upload file to smb
        """
        self.smb_conn.storeFile(self.sharename, '/' + file_path, open(file_path,'rb'))


    def MK_Common_CIFS_Share_File_Download(self, file_path):
        """
        Download from smb
        """
        self.smb_conn.retrieveFile(self.sharename, open(file_path, 'wb'))


    def MK_Common_CIFS_Share_File_Delete(self, share_name, file_path):
        """
        Delete from smb
        """
        self.smb_conn.deleteFiles(share_name, '/' + file_path)


    def MK_Common_CIFS_Close(self):
        """
        Close connection
        """
        self.smb_conn.close()


    def MK_Common_CIFS_Walk(self, share_name, file_path='/'):
        """
        cifs directory walk
        """
        dirs , nondirs = [], []
        for name in self.smb_conn.listPath(share_name, file_path):
            if name.isDirectory:
                if name.filename not in ['.', '..']:
                    dirs.append(name.filename)
            else:
                nondirs.append(name.filename)
        yield file_path, dirs, nondirs
        for name in dirs:
            new_path = file_path + '\\' + name
            for x in self.MK_Common_CIFS_Walk(share_name, new_path):
                yield x

#    ans = MK_Common_CIFS_Walk(conn, 'SHARE_FOLDER',file_path= '/')