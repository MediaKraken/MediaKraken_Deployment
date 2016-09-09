"""
Program will update all yer pip install programs
"""
# Code from answer posted by http://stackoverflow.com/users/515656/ramana

from __future__ import absolute_import, division, print_function, unicode_literals
from subprocess import call
import pip

for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
