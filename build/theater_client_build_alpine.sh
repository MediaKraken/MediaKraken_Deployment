# setup discid libs
tar -xvf ./lib/libdiscid-0.6.1.tar.gz
cd ./libdiscid-0.6.1
./configure
make -j`getconf _NPROCESSORS_ONLN`
make install
cp -R /usr/local/lib/discid /usr/local/.
C_INCLUDE_PATH=$C_INCLUDE_PATH:/usr/local/include
export C_INCLUDE_PATH
CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/usr/local/include
export CPLUS_INCLUDE_PATH
export LD_LIBRARY_PATH=/usr/local/include
cd ..
rm -Rf libdiscid-0.6.1
