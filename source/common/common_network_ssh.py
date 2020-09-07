"""
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
"""

import paramiko


class CommonNetworkSSH:
    """
    Class for interfacing via SSH
    """

    def __init__(self, host, user_name, user_password):
        # Create an SSH session to be used for all our requests
        self.ssh_connection = paramiko.SSHClient()
        self.ssh_connection.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        self.ssh_connection.connect(
            host, username=user_name, password=user_password)

    def com_net_ssh_run_sudo_command(self, command_text, sudo_password='metaman'):
        """
        Run specified command as sudo so it will send the password
        """
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh_connection.exec_command(command_text,
                                                                             get_pty=True)
        ssh_stdin.write(sudo_password + '\n')
        ssh_stdin.flush()
        return ssh_stdout.read()

    def com_net_ssh_run_command(self, command_text):
        """
        Run specified command and write output
        """
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh_connection.exec_command(command_text,
                                                                             get_pty=True)
        return ssh_stdout.read()

    def com_net_ssh_close(self):
        """
        Close the ssh connection
        """
        self.ssh_connection.close()
