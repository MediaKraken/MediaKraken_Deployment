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
