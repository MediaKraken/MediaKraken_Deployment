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
import logging  # pylint: disable=W0611
import sys
import subprocess
import os
from common import common_config_ini
from common import common_docker
from common import common_logging_elasticsearch
from common import common_network_share
from common import common_version

# start logging
common_logging.com_logging_start()

logging.info('PATH: %s' % os.environ['PATH'])

logging.info('Check Certs')
# check for and create ssl certs if needed
if not os.path.isfile('./key/cacert.pem'):
    logging.info('Cert not found, generating.')
    proc_ssl = subprocess.Popen(
        ['python', './subprogram_ssl_keygen.py'], shell=False)
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
    db_create_pid = subprocess.Popen(
        ['python', './db_update_version.py'], shell=False)
    db_create_pid.wait()
    logging.info('Database upgrade complete.')

# setup the docker environment
docker_inst = common_docker.CommonDocker()
# check for swarm id (should already be master then)
docker_info = docker_inst.com_docker_info()
if ('Managers' in docker_info['Swarm'] and docker_info['Swarm']['Managers'] == 0) \
        or 'Managers' not in docker_info['Swarm']:
    logging.info('attempting to init swarm as manager')
    # init host to swarm mode
    docker_inst.com_docker_swarm_init()

# mount all the shares first so paths exist for validation
common_network_share.com_net_share_mount(db_connection.db_audit_shares())

logging.info("Validate Paths")
# validate paths in ini file
if not os.path.isdir(option_config_json['MediaKrakenServer']['BackupLocal']):
    logging.critical(
        "MediaKrakenServer/BackupLocal is not a valid directory!  Exiting...")
    logging.critical("Invalid Path: %s" %
                     option_config_json['MediaKrakenServer']['BackupLocal'])
    sys.exit()

# startup the other reactor via popen as it's non-blocking
proc = subprocess.Popen(
    ['python', './subprogram_reactor_line.py'], shell=False)
logging.info("Reactor PID: %s", proc.pid)

# fire up cron service
proc_cron = subprocess.Popen(
    ['python', './subprogram_cron_checker.py'], shell=False)
logging.info("Cron PID: %s", proc_cron.pid)

# fire up link servers
link_pid = {}
for link_data in db_connection.db_link_list():
    proc_link = subprocess.Popen(['python', './main_server_link.py', link_data[2]['IP'],
                                  str(link_data[2]['Port'])], shell=False)
    logging.info("Link PID: %s", proc_link.pid)
    link_pid[link_data[0]] = proc_link.pid

# hold here
# this will key off the twisted reactor...only reason is so watchdog doesn't shut down
proc.wait()

# log stop
db_connection.db_activity_insert('MediaKraken_Server Stop', None, 'System: Server Stop',
                                 'ServerStop', None, None, 'System')

# commit
db_connection.db_commit()

# close the database
db_connection.db_close()
