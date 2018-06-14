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

import onedrivesdk
from onedrivesdk.model.item_reference import ItemReference


# import asyncio


# @asyncio.coroutine
# def run_gets(client):
#    coroutines = [client.drive("me").request().get_async() for i in range(3)]
#    for future in asyncio.as_completed(coroutines):
#        drive = yield from future
#        print(drive.id)


class CommonCloudOneDrive(object):
    """
    Class for interfacing with onedrive
    """

    def __init__(self, option_config_json):
        # set active false so if following falls
        self.active = False
        # authenticate

    #        redirect_uri = "http://localhost:8080/"
    #        client_secret = "your_app_secret"
    #        client = onedrivesdk.get_default_client(client_id='your_client_id',
    #                                                scopes=['wl.signin',
    #                                                        'wl.offline_access',
    #                                                        'onedrive.readwrite'])
    #        auth_url = client.auth_provider.get_auth_url(redirect_uri)
    #        #this will block until we have the code
    #        code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
    #        client.auth_provider.authenticate(code, redirect_uri, client_secret)
    # self.active = True

    def com_cloud_onedrive_update(self, file_name, file_path):
        """
        upload
        """
        returned_item = self.client.item(drive="me", id="root").children["newfile.txt"]. \
            upload("./path_to_file.txt")

    def com_cloud_onedrive_download(self, file_name, file_path):
        """
        Download
        """
        root_folder = self.client.item(drive="me", id="root").children.get()
        id_of_file = root_folder[0].id
        self.client.item(drive="me", id=id_of_file).download(
            "./path_to_download_to.txt")

    def com_cloud_onedrive_add_folder(self, folder_name):
        """
        Add folder
        """
        folder_handle = onedrivesdk.Folder()
        i = onedrivesdk.Item()
        i.name = folder_name
        i.folder = folder_handle
        self.client.item(drive="me", id="root").children.add(i)

    def com_cloud_onedrive_copy(self, file_from, file_to):
        """
        Copy file
        """
        ref = ItemReference()
        ref.id = "yourparent!id"  # path also supported
        copy_operation = self.client.item(drive="me",
                                          id="youritemtocopy!id").copy(name="new copied name",
                                                                       parent_reference=ref).post()
        # copy_operation.item will return None until the copy has completed.
        # If you would like to block until the operation has been completed
        # and copy_operation.item is no longer None
        copy_operation.poll_until_complete()

    def com_cloud_onedrive_name(self, file_from, file_to):
        """
        File rename
        """
        renamed_item = onedrivesdk.Item()
        renamed_item.name = "NewItemName"
        renamed_item.id = "youritemtorename!id"
        new_item = self.client.item(
            drive="me", id=renamed_item.id).update(renamed_item)

    def com_cloud_onedrive_page(self):
        """
        page through collection
        """
        # get the top three elements of root, leaving the next page for more elements
        collection = self.client.item(
            drive="me", id="root").children.request(top=3).get()
        # get the first item in the collection
        item = collection[0]
        # get the next page of three elements, if none exist, returns None
        collection2 = collection.next_page_request.get()

###############
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run_gets(self.client))
