from __future__ import absolute_import, division, print_function, unicode_literals
import logging  # pylint: disable=W0611
import gudev


# https://stackoverflow.com/questions/2861098/how-do-i-use-udev-to-find-info-about-inserted-video-media-e-g-dvds
def com_hard_cddvdbrrom():
    client = gudev.Client(['block'])
    drives = []
    for device in client.query_by_subsystem("block"):
        if device.has_property("ID_CDROM"):
            common_global.es_inst.com_elastic_index('info', {'stuff':"Found CD/DVD drive at %s" % device.get_device_file())
            if device.has_property("ID_FS_LABEL"):
                common_global.es_inst.com_elastic_index('info', {'stuff':"Found disc: %s" %
                             device.get_property("ID_FS_LABEL"))
                drives[device.get_device_file()] = (
                    True, device.get_property("ID_FS_LABEL"))
            elif device.has_property("ID_FS_TYPE"):
                drives[device.get_device_file()] = (True, None)
                common_global.es_inst.com_elastic_index('info', {'stuff':"Found disc")
            else:
                drives[device.get_device_file()] = (False, None)
    return drives
