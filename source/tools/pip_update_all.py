"""
Program will update all yer pip install programs
"""
# Code from answer posted by http://stackoverflow.com/users/515656/ramana


import pip
from subprocess import call

for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
