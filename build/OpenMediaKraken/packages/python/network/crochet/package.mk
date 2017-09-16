
PKG_NAME="crochet"
PKG_VERSION="1.9.0"
PKG_ARCH="any"
PKG_LICENSE="OSS"
PKG_SITE="https://github.com/itamarst/crochet"
PKG_URL="https://github.com/itamarst/crochet/archive/$PKG_VERSION.tar.gz"
PKG_DEPENDS_TARGET="toolchain Python distutilscross:host"
PKG_SECTION="python/network"
PKG_SHORTDESC="Crochet: use Twisted anywhere!"
PKG_LONGDESC="Crochet: use Twisted anywhere!"

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
