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
