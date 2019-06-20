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

import subprocess
import time

from common import common_config_ini
from common import common_docker
from common import common_global
from common import common_logging_elasticsearch
from common import common_signal
from network import network_base_line as network_base
from twisted.internet import reactor, protocol
from twisted.internet import ssl

mk_containers = {}
docker_inst = common_docker.CommonDocker()


class MediaKrakenServerApp(protocol.ServerFactory):
    def __init__(self):
        # set other data
        self.server_start_time = time.mktime(time.gmtime())
        self.users = {}  # maps user names to network instances
        self.option_config_json, self.db_connection = common_config_ini.com_config_read()
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Ready for twisted connections!'})
        for cast_devices in self.db_connection.db_device_list(device_type='cast'):
            common_global.client_devices.append(('cast', cast_devices))
        for cast_devices in self.db_connection.db_device_list(device_type='roku'):
            common_global.client_devices.append(('roku', cast_devices))

    def buildProtocol(self, addr):
        return network_base.NetworkEvents(self.users, self.db_connection)


if __name__ == '__main__':
    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
        'subprogram_reactor_line')
    # set signal exit breaks
    common_signal.com_signal_set_break()

    # start up the pika engine
    subprocess.Popen(['python3', './subprogram_pika.py'], shell=False)

    # setup for the ssl keys
    reactor.listenSSL(8903, MediaKrakenServerApp(),
                      ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
    reactor.run()
