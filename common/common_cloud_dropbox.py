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
import os
import dropbox


class CommonCloudDropbox(object):
    """
    Class for interfacing with dropbox
    """
    def __init__(self):
        # set active false so if following falls
        self.active = False
        # pull in the ini file config
        import ConfigParser
        Config = ConfigParser.ConfigParser()
        if os.path.isfile("MediaKraken.ini"):
            Config.read("MediaKraken.ini")
        else:
            Config.read("../MediaKraken.ini")
        if Config.get('Dropbox', 'APIKey').strip() != 'None':
            flow = dropbox.client.DropboxOAuth2FlowNoRedirect(Config.get('Dropbox', 'APIKey').strip(), Config.get('Dropbox', 'APISecret').strip())
            self.active = True


    def com_cloud_dropbox_user_auth(self):
        """
        Have the user sign in and authorize this token
        """
        authorize_url = flow.start()
        print('1. Go to: %s', authorize_url)
        print('2. Click "Allow" (you might have to log in first)')
        print('3. Copy the authorization code.')
        code = raw_input("Enter the authorization code here: ").strip()
        # This will fail if the user enters an invalid authorization code
        access_token, user_id = flow.finish(code)
        self.client = dropbox.client.DropboxClient(access_token)
        print('linked account: %s', self.client.account_info())


    def com_cloud_dropbox_upload(self, file_name, file_save_name):
        """
        Upload
        """
        f = open(file_name, 'rb')
        response = self.client.put_file(file_save_name, f)
        print('uploaded: %s', response)


    def com_cloud_dropbox_list(self, dir_name='/'):
        """
        List files in folder
        """
        folder_metadata = self.client.metadata(dir_name)
        print('metadata: %s', folder_metadata)


    def com_cloud_dropbox_download(self, file_name, file_save_name):
        """
        Download file from dropbox
        """
        f, metadata = self.client.get_file_and_metadata(file_name)
        out = open(file_save_name, 'wb')
        out.write(f.read())
        out.close()
        print(metadata)
