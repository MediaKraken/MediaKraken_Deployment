# cd /mediakraken/install/
# git clone https://github.com/georgmartius/vid.stab.git
cd /mediakraken/install/scripts/vid.stab.0.98b
cmake .
make -j`getconf _NPROCESSORS_ONLN`
make install
