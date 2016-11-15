from ctypes import *

from pyhdhomerun.utility import ip_int_to_ascii
from pyhdhomerun.constants import *

class TYPE_hdhomerun_discover_device_t(Structure):
    _fields_ = [('ip_addr',     c_uint, 32),
                ('device_type', c_uint, 32),
                ('device_id',   c_uint, 32),
                ('tuner_count', c_ubyte) 
               ]

    @property
    def nice_ip(self):
        return ip_int_to_ascii(self.ip_addr)

    @property
    def nice_device_id(self):
        return ("%X" % self.device_id)

    def __str__(self):
        return ('DISCOVER  ID= [%s]  TYPE= (%d)  IP= [%s]  TUNERS= (%d)' % 
                (self.nice_device_id, self.device_type, self.nice_ip, 
                 self.tuner_count))

class TYPE_hdhomerun_channel_entry_t(Structure):
    def __str__(self):
        return ("CHANNEL-ENTRY  NEXT= [%s]  PREV= [%s]  FREQ= (%d)  CHAN= (%d)"
                "  NAME= [%s]" % ('<present>' if self.next else None, 
                                  '<present>' if self.prev else None, 
                                  self.frequency, self.channel_number, 
                                  ''))#self.name.value))
    
TYPE_hdhomerun_channel_entry_t._fields_ = \
    [('next',           POINTER(TYPE_hdhomerun_channel_entry_t)),
     ('prev',           POINTER(TYPE_hdhomerun_channel_entry_t)),
     ('frequency',      c_uint, 32),
     ('channel_number', c_uint, 16),
     ('name',           c_char * 16) 
    ]

class TYPE_hdhomerun_channel_list_t(Structure):
    _fields_ = [('head', POINTER(TYPE_hdhomerun_channel_entry_t)),
                ('tail', POINTER(TYPE_hdhomerun_channel_entry_t))
               ]

    def __str__(self):
        return ('CHANNEL-LIST  HEAD= [%s]  TAIL= [%s]' % 
                    ('<present>' if self.head else None, 
                     '<present>' if self.tail else None))

#class TYPE_hdhomerun_channelmap_range_t(Structure):
#    _fields_ = [('channel_range_start', c_uint, 16),
#                ('channel_range_end',   c_uint, 16),
#                ('frequency',           c_uint, 32),
#                ('spacing',             c_uint, 32),
#               ]

#class TYPE_hdhomerun_channelmap_record_t(Structure):
#    _fields_ = [('channelmap',            c_char_p),
#                ('range_list',            POINTER(TYPE_hdhomerun_channelmap_range_t)),
#                ('channelmap_scan_group', c_char_p),
#                ('countrycodes',          c_char_p)
#               ]

class TYPE_hdhomerun_tuner_status_t(Structure):
    _fields_ = [('channel',                 c_char * 32),
                ('lock_str',                c_char * 32),
                ('signal_present',          c_int, 32),
                ('lock_supported',          c_int, 32),
                ('lock_unsupported',        c_int, 32),
                ('signal_strength',         c_uint, 32),
                ('signal_to_noise_quality', c_uint, 32),
                ('symbol_error_quality',    c_uint, 32),
                ('raw_bits_per_second',     c_uint, 32),
                ('packets_per_second',      c_uint, 32)
               ]

    def __str__(self):
        return ("STATUS  CHANNEL= [%s]  LOCK_STR= [%s]  SIG_PRESENT= [%s]  "
                "LOCK_SUPP= [%s]  LOCK_UNSUPP= [%s]  SIG_STRENGTH= (%d)  "
                "SN_QUAL= (%d)  SYMERR_QUAL= (%d)  RAW_BPS= (%d)  PPS= (%d)" %
                (self.channel, self.lock_str, not not self.signal_present, 
                 not not self.lock_supported, not not self.lock_unsupported, 
                 self.signal_strength, self.signal_to_noise_quality, 
                 self.symbol_error_quality, self.raw_bits_per_second, 
                 self.packets_per_second))
               
class TYPE_hdhomerun_channelscan_program_t(Structure):
    _fields_ = [('program_str',    c_char * 64),
                ('program_number', c_uint, 16),
                ('virtual_major',  c_uint, 16),
                ('virtual_minor',  c_uint, 16),
                ('type',           c_uint, 16),
                ('name',           c_char * 32)
               ]

    def __str__(self):
        return ("PROGRAM  STR= [%s]  NUM= (%d)  VMAJ= (%d)  VMIN= (%d)  "
                "TYPE= (%d)  NAME= [%s]" % (self.program_str, 
                                            self.program_number, 
                                            self.virtual_major,
                                            self.virtual_minor,
                                            self.type,
                                            self.name))

class TYPE_hdhomerun_channelscan_result_t(Structure):
    _fields_ = [('channel_str',                  c_char * 64),
                ('channelmap',                   c_uint, 32),
                ('frequency',                    c_uint, 32),
                ('status',                       TYPE_hdhomerun_tuner_status_t),
                ('program_count',                c_int, 32),
                ('programs',                     TYPE_hdhomerun_channelscan_program_t * HDHOMERUN_CHANNELSCAN_MAX_PROGRAM_COUNT),
                ('transport_stream_id_detected', c_int, 32),
                ('transport_stream_id',          c_uint, 16)
               ]

    def __str__(self):
        return ("CHANNELSCAN-RES  STR= [%s]  MAP= (%d)  FREQ= (%d)  STATUS= "
                "[%s]  PROG_COUNT= (%d)  STREAM_DETECTED= [%s]  STREAM_ID= "
                "(%d)" % (self.channel_str, self.channelmap, self.frequency,
                          '<present>' if self.status else None, self.program_count, 
                          not not self.transport_stream_id_detected, 
                          self.transport_stream_id))

    def dump_programs(self):
        i = 0
        for i in xrange(self.program_count):
            print("%d: %s" % (i, self.programs[i]))

            i += 1

class TYPE_hdhomerun_channelscan_t(Structure):
    def __str__(self):
        return ("CHANNELSCAN  DEVICE= [%s]  SCANNED= (%d)  LIST= [%s]  "
                "NEXT= [%s]" % (self.hd.contents, self.scanned_channels, 
                                self.channel_list.contents, 
                                '<present>' if self.next_channel else None))

class TYPE_hdhomerun_device_t(Structure):
    @property
    def nice_multicast_ip(self):
        return ip_int_to_ascii(self.multicast_ip)

    @property
    def nice_device_id(self):
        return ("%X" % self.device_id)

    def __str__(self):
        return ("DEVICE  SCAN= [%s]  MC_IP= [%s]  MS_PORT= [%s]  "
                "ID= [%s]  TUNER= (%d)  LK= (%d)  NAME= [%s]  MODEL= [%s]" % 
                (self.scan.contents if self.scan else None, self.nice_multicast_ip, self.multicast_port, 
                 self.nice_device_id, self.tuner, self.lockkey, self.name,
                 self.model))

TYPE_hdhomerun_channelscan_t._fields_ = \
   [('hd',               POINTER(TYPE_hdhomerun_device_t)),
    ('scanned_channels', c_uint, 32),
    ('channel_list',     POINTER(TYPE_hdhomerun_channel_list_t)),
    ('next_channel',     POINTER(TYPE_hdhomerun_channel_entry_t))
   ]

class TYPE_hdhomerun_debug_message_t(Structure):
    pass

TYPE_hdhomerun_debug_message_t._fields_ = \
    [('next',   POINTER(TYPE_hdhomerun_debug_message_t)),
     ('prev',   POINTER(TYPE_hdhomerun_debug_message_t)),
     ('buffer', c_char * 2048)
    ]

#class TYPE_hdhomerun_debug_t(Structure);
#    _fields_ = [('thread', c_int, 32),
#                
#               ]

#struct hdhomerun_debug_t
#{
#	pthread_t thread;
#	volatile bool_t enabled;
#	volatile bool_t terminate;
#	char *prefix;
#
#	pthread_mutex_t print_lock;
#	pthread_mutex_t queue_lock;
#	pthread_mutex_t send_lock;
#
#	struct hdhomerun_debug_message_t *queue_head;
#	struct hdhomerun_debug_message_t *queue_tail;
#	uint32_t queue_depth;
#
#	uint64_t connect_delay;
#
#	char *file_name;
#	FILE *file_fp;
#	hdhomerun_sock_t sock;
#};

#class TYPE_hdhomerun_control_sock_t(Structure):
#    _fields_ = [
#                ('desired_device_id', c_uint, 32),
#                ('desired_device_ip', c_uint, 32),
#                ('actual_device_id', c_uint, 32),
#                ('actual_device_ip', c_uint, 32),
#                ('sock', c_int, 32),
#                ('dbg', POINTER(TYPE_hdhomerun_debug_t)),
#
#
#               ]
#
#struct hdhomerun_pkt_t {
#	uint8_t *pos;
#	uint8_t *start;
#	uint8_t *end;
#	uint8_t *limit;
#	uint8_t buffer[3074];
#};

#struct hdhomerun_control_sock_t {
#	uint32_t desired_device_id;
#	uint32_t desired_device_ip;
#	uint32_t actual_device_id;
#	uint32_t actual_device_ip;
#	uint sock;
#	struct hdhomerun_debug_t *dbg;
#	struct hdhomerun_pkt_t tx_pkt;
#	struct hdhomerun_pkt_t rx_pkt;
#};
#
#struct hdhomerun_video_sock_t {
#	pthread_mutex_t lock;
#	struct hdhomerun_debug_t *dbg;
#	hdhomerun_sock_t sock;
#
#	volatile size_t head;
#	volatile size_t tail;
#	uint8_t *buffer;
#	size_t buffer_size;
#	size_t advance;
#
#	pthread_t thread;
#	volatile bool_t terminate;
#
#	volatile uint32_t packet_count;
#	volatile uint32_t transport_error_count;
#	volatile uint32_t network_error_count;
#	volatile uint32_t sequence_error_count;
#	volatile uint32_t overflow_error_count;
#
#	volatile uint32_t rtp_sequence;
#	volatile uint8_t sequence[0x2000];
#};

TYPE_hdhomerun_device_t._fields_ = \
    [('cs',            POINTER(c_void_p)), # Not implemented, here.
    ('vs',             POINTER(c_void_p)),  # Not implemented, here.
    ('dbg',            POINTER(c_void_p)), # Not implemented, here.
    ('scan',           POINTER(TYPE_hdhomerun_channelscan_t)),
    ('multicast_ip',   c_uint, 32),
    ('multicast_port', c_uint, 16),
    ('device_id',      c_uint, 32),
    ('tuner',          c_uint, 32),
    ('lockkey',        c_uint, 32),
    ('name',           c_char * 32),
    ('model',          c_char * 32)
   ]

class TYPE_hdhomerun_tuner_vstatus_t(Structure):
    _fields_ = [
                ('vchannel',       c_char * 32),
                ('name',           c_char * 32),
                ('auth',           c_char * 32),
                ('cci',            c_char * 32),
                ('cgms',           c_char * 32),
                ('not_subscribed', c_int, 32),
                ('not_available',  c_int, 32),
                ('copy_protected', c_int, 32)
               ]

    @property
    def not_subscribed(self):
        return not not self.not_subscribed

    @property
    def not_available(self):
        return not not self.not_available

    @property
    def copy_protected(self):
        return not not self.copy_protected

    def __str__(self):
        return ("VSTATUS  VCHANNEL= [%s]  NAME= [%s]  AUTH= [%s]  CCI= [%s]  "
                "CGMS= [%s]  NOT_SUB= [%s]  NOT_AVAIL= [%s]  "
                "COPY_PROTECTED= [%s]" % (self.vchannel, self.name, self.auth,
                 self.cci, self.cgms, not not self.not_subscribed, 
                 not not self.not_available, not not self.copy_protected))

