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

import os

import httplib2
import oauth2client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

from . import common_global

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class CommonCloudGoogleDrive(object):
    """
    Class for interfacing with google drive
    """

    def __init__(self, option_config_json):
        # set active false so if following falls
        self.active = False
        # pull in the ini file config
        if option_config_json['GoogleDrive']['SecretFile'] is not None:
            # flow = dropbox.client.DropboxOAuth2FlowNoRedirect
            # (option_config_json.get('GoogleDrive', 'SecretFile').strip())
            self.active = True

    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Drive API Python Quickstart'

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(
            credential_dir, 'drive-python-quickstart.json')
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatability with Python 2.6
                credentials = tools.run(flow, store)
            print(('Storing credentials to %s', credential_path))
        return credentials

    def main():
        """Shows basic usage of the Google Drive API.

        Creates a Google Drive API service object and outputs the names and IDs
        for up to 10 files.
        """
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v2', http=http)
        results = service.files().list(maxResults=10).execute()
        items = results.get('items', [])
        if not items:
            common_global.es_inst.com_elastic_index('error', {'stuff': 'No files found.'})
        else:
            for item in items:
                print(('{0} ({1})'.format(item['title'], item['id'])))

    if __name__ == '__main__':
        main()
