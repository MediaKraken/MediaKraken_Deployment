from distutils.core import setup
from distutils.extension import Extension

from Cython.Build import cythonize

extensions = [
    Extension("video_mpv", ["video_mpv.pyx"],
              include_dirs=['/usr/lib/python2.7/dist-packages/kivy/include'])
    #        libraries = [...],
    #        library_dirs = [...]),
]
setup(
    name="MKKivyMPV",
    ext_modules=cythonize(extensions),
)
