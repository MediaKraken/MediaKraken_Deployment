"""
Program will update all yer pip install programs
"""
# Code from answer posted by http://stackoverflow.com/users/515656/ramana


from subprocess import call

import pip

for dist in pip.get_installed_distributions():
    call("pip3 install --upgrade " + dist.project_name, shell=True)
