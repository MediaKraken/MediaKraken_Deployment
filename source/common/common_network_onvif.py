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

# https://github.com/FalkTannhaeuser/python-onvif-zeep
from onvif import ONVIFCamera, ONVIFError


class CommonNetOnvif(object):
    def __init__(self, hostname="192.168.1.1", port=80, username="user",
                 password="password"):
        self.onvif_device = ONVIFCamera(hostname, port, username, password, '/etc/onvif/wsdl/')

    def com_net_onvif_get_hostname(self):
        return self.onvif_device.devicemgmt.GetHostname()

    def com_net_onvif_get_time(self):
        return self.onvif_device.devicemgmt.GetSystemDateAndTime()

    def com_net_onvif_getwsdlurl(self):
        return self.onvif_device.devicemgmt.GetWsdlUrl()

    def com_net_onvif_getservices(self):
        """
        Returns a collection of the devices
        services and possibly their available capabilities
        """
        params = {'IncludeCapability': True}
        self.onvif_device.devicemgmt.GetServices(params)
        params = self.onvif_device.devicemgmt.create_type('GetServices')
        params.IncludeCapability = False
        return self.onvif_device.devicemgmt.GetServices(params)

    def com_net_onvif_getservicecapabilities(self):
        """Returns the capabilities of the device service."""
        return self.onvif_device.devicemgmt.GetServiceCapabilities()

    def com_net_onvif_getcapabilities(self):
        """
        Provides a backward compatible interface for the base capabilities.
        """
        categories = ['PTZ', 'Media', 'Imaging',
                      'Device', 'Analytics', 'Events']
        self.onvif_device.devicemgmt.GetCapabilities()
        for category in categories:
            self.onvif_device.devicemgmt.GetCapabilities({'Category': category})

        with self.assertRaises(ONVIFError):
            self.onvif_device.devicemgmt.GetCapabilities({'Category': 'unknown'})

    def com_net_onvif_sethostname(self, new_hostname):
        """
        Set the hostname on a device
        A device shall accept strings formatted according to
        RFC 1123 section 2.1 or alternatively to RFC 952,
        other string shall be considered as invalid strings
        """
        self.onvif_device.devicemgmt.SetHostname({'Name': new_hostname})

    #
    # def test_SetHostnameFromDHCP(self):
    #     """ Controls whether the hostname shall be retrieved from DHCP """
    #     ret = self.onvif_device.devicemgmt.SetHostnameFromDHCP(dict(FromDHCP=False))
    #     self.assertTrue(isinstance(ret, bool))
    #
    # def test_GetDNS(self):
    #     """ Gets the DNS setting from a device """
    #     ret = self.onvif_device.devicemgmt.GetDNS()
    #     self.assertTrue(hasattr(ret, 'FromDHCP'))
    #     if not ret.FromDHCP and len(ret.DNSManual) > 0:
    #         log(ret.DNSManual[0].Type)
    #         log(ret.DNSManual[0].IPv4Address)
    #
    # def test_SetDNS(self):
    #     """ Set the DNS settings on a device """
    #     self.onvif_device.devicemgmt.SetDNS(dict(FromDHCP=False))
    #
    # def test_GetNTP(self):
    #     """ Get the NTP settings from a device """
    #     ret = self.onvif_device.devicemgmt.GetNTP()
    #     if not ret.FromDHCP:
    #         self.assertTrue(hasattr(ret, 'NTPManual'))
    #         log(ret.NTPManual)
    #
    # def test_SetNTP(self):
    #     """Set the NTP setting"""
    #     self.onvif_device.devicemgmt.SetNTP(dict(FromDHCP=False))
    #
    # def test_GetDynamicDNS(self):
    #     """Get the dynamic DNS setting"""
    #     ret = self.onvif_device.devicemgmt.GetDynamicDNS()
    #     log(ret)
    #
    # def test_SetDynamicDNS(self):
    #     """ Set the dynamic DNS settings on a device """
    #     self.onvif_device.devicemgmt.GetDynamicDNS()
    #     self.onvif_device.devicemgmt.SetDynamicDNS({'Type': 'NoUpdate', 'Name': None,
    #                                                 'TTL': None})
