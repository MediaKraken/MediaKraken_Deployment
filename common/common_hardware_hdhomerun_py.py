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

import logging
from pyhdhomerun.adapter import HdhrUtility, HdhrDeviceQuery
from pyhdhomerun.constants import MAP_US_BCAST


class MK_Common_Hardware_HDHomeRun_API_Py:
    def __init__(self):
        pass


    def MK_Common_HDHomeRun_Discover(self):
        """
        Look for hdhomerun divices
        """
        self.devices = HdhrUtility.discover_find_devices_custom()


    def MK_Common_HDHomeRun_List(self):
        return self.devices


    def get_tuner_vstatus(self, device_adapter):
        (vstatus, raw_data) = device_adapter.get_tuner_vstatus()
        logging.debug(vstatus)


    def set_tuner_vchannel(self, device_adapter, vchannel):
        device_adapter.set_tuner_vchannel(vchannel)
        (vstatus, raw_data) = device_adapter.get_tuner_vstatus()
        logging.debug(vstatus)


    def set_stream(self, device_adapter, vchannel, target_uri):
        device_adapter.set_tuner_vchannel(vchannel)
        device_adapter.set_tuner_target(target_uri)


    def get_supported(self, device_adapter):
        logging.debug(device_adapter.get_supported())


    def scan(self, device_adapter):
        """
        Generator for scan by channel map
        """
        device_adapter.scan_channels(MAP_US_BCAST)


    def get_count(self):
        return HdhrUtility.get_channels_in_range(MAP_US_BCAST)


'''
test_class = MK_Common_HDHomeRun_API_Py()
test_class.MK_Common_HDHomeRun_Discover()
devices = test_class.MK_Common_HDHomeRun_List()

i = 0
for device in devices:
    logging.debug("%d: %s" % (i, device))
    i += 1

first_device_str = ("%s-%d" % (devices[0].nice_device_id, 1))
print "str: ", first_device_str
hd = HdhrUtility.device_create_from_str(first_device_str)

device_adapter = HdhrDeviceQuery(hd)
print "supported: ", test_class.get_supported(device_adapter)

print "scan: ", test_class.scan(device_adapter)
#status = test_class.get_tuner_vstatus(device_adapter)
#print("Status: %s" % (status))

#device_adapter.set_tuner_vchannel(13)
#device_adapter.set_tuner_target('rtp://192.168.5.13:7891')
#device_adapter.set_tuner_target(None)
print "channel count:", test_class.get_count()
#print test_class.scan(device_adapter)
'''