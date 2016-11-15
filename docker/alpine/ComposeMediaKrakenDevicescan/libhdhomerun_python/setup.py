#!/usr/bin/env python

import platform
from distutils.core import setup, Extension

source_files = [
    'device_common.c',
    'device_get.c',
    'device_type.c',
    'device_set.c',
]

module = Extension(
    name = 'hdhomerun',
    sources = source_files,
    libraries = ['hdhomerun'],
    include_dirs = ['libhdhomerun'],
    extra_compile_args=['-std=c99'],
    extra_link_args=[],
)

setup(
    name='hdhomerun',
    version='1.0',
    ext_modules=[module],
)
