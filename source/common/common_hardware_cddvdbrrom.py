import gudev

from common import common_logging_elasticsearch_httpx


# https://stackoverflow.com/questions/2861098/how-do-i-use-udev-to-find-info-about-inserted-video-media-e-g-dvds
def com_hard_cddvdbrrom():
    client = gudev.Client(['block'])
    drives = []
    for device in client.query_by_subsystem("block"):
        if device.has_property("ID_CDROM"):
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                "Found CD/DVD drive at":
                    device.get_device_file()})
            if device.has_property("ID_FS_LABEL"):
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={"Found disc":
                                                                         device.get_property(
                                                                             "ID_FS_LABEL")})
                drives[device.get_device_file()] = (
                    True, device.get_property("ID_FS_LABEL"))
            elif device.has_property("ID_FS_TYPE"):
                drives[device.get_device_file()] = (True, None)
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         'stuff': "Found disc"})
            else:
                drives[device.get_device_file()] = (False, None)
    return drives
