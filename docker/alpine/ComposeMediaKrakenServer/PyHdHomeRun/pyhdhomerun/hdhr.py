from ctypes import cdll
from ctypes.util import find_library

_FILEPATH = find_library('hdhomerun')
if _FILEPATH is None:
    _FILEPATH = 'libhdhomerun.so'

library = cdll.LoadLibrary(_FILEPATH)

