VERSION=1.10.7

sudo apt-get install build-essential pkg-config libc6-dev libssl-dev libexpat1-dev libavcodec-dev libgl1-mesa-dev libqt4-dev

wget http://www.makemkv.com/download/makemkv-bin-$VERSION.tar.gz
wget http://www.makemkv.com/download/makemkv-oss-$VERSION.tar.gz

gunzip makemkv-*
tar -vxf makemkv-bin-$VERSION.tar.gz
tar -vxf makemkv-oss-$VERSION.tar.gz

cd makemkv-oss-$VERSION.tar.gz
./configure
make -j`getconf _NPROCESSORS_ONLN`
sudo make install

cd ../makemkv-bin-$VERSION.tar.gz
make
sudo make install

