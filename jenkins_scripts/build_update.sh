git pull
./source_sync.sh
./webcode_minify/minify-web-scripts.sh

# must move base dir so the docker-compose commands work
cd /home/metaman/MediaKraken_Deployment/docker/alpine

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
cd ../ComposeMediaKrakenBase37
docker build -t mediakraken/mkbase37 .

# base python 3 images
cd ../ComposeMediaKrakenBase37Py3
docker build -t mediakraken/mkbase37py3 .

# base python 3 images
cd ../ComposeMediaKrakenBase38Py3
docker build -t mediakraken/mkbase38py3 --build-arg ALPMIRROR=10.0.0.122 .

# Build the base cuda from alpine
#cd ../ComposeMediaKrakenBaseCuda
#docker build -t mediakraken/mkbasecuda .

# Build the base FFMPEG from base images
# Image that simply has ffmpeg and ffprobe for use by other containers.
cd ../ComposeMediaKrakenBaseFFMPEG
docker build -t mediakraken/mkbaseffmpeg .

# build the base node
# Adds NODE to the base ffmpeg and ffprobe.
cd ../ComposeMediaKrakenBaseNodeFFMPEG
docker build -t mediakraken/mkbasenodeffmpeg .

# Build the nginx RTMP
#cd ../ComposeMediaKrakenNginxRTMP
#docker build -t mediakraken/mknginxrtmp .

# build the device scan
# When run it will scan the HOST network for HDHomerun, Chromecast and Roku devices.
cd ../ComposeMediaKrakenDevicescan
docker build -t mediakraken/mkdevicescan .

# build the openldap
#cd ../ComposeMediaKrakenOpenLDAP
#docker build -t mediakraken/mkopenldap .

# build the tmdb prefetch
cd ../ComposeMediaKrakenPrefetchTMDB
docker build -t mediakraken/mkprefetchtmdb .

# build the tvamze prefetch
cd ../ComposeMediaKrakenPrefetchTVMaze
docker build -t mediakraken/mkprefetchtvmaze .

# Build the base slave images from other base images (basenodeffmpeg)
cd ../ComposeMediaKrakenSlave
docker build -t mediakraken/mkslave .

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
docker build -t mediakraken/mkelk .

# build the mumble
cd ../ComposeMediaKrakenMumble
docker build -t mediakraken/mkmumble .

# build the mediabrainz
cd ../ComposeMediaKrakenMusicBrainz
docker build -t mediakraken/mkmusicbrainz .

# build the stream container
#cd ../ComposeMediaKrakenStream
#docker build -t mediakraken/mkstream .

# build the teamspeak
cd ../ComposeMediaKrakenTeamspeak
docker build -t mediakraken/mkteamspeak .

# build the transmission
cd ../ComposeMediaKrakenTransmission
docker build -t mediakraken/mktransmission .

# build the wireshark
cd ../ComposeMediaKrakenWireshark
docker build -t mediakraken/mkwireshark .

# build the tvheadend
cd ../ComposeMediaKrakenTvheadend
#docker build -t mediakraken/mktvheadend .

# nuke old images (commented due to base ffmpeg)
#../../purge_images_none.sh
