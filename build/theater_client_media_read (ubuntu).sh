sudo apt-get install python3-pip python3-dev libdvdread-dev libbluray-dev
sudo pip3 install crudexml

git go https://github.com/cmlburnett/PyBluRead
cd PyBluRead
python3 setup.py build
python3 setup.py install

cd ..
git co https://github.com/cmlburnett/PyDvdRead
cd PyDvdRead
python3 setup.py build
python3 setup.py install


