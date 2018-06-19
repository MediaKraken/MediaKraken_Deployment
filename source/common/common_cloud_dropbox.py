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

import dropbox


class CommonCloudDropbox(object):
    """
    Class for interfacing with dropbox
    """

    def __init__(self, option_config_json):
        # set active false so if following falls
        self.active = False
        if option_config_json['Dropbox']['APIKey'] is not None:
            self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(
                option_config_json['Dropbox']['APIKey'],
                option_config_json['Dropbox']['APISecret'])
            self.active = True
        self.client = None

    def com_cloud_dropbox_user_auth(self):
        """
        Have the user sign in and authorize this token
        """
        authorize_url = self.flow.start()
        print(('1. Go to: %s', authorize_url))
        print('2. Click "Allow" (you might have to log in first)')
        print('3. Copy the authorization code.')
        code = input("Enter the authorization code here: ").strip()
        # This will fail if the user enters an invalid authorization code
        access_token, user_id = self.flow.finish(code)  # pylint: disable=W0612
        self.client = dropbox.client.DropboxClient(access_token)
        print(('linked account: %s', self.client.account_info()))

    def com_cloud_dropbox_upload(self, file_name, file_save_name):
        """
        Upload
        """
        file_handle = open(file_name, 'rb')
        response = self.client.put_file(file_save_name, file_handle)
        print(('uploaded: %s', response))

    def com_cloud_dropbox_list(self, dir_name='/'):
        """
        List files in folder
        """
        folder_metadata = self.client.metadata(dir_name)
        print(('metadata: %s', folder_metadata))

    def com_cloud_dropbox_download(self, file_name, file_save_name):
        """
        Download file from dropbox
        """
        file_handle, metadata = self.client.get_file_and_metadata(file_name)
        out = open(file_save_name, 'wb')
        out.write(file_handle.read())
        out.close()
        print(metadata)
