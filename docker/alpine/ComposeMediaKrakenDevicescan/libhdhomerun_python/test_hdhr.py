#!/usr/bin/python

from pprint import pprint
from hdhomerun import Device, DeviceError

devices = Device.discover()
if len(devices) > 0:
    try:
        devices[0].set_tuner(2)
        devices[0].tuner_lockkey_request()
        #devices[0].upgrade(filename='hdhomerun3_cablecard_firmware_20150604.bin', wait=True)
        devices[0].set_var(item='/tuner2/vchannel', value='702')
        pprint(devices[0].wait_for_lock())
        pprint(devices[0].get_tuner_status())
        pprint(devices[0].get_tuner_vstatus())
        print 'Tuner 2 lockkey owner: ' + devices[0].get_tuner_lockkey_owner()
        print 'Tuner 2 vchannel: ' + devices[0].get_var(item='/tuner2/vchannel')
        print 'Tuner 2 channel: ' + devices[0].get_var(item='/tuner2/channel')
        print 'Tuner 2 channelmap: ' + devices[0].get_var(item='/tuner2/channelmap')
        print 'Model: ' + devices[0].get_var(item='/sys/model')
        print 'HWModel: ' + devices[0].get_var(item='/sys/hwmodel')
        print 'Name: ' + devices[0].get_name()
        print 'Device ID: %08X' % devices[0].get_device_id()
        print 'Device IP: %08X' % devices[0].get_device_ip()
        print 'Stream info: %s' % devices[0].get_tuner_streaminfo()
        print devices[0].get_tuner_filter()
        print devices[0].get_tuner_program()
        print devices[0].get_tuner_target()
        xx = devices[0].clone()
        print 'OOB status: ' + str(xx.get_oob_status())
        print 'Versions: %s %d' % xx.get_version()
        #print 'Supported: %s' % devices[0].get_supported(prefix='tuner')
        #print devices[0].get_tuner_plotsample()
        devices[0].tuner_lockkey_release()
    except DeviceError as sd_error:
        print 'Failure: ' + str(sd_error)

