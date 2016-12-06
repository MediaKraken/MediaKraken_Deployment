from setuptools import setup, find_packages
import sys, os

import os.path
dev_path = os.path.dirname(__file__)
sys.path.insert(0, dev_path)

try:
    import pyhdhomerun.hdhr
except OSError as e:
    print("Could not load HDHomeRun library: %s" % (e))
    sys.exit(1)
else:
    print("HDHomeRun libraries verified.")
    
long_description = "HDHomeRun interface library. Supports device discovery, " \
                   "channel-scanning, streaming, status inquiries, channel " \
                   "changes, etc.."""
    
setup(name='pyhdhomerun',
      version='2.3.5',
      description="HDHomeRun interface library.",
      long_description=long_description,
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Multimedia :: Video :: Capture'],
      keywords='tv television tuner tvtuner hdhomerun',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/PyHdHomeRun',
      license='GPL 2',
      packages=['pyhdhomerun'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
      ],
)

