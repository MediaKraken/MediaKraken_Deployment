cd $HOME/install
git clone https://github.com/ultravideo/kvazaar.git
cd $HOME/install/kvazaar
./autogen.sh
./configure --enable-static
make -j`getconf _NPROCESSORS_ONLN`
make install
