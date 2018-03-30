'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
import logging  # pylint: disable=W0611
import rdma
import rdma.vmad
# import rdma.IBA as IBA
# import rdma.ibverbs as ibv
import rdma.satransactor
import rdma.path


def com_rdma_get_devices():
    """
    # get list of RDMA devices
    """
    rdma_device_list = rdma.get_devices()
    common_global.es_inst.com_elastic_index('info', {'stuff':"RDMA devices: %s", rdma_device_list)
    for rdma_device in rdma_device_list:
        common_global.es_inst.com_elastic_index('info', {'stuff':"RDMA Device '%s'", (rdma_device.name))
        for rdma_node in ['node_type', 'fw_ver', 'node_guid', 'node_desc', 'sys_image_guid',
                          'board_id', 'hw_ver']:
            common_global.es_inst.com_elastic_index('info', {'stuff':"    %s: %s", rdma_node, repr(
                getattr(rdma_device, rdma_node)))
        for rdma_device_end_port in rdma_device.end_ports:
            common_global.es_inst.com_elastic_index('info', {'stuff':"    port: %u", (rdma_device_end_port.port_id))
            for rdma_attr in ['lid', 'lmc', 'phys_state', 'state', 'sm_lid', 'sm_sl', 'gids',
                              'pkeys']:
                common_global.es_inst.com_elastic_index('info', {'stuff':"        %s: %s", rdma_attr,
                             repr(getattr(rdma_device_end_port, rdma_attr)))
    return rdma_device_list
