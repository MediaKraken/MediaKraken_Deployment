'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

# data order
# 0 - container_command,
# 1 - container_name,
# 2 - container_image_name='mediakraken/mkslave',
# 3 - container_detach=True,
# 4 - container_port={'5050/tcp': 5050, '5060/tcp': 5060},
# 5 - container_network='mk_mediakraken_network',
# 6 - container_volumes= {'/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
#           '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}}
# 7 - container_remove=True,
# 8 - container_environment=None

DOCKER_DEFAULT = ()

DOCKER_ELK = ()

DOCKER_MUMBLE = ()

DOCKER_MUSICBRAINZ = ()

DOCKER_PORTAINER = ()

DOCKER_PGADMIN = ()

DOCKER_SMTP = ()

DOCKER_TEAMSPEAK = ()

DOCKER_TRANSMISSION = ('/start-transmission.sh',
                       'mktransmission',
                       'mediakraken/mktransmission',
                       True,
                       {"9091": 9091, "51413/tcp": 51413, "51413/udp": 51413},
                       'mk_mediakraken_network',
                       {'/var/opt/mediakraken/transmission/downloads':
                            {'bind': '/transmission/downloads', 'mode': 'rw'},
                        '/var/opt/mediakraken/transmission/incomplete':
                            {'bind': '/transmission/incomplete', 'mode': 'rw'}
                        },
                       True,
                       {'USERNAME': os.environ['TRANSUSER'],
                        'PASSWORD': os.environ['TRANSPASSWORD']}
                       )
