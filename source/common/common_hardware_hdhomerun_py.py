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

from pyhdhomerun.adapter import HdhrUtility
from pyhdhomerun.constants import MAP_US_BCAST

from . import common_global


# https://github.com/MediaKraken/PyHdHomeRun

class CommonHardwareHDHomeRunPY:
    """
    Class for interfacing with hdhomerun
    """

    def __init__(self):
        self.devices = None

    def com_hdhomerun_discover(self):
        """
        Look for hdhomerun devices
        """
        self.devices = HdhrUtility.discover_find_devices_custom()

    def com_hdhomerun_list(self):
        """
        List hdhomerun tuners
        """
        return self.devices

    def get_tuner_vstatus(self, device_adapter):
        """
        Get tuner status
        """
        (vstatus, raw_data) = device_adapter.get_tuner_vstatus()
        common_global.es_inst.com_elastic_index('info', {'stuff': vstatus})

    def set_tuner_vchannel(self, device_adapter, vchannel):
        """
        Set current channel
        """
        device_adapter.set_tuner_vchannel(vchannel)
        (vstatus, raw_data) = device_adapter.get_tuner_vstatus()
        common_global.es_inst.com_elastic_index('info', {'stuff': vstatus})

    def set_stream(self, device_adapter, vchannel, target_uri):
        """
        Set stream
        """
        device_adapter.set_tuner_vchannel(vchannel)
        device_adapter.set_tuner_target(target_uri)

    def get_supported(self, device_adapter):
        """
        Get supported info
        """
        common_global.es_inst.com_elastic_index('info', {'stuff': device_adapter.get_supported()})

    def scan(self, device_adapter):
        """
        Generator for scan by channel map
        """
        device_adapter.scan_channels(MAP_US_BCAST)

    def get_count(self):
        """
        Return count of channels
        """
        return HdhrUtility.get_channels_in_range(MAP_US_BCAST)


'''
test_class = com_HDHomeRun_API_Py()
test_class.com_HDHomeRun_Discover()
devices = test_class.com_HDHomeRun_List()

i = 0
for device in devices:
    common_global.es_inst.com_elastic_index('info', {'stuff':"%d: %s" % (i, device))
    i += 1

first_device_str = ("%s-%d" % (devices[0].nice_device_id, 1))
print("str: %s", first_device_str)
hd = HdhrUtility.device_create_from_str(first_device_str)

device_adapter = HdhrDeviceQuery(hd)
print("supported: %s", test_class.get_supported(device_adapter))

print("scan: %s", test_class.scan(device_adapter))
#status = test_class.get_tuner_vstatus(device_adapter)
#print("Status: %s" % (status))

#device_adapter.set_tuner_vchannel(13)
#device_adapter.set_tuner_target('rtp://192.168.5.13:7891')
#device_adapter.set_tuner_target(None)
print("channel count: %s", test_class.get_count())
#print(test_class.scan(device_adapter))
'''
