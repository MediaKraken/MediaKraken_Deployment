
    zfs_status = ssh_instance.com_net_ssh_run_command(
        'zpool list -H -o health')
    # TODO check zfs_status for string to determine bad pool
    # TODO and send notification
    ssh_instance.com_net_ssh_close()

