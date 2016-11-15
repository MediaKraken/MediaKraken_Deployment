import logging

from ctypes import *

import pyhdhomerun.hdhr

from pyhdhomerun.types import *
from pyhdhomerun.constants import MAX_DEVICES

try:
    hdhr = pyhdhomerun.hdhr.library
except:
    logging.exception("Could not acquire HDHR object for bindings.")
    raise

CFUNC_hdhomerun_discover_find_devices_custom = \
    hdhr.hdhomerun_discover_find_devices_custom
CFUNC_hdhomerun_discover_find_devices_custom.argtypes = \
    [c_uint, 
     c_uint, 
     c_uint, 
     TYPE_hdhomerun_discover_device_t * MAX_DEVICES, 
     c_int
    ]

CFUNC_hdhomerun_device_create_from_str = \
    hdhr.hdhomerun_device_create_from_str
CFUNC_hdhomerun_device_create_from_str.argtypes = \
    [c_char_p, 
     c_void_p
    ]
CFUNC_hdhomerun_device_create_from_str.restype = \
    POINTER(TYPE_hdhomerun_device_t)

CFUNC_hdhomerun_device_destroy = \
    hdhr.hdhomerun_device_destroy
CFUNC_hdhomerun_device_destroy.argtypes = \
    [POINTER(TYPE_hdhomerun_device_t)
    ]
CFUNC_hdhomerun_device_destroy.restype = \
    None

CFUNC_hdhomerun_device_get_tuner_vstatus = \
    hdhr.hdhomerun_device_get_tuner_vstatus
CFUNC_hdhomerun_device_get_tuner_vstatus.argtypes = \
    [POINTER(TYPE_hdhomerun_device_t),
     POINTER(c_char_p),
     POINTER(TYPE_hdhomerun_tuner_vstatus_t)
    ]

CFUNC_hdhomerun_device_get_supported = \
    hdhr.hdhomerun_device_get_supported
CFUNC_hdhomerun_device_get_supported.argtypes = \
    [POINTER(TYPE_hdhomerun_device_t), 
     c_void_p,
     POINTER(c_char_p)
    ]

#CFUNC_hdhomerun_channel_list_create = \
#    hdhr.hdhomerun_channel_list_create
#CFUNC_hdhomerun_channel_list_create.argtypes = 
#    [ c_char_p ]
#CFUNC_hdhomerun_channel_list_create.restype = 
#    POINTER(TYPE_hdhomerun_channel_list_t)
#
#CFUNC_hdhomerun_channel_list_first = \
#    hdhr.hdhomerun_channel_list_first
#CFUNC_hdhomerun_channel_list_first.argtypes = \
#    [ POINTER(TYPE_hdhomerun_channel_list_t) ]
#CFUNC_hdhomerun_channel_list_first.restype = \
#    POINTER(TYPE_hdhomerun_channel_entry_t)

CFUNC_channelscan_create = \
    hdhr.channelscan_create
CFUNC_channelscan_create.argtypes = \
    [POINTER(TYPE_hdhomerun_device_t), 
     c_char_p
    ]
CFUNC_channelscan_create.restype = \
     POINTER(TYPE_hdhomerun_channelscan_t)

CFUNC_channelscan_destroy = \
    hdhr.channelscan_destroy
CFUNC_channelscan_destroy.argtypes = \
    [POINTER(TYPE_hdhomerun_channelscan_t)
    ]
CFUNC_channelscan_destroy.restype = \
    None

CFUNC_channelscan_advance = \
    hdhr.channelscan_advance
CFUNC_channelscan_advance.argtypes = \
    [POINTER(TYPE_hdhomerun_channelscan_t),
     POINTER(TYPE_hdhomerun_channelscan_result_t)
    ]

CFUNC_channelscan_detect = \
    hdhr.channelscan_detect
CFUNC_channelscan_detect.argtypes = \
    [POINTER(TYPE_hdhomerun_channelscan_t),
     POINTER(TYPE_hdhomerun_channelscan_result_t)
    ]

CFUNC_hdhomerun_channel_list_create = \
    hdhr.hdhomerun_channel_list_create
CFUNC_hdhomerun_channel_list_create.argtypes = \
    [c_char_p
    ]
CFUNC_hdhomerun_channel_list_create.restype = \
    POINTER(TYPE_hdhomerun_channel_list_t)

CFUNC_hdhomerun_channel_list_destroy = \
    hdhr.hdhomerun_channel_list_destroy
CFUNC_hdhomerun_channel_list_destroy.argtypes = \
    [
    POINTER(TYPE_hdhomerun_channel_list_t)
    ]
CFUNC_hdhomerun_channel_list_destroy.restype = \
    None

CFUNC_hdhomerun_channel_list_total_count = \
    hdhr.hdhomerun_channel_list_total_count
CFUNC_hdhomerun_channel_list_total_count.argtypes = \
    [
    POINTER(TYPE_hdhomerun_channel_list_t)
    ]
CFUNC_hdhomerun_channel_list_total_count.restype = \
    (c_uint32)

CFUNC_hdhomerun_device_set_tuner_vchannel = \
    hdhr.hdhomerun_device_set_tuner_vchannel
CFUNC_hdhomerun_device_set_tuner_vchannel.argtypes = \
    [POINTER(TYPE_hdhomerun_device_t),
     c_char_p
    ]

CFUNC_hdhomerun_device_set_tuner_target = \
    hdhr.hdhomerun_device_set_tuner_target
CFUNC_hdhomerun_device_set_tuner_target.argtypes = \
    [POINTER(TYPE_hdhomerun_device_t),
     c_char_p
    ]

CFUNC_hdhomerun_device_stream_start = \
    hdhr.hdhomerun_device_stream_start
CFUNC_hdhomerun_device_stream_start.argtypes = \
    [POINTER(TYPE_hdhomerun_device_t),
    ]

CFUNC_hdhomerun_device_stream_stop = \
    hdhr.hdhomerun_device_stream_stop
CFUNC_hdhomerun_device_stream_stop.argtypes = \
    [POINTER(TYPE_hdhomerun_device_t),
    ]
CFUNC_hdhomerun_device_stream_stop.restype = None

CFUNC_hdhomerun_device_stream_recv = \
    hdhr.hdhomerun_device_stream_recv
CFUNC_hdhomerun_device_stream_recv.argtypes = \
    [POINTER(TYPE_hdhomerun_device_t),
     c_uint32,
     POINTER(c_uint32)
    ]
CFUNC_hdhomerun_device_stream_recv.restype = \
    POINTER(c_uint8)

