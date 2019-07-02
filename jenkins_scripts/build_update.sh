git pull
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
docker build -t mediakraken/mkbase38py3:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

cd ../ComposeMediaKrakenBase39Py3
docker build -t mediakraken/mkbase39py3:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

cd ../ComposeMediaKrakenBase310Py3
docker build -t mediakraken/mkbase310py3:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# Build the base FFMPEG from base images
# Image that simply has ffmpeg and ffprobe for use by other containers.
cd ../ComposeMediaKrakenBaseFFMPEG
docker build -t mediakraken/mkbaseffmpeg:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the base node
# Adds NODE to the base ffmpeg and ffprobe.
cd ../ComposeMediaKrakenBaseNodeFFMPEG
docker build -t mediakraken/mkbasenodeffmpeg:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# this will include the nvidia cuda/nvec/driver
cd ../ComposeMediaKrakenBaseFFMPEGUbuntu
docker build -t mediakraken/mkbaseffmpegubuntu:dev --build-arg PIPMIRROR=pypi.python.org

# build the base node for ubuntu
# Adds NODE to the base ffmpeg and ffprobe for ubuntu
cd ../ComposeMediaKrakenBaseNodeFFMPEGUbuntu:dev
docker build -t mediakraken/mkbasenodeffmpegubuntu --build-arg PIPMIRROR=pypi.python.org .

# build the base NODE image from alpine 3.9
cd ../ComposeMediaKrakenBaseNodeJS
docker build -t mediakraken/mkbasenode:dev --build-arg PIPMIRROR=pypi.python.org .

# build the device scan
# When run it will scan the HOST network for HDHomerun, Chromecast and Roku devices.
cd ../ComposeMediaKrakenDevicescan
docker build -t mediakraken/mkdevicescan:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the openldap
#cd ../ComposeMediaKrakenOpenLDAP
#docker build -t mediakraken/mkopenldap:dev .

# build the tmdb prefetch
cd ../ComposeMediaKrakenPrefetchTMDB
docker build -t mediakraken/mkprefetchtmdb:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the tvmaze prefetch
cd ../ComposeMediaKrakenPrefetchTVMaze
docker build -t mediakraken/mkprefetchtvmaze:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the game metadata
cd ../ComposeMediaKrakenGameData
docker build -t mediakraken/mkgamedata:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# Build the base slave images from other base images (basenodeffmpeg)
cd ../ComposeMediaKrakenSlave
docker build -t mediakraken/mkslave:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# Build the base slave images from other base images (basenodeffmpeg) for ubuntu
cd ../ComposeMediaKrakenSlaveUbuntu
docker build -t mediakraken/mkslaveubuntu:dev --build-arg PIPMIRROR=pypi.python.org .

# Build the base twitch recorder
cd ../ComposeMediaKrakenTwitchRecordUser
docker build -t mediakraken/mktwitchrecorduser:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# Build the castpy
cd ../ComposeMediaKrakenCastImage
docker build -t mediakraken/mkcastimage:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# Build the grapesjs
cd ../ComposeMediaKrakenGrapesJS
docker build -t mediakraken/mkgrapesjs:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# move here so all the "deps" are built first
docker-compose build --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org

# containers here and later are "standalone" with no deps

# build the retroarch web
cd ../ComposeMediaKrakenRetroArchWeb
docker build -t mediakraken/mkretroarchweb:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the dosbox web
cd ../ComposeMediaKrakenDosBoxWeb
docker build -t mediakraken/mkdosboxweb:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the mumble
cd ../ComposeMediaKrakenMumble
docker build -t mediakraken/mkmumble:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the mediabrainz
cd ../ComposeMediaKrakenMusicBrainz
docker build -t mediakraken/mkmusicbrainz:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the inotify
cd ../ComposeMediaKrakenInotify
docker build -t mediakraken/mkinotify:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the teamspeak
cd ../ComposeMediaKrakenTeamspeak
docker build -t mediakraken/mkteamspeak:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# build the transmission
cd ../ComposeMediaKrakenTransmission
docker build -t mediakraken/mktransmission:dev --build-arg ALPMIRROR=dl-cdn.alpinelinux.org --build-arg PIPMIRROR=pypi.python.org .

# nuke old images (commented due to base ffmpeg)
#../../purge_images_none.sh

# retag all the images - need to back out of docker/alpine as well as docker directory for container
../../../jenkins_scripts/dockerhub_deploy/tag_rename_images.sh
