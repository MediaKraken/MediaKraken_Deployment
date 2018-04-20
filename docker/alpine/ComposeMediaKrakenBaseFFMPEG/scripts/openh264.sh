cd /mediakraken/install
git clone https://github.com/cisco/openh264.git 
cd /mediakraken/install/openh264
make -j`getconf _NPROCESSORS_ONLN`
make install
make clean
