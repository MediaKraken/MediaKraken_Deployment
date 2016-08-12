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
import logging
from pprint import pprint
from hdhomerun import Device, DeviceError


class CommonHardwareHDHomeRun(object):
    """
    Class for interfacing with hdhomerun
    """
    def __init__(self):
        pass


    def MK_Common_HDHomeRun_Discover(self):
        """
        Discover hdhomerun devices
        """
        self.devices = Device.discover()


    def MK_Common_HDHomeRun_List(self):
        return self.devices


    def MK_Common_HDHomeRun_Detail(self, ndx):
        print('Model: %s', self.devices[ndx].get_var(item='/sys/model'))
        print('HWModel: %s ', self.devices[ndx].get_var(item='/sys/hwmodel'))
        print('Name: %s', self.devices[ndx].get_name())
        print('Device ID: %08X' % self.devices[ndx].get_device_id())
        print('Device IP: %08X' % self.devices[ndx].get_device_ip())
        print('Stream info: %s' % self.devices[ndx].get_tuner_streaminfo())
        print('Versions: %s %d' % self.devices[ndx].get_version())


    # firmware upgrade
    def MK_Common_HDHomeRun_Upgrade(self, ndx, firmware_file):
        self.devices[ndx].upgrade(filename=firmware_file, wait=True)


    # set lock request
    def MK_Common_HDHomeRun_Lock_Request(self, ndx):
        self.devices[ndx].tuner_lockkey_request()
        self.devices[ndx].wait_for_lock()


    # release lock
    def MK_Common_HDHomeRun_Lock_Release(self, ndx):
        self.devices[ndx].tuner_lockkey_release()


    # get lock owner
    def MK_Common_HDHomeRun_Lock_Owner(self, ndx):
        return self.devices[0].get_tuner_lockkey_owner()


    # set tuner
    def MK_Common_HDHomeRun_Set_Tuner(self, ndx, tuner_no):
        self.devices[ndx].set_tuner(tuner_no)


    # get tuner status
    def MK_Common_HDHomeRun_Get_Tuner_Status(self, ndx):
         return self.devices[ndx].get_tuner_status()





    def stuff_to_code(self):
        #self.devices[0].set_var(item='/tuner1/vchannel', value='702')
        #pprint(self.devices[0].get_tuner_vstatus())
        #print 'Tuner 2 vchannel: ' + self.devices[0].get_var(item='/tuner2/vchannel')
        #print 'Tuner 2 channel: ' + self.devices[0].get_var(item='/tuner2/channel')
        #print 'Tuner 2 channelmap: ' + self.devices[0].get_var(item='/tuner2/channelmap')
        print(self.devices[0].get_tuner_filter())
        print(self.devices[0].get_tuner_program())
        print(self.devices[0].get_tuner_target())
        #print 'OOB status: ' + str(self.devices[0].get_oob_status())
        #print 'Supported: %s' % self.devices[0].get_supported(prefix='tuner')
        #print self.devices[0].get_tuner_plotsample()

