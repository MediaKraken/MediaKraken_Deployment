"""
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
"""

import subprocess

import psutil
from common import common_logging_elasticsearch_httpx

from . import common_string


def com_system_virtual_memory(attribute_list=None):
    """
    Return virtual memory
    """
    return_list = []
    if attribute_list is None:
        return pprint_ntuple(psutil.virtual_memory(), True)
    else:
        nt_result = psutil.virtual_memory()
        for name in attribute_list:
            value = getattr(nt_result, name)
            if name != 'percent':
                value = common_string.com_string_bytes2human(value)
            return_list.append(value)
    return return_list


def com_system_swap_memory(attribute_list=None):
    """
    Return swap memory
    """
    return_list = []
    if attribute_list is None:
        pprint_ntuple(psutil.swap_memory())
    else:
        nt_result = psutil.swap_memory()
        for name in attribute_list:
            value = getattr(nt_result, name)
            if name != 'percent':
                value = common_string.com_string_bytes2human(value)
            return_list.append(value)
    return return_list


def com_system_cpu_count():
    """
    Return cpu count
    """
    return psutil.cpu_count()


def com_system_partitions():
    """
    Return partitions
    """
    return psutil.disk_partitions()


def com_system_boot_time():
    """
    Get boot time
    """
    return psutil.boot_time()


def com_system_users():
    """
    Get users
    """
    return psutil.users()


def com_system_cpu_usage(per_cpu=False):
    """
    Get cpu percentage
    """
    return psutil.cpu_times_percent(interval=1, percpu=per_cpu)


def com_system_cpu_times():
    """
    Get cpu times
    """
    return psutil.cpu_times()


def com_system_disk_usage(file_path='/'):
    """
    Get disk usage for specified path
    """
    return psutil.disk_usage(file_path)


def com_system_disk_usage_all(human_readable=False):
    """
    Get disk usage of all partitions
    """
    disk_usage_data = []
    for row_data in com_system_partitions():
        if human_readable:
            formatted_list = []
            for space_value in com_system_disk_usage(row_data[1]):
                if len(formatted_list) == 3:
                    formatted_list.append(space_value)
                else:
                    formatted_list.append(
                        common_string.com_string_bytes2human(space_value))
            disk_usage_data.append((row_data[1], formatted_list))
        else:
            disk_usage_data.append(
                (row_data[1], com_system_disk_usage(row_data[1])))
    return disk_usage_data


def com_system_disk_io(per_disk=False):
    """
    Get disk IO
    """
    return psutil.disk_io_counters(perdisk=per_disk)


def com_system_uptime():
    """
    Get system uptime
    """
    uptime_proc = subprocess.Popen(['uptime'], stdout=subprocess.PIPE, shell=False)
    out, err = uptime_proc.communicate()
    uptime_proc.wait()
    out = str(out).split(' up ', 1)[1].split(',', 2)[
              0] + str(out).split(' up ', 1)[1].split(',', 2)[1]
    return out


def com_process_list(process_name=None):
    """
    Get processes and optionally check for one
    """
    if process_name is not None:
        return process_name in psutil.process_iter()
    else:
        return psutil.process_iter()
