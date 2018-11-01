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

# base python 2 images
#cd ../ComposeMediaKrakenBase37
#docker build -t mediakraken/mkbase37 .

# base python 3 images
#cd ../ComposeMediaKrakenBase37Py3
#docker build -t mediakraken/mkbase37py3 .

# base python 3 images
cd ../ComposeMediaKrakenBase38Py3
docker build -t mediakraken/mkbase38py3 --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# Build the base cuda from alpine
#cd ../ComposeMediaKrakenBaseCuda
#docker build -t mediakraken/mkbasecuda .

# Build the base FFMPEG from base images
# Image that simply has ffmpeg and ffprobe for use by other containers.
cd ../ComposeMediaKrakenBaseFFMPEG
docker build -t mediakraken/mkbaseffmpeg --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the base node
# Adds NODE to the base ffmpeg and ffprobe.
cd ../ComposeMediaKrakenBaseNodeFFMPEG
docker build -t mediakraken/mkbasenodeffmpeg --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the device scan
# When run it will scan the HOST network for HDHomerun, Chromecast and Roku devices.
cd ../ComposeMediaKrakenDevicescan
docker build -t mediakraken/mkdevicescan --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the openldap
#cd ../ComposeMediaKrakenOpenLDAP
#docker build -t mediakraken/mkopenldap .

# build the tmdb prefetch
cd ../ComposeMediaKrakenPrefetchTMDB
docker build -t mediakraken/mkprefetchtmdb --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the tvmaze prefetch
cd ../ComposeMediaKrakenPrefetchTVMaze
docker build -t mediakraken/mkprefetchtvmaze --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the game metadata
cd ../ComposeMediaKrakenGameData
docker build -t mediakraken/mkgamedata --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# Build the base slave images from other base images (basenodeffmpeg)
cd ../ComposeMediaKrakenSlave
docker build -t mediakraken/mkslave --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# Build the base twitch recorder
cd ../ComposeMediaKrakenTwitchRecordUser
docker build -t mediakraken/mktwitchrecorduser --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# Build the castpy
cd ../ComposeMediaKrakenCastImage
docker build -t mediakraken/mkcastimage --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

#cd ../ComposeMediaKrakenSlaveNvidia
#docker build -t mediakraken/mkslavenvidia .

#cd ../ComposeMediaKrakenSlaveNvidiaDebian
#docker build -t mediakraken/mkslavenvidiadebian .

# Build the base Nvidia Cuda
#cd ../ComposeMediaKrakenBaseNvidia
#docker build -t mediakraken/mkbasenvidia .

#cd ../ComposeMediaKrakenBaseNvidiaDebian
#docker build -t mediakraken/mkbasenvidiadebian .

#cd ../ComposeMediaKrakenBaseFFMPEGNvidia
#docker build -t mediakraken/mkbaseffmpegnvidia .

#cd ../ComposeMediaKrakenBaseFFMPEGNvidiaDebian
#docker build -t mediakraken/mkbaseffmpegnvidiadebian .

# move here so all the "deps" are built first
docker-compose build

# containers here and later are "standalone" with no deps

# build the elk
cd ../ComposeMediaKrakenELK
docker build -t mediakraken/mkelk --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the mumble
cd ../ComposeMediaKrakenMumble
docker build -t mediakraken/mkmumble --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the mediabrainz
cd ../ComposeMediaKrakenMusicBrainz
docker build -t mediakraken/mkmusicbrainz --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the pgadmin4
cd ../ComposeMediaKrakenPgAdmin4
docker build -t mediakraken/mkpgadmin --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the inotify
cd ../ComposeMediaKrakenInotify
docker build -t mediakraken/mkinotify --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the stream container
#cd ../ComposeMediaKrakenStream
#docker build -t mediakraken/mkstream .

# build the teamspeak
cd ../ComposeMediaKrakenTeamspeak
docker build -t mediakraken/mkteamspeak --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the transmission
cd ../ComposeMediaKrakenTransmission
docker build -t mediakraken/mktransmission --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the wireshark
cd ../ComposeMediaKrakenWireshark
docker build -t mediakraken/mkwireshark --build-arg ALPMIRROR=10.0.0.122 --build-arg PIPMIRROR=pypi.python.org .

# build the tvheadend
cd ../ComposeMediaKrakenTvheadend
#docker build -t mediakraken/mktvheadend .

# nuke old images (commented due to base ffmpeg)
#../../purge_images_none.sh
