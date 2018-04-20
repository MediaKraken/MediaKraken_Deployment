cd /mediakraken/install/
git clone https://github.com/georgmartius/vid.stab.git
cd /mediakraken/install/vid.stab/
cmake .
make -j`getconf _NPROCESSORS_ONLN`
make install

