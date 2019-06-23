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
import signal
import subprocess
import sys

sys.path.append('.')
from common import common_global
from common import common_network_mediakraken


class TestSubprogramBroadcast:
    """
    Test broadcast
    """

    def __init__(self):
        """
        Class init
        """
        self.proc_broadcast = None

    @classmethod
    def setup_class(self):
        # fire up broadcast server
        self.proc_broadcast = subprocess.Popen(['python3', './subprogram_broadcast.py'],
                                               shell=False)
        common_global.es_inst.com_elastic_index('info',
                                                {'stuff': "PID: %s" % self.proc_broadcast.pid})

    @classmethod
    def teardown_class(self):
        os.kill(self.proc_broadcast.pid, signal.SIGTERM)

    def test_sub_broadcast(self):
        """
        Test function
        """
        common_network_mediakraken.com_net_mediakraken_find_server()
