# install python_vlc and vlc

# clone vlc
git clone https://github.com/videolan/vlc

# clone python vlc into vlc/src/.
git clone git://git.videolan.org/vlc/bindings/python.git

cd vlc/src/python
python setup.py install

************ dev

# setup the newest stable build
sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get update && sudo apt-get dist-upgrade

sudo apt-get install python-kivy mpv dosbox
# wmctrl python-simplejson   - not sure if needed

# setup adb tools for android
sudo apt-get install android-tools-adb cython javacc openjdk-7-jdk
git clone https://github.com/kivy/buildozer.git 
cd buildozer
sudo python setup.py install

# fire up android table
# fire up the ADB WiFi and record IP adress

adb connect 10.0.0.108

COMPILED APK!!!!!!!!!!
buildozer -v android debug

holy crap it deploys!!!!!!!!!!!
buildozer android debug deploy run

* clean environment
buildozer -v android clean

You can combine the compilation with the deployment:
buildozer -v android debug deploy run logcat

********alpine 3.6**********
add community and edge to repo
apk add mpv-libs mpv py-pip cython
* this adds 0.26.r0 (which is the latest release)

apk add sdl2 sdl2_ttf sdl2_image sdl2_mixer sdl2-dev sdl2_ttf-dev sdl2_image-dev sdl2_mixer-dev
apk add gstreamer1 gstreamer1-dev 
# stuff for whipper
apk add flac sox swig cdparanoia py-gobject libcddb libcdio-dev
pip install kivy


********* xubuntu 17.04 lts **********
sudo dd if=xubuntu-17.04-desktop-amd64.iso of=/dev/sdb

dl updates while install and 3rd party mp3 etc

autologin

-----

sudo apt-get install openssh-server

sudo apt-get install python-pip

# sudo apt-get install python-pip cython libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev libsdl2-dev libgstreamer1.0-dev
# for dev purposes
sudo apt-get install git
git clone https://github.com/MediaKraken/MediaKraken_Deployment
git checkout dev-0.7.2
pip install the requirements file

#sudo add-apt-repository ppa:kivy-team/kivy
#sudo apt-get update
#sudo apt-get install python-kivy

sudo apt-get install mpv libmpv1


sudo apt-get install python-pyqt5 pyqt5-dev-tools

# for mpv kivy thingie
libmpv-dev


pip install qt5reactor


# maybe not needed after mpv
python-pyqt5.qtmultimedia







