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

PKG_NAME="postgresql"
PKG_VERSION="9.6.5"
PKG_ARCH="any"
PKG_LICENSE="BSD"
PKG_SITE="https://www.postgresql.org/"
PKG_URL="https://www.postgresql.org/ftp/source/v$PKG_VERSION/$PKG_VERSION.tar.gz"
PKG_DEPENDS_HOST="zlib:host"
PKG_DEPENDS_TARGET="toolchain zlib netbsd-curses openssl"
PKG_SECTION="database"
PKG_SHORTDESC="postgresql: A database server"
PKG_LONGDESC="PostgreSQL is a powerful, open source object-relational database system."

PKG_IS_ADDON="no"
PKG_AUTORECONF="no"

configure_target() {
  ./configure
}

makeinstall_target() {
	# install client library only
	make -C src/bin install
	make -C src/include install
	make -C src/interfaces install
	make -C doc install
}
