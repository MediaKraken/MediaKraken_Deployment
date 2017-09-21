#
#  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  version 2, as published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License version 2 for more details.
#
#  You should have received a copy of the GNU General Public License
#  version 2 along with this program; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

PKG_NAME="cython"
PKG_VERSION="0.26.1"
PKG_ARCH="any"
PKG_LICENSE="apache"
PKG_SITE="http://cython.org/"
PKG_URL="https://github.com/cython/cython/archive/$PKG_VERSION.tar.gz"
PKG_DEPENDS_HOST="Python:host"
PKG_SECTION="python/devel"
PKG_SHORTDESC="cython: A Python to C compiler "
PKG_LONGDESC="Cython (http://cython.org) is a language that makes writing C extensions for the Python language as easy as Python itself.  Cython is based on the well-known Pyrex, but supports more cutting edge functionality and optimizations."

PKG_IS_ADDON="no"
PKG_AUTORECONF="no"

make_host() {
  make
}

makeinstall_host() {
  make install
}
