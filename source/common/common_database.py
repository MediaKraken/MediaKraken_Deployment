import os
import time

from . import common_docker


def com_database_backup():
    # generate file name
    backup_file_name = 'MediaKraken_Database_Backup_' + \
                       time.strftime("%Y%m%d%H%M%S") + '.dump'
    print('docker', flush=True)
    # create backup command
    docker_command_to_exec = 'PGPASSWORD=' + os.environ[
        'POSTGRES_PASSWORD'] + ' pg_dump -h mkstack_database -U postgres postgres -F c -f ' \
                             + os.path.join('/mediakraken/backup', backup_file_name)
    # setup docker connection
    print(docker_command_to_exec, flush=True)
    docker_inst = common_docker.CommonDocker()
    # run command to backup against the database
    docker_inst.com_docker_run_command_via_exec(
        container_id=docker_inst.com_docker_container_id_by_name(
            container_name='/mkstack_database'),
        docker_command=docker_command_to_exec)


def com_database_restore(restore_image_name):
    # create restore command
    docker_command_to_exec = 'PGPASSWORD=' + os.environ[
        'POSTGRES_PASSWORD'] + ' psql -U postgres postgres < ' + restore_image_name
    # setup docker connection
    docker_inst = common_docker.CommonDocker()
    # run command to backup against the database
    docker_inst.com_docker_run_command_via_exec(
        container_id=docker_inst.com_docker_container_id_by_name(
            container_name='/mkstack_database'),
        docker_command=docker_command_to_exec)
