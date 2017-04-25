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
import logging # pylint: disable=W0611
import sys
import subprocess
import signal
import os
from common import common_logging
from common import common_signal


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start()


logging.info('Check Certs')
# check for and create ssl certs if needed
if not os.path.isfile('./key/cacert.pem'):
    proc_ssl = subprocess.Popen(['subprogram_ssl_keygen'], shell=False)
    proc_ssl.wait()
    if not os.path.isfile('./key/cacert.pem'):
        logging.critical("Cannot generate SSL certificate. Exiting.....")
        sys.exit()


# startup the other reactor via popen as it's non-blocking
proc = subprocess.Popen(['subprogram_reactor_string_weblog'], shell=False)
logging.info("Reactor PID: %s", proc.pid)


# fire up uwsgi server
proc_web_app = subprocess.Popen(['uwsgi', '--socket', '0.0.0.0:8081', '--protocol', 'http',
        '--chdir=./server/web_log', '--ini', './server/web_log/weblog_uwsgi.ini'],
        shell=False)


# hold here
proc_web_app.wait()


# stop children
os.kill(proc.pid, signal.SIGTERM)
os.kill(proc_web_app.pid, signal.SIGTERM)
