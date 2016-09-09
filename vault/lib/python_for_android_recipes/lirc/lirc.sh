#!/bin/bash

# REPLACE ALL THE "lirc" OF THIS FILE WITH THE MODULE NAME
# THEN REMOVE THIS ERROR AND EXIT
error "not configure" && exit -1

# version of your package
VERSION_lirc=${VERSION_lirc:-1.3}

# dependencies of this recipe
DEPS_lirc=()

# url of the package
URL_lirc=http://downloads.sourceforge.net/project/lirc/LIRC/0.9.2a/lirc-0.9.2a.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Flirc%2Ffiles%2FLIRC%2F0.9.2a%2F&ts=1430692122&use_mirror=hivelocity

# md5 of the package
MD5_lirc=c39d6bc901157c308163e6fd58727346

# default build path
BUILD_lirc=$BUILD_PATH/lirc/$(get_directory $URL_lirc)

# default recipe path
RECIPE_lirc=$RECIPES_PATH/lirc

# function called for preparing source code if needed
# (you can apply patch etc here.)
function prebuild_lirc() {
	true
}

# function called to build the source code
function build_lirc() {
	true
}

# function called after all the compile have been done
function postbuild_lirc() {
	true
}
