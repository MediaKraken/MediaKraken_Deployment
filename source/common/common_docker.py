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

import os
import socket

import docker

from . import common_global


class CommonDocker(object):
    """
    Class for interfacing with docker
    """

    def __init__(self):
        self.cli = docker.from_env()
        self.cli_api = docker.APIClient(base_url='unix://var/run/docker.sock')

    def com_docker_container_list(self):
        """
        List containers on host
        """
        return self.cli.containers()

    def com_docker_info(self):
        """
        docker info on host
        """
        return self.cli.info()

    def com_docker_port(self, container_id=None, mapped_port=5050):
        """
        pull mapped ports for container
        """
        if container_id is None:
            # docker containers spun up have container id as hostname
            container_id = socket.gethostname()
        return self.cli_api.port(container_id, mapped_port)

    def com_docker_swarm_init(self):
        """
        initialize swarm on host
        """
        if os.environ['SWARMIP'] == 'None':
            try:
                return self.cli_api.init_swarm()
            except:
                common_global.es_inst.com_elastic_index('critical', {'stuff':
                                                                         'Must define Docker Swarm IP in ENV file since multiple IP'})
        else:
            return self.cli_api.init_swarm(advertise_addr=os.environ['SWARMIP'])

    def com_docker_swarm_inspect(self):
        """
        swarm info on host
        """
        return self.cli_api.inspect_swarm()

    def com_docker_swarm_leave(self):
        """
        leave current swarm
        """
        return self.cli_api.leave_swarm()

    def com_docker_node_list(self):
        """
        List nodes in swarm
        """
        return self.cli_api.nodes()

    def com_docker_version(self):
        """
        return docker version on host
        """
        return self.cli.version()

    def com_docker_volume_info(self, volume_name):
        """
        return info no specified volume
        """
        return self.cli.inspect_volume(volume_name)

    def com_docker_volume_remove(self, volume_name):
        """
        remove volume from docker
        """
        return self.cli.remove_volume(volume_name)

    def com_docker_volume_list(self):
        """
        list docker volumes
        """
        return self.cli.volumes()

    def com_docker_run_command(self, container_id, docker_command):
        """
        run command in a container
        """
        return self.cli.exec_run(cmd=docker_command)

    # https://docker-py.readthedocs.io/en/stable/containers.html
    def com_docker_run_container(self, container_data_list):
        """
        Launch container (usually for slave play)
        """
        return self.cli.containers.run(image=container_data_list[2],
                                       network=container_data_list[5],
                                       detach=container_data_list[3],
                                       ports=container_data_list[4],
                                       command=container_data_list[0],
                                       volumes=container_data_list[6],
                                       name=container_data_list[1],
                                       environment=container_data_list[8])
        # auto_remove=container_remove)

    def com_docker_delete_container(self, container_image_name, container_force=True):
        """
        Remove container from disk and term it forcefully if asked
        """
        return self.cli_api.remove_container(container=container_image_name,
                                             force=container_force)

    def com_docker_pause_container(self, container_image_name):
        """
        pause container
        """
        return self.cli_api.pause(container=container_image_name)

    def com_docker_unpause_container(self, container_image_name):
        """
        unpause container
        """
        return self.cli_api.unpause(container=container_image_name)

    def com_docker_network_create(self, network_name):
        """
        create network
        """
        # TODO make sure the network doesn't already exist
        return self.cli.networks.create(name=network_name, driver="bridge")

    def com_docker_network_prune(self):
        """
        prune network
        """
        return self.cli.networks.prune()

    def com_docker_run_device_scan(self):
        return self.cli.containers.run(image='mediakraken/mkdevicescan',
                                       detach=True,
                                       command='python main_hardware_discover.py',
                                       name='mkdevicescan',
                                       network_mode='host')

    def com_docker_run_elk(self):
        return self.cli.containers.run(image='mediakraken/mkelk',
                                       detach=True,
                                       ports={"5044": 5044, "5601": 5601, "9200": 9200},
                                       name='mkelk',
                                       network='mk_mediakraken_network',
                                       volumes={'/var/log/mediakraken/elk':
                                                    {'bind': '/var/lib/elasticsearch',
                                                     'mode': 'rw'}
                                                },
                                       environment={'ELASTICSEARCH_START': 1,
                                                    'LOGSTASH_START': 0,
                                                    'KIBANA_START': 1}
                                       )

    def com_docker_run_musicbrainz(self, brainzcode):
        return self.cli.containers.run(image='mediakraken/mkmusicbrainz',
                                       detach=True,
                                       name='mkmusicbrainz',
                                       network='mk_mediakraken_network',
                                       environment={'BRAINZCODE': brainzcode}
                                       )

    def com_docker_run_mumble(self):
        return self.cli.containers.run(image='mediakraken/mkmumble',
                                       detach=True,
                                       ports={"64738": 64738},
                                       name='mkmumble',
                                       volumes={'/var/opt/mediakraken/mumble':
                                                    {'bind': '/etc/mumble',
                                                     'mode': 'rw'}
                                                }
                                       )

    def com_docker_run_openldap(self):
        return self.cli.containers.run(image='mediakraken/mkopenldap',
                                       detach=True,
                                       name='mkopenldap',
                                       ports={"389": 389, "636": 636},
                                       network='mk_mediakraken_network')

    def com_docker_run_pgadmin(self, user_email, user_password):
        return self.cli.containers.run(image='dpage/pgadmin4',
                                       detach=True,
                                       name='mkpgadmin',
                                       ports={"12345": 80},
                                       network='mk_mediakraken_dbnetwork',
                                       environment={'PGADMIN_DEFAULT_EMAIL': user_email,
                                                    'PGADMIN_DEFAULT_PASSWORD': user_password})

    def com_docker_run_portainer(self):
        return self.cli.containers.run(image='portainer/portainer',
                                       detach=True,
                                       name='mkportainer',
                                       ports={"9000": 9000},
                                       environment={'/var/run/docker.sock':
                                                        {'bind': '/var/run/docker.sock',
                                                         'mode': 'ro'},
                                                    '/var/opt/mediakraken/data':
                                                        {'bind': '/ data', 'mode': 'rw'}})

    def com_docker_run_slave(self, hwaccel, name_container, container_command):
        """
        Launch container for slave play
        """
        if hwaccel:
            image_name = 'mediakraken/mkslavenvidiadebian:latest'
        else:
            image_name = 'mediakraken/mkslave:latest'
        return self.cli.containers.run(container_image_name=image_name,
                                       container_name=name_container,
                                       container_command=container_command)

    def com_docker_run_teamspeak(self):
        return self.cli.containers.run(image='mediakraken/mkteamspeak',
                                       detach=True,
                                       ports={"9987/upd": 9987, "10011": 10011,
                                              "30033": 30033},
                                       volumes={'/var/opt/mediakraken/teamspeak/data':
                                                    {'bind': '/teamspeak/data',
                                                     'mode': 'rw'},
                                                '/var/opt/mediakraken/teamspeak/logs':
                                                    {'bind': '/teamspeak/logs',
                                                     'mode': 'rw'}
                                                },
                                       name='mkteamspeak')

    def com_docker_run_transmission(self, username, password):
        """
        run transmission daemon
        """
        return self.cli.containers.run(image='mediakraken/mktransmission',
                                       network='mk_mediakraken_network',
                                       detach=True,
                                       ports={"9091": 9091, "51413/tcp": 51413, "51413/udp": 51413},
                                       command='/start-transmission.sh',
                                       volumes={'/var/opt/mediakraken/transmission/downloads':
                                                    {'bind': '/transmission/downloads',
                                                     'mode': 'rw'},
                                                '/var/opt/mediakraken/transmission/incomplete':
                                                    {'bind': '/transmission/incomplete',
                                                     'mode': 'rw'}
                                                },
                                       name='mktransmission',
                                       environment={'USERNAME': username,
                                                    'PASSWORD': password})
