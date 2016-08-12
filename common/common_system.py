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
import logging
import subprocess
import sys
import psutil
import com_string


def pprint_ntuple(nt, return_value=None):
    tuple_print = []
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = com_string.bytes2human(value)
        logging.debug('%-10s : %7s' % (name.capitalize(), value))
        tuple_print.append('%-10s : %7s' % (name.capitalize(), value))
    if return_value is not None:
        return tuple_print


def com_system_Virtual_Memory(attribute_list=None):
    """
    Return virtual memory
    """
    return_list = []
    if attribute_list is None:
        return pprint_ntuple(psutil.virtual_memory(), True)
    else:
        nt = psutil.virtual_memory()
        for name in attribute_list:
            value = getattr(nt, name)
            if name != 'percent':
                value = com_string.bytes2human(value)
            logging.debug('%-10s : %7s' % (name.capitalize(), value))
            return_list.append(value)
    return return_list


def com_system_SWAP_Memory(attribute_list=None):
    """
    Return swap memory
    """
    return_list = []
    if attribute_list is None:
        pprint_ntuple(psutil.swap_memory())
    else:
        nt = psutil.swap_memory()
        for name in attribute_list:
            value = getattr(nt, name)
            if name != 'percent':
                value = com_string.bytes2human(value)
            logging.debug('%-10s : %7s' % (name.capitalize(), value))
            return_list.append(value)
    return return_list


def com_system_CPU_Count():
    """
    Return cpu count
    """
    return psutil.cpu_count()


def com_system_Partitions():
    """
    Return partitions
    """
    return psutil.disk_partitions()


def com_system_Boot_Time():
    """
    Get boot time
    """
    return psutil.boot_time()


def com_system_Users():
    """
    Get users
    """
    return psutil.users()


def com_system_CPU_Usage(per_cpu=False):
    """
    Get cpu percentage
    """
    return psutil.cpu_times_percent(interval=1, percpu=per_cpu)


def com_system_CPU_Times():
    """
    Get cpu times
    """
    return psutil.cpu_times()


def com_system_Disk_Usage(file_path='/'):
    """
    Get disk usage for specified path
    """
    return psutil.disk_usage(file_path)


def com_system_Disk_Usage_All(human_readable=False):
    """
    Get disk usage of all partitions
    """
    disk_usage_data = []
    for row_data in com_system_Partitions():
        if human_readable:
            formatted_list = []
            for space_value in com_system_Disk_Usage(row_data[1]):
                if len(formatted_list) == 3:
                    formatted_list.append(space_value)
                else:
                    formatted_list.append(com_string.bytes2human(space_value))
            disk_usage_data.append((row_data[1], formatted_list))
        else:
            disk_usage_data.append((row_data[1], com_system_Disk_Usage(row_data[1])))
    return disk_usage_data


def com_system_Disk_IO(per_disk=False):
    """
    Get disk IO
    """
    return psutil.disk_io_counters(perdisk=per_disk)


def com_system_Uptime():
    """
    Get system uptime
    """
    if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
        uptime_proc = subprocess.Popen(['net', 'statistics', 'server'], stdout=subprocess.PIPE)
        out, err = uptime_proc.communicate()
        uptime_proc.wait()
        for out_line in out:
            if out_line.find('Statistics since') != -1:
                out = out_line.replace('Statistics since ', '')
                break
    else:
        uptime_proc = subprocess.Popen(['uptime'], stdout=subprocess.PIPE)
        out, err = uptime_proc.communicate()
        uptime_proc.wait()
        out = out.split(' up ', 1)[1].split(',', 2)[0] + out.split(' up ', 1)[1].split(',', 2)[1]
    return out


def com_process_list(process_name=None):
    """
    Get processes and optionally check for one
    """
    if process_name is not None:
        if process_name in psutil.process_iter():
            return True
        else:
            return False
    else:
        return psutil.process_iter()
