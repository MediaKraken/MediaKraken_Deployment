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

PKG_NAME="pip"
PKG_VERSION="9.0.1"
PKG_ARCH="any"
PKG_LICENSE="PIP"
PKG_SITE="https://pip.pypa.io/en/stable/"
PKG_URL="https://github.com/pypa/pip/archive/$PKG_VERSION.tar.gz"

PKG_DEPENDS_TARGET="toolchain Python distutilscross:host"
PKG_SECTION="python/devel"
PKG_SHORTDESC="The PyPA recommended tool for installing Python packages"
PKG_LONGDESC="The PyPA recommended tool for installing Python packages"

PKG_IS_ADDON="no"
PKG_AUTORECONF="no"

pre_make_target() {
  strip_lto
  export PYTHONXCPREFIX="$SYSROOT_PREFIX/usr"
}

make_target() {
  python setup.py build --cross-compile
}

makeinstall_target() {
  python setup.py install --root=$INSTALL --prefix=/usr
}

post_makeinstall_target() {
  find $INSTALL/usr/lib -name "*.py" -exec rm -rf "{}" ";"
  rm -rf $INSTALL/usr/lib/python*/site-packages/*/tests
}
