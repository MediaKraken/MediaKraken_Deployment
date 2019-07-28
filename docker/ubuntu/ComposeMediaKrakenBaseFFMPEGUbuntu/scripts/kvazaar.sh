cd /mediakraken/install
git clone https://github.com/ultravideo/kvazaar.git
cd /mediakraken/install/kvazaar
./autogen.sh
./configure --enable-static
make -j`getconf _NPROCESSORS_ONLN`
make install
