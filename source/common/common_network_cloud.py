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
from datetime import date

# from gevent import monkey  # pylint: disable=import-error
#
# monkey.patch_all()
import libcloud
from common import common_logging_elasticsearch_httpx
from libcloud.storage.providers import DRIVERS

from . import common_internationalization


def com_libcloud_storage_provider_list():
    return DRIVERS


class CommonLibCloud:
    """
    Class for interfacing with cloud
    """

    def __init__(self, option_config_json, cloud_provider='Local Storage'):
        self.cls = libcloud.get_driver(DRIVERS[cloud_provider][1])
        self.driver = self.cls(key=option_config_json['Cloud'][cloud_provider]['User'],
                               secret=option_config_json['Cloud'][cloud_provider]['API_Key'])
        self.user = option_config_json['Cloud'][cloud_provider]['User']

    def com_net_cloud_upload(self, container_name, input_file_name, output_file_name):
        container = self.driver.get_container(container_name=container_name)
        extra = {'meta_data': {'owner': self.user,
                               'created': common_internationalization.com_inter_date_format(
                                   date.today())}}
        with open(input_file_name, 'rb') as iterator:
            obj = self.driver.upload_object_via_stream(iterator=iterator,
                                                       container=container,
                                                       object_name=output_file_name,
                                                       extra=extra)

    def com_net_cloud_download(self, container, obj):
        obj = self.driver.get_object(container_name=container.name,
                                     object_name=obj.name)
        filename = os.path.basename(obj.name)
        path = os.path.join(os.path.expanduser('~/Downloads'), filename)
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
        {'Downloading': '%s to %s' % (obj.name, path)})
        obj.download(destination_path=path)

    def com_net_cloud_list_container(self):
        return self.driver.list_containers()

    def com_net_cloud_list_data_in_container(self, container_name):
        pass

    def com_net_cloud_node_list(self):
        return self.driver.list_nodes()

    def com_net_cloud_node_sizes(self):
        return self.driver.list_sizes()
