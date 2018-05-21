git pull
./source_sync.sh

# must move base dir so the docker-compose commands work
cd /home/metaman/MediaKraken_Deployment/docker/alpine

docker-compose down
docker-compose build

# Build the base pypy
cd ComposeMediaKrakenBasePYPY/2
docker build -t mediakraken/mkbasepypy2 .

cd ../ComposeMediaKrakenBasePYPY/3
docker build -t mediakraken/mkbasepypy3 .
# needs to be here to exit out of 2/3 level
cd ../

# base python 2 images
cd ../ComposeMediaKrakenBase34
docker build -t mediakraken/mkbase34 .

cd ../ComposeMediaKrakenBase35
docker build -t mediakraken/mkbase35 .

cd ../ComposeMediaKrakenBase36
docker build -t mediakraken/mkbase36 .

cd ../ComposeMediaKrakenBase37
docker build -t mediakraken/mkbase37 .

# base python 3 images
cd ../ComposeMediaKrakenBase34Py3
docker build -t mediakraken/mkbase34py3 .

cd ../ComposeMediaKrakenBase35Py3
docker build -t mediakraken/mkbase35py3 .

cd ../ComposeMediaKrakenBase36Py3
docker build -t mediakraken/mkbase36py3 .

cd ../ComposeMediaKrakenBase37Py3
docker build -t mediakraken/mkbase37py3 .

# Build the base cuba from alpine
cd ../ComposeMediaKrakenBaseCuda
docker build -t mediakraken/mkbasecuda .

# Build the base FFMPEG from base images
cd ../ComposeMediaKrakenBaseFFMPEG
docker build -t mediakraken/mkbaseffmpeg .

# Build the base Nvidia Cuda
cd ../ComposeMediaKrakenBaseNvidia
#docker build -t mediakraken/mkbasenvidia .

cd ../ComposeMediaKrakenBaseNvidiaDebian
#docker build -t mediakraken/mkbasenvidiadebian .

cd ../ComposeMediaKrakenBaseFFMPEGNvidia
#docker build -t mediakraken/mkbaseffmpegnvidia .

cd ../ComposeMediaKrakenBaseFFMPEGNvidiaDebian
#docker build -t mediakraken/mkbaseffmpegnvidiadebian .

# Build the base slave images from other base images
cd ../ComposeMediaKrakenSlave
docker build -t mediakraken/mkslave .

cd ../ComposeMediaKrakenSlaveNvidia
#docker build -t mediakraken/mkslavenvidia .

cd ../ComposeMediaKrakenSlaveNvidiaDebian
#docker build -t mediakraken/mkslavenvidiadebian .

# Build the nginx RTMP
cd ../ComposeMediaKrakenNginxRTMP
docker build -t mediakraken/mknginxrtmp .

# build the mediabrainz
cd ../ComposeMediaKrakenMusicBrainz
docker build -t mediakraken/mkmusicbrainz .

# build the teamspeak
cd ../ComposeMediaKrakenTeamspeak
docker build -t mediakraken/mkteamspeak .

# build the transmission
cd ../ComposeMediaKrakenTransmission
docker build -t mediakraken/mktransmission .

# build the device scan
cd ../ComposeMediaKrakenDevicescan
docker build -t mediakraken/mkdevicescan .

# build the openldap
cd ../ComposeMediaKrakenOpenLDAP
docker build -t mediakraken/mkopenldap .

# build the mumble
cd ../ComposeMediaKrakenMumble
docker build -t mediakraken/mkmumble .

# build the elk
cd ../ComposeMediaKrakenELK
docker build -t mediakraken/mkelk .

# build the debug
cd ../ComposeMediaKrakenDebug
docker build -t mediakraken/mkdebug .

# build the wireshark
cd ../ComposeMediaKrakenWireshark
docker build -t mediakraken/mkwireshark .

# build the tmdb prefetch
cd ../ComposeMediaKrakenPrefetchTMDB
docker build -t mediakraken/mkprefetchtmdb .

# build the tvamze prefetch
cd ../ComposeMediaKrakenPrefetchTVMaze
docker build -t mediakraken/mkprefetchtvmaze .

# build the base node
cd ../ComposeMediaKrakenBaseNodeFFMPEG
docker build -t mediakraken/mkbasenodeffmpeg .

# nuke old images (commented due to base ffmpeg)
#../../purge_images_none.sh
