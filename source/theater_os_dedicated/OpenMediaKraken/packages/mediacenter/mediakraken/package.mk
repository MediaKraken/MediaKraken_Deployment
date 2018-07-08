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

PKG_NAME="mediakraken"
PKG_VERSION="dev-0.7.4"
PKG_ARCH="any"
PKG_LICENSE="GPL"
PKG_SITE="http://www.mediakraken.org"
PKG_URL="https://github.com/MediaKraken/MediaKraken_Deployment/archive/$PKG_VERSION.zip"
PKG_DEPENDS_TARGET="Python setuptools pyopenssl libhdhomerun mpv kivy crochet mkmakemkv libretro-4do libretro-stella mame libretro-dosbox libretro-mupen64plus libretro-vecx"
PKG_SECTION="mediacenter"
PKG_SHORTDESC="MediaKraken: MediaKraken Mediacenter"
PKG_LONGDESC="MediaKraken is a free and open source cross-platform media player and home entertainment system."
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
