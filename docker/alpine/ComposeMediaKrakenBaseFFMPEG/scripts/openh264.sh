cd $HOME/install
git clone https://github.com/cisco/openh264.git 
cd $HOME/install/openh264
make -j`getconf _NPROCESSORS_ONLN`
make install
make clean
