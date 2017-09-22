git pull
./source_sync.sh
docker-compose down
docker-compose build

# Build the base FFMPEG from base images
cd ComposeMediaKrakenBaseFFMPEG
docker build -t mediakraken/mkbaseffmpeg .

# Build the base Nvidia Cuda
cd ../ComposeMediaKrakenBaseNvidia
docker build -t mediakraken/mkbasenvidia .

cd ../ComposeMediaKrakenBaseNvidiaDebian
docker build -t mediakraken/mkbasenvidiadebian .

cd ../ComposeMediaKrakenBaseFFMPEGNvidia
#docker build -t mediakraken/mkbaseffmpegnvidia .

cd ../ComposeMediaKrakenBaseFFMPEGNvidiaDebian
docker build -t mediakraken/mkbaseffmpegnvidiadebian .

# Build the base slave images from other base images
cd ../ComposeMediaKrakenSlave
docker build -t mediakraken/mkslave .

#cd ../ComposeMediaKrakenSlaveNvidia
#docker build -t mediakraken/mkslavenvidia .

cd ../ComposeMediaKrakenSlaveNvidiaDebian
docker build -t mediakraken/mkslavenvidiadebian .

# Build the nginx RTMP
cd ../ComposeMediaKrakenNginxRTMP
docker build -t mediakraken/mknginxrtmp .

# build the mediabrainz
cd ../ComposeMediaKrakenMusicBrainz
docker build -t mediakraken/mkmusicbrainz .

# nuke old images
../../purge_images_none.sh
