"""
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
"""

import json
import os
import subprocess
import sys
import time

from common import common_config_ini
from common import common_docker
from common import common_file
from common import common_hash
from common import common_logging_elasticsearch_httpx
from common import common_network_share
from common import common_signal
from common import common_version

# start logging
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='START',
                                                     index_name='main_server')

# set signal exit breaks
common_signal.com_signal_set_break()

common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'PATH': os.environ['PATH']})

# check for and create ssl certs if needed
if not os.path.isfile('./key/cacert.pem'):
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        'stuff': 'Cert not found, generating.'})
    proc_ssl = subprocess.Popen(['python3', './subprogram_ssl_keygen.py'], stdout=subprocess.PIPE,
                                shell=False)
    proc_ssl.wait()
    if not os.path.isfile('./key/cacert.pem'):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='critical', message_text=
        {
            'stuff': 'Cannot generate SSL certificate. Exiting.....'})
        sys.exit()

# create crypto keys if needed
if not os.path.isfile('./secure/data.zip'):
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        'stuff': 'data.zip not found, generating.'})
    data = common_hash.CommonHashCrypto()
    if not os.path.isfile('./secure/data.zip'):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='critical', message_text=
        {
            'stuff': 'Cannot generate crypto. Exiting.....'})
        sys.exit()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# check db version
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
    'db1': db_connection.db_version_check()})
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
    'db2': common_version.DB_VERSION})
if db_connection.db_version_check() != common_version.DB_VERSION:
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
    {'stuff': 'Database upgrade in progress...'})
    db_create_pid = subprocess.Popen(['python3', './db_update_version.py'], stdout=subprocess.PIPE,
                                     shell=False)
    db_create_pid.wait()
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        'stuff': 'Database upgrade complete.'})

# setup the docker environment
docker_inst = common_docker.CommonDocker()
# check for swarm id (should already be master then)
docker_info = docker_inst.com_docker_info()
if ('Managers' in docker_info['Swarm'] and docker_info['Swarm']['Managers'] == 0) \
        or 'Managers' not in docker_info['Swarm']:
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
    {'stuff': 'attempting to init swarm as manager'})
    # init host to swarm mode
    docker_inst.com_docker_swarm_init()

# mount all the shares first so paths exist for validation
common_network_share.com_net_share_mount(db_connection.db_audit_shares())

# fire up link servers
link_pid = {}
for link_data in db_connection.db_link_list():
    proc_link = subprocess.Popen(['python3', './main_server_link.py', link_data[2]['IP'],
                                  str(link_data[2]['Port'])], stdout=subprocess.PIPE, shell=False)
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text={'Link PID': proc_link.pid})
    link_pid[link_data[0]] = proc_link.pid

# get current working directory from host maps
# this is used so ./data can be used for all the containers launched from docker-py
current_host_working_directory = docker_inst.com_docker_container_bind(container_name='/mkserver',
                                                                       bind_match='/data/devices')

# start up other docker containers if needed
if option_config_json['Docker Instances']['elk']:
    docker_inst.com_docker_run_elk(current_host_working_directory)

if option_config_json['Docker Instances']['mumble']:
    docker_inst.com_docker_run_mumble(current_host_working_directory)

if option_config_json['Docker Instances']['musicbrainz'] \
        and option_config_json['API']['musicbrainz'] is not None:
    docker_inst.com_docker_run_musicbrainz(current_host_working_directory,
                                           option_config_json['API']['musicbrainz'])

if option_config_json['Docker Instances']['pgadmin']:
    docker_inst.com_docker_run_pgadmin(current_host_working_directory)

# if option_config_json['Docker Instances']['smtp']:
#     docker_inst.com_docker_run_container()

if option_config_json['Docker Instances']['teamspeak']:
    docker_inst.com_docker_run_teamspeak(current_host_working_directory)

if option_config_json['Docker Instances']['transmission']:
    docker_inst.com_docker_run_transmission(current_host_working_directory,
                                            option_config_json['Transmission']['Username'],
                                            option_config_json['Transmission']['Password'])

if option_config_json['Docker Instances']['wireshark']:
    docker_inst.com_docker_run_wireshark()

# fire off the hardware scanner
docker_inst.com_docker_run_device_scan(current_host_working_directory)

# sleep for minute so hardware scan has time to run
time.sleep(60)
if os.path.exists('/mediakraken/devices/device_scan.txt'):
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        'hardware_device': 'file exists'})
    for hardware_device in common_file.com_file_load_data(
            file_name='/mediakraken/devices/device_scan.txt', as_pickle=True):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'hardware_device': hardware_device})
        if 'Chromecast' in hardware_device:
            db_connection.db_device_upsert(device_type='Chromecast',
                                           device_json=json.dumps(hardware_device))
        elif 'DLNA' in hardware_device:
            db_connection.db_device_upsert(device_type='DLNA',
                                           device_json=json.dumps(hardware_device))
        elif 'HDHomeRun' in hardware_device:
            db_connection.db_device_upsert(device_type='HDHomeRun',
                                           device_json=json.dumps(hardware_device))
        elif 'Phue' in hardware_device:
            db_connection.db_device_upsert(device_type='Phue',
                                           device_json=json.dumps(hardware_device))
        elif 'Roku' in hardware_device:
            db_connection.db_device_upsert(device_type='Roku',
                                           device_json=json.dumps(hardware_device))
        elif 'Soco' in hardware_device:
            db_connection.db_device_upsert(device_type='Soco',
                                           device_json=json.dumps(hardware_device))
    os.remove('/mediakraken/devices/device_scan.txt')
else:
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='error',
                                                         message_text={'no device_scan file found'})

# commit
db_connection.db_commit()

# close the database
db_connection.db_close()
