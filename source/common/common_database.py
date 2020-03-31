import os
import time

from . import common_docker


def com_database_backup():
    # generate file name
    backup_file_name = 'MediaKraken_Database_Backup_' + \
                       time.strftime("%Y%m%d%H%M%S") + '.dump'
    print('docker', flush=True)
    # create backup command
    docker_command_to_exec = '/bin/sh -c \'PGPASSWORD=' + os.environ[
        'POSTGRES_PASSWORD'] + ' pg_dump -h mkstack_database -U postgres postgres -F c -f ' \
                             + os.path.join('/mediakraken/backup', backup_file_name) + '\''
    # setup docker connection
    print(docker_command_to_exec, flush=True)
    docker_inst = common_docker.CommonDocker()
    # run command to backup against the database
    docker_id = docker_inst.com_docker_container_id_by_name('/mkstack_database')
    print(type(docker_id), flush=True)
    exec_instance = docker_inst.com_docker_run_command_via_exec(docker_id, docker_command_to_exec)
    print(exec_instance, flush=True)
    # set to false so not a generator for output
    docker_output = docker_inst.com_docker_start_exec(exec_instance['Id'], stream_output=False)
    print(docker_output, flush=True)


def com_database_restore(restore_image_name):
    # create restore command
    docker_command_to_exec = '/bin/sh -c \'PGPASSWORD=' + os.environ[
        'POSTGRES_PASSWORD'] + ' psql -U postgres postgres < ' + restore_image_name + '\''
    # setup docker connection
    docker_inst = common_docker.CommonDocker()
    # run command to backup against the database
    exec_instance = docker_inst.com_docker_run_command_via_exec(
        docker_inst.com_docker_container_id_by_name('/mkstack_database'), docker_command_to_exec)
    # set to false so not a generator for output
    docker_output = docker_inst.com_docker_start_exec(exec_instance['Id'], stream_output=False)
    print(docker_output, flush=True)
