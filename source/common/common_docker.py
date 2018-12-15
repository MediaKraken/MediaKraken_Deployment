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
import socket
import subprocess

import docker
from . import common_global


# https://docker-py.readthedocs.io/en/stable/

# the following function is used in ALPINE until socket.gethostbyname('host.docker.internal') is valid
def com_docker_host_ip():
    # this doesn't work from a container!  it'll just give the route ip to the host  ie 172.x.x.x
    return subprocess.check_output(['ip', '-4', 'route', 'show', 'default']).decode("utf-8").split(' ')[2]


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
        return self.cli_api.containers()

    def com_docker_container_bind(self, container_name='/mkserver', bind_match='/data/devices'):
        for container_inst in self.com_docker_container_list():
            # common_global.es_inst.com_elastic_index('info', {'container_inst': container_inst})
            if container_inst['Names'][0] == container_name:
                for mount_points in container_inst['Mounts']:
                    if mount_points['Source'].endswith(bind_match):
                        return mount_points['Source'].replace(bind_match, '')

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

    def com_docker_ports_free(self):
        """
        return list of ports in use by docker
        """
        port_list = []
        for container_inst in self.com_docker_container_list():
            for port_ndx in container_inst['Ports']:
                if 'PublicPort' in port_ndx:  # as not all containers have open port
                    port_list.append(port_ndx['PublicPort'])
        return port_list

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
        return self.cli_api.volumes()

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
        try:
            # since the container might not exist (like starting the main_debug.py
            return self.cli_api.remove_container(container=container_image_name,
                                                 force=container_force)
        except:
            pass

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

    def com_docker_network_create(self, network_name='mk_mediakraken_network'):
        """
        create network
        """
        # verify the network doesn't already exist
        if len(self.com_docker_network_list(network_name)) == 0:
            return self.cli.networks.create(name=network_name, driver="bridge")

    def com_docker_network_list(self, network_name='mk_mediakraken_network'):
        return self.cli.networks.list(network_name)

    def com_docker_network_prune(self):
        """
        prune network
        """
        return self.cli.networks.prune()

    def com_docker_run_device_scan(self, current_host_working_directory):
        common_global.es_inst.com_elastic_index('info',
                                                {'path': os.path.join(current_host_working_directory, 'data/devices')})
        self.com_docker_delete_container('mkdevicescan')
        return self.cli.containers.run(image='mediakraken/mkdevicescan',
                                       detach=True,
                                       command='python3 /mediakraken/main_hardware_discover.py',
                                       name='mkdevicescan',
                                       network_mode='host',
                                       volumes={os.path.join(current_host_working_directory, 'data/devices'):
                                                    {'bind': '/mediakraken/devices',
                                                     'mode': 'rw'}
                                                },
                                       environment={'DEBUG': os.environ['DEBUG']},
                                       )

    def com_docker_run_elk(self, current_host_working_directory):
        self.com_docker_delete_container('mkelk')
        self.com_docker_network_create('mk_mediakraken_network')
        return self.cli.containers.run(image='mediakraken/mkelk',
                                       detach=True,
                                       ports={"5044": 5044, "5601": 5601, "9200": 9200},
                                       name='mkelk',
                                       network='mk_mediakraken_network',
                                       volumes={os.path.join(current_host_working_directory, 'data/elk'):
                                                    {'bind': '/var/lib/elasticsearch',
                                                     'mode': 'rw'}
                                                },
                                       environment={'ELASTICSEARCH_START': 1,
                                                    'LOGSTASH_START': 0,
                                                    'KIBANA_START': 1}
                                       )

    def com_docker_run_game_data(self, current_host_working_directory,
                                 container_command='python3 /mediakraken/subprogram_metadata_games.py'):
        """
        Launch container for game data load
        """
        self.com_docker_delete_container('mkgamedata')
        return self.cli.containers.run(image='mediakraken/mkgamedata',
                                       network='mk_mediakraken_network',
                                       command=container_command,
                                       detach=True,
                                       volumes={os.path.join(current_host_working_directory, 'data/emulation'):
                                                    {'bind': '/mediakraken/emulation',
                                                     'mode': 'rw'}
                                                },
                                       environment={'POSTGRES_DB': os.environ['POSTGRES_DB'],
                                                    'POSTGRES_USER': os.environ['POSTGRES_USER'],
                                                    'POSTGRES_PASSWORD': os.environ['POSTGRES_PASSWORD'],
                                                    'DEBUG': os.environ['DEBUG'],
                                                    },
                                       name='mkgamedata')

    def com_docker_run_cast(self, hwaccel, name_container, container_command):
        """
        Launch container for cast play
        """
        # docker run --name waffleboy -it --rm --net host -v /mediakraken/nfsmount:/mediakraken/mnt mediakraken/mkslave castnow
        #  --tomp4 --ffmpeg-acodec ac3 --ffmpeg-movflags frag_keyframe+empty_moov+faststart
        # --address 10.0.0.220 --myip 10.0.0.198 '/mediakraken/mnt/DVD/Creep (2004)/Creep (2004).mkv'
        if hwaccel:
            image_name = 'mediakraken/mkslavenvidiadebian'
        else:
            image_name = 'mediakraken/mkslave'
        # rm - cleanup after exit
        # it - interactive tty
        # container_command = 'docker run -it --rm --net host -v ' \
        #     +  '/mediakraken/nfsmount:/mediakraken/mnt ' \
        #     +  'mediakraken/mkslave ' + container_command)
        return self.cli.containers.run(image=image_name,
                                       network_mode='host',
                                       command=container_command,
                                       detach=True,
                                       volumes={'/var/run/docker.sock':
                                                    {'bind': '/var/run/docker.sock',
                                                     'mode': 'ro'},
                                                '/mediakraken/nfsmount':
                                                    {'bind': '/mediakraken/mnt',
                                                     'mode': 'ro'}
                                                },
                                       name=name_container)

    def com_docker_run_musicbrainz(self, current_host_working_directory, brainzcode):
        self.com_docker_delete_container('mkmusicbrainz')
        return self.cli.containers.run(image='mediakraken/mkmusicbrainz',
                                       detach=True,
                                       name='mkmusicbrainz',
                                       network='mk_mediakraken_network',
                                       ports={"5000": 5000},
                                       environment={'BRAINZCODE': brainzcode},
                                       volumes={os.path.join(current_host_working_directory, 'data/mbrainz/config'):
                                                    {'bind': '/config', 'mode': 'rw'},
                                                os.path.join(current_host_working_directory, 'data/mbrainz/data'):
                                                    {'bind': '/data', 'mode': 'rw'}})

    def com_docker_run_mumble(self, current_host_working_directory):
        self.com_docker_delete_container('mkmumble')
        return self.cli.containers.run(image='mediakraken/mkmumble',
                                       detach=True,
                                       ports={"64738": 64738},
                                       name='mkmumble',
                                       volumes={os.path.join(current_host_working_directory, 'data/mumble'):
                                                    {'bind': '/etc/mumble',
                                                     'mode': 'rw'}
                                                }
                                       )

    def com_docker_run_openldap(self, current_host_working_directory):
        self.com_docker_delete_container('mkopenldap')
        return self.cli.containers.run(image='mediakraken/mkopenldap',
                                       detach=True,
                                       name='mkopenldap',
                                       ports={"389": 389, "636": 636},
                                       volumes={os.path.join(current_host_working_directory, 'data/openldap/conf'):
                                                    {'bind': '/etc/openldap',
                                                     'mode': 'rw'},
                                                os.path.join(current_host_working_directory, 'data/openldap/data'):
                                                    {'bind': '/var/lib/openldap/openldap-data',
                                                     'mode': 'rw'}},
                                       network='mk_mediakraken_network')

    def com_docker_run_pgadmin(self, user_email='spootdev@gmail.com', user_password='metaman'):
        self.com_docker_delete_container('mkpgadmin')
        self.com_docker_network_create('mk_mediakraken_network')
        return self.cli.containers.run(image='mediakraken/mkpgadmin',
                                       detach=True,
                                       name='mkpgadmin',
                                       ports={"5050": 5050},
                                       network='mk_mediakraken_network',
                                       environment={'PGADMIN_DEFAULT_EMAIL': user_email,
                                                    'PGADMIN_DEFAULT_PASSWORD': user_password})

    def com_docker_run_portainer(self, current_host_working_directory):
        self.com_docker_delete_container('mkportainer')
        return self.cli.containers.run(image='portainer/portainer',
                                       detach=True,
                                       name='mkportainer',
                                       ports={"9000": 9000},
                                       volumes={'/var/run/docker.sock':
                                                    {'bind': '/var/run/docker.sock',
                                                     'mode': 'ro'},
                                                os.path.join(current_host_working_directory, 'data/portainer'):
                                                    {'bind': '/ data', 'mode': 'rw'}})

    def com_docker_run_slave(self, hwaccel, port_mapping, name_container, container_command):
        """
        Launch container for slave play
        """
        if hwaccel:
            image_name = 'mediakraken/mkslavenvidiadebian'
        else:
            image_name = 'mediakraken/mkslave'
        self.com_docker_delete_container(image_name.replace('mediakraken/', ''))
        return self.cli.containers.run(image=image_name,
                                       ports=port_mapping,
                                       network='mk_mediakraken_network',
                                       command=container_command,
                                       detach=True,
                                       volumes={'/var/run/docker.sock':
                                                    {'bind': '/var/run/docker.sock',
                                                     'mode': 'ro'},
                                                '/mediakraken/nfsmount':
                                                    {'bind': '/mediakraken/mnt',
                                                     'mode': 'ro'}
                                                },
                                       name=name_container)

    def com_docker_run_teamspeak(self, current_host_working_directory):
        self.com_docker_delete_container('mkteamspeak')
        return self.cli.containers.run(image='mediakraken/mkteamspeak',
                                       ports={"9987/upd": 9987, "10011": 10011,
                                              "30033": 30033},
                                       volumes={os.path.join(current_host_working_directory, 'data/teamspeak/data'):
                                                    {'bind': '/opt/teamspeak',
                                                     'mode': 'rw'},
                                                },
                                       name='mkteamspeak')

    def com_docker_run_transmission(self, current_host_working_directory, username, password):
        """
        run transmission daemon
        """
        self.com_docker_delete_container('mktransmission')
        return self.cli.containers.run(image='mediakraken/mktransmission',
                                       network='mk_mediakraken_network',
                                       detach=True,
                                       ports={"9091": 9091, "51413/tcp": 51413,
                                              "51413/udp": 51413},
                                       command='/start-transmission.sh',
                                       volumes={
                                           os.path.join(current_host_working_directory, 'data/transmission/downloads'):
                                               {'bind': '/transmission/downloads',
                                                'mode': 'rw'},
                                           os.path.join(current_host_working_directory,
                                                        '/data/transmission/incomplete'):
                                               {'bind': '/transmission/incomplete',
                                                'mode': 'rw'}
                                       },
                                       name='mktransmission',
                                       environment={'USERNAME': username,
                                                    'PASSWORD': password})

    def com_docker_run_twitch_record_user(self, twitch_user):
        """
        Launch container for twitch user recording
        """
        return self.cli.containers.run(image='mediakraken/mkslave',
                                       command='python3 check.py ' + twitch_user,
                                       detach=True,
                                       volumes={
                                           '/mediakraken/nfsmount':
                                               {'bind': '/mediakraken/mnt',
                                                'mode': 'rw'}
                                       },
                                       environment={'DEBUG': os.environ['DEBUG']},
                                       name='mktwitchrecorduser_' + twitch_user)

    def com_docker_run_wireshark(self):
        """
        run wireshark
        """
        self.com_docker_delete_container('mkwireshark')
        self.com_docker_network_create('mk_mediakraken_network')
        return self.cli.containers.run(image='mediakraken/mkwireshark',
                                       detach=True,
                                       name='mkwireshark',
                                       ports={"14500": 14500},
                                       cap_add=('NET_ADMIN'),
                                       environment={'XPRA_PW': 'wireshark'})
