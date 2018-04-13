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

import os
import subprocess
import sys

from common import common_config_ini
from common import common_docker
from common import common_global
from common import common_logging_elasticsearch
from common import common_network_share
from common import common_version

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_server')

common_global.es_inst.com_elastic_index('info', {'PATH': os.environ['PATH']})

# check for and create ssl certs if needed
if not os.path.isfile('./key/cacert.pem'):
    common_global.es_inst.com_elastic_index('info', {'stuff': 'Cert not found, generating.'})
    proc_ssl = subprocess.Popen(
        ['python', './subprogram_ssl_keygen.py'], shell=False)
    proc_ssl.wait()
    if not os.path.isfile('./key/cacert.pem'):
        common_global.es_inst.com_elastic_index('critical',
                                                    {
                                                        'stuff': 'Cannot generate SSL certificate. Exiting.....'})
        sys.exit()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# check db version
if db_connection.db_version_check() != common_version.DB_VERSION:
    common_global.es_inst.com_elastic_index('info',
                                                {'stuff': 'Database upgrade in progress...'})
    db_create_pid = subprocess.Popen(
        ['python', './db_update_version.py'], shell=False)
    db_create_pid.wait()
    common_global.es_inst.com_elastic_index('info', {'stuff': 'Database upgrade complete.'})

# setup the docker environment
docker_inst = common_docker.CommonDocker()
# check for swarm id (should already be master then)
docker_info = docker_inst.com_docker_info()
if ('Managers' in docker_info['Swarm'] and docker_info['Swarm']['Managers'] == 0) \
        or 'Managers' not in docker_info['Swarm']:
    common_global.es_inst.com_elastic_index('info',
                                                {'stuff': 'attempting to init swarm as manager'})
    # init host to swarm mode
    docker_inst.com_docker_swarm_init()

# mount all the shares first so paths exist for validation
common_network_share.com_net_share_mount(db_connection.db_audit_shares())

common_global.es_inst.com_elastic_index('info', {'stuff': 'Validate Paths'})
# validate paths in ini file
if not os.path.isdir(option_config_json['MediaKrakenServer']['BackupLocal']):
    common_global.es_inst.com_elastic_index('critical',
                                                {'Backup Dir': 'MediaKrakenServer/BackupLocal is '
                                                               'not a valid directory!  Exiting...'})
    common_global.es_inst.com_elastic_index('critical', {
            'Invalid Path': option_config_json['MediaKrakenServer']['BackupLocal']})
    sys.exit()

# startup the other reactor via popen as it's non-blocking
proc = subprocess.Popen(
    ['python', './subprogram_reactor_line.py'], shell=False)
common_global.es_inst.com_elastic_index('info', {'Reactor PID': proc.pid})

# fire up cron service
proc_cron = subprocess.Popen(
    ['python', './subprogram_cron_checker.py'], shell=False)
common_global.es_inst.com_elastic_index('info', {'Cron PID': proc_cron.pid})

# fire up link servers
link_pid = {}
for link_data in db_connection.db_link_list():
    proc_link = subprocess.Popen(['python', './main_server_link.py', link_data[2]['IP'],
                                  str(link_data[2]['Port'])], shell=False)
    common_global.es_inst.com_elastic_index('info', {'Link PID': proc_link.pid})
    link_pid[link_data[0]] = proc_link.pid

# start up other docker containers if needed
if option_config_json['Docker Instances']['mumble']:
    docker_inst.com_docker_run_mumble()

if option_config_json['Docker Instances']['musicbrainz']:
    docker_inst.com_docker_run_musicbrainz(option_config_json['API']['mediabrainz'])

if option_config_json['Docker Instances']['portainer']:
    docker_inst.com_docker_run_portainer()

# if option_config_json['Docker Instances']['smtp']:
#     docker_inst.com_docker_run_container()

if option_config_json['Docker Instances']['teamspeak']:
    docker_inst.com_docker_run_teamspeak()

if option_config_json['Docker Instances']['transmission']:
    docker_inst.com_docker_run_transmission(option_config_json['Transmission']['Username'],
                                            option_config_json['Transmission']['Password'])

# hold here
# this will key off the twisted reactor...only reason is so watchdog doesn't shut down
proc.wait()

# commit
db_connection.db_commit()

# close the database
db_connection.db_close()
