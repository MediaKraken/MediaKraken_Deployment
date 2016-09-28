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
import logging # pylint: disable=W0611
import sys
import subprocess
import signal
import os
from common import common_config_ini
from common import common_logging
from common import common_signal
from common import common_watchdog
rmda_enabled_os = False
try:
    from common import common_rmda
    rmda_enabled_os = True
except:
    pass


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


logging.info("Open DB")
# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


logging.info("Validate Paths")
# validate paths in ini file
# keep the checks split so user can be told which one is wrong
if not os.path.isdir(option_config_json['MediaKrakenServer']['MetadataImageLocal']):
    logging.critical("MediaKrakenServer/MetadataImageLocal is not a valid directory!  Exiting...")
    logging.critical("Invalid Path: %s" %\
        option_config_json['MediaKrakenServer']['MetadataImageLocal'])
    sys.exit()
if not os.path.isdir(option_config_json['MediaKrakenServer']['BackupLocal']):
    logging.critical("MediaKrakenServer/BackupLocal is not a valid directory!  Exiting...")
    logging.critical("Invalid Path: %s" %\
        option_config_json['MediaKrakenServer']['BackupLocal'])
    sys.exit()


db_connection.db_activity_insert('MediaKraken_Server Start', None, 'System: Server Start',\
                                 'ServerStart', None, None, 'System')


# look for infiniband rdma devices
if rmda_enabled_os:
    rmda_devices = common_rmda.com_rdma_get_devices()
    if rmda_devices is None:
        rmda_enabled_os = False


logging.info("Start Watchdog")
# startup watchdog
watchdog = common_watchdog.CommonWatchdog()
watchdog.com_watchdog_start(db_connection.db_audit_paths(None, None))


# startup the other reactor via popen as it's non-blocking
proc = subprocess.Popen(['subprogram_reactor_string'], shell=False)
logging.info("Reactor PID: %s", proc.pid)


# fire up web image server
proc_image = subprocess.Popen(['subprogram_reactor_web_images'], shell=False)
logging.info("Reactor Web Image PID: %s", proc_image.pid)


# fire up broadcast server
proc_broadcast = subprocess.Popen(['subprogram_broadcast'], shell=False)
logging.info("Broadcast PID: %s", proc_broadcast.pid)


# fire up cron service
proc_cron = subprocess.Popen(['subprogram_cron_checker'], shell=False)
logging.info("Cron PID: %s", proc_cron.pid)


# fire up ffserver
proc_ffserver = subprocess.Popen(['./bin/ffserver', '-f', './conf/ffserver.conf'], shell=False)
logging.info("FFServer PID: %s", proc_ffserver.pid)


# fire up trigger procress
proc_trigger = subprocess.Popen(['main_server_trigger'], shell=False)
logging.info("Trigger PID: %s", proc_trigger.pid)


# fire up api server
proc_api = subprocess.Popen(['main_server_api'], shell=False)
logging.info("API PID: %s", proc_api.pid)


# fire up link servers
link_pid = {}
for link_data in db_connection.db_link_list():
    proc_link = subprocess.Popen(['main_server_link', link_data[2]['IP'],\
        str(link_data[2]['Port'])], shell=False)
    logging.info("Link PID: %s", proc_link.pid)
    link_pid[link_data[0]] = proc_link.pid


# fire up uwsgi server
proc_web_app = subprocess.Popen(['uwsgi', '--socket', '0.0.0.0:8080', '--protocol', 'http',\
                                 '--chdir=./web_app', '--ini', './web_app/mediakraken_uwsgi.ini'],\
                                 shell=False)


# hold here
proc_web_app.wait()


# stop watchdog
watchdog.com_watchdog_stop()


# log stop
db_connection.db_activity_insert('MediaKraken_Server Stop', None, 'System: Server Stop',\
                                 'ServerStop', None, None, 'System')

# commit
db_connection.db_commit()


# close the database
db_connection.db_close()


# stop children
os.kill(proc.pid, signal.SIGTERM)
os.kill(proc_image.pid, signal.SIGTERM)
os.kill(proc_broadcast.pid, signal.SIGTERM)
os.kill(proc_cron.pid, signal.SIGTERM)
os.kill(proc_ffserver.pid, signal.SIGTERM)
os.kill(proc_web_app.pid, signal.SIGTERM)
os.kill(proc_trigger, signal.SIGTERM)
os.kill(proc_api, signal.SIGTERM)
for link_data in link_pid.keys():
    os.kill(link_pid[link_data], signal.SIGTERM)
