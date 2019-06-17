# rsync the git checkout to local code (so dont' have to commit, etc)
rsync -r ../../MediaKraken_Deployment/* ../../MediaKraken_Docker_Build

cd ../../MediaKraken_Docker_Build/jenkins_scripts

./source_sync.sh
# ./webcode_minify/minify-web-scripts.sh

# must move base dir so the docker-compose commands work
cd ../docker/alpine

docker-compose down

# Build the base pypy
# leave this here so all the cd ../ work later
cd ComposeMediaKrakenBasePYPY/2
#docker build -t mediakraken/mkbasepypy2 .

#cd ../ComposeMediaKrakenBasePYPY/3
#docker build -t mediakraken/mkbasepypy3 .
# needs to be here to exit out of 2/3 level
cd ../

# base python 3 images
cd ../ComposeMediaKrakenBase38Py3
docker build -t mediakraken/mkbase38py3 --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

cd ../ComposeMediaKrakenBase39Py3
docker build -t mediakraken/mkbase39py3 --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# Build the base FFMPEG from base images
# Image that simply has ffmpeg and ffprobe for use by other containers.
cd ../ComposeMediaKrakenBaseFFMPEG
docker build -t mediakraken/mkbaseffmpeg --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the base node
# Adds NODE to the base ffmpeg and ffprobe.
cd ../ComposeMediaKrakenBaseNodeFFMPEG
docker build -t mediakraken/mkbasenodeffmpeg --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# this will include the nvidia cuda/nvec/driver
cd ../ComposeMediaKrakenBaseFFMPEGUbuntu
docker build -t mediakraken/mkbaseffmpegubuntu --build-arg PIPMIRROR=th-pypi-1 

# build the base node for ubuntu
# Adds NODE to the base ffmpeg and ffprobe for ubuntu
cd ../ComposeMediaKrakenBaseNodeFFMPEGUbuntu
docker build -t mediakraken/mkbasenodeffmpegubuntu --build-arg PIPMIRROR=th-pypi-1 .

# build the base NODE image from alpine 3.9
cd ../ComposeMediaKrakenBaseNodeJS
docker build -t mediakraken/mkbasenode --build-arg PIPMIRROR=th-pypi-1 .

# build the device scan
# When run it will scan the HOST network for HDHomerun, Chromecast and Roku devices.
cd ../ComposeMediaKrakenDevicescan
docker build -t mediakraken/mkdevicescan --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the openldap
#cd ../ComposeMediaKrakenOpenLDAP
#docker build -t mediakraken/mkopenldap .

# build the tmdb prefetch
cd ../ComposeMediaKrakenPrefetchTMDB
docker build -t mediakraken/mkprefetchtmdb --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the tvmaze prefetch
cd ../ComposeMediaKrakenPrefetchTVMaze
docker build -t mediakraken/mkprefetchtvmaze --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the game metadata
cd ../ComposeMediaKrakenGameData
docker build -t mediakraken/mkgamedata --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# Build the base slave images from other base images (basenodeffmpeg)
cd ../ComposeMediaKrakenSlave
docker build -t mediakraken/mkslave --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# Build the base slave images from other base images (basenodeffmpeg) for ubuntu
cd ../ComposeMediaKrakenSlaveUbuntu
docker build -t mediakraken/mkslaveubuntu --build-arg PIPMIRROR=th-pypi-1 .

# Build the base twitch recorder
cd ../ComposeMediaKrakenTwitchRecordUser
docker build -t mediakraken/mktwitchrecorduser --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# Build the castpy
cd ../ComposeMediaKrakenCastImage
docker build -t mediakraken/mkcastimage --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# Build the grapesjs
cd ../ComposeMediaKrakenGrapesJS
docker build -t mediakraken/mkgrapesjs --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# move here so all the "deps" are built first
docker-compose build

# containers here and later are "standalone" with no deps

# build the dosbox
cd ../ComposeMediaKrakenDosBox
docker build -t mediakraken/mkdosbox --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the elk
cd ../ComposeMediaKrakenELK
docker build -t mediakraken/mkelk --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the mumble
cd ../ComposeMediaKrakenMumble
docker build -t mediakraken/mkmumble --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the mediabrainz
cd ../ComposeMediaKrakenMusicBrainz
docker build -t mediakraken/mkmusicbrainz --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the pgadmin4
cd ../ComposeMediaKrakenPgAdmin4
docker build -t mediakraken/mkpgadmin --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the inotify
cd ../ComposeMediaKrakenInotify
docker build -t mediakraken/mkinotify --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the teamspeak
cd ../ComposeMediaKrakenTeamspeak
docker build -t mediakraken/mkteamspeak --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the transmission
cd ../ComposeMediaKrakenTransmission
docker build -t mediakraken/mktransmission --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# build the wireshark
cd ../ComposeMediaKrakenWireshark
docker build -t mediakraken/mkwireshark --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=th-pypi-1 .

# nuke old images (commented due to base ffmpeg)
#../../purge_images_none.sh

# retag all the images - need to back out of docker/alpine as well as docker directory for container
../../../jenkins_scripts/dockerhub_deploy/tag_rename_images.sh
