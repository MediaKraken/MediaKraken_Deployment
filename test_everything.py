'''
  Copyright (C) 2019 Quinn D Granfor <spootdev@gmail.com>

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
import shlex
import subprocess
import sys
import time

from dotenv import load_dotenv

from common import common_docker_images
from common import common_network_email

# load .env stats
load_dotenv()

CWD_HOME_DIRECTORY = os.getcwd().rsplit('MediaKraken_CI', 1)[0]
print(CWD_HOME_DIRECTORY, flush=True)

#####################################
# lint and validate code
#####################################


# run radon to determine code complexity
try:
    pid_proc = subprocess.Popen(
        shlex.split('radon cc %s' % os.path.join(CWD_HOME_DIRECTORY, 'MediaKraken_Deployment')),
        stdout=subprocess.PIPE, shell=False)
except subprocess.CalledProcessError as e:
    print(e.output, flush=True)
    sys.exit()
email_body = ''
try:
    while True:
        line = pid_proc.stdout.readline()
        if not line:
            break
        email_body += line.decode("utf-8")
        print(line.rstrip(), flush=True)
    pid_proc.wait()
except:
    pass
common_network_email.com_net_send_email(os.environ['MAILUSER'], os.environ['MAILPASS'],
                                        os.environ['MAILUSER'],
                                        'Radon (Code Complexity)',
                                        email_body,
                                        smtp_server=os.environ['MAILSERVER'],
                                        smtp_port=os.environ['MAILPORT'])

# run pytype to run type checking
try:
    pid_proc = subprocess.Popen(
        shlex.split('pytype %s' % os.path.join(CWD_HOME_DIRECTORY, 'MediaKraken_Deployment')),
        stdout=subprocess.PIPE, shell=False)
except subprocess.CalledProcessError as e:
    print(e.output, flush=True)
    sys.exit()
email_body = ''
try:
    while True:
        line = pid_proc.stdout.readline()
        if not line:
            break
        email_body += line.decode("utf-8")
        print(line.rstrip(), flush=True)
    pid_proc.wait()
except:
    pass
common_network_email.com_net_send_email(os.environ['MAILUSER'], os.environ['MAILPASS'],
                                        os.environ['MAILUSER'],
                                        'Pytype (Type Checking)',
                                        email_body,
                                        smtp_server=os.environ['MAILSERVER'],
                                        smtp_port=os.environ['MAILPORT'])

# run pylama to code quality
try:
    pid_proc = subprocess.Popen(
        shlex.split('pylama %s' % os.path.join(CWD_HOME_DIRECTORY, 'MediaKraken_Deployment')),
        stdout=subprocess.PIPE, shell=False)
except subprocess.CalledProcessError as e:
    print(e.output, flush=True)
    sys.exit()
email_body = ''
try:
    while True:
        line = pid_proc.stdout.readline()
        if not line:
            break
        email_body += line.decode("utf-8")
        print(line.rstrip(), flush=True)
    pid_proc.wait()
except:
    pass
common_network_email.com_net_send_email(os.environ['MAILUSER'], os.environ['MAILPASS'],
                                        os.environ['MAILUSER'],
                                        'Pylama (Code Quality)',
                                        email_body,
                                        smtp_server=os.environ['MAILSERVER'],
                                        smtp_port=os.environ['MAILPORT'])

#####################################
# docker container scanning
#####################################


# change dir for clair scanner
os.chdir(os.path.join(CWD_HOME_DIRECTORY, 'MediaKraken_CI', 'docker/clair/'))
for build_stages in (common_docker_images.STAGE_ONE_IMAGES,
                     common_docker_images.STAGE_TWO_IMAGES,
                     common_docker_images.STAGE_COMPOSE_IMAGES,
                     common_docker_images.STAGE_ONE_FS,
                     common_docker_images.STAGE_ONE_GAME_SERVERS,
                     common_docker_images.STAGE_TWO_GAME_SERVERS):
    for docker_images in build_stages:
        # Run Clair on each image
        try:
            pid_proc = subprocess.Popen(
                shlex.split('docker-compose run --rm clair-scanner %s/mediakraken/%s:dev' %
                            (common_docker_images.DOCKER_REPOSITORY,
                             build_stages[docker_images][0])),
                stdout=subprocess.PIPE, shell=False)
        except subprocess.CalledProcessError as e:
            print(e.output, flush=True)
            sys.exit()
        email_body = ''
        try:
            while True:
                line = pid_proc.stdout.readline()
                if not line:
                    break
                email_body += line.decode("utf-8")
                print(line.rstrip(), flush=True)
            pid_proc.wait()
        except:
            pass
        common_network_email.com_net_send_email(os.environ['MAILUSER'], os.environ['MAILPASS'],
                                                os.environ['MAILUSER'],
                                                'Clair image: '
                                                + build_stages[docker_images][0],
                                                email_body,
                                                smtp_server=os.environ['MAILSERVER'],
                                                smtp_port=os.environ['MAILPORT'])

# TODO the exec below isn't right, might need to talk to seperate server
# # change dir for anchore scanner
# os.chdir(os.path.join(CWD_HOME_DIRECTORY, 'MediaKraken_CI', 'docker/anchore/'))
# for build_stages in (common_docker_images.STAGE_ONE_IMAGES,
#                      common_docker_images.STAGE_TWO_IMAGES,
#                      common_docker_images.STAGE_COMPOSE_IMAGES,
#                      common_docker_images.STAGE_ONE_FS,
#                      common_docker_images.STAGE_ONE_GAME_SERVERS,
#                      common_docker_images.STAGE_TWO_GAME_SERVERS):
#     for docker_images in build_stages:
#         # Run anchore on each image
#         try:
#             pid_proc = subprocess.Popen(
#                 shlex.split('docker-compose exec engine-api anchore-cli image vuln'
#                             ' %s/mediakraken/%s:dev all' %
#                             (common_docker_images.DOCKER_REPOSITORY,
#                              build_stages[docker_images][0])),
#                 stdout=subprocess.PIPE, shell=False)
#         except subprocess.CalledProcessError as e:
#             print(e.output, flush=True)
#             sys.exit()
#         email_body = ''
#         try:
#             while True:
#                 line = pid_proc.stdout.readline()
#                 if not line:
#                     break
#                 email_body += line.decode("utf-8")
#                 print(line.rstrip(), flush=True)
#             pid_proc.wait()
#         except:
#             pass
#         common_network_email.com_net_send_email(os.environ['MAILUSER'], os.environ['MAILPASS'],
#                                                 os.environ['MAILUSER'],
#                                                 'Anchore image scan: '
#                                                 + build_stages[docker_images][0],
#                                                 email_body,
#                                                 smtp_server=os.environ['MAILSERVER'],
#                                                 smtp_port=os.environ['MAILPORT'])



# run docker-bench on all images as it checks for common best practices
os.chdir(os.path.join(CWD_HOME_DIRECTORY, 'MediaKraken_CI', 'source'))
pid_proc = subprocess.Popen(shlex.split('./bench.sh'),
                            stdout=subprocess.PIPE, shell=False)
email_body = ''
while True:
    line = pid_proc.stdout.readline()
    if not line:
        break
    email_body += line.decode("utf-8")
    print(line.rstrip(), flush=True)
pid_proc.wait()
common_network_email.com_net_send_email(os.environ['MAILUSER'], os.environ['MAILPASS'],
                                        os.environ['MAILUSER'],
                                        'Docker Bench', email_body,
                                        smtp_server=os.environ['MAILSERVER'],
                                        smtp_port=os.environ['MAILPORT'])

# # run under started app as need the db connection
# # TODO that won't work.....as it's a docker db
# pytest_pid = subprocess.Popen(shlex.split(
#     'python3 -m pytest --capture=no testing/test_common/test_common_network_youtube.py'))
# pytest_pid.wait()

#####################################
# run application web test/etc
#####################################



# Test the SSL security of the ssl setup via testssl.sh
pid_proc = subprocess.Popen(shlex.split('docker run -ti %s/mediakraken/mktestssl:dev localhost:8900'
                                        % (common_docker_images.DOCKER_REPOSITORY,)),
                            stdout=subprocess.PIPE, shell=False)
email_body = ''
while True:
    line = pid_proc.stdout.readline()
    if not line:
        break
    email_body += line.decode("utf-8")
    print(line.rstrip(), flush=True)
pid_proc.wait()
common_network_email.com_net_send_email(os.environ['MAILUSER'], os.environ['MAILPASS'],
                                        os.environ['MAILUSER'],
                                        'TestSSL', email_body,
                                        smtp_server=os.environ['MAILSERVER'],
                                        smtp_port=os.environ['MAILPORT'])



# run sitadel web security scanner
pid_proc = subprocess.Popen(shlex.split('docker run -ti %s/mediakraken/mksitadel:dev '
                                        'localhost:8900'
                                        % (common_docker_images.DOCKER_REPOSITORY,)),
                            stdout=subprocess.PIPE, shell=False)
email_body = ''
while True:
    line = pid_proc.stdout.readline()
    if not line:
        break
    email_body += line.decode("utf-8")
    print(line.rstrip(), flush=True)
pid_proc.wait()
common_network_email.com_net_send_email(os.environ['MAILUSER'], os.environ['MAILPASS'],
                                        os.environ['MAILUSER'],
                                        'sitadel', email_body,
                                        smtp_server=os.environ['MAILSERVER'],
                                        smtp_port=os.environ['MAILPORT'])

