'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
import logging # pylint: disable=W0611
import telnetlib


class CommonHardwareMarantz(object):
    """
    Class for interfacing with Marantz equipment
    """
    def __init__(self, marantz_ip):
        self.device = telnetlib.Telnet(marantz_ip)

    def com_hardware_marantz_command(self, command_string, resp_cnt):
        command_string = command_string.encode("ascii")
        print("Sending cmd %s" % command_string)
        self.device.read_very_eager()  # clear any old stuff
        self.device.write(command_string)
        # # Some commands return several pieces of state info, so
        # # grab them all.
        resp = []
        for r in range(resp_cnt):
            # Strip the trailing \r
            resp.append(self.device.read_until('\r', 1)[:-1])
        print("Response: ",resp)
        return resp

    def com_hardware_marantz_close(self):
        self.device.close()

    def com_hardware_marantz_vol_to_db(self, vol):
        """
        Calculate DB from results
        """
        if len(vol) == 2:
            return int(vol) - 80
        # three digits means half dB steps
        return (int(vol) / 10.0) - 80

    def com_hardware_marantz_check_power(self):
        return self.com_hardware_marantz_command('PW?', 1)[0]

    def com_hardware_marantz_power_on(self):
        return self.com_hardware_marantz_command('PWON', 1)[0]

    def com_hardware_marantz_power_standby(self):
        return self.com_hardware_marantz_command('PWSTANDBY', 1)[0]

    def com_hardware_marantz_volume_get(self):
        return self.com_hardware_marantz_vol_to_db(self.com_hardware_marantz_command('MV?\r', 2)[0][2:])


# testing against AV7703

# connect test
teststuff = CommonHardwareMarantz('10.0.0.209')

# # get front speakers?
# print(teststuff.com_hardware_marantz_command('PSFRONT?\r', 2))
#
# # get current input status
# print(teststuff.com_hardware_marantz_command('SI?\r', 2))

# get surround mode
print(teststuff.com_hardware_marantz_command('MS?\r', 6))  # others say 9

# connect close
teststuff.com_hardware_marantz_close()
