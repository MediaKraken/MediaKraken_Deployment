cd $HOME/install/
git clone https://github.com/georgmartius/vid.stab.git
cd $HOME/install/vid.stab/
cmake .
make -j`getconf _NPROCESSORS_ONLN`
make install

