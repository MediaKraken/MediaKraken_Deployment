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

# from pprint import pprint
from hdhomerun import Device


class CommonHardwareHDHomeRun(object):
    """
    Class for interfacing with hdhomerun
    """

    def __init__(self):
        self.devices = None

    def com_hdhomerun_discover(self):
        """
        Discover hdhomerun devices
        """
        self.devices = Device.discover()

    def com_hdhomerun_list(self):
        """
        List found devices
        """
        return self.devices

    def com_hdhomerun_detail(self, ndx):
        """
        Detail on specified device
        """
        print(('Model: %s', self.devices[ndx].get_var(item='/sys/model')))
        print(('HWModel: %s ', self.devices[ndx].get_var(item='/sys/hwmodel')))
        print(('Name: %s', self.devices[ndx].get_name()))
        print(('Device ID: %08X' % self.devices[ndx].get_device_id()))
        print(('Device IP: %08X' % self.devices[ndx].get_device_ip()))
        print(('Stream info: %s' % self.devices[ndx].get_tuner_streaminfo()))
        print(('Versions: %s %d' % self.devices[ndx].get_version()))

    def com_hdhomerun_upgrade(self, ndx, firmware_file):
        """
        # firmware upgrade
        """
        self.devices[ndx].upgrade(filename=firmware_file, wait=True)

    def com_hdhomerun_lock_request(self, ndx):
        """
        # set lock request
        """
        self.devices[ndx].tuner_lockkey_request()
        self.devices[ndx].wait_for_lock()

    def com_hdhomerun_lock_release(self, ndx):
        """
        # release lock
        """
        self.devices[ndx].tuner_lockkey_release()

    def com_hdhomerun_lock_owner(self, ndx):
        """
        # get lock owner
        """
        return self.devices[ndx].get_tuner_lockkey_owner()

    def com_hdhomerun_set_tuner(self, ndx, tuner_no):
        """
        # set tuner
        """
        self.devices[ndx].set_tuner(tuner_no)

    def com_hdhomerun_get_tuner_status(self, ndx):
        """
        # get tuner status
        """
        return self.devices[ndx].get_tuner_status()

    def stuff_to_code(self):
        # self.devices[0].set_var(item='/tuner1/vchannel', value='702')
        # pprint(self.devices[0].get_tuner_vstatus())
        # print 'Tuner 2 vchannel: ' + self.devices[0].get_var(item='/tuner2/vchannel')
        # print 'Tuner 2 channel: ' + self.devices[0].get_var(item='/tuner2/channel')
        # print 'Tuner 2 channelmap: ' + self.devices[0].get_var(item='/tuner2/channelmap')
        print((self.devices[0].get_tuner_filter()))
        print((self.devices[0].get_tuner_program()))
        print((self.devices[0].get_tuner_target()))
        # print 'OOB status: ' + str(self.devices[0].get_oob_status())
        # print 'Supported: %s' % self.devices[0].get_supported(prefix='tuner')
        # print self.devices[0].get_tuner_plotsample()
