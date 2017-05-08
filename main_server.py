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
from common import common_network_share
from common import common_signal
#from common import common_watchdog
from common import common_version
#rmda_enabled_os = False
#try:
#    from common import common_rmda
#    rmda_enabled_os = True
#except:
#    pass

# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start()


logging.info('PATH: %s' % os.environ['PATH'])
#os.environ['PATH'] += ":./"
#logging.info(os.environ['PATH'])


logging.info('Check Certs')
# check for and create ssl certs if needed
if not os.path.isfile('./key/cacert.pem'):
    logging.info('Cert not found, generating.')
    proc_ssl = subprocess.Popen(['python', './subprogram_ssl_keygen.py'], shell=False)
    proc_ssl.wait()
    if not os.path.isfile('./key/cacert.pem'):
        logging.critical("Cannot generate SSL certificate. Exiting.....")
        sys.exit()


logging.info("Open DB")
# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


db_connection.db_activity_insert('MediaKraken_Server Start', None, 'System: Server Start',
                                 'ServerStart', None, None, 'System')


# check db version
if db_connection.db_version_check() != common_version.DB_VERSION:
    logging.info('Database upgrade in progress...')
    db_create_pid = subprocess.Popen(['python', './db_update_version.py'], shell=False)
    db_create_pid.wait()
    logging.info('Database upgrade complete.')


# mount all the shares first so paths exist for validation
common_network_share.com_net_share_mount(db_connection.db_audit_shares())


logging.info("Validate Paths")
# validate paths in ini file
# keep the checks split so user can be told which one is wrong
#if not os.path.isdir(option_config_json['MediaKrakenServer']['MetadataImageLocal']):
#    logging.critical("MediaKrakenServer/MetadataImageLocal is not a valid directory!  Exiting...")
#    logging.critical("Invalid Path: %s" %
#        option_config_json['MediaKrakenServer']['MetadataImageLocal'])
#    sys.exit()
if not os.path.isdir(option_config_json['MediaKrakenServer']['BackupLocal']):
    logging.critical("MediaKrakenServer/BackupLocal is not a valid directory!  Exiting...")
    logging.critical("Invalid Path: %s" %\
        option_config_json['MediaKrakenServer']['BackupLocal'])
    sys.exit()


## look for infiniband rdma devices
#if rmda_enabled_os:
#    rmda_devices = common_rmda.com_rdma_get_devices()
#    if rmda_devices is None:
#        rmda_enabled_os = False


#logging.info("Start Watchdog")
## startup watchdog
#watchdog = common_watchdog.CommonWatchdog()
#watchdog.com_watchdog_start(db_connection.db_audit_paths(None, None))


# startup the other reactor via popen as it's non-blocking
proc = subprocess.Popen(['python', './subprogram_reactor.py'], shell=False)
logging.info("Reactor PID: %s", proc.pid)


## fire up web image server
#proc_image = subprocess.Popen(['python', './subprogram_reactor_web_images.py'], shell=False)
#logging.info("Reactor Web Image PID: %s", proc_image.pid)


# fire up cron service
proc_cron = subprocess.Popen(['python', './subprogram_cron_checker.py'], shell=False)
logging.info("Cron PID: %s", proc_cron.pid)


# fire up trigger procress
proc_trigger = subprocess.Popen(['python', './main_server_trigger.py'], shell=False)
logging.info("Trigger PID: %s", proc_trigger.pid)


# fire up link servers
link_pid = {}
for link_data in db_connection.db_link_list():
    proc_link = subprocess.Popen(['python', './main_server_link.py', link_data[2]['IP'],
        str(link_data[2]['Port'])], shell=False)
    logging.info("Link PID: %s", proc_link.pid)
    link_pid[link_data[0]] = proc_link.pid


## hold here
# this will key off the twisted reactor...only reason is so watchdog doesn't shut down
proc.wait()


## stop watchdog
#watchdog.com_watchdog_stop()


# log stop
db_connection.db_activity_insert('MediaKraken_Server Stop', None, 'System: Server Stop',
                                 'ServerStop', None, None, 'System')


# commit
db_connection.db_commit()


# close the database
db_connection.db_close()


# stop children
os.kill(proc.pid, signal.SIGTERM)
#os.kill(proc_image.pid, signal.SIGTERM)
os.kill(proc_cron.pid, signal.SIGTERM)
os.kill(proc_trigger.pid, signal.SIGTERM)
for link_data in link_pid.keys():
    os.kill(link_pid[link_data], signal.SIGTERM)
