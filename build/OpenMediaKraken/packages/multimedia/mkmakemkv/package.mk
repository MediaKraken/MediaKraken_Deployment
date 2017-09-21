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

PKG_NAME="mkmakemkv"
PKG_VERSION="1.10.7"
PKG_ARCH="x86_64"
PKG_LICENSE="OSS"
PKG_SITE="http://www.makemkv.com/forum2/viewtopic.php?f=3&t=224"
PKG_URL="http://www.makemkv.com/download/makemkv-oss-$PKG_VERSION.tar.gz"
PKG_SOURCE_DIR="makemkv-oss-$PKG_VERSION"
PKG_DEPENDS_TARGET="toolchain openssl expat mkffmpeg zlib"
PKG_SECTION="multimedia"
PKG_SHORTDESC="MakeMKV is your one-click solution to convert video that you own into free and patents-unencumbered format that can be played everywhere."
PKG_LONGDESC="MakeMKV is your one-click solution to convert video that you own into free and patents-unencumbered format that can be played everywhere."

PKG_AUTORECONF="no"

PKG_CONFIGURE_OPTS_TARGET="--disable-gui"

post_unpack() {
  curl -s http://www.makemkv.com/download/makemkv-bin-$PKG_VERSION.tar.gz | tar -C $PKG_BUILD -zxf -
}

pre_configure_target() {
  cd ..
  rm -rf .$TARGET_NAME
}

makeinstall_target() {
  :
}

addon() {
  mkdir -p $ADDON_BUILD/$PKG_ADDON_ID/bin
  install -m 0755 $PKG_BUILD/makemkv-bin-$PKG_VERSION/bin/amd64/makemkvcon $ADDON_BUILD/$PKG_ADDON_ID/bin/makemkvcon.bin

  mkdir -p $ADDON_BUILD/$PKG_ADDON_ID/lib
  cp $PKG_BUILD/out/libmakemkv.so.? $ADDON_BUILD/$PKG_ADDON_ID/lib
  cp $PKG_BUILD/out/libdriveio.so.? $ADDON_BUILD/$PKG_ADDON_ID/lib
  cp $PKG_BUILD/out/libmmbd.so.? $ADDON_BUILD/$PKG_ADDON_ID/lib
  cp -PL $(get_build_dir openssl)/.install_pkg/usr/lib/libcrypto.so.?.? $ADDON_BUILD/$PKG_ADDON_ID/lib

  mkdir -p $ADDON_BUILD/$PKG_ADDON_ID/license
  cp $PKG_BUILD/makemkv-bin-$PKG_VERSION/src/eula_en_linux.txt $ADDON_BUILD/$PKG_ADDON_ID/license
}
