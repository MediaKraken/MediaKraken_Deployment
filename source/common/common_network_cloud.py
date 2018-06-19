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

import os

import libcloud
from gevent import monkey

monkey.patch_all()


class CommonLibCloud(object):
    """
    Class for interfacing with cloud
    """

    def __init__(self, option_config_json):
        self.cls = libcloud.get_driver(libcloud.DriverType.COMPUTE,
                                       libcloud.DriverType.COMPUTE.RACKSPACE)
        self.driver = self.cls('my username', 'my api key')

    def com_net_cloud_upload(self, input_file_name, output_file_name):
        container = self.driver.get_container(
            container_name='my-backups-12345')
        extra = {'meta_data': {'owner': 'myuser', 'created': '2014-02-2'}}
        with open(input_file_name, 'rb') as iterator:
            obj = self.driver.upload_object_via_stream(iterator=iterator,
                                                       container=container,
                                                       object_name=output_file_name,
                                                       extra=extra)

    #
    # pprint(driver.list_sizes())
    # pprint(driver.list_nodes())

    def download_obj(self, container, obj):
        obj = self.driver.get_object(container_name=container.name,
                                     object_name=obj.name)
        filename = os.path.basename(obj.name)
        path = os.path.join(os.path.expanduser('~/Downloads'), filename)
        print(('Downloading: %s to %s' % (obj.name, path)))
        obj.download(destination_path=path)

# containers = self.driver.list_containers()
#
# jobs = []
# pool = Pool(20)
#
# for index, container in enumerate(containers):
#     objects = container.list_objects()
#
#     for obj in objects:
#         pool.spawn(download_obj, container, obj)
#
# pool.join()
