cd /mediakraken/install/
git clone https://github.com/georgmartius/vid.stab.git
cd /mediakraken/install/vid.stab/
cmake -DCMAKE_INSTALL_PREFIX:PATH=/mediakraken
make -j`getconf _NPROCESSORS_ONLN`
make install
