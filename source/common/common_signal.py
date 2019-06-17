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

import signal
import sys

import os

from . import common_global


def com_signal_receive(signum, frame):  # pylint: disable=W0613
    """
    Handle signal interrupt
    """
    common_global.es_inst.com_elastic_index('info', {'stuff': 'Application: Received USR1'})
    if common_global.pid_dict is not None:
        # term all running pids
        for pid_data in common_global.pid_dict:
            os.kill(common_global.pid_dict[pid_data], signal.SIGTERM)
    sys.stdout.flush()
    sys.exit(0)


def com_signal_set_break():
    # set signal breaks
    if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
        # ctrl-c # pylint: disable=E1101
        signal.signal(signal.SIGBREAK, com_signal_receive)
    else:
        signal.signal(signal.SIGTSTP, com_signal_receive)  # ctrl-z
        signal.signal(signal.SIGUSR1, com_signal_receive)  # ctrl-c
        signal.signal(signal.SIGTERM, com_signal_receive)
