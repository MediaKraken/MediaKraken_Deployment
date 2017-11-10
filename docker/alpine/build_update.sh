git pull
./source_sync.sh
docker-compose down
docker-compose build

# Build the base pypy
cd alpine-pypy/2
docker build -t mediakraken/mkbasepypy .
cd ../

# base python 2 images
cd ../ComposeMediaKrakenBase34
docker build -t mediakraken/mkbase34 .

cd ../ComposeMediaKrakenBase35
docker build -t mediakraken/mkbase35 .

cd ../ComposeMediaKrakenBase36
docker build -t mediakraken/mkbase36 .

# base python 3 images
cd ../ComposeMediaKrakenBase34Py3
docker build -t mediakraken/mkbase34py3 .

cd ../ComposeMediaKrakenBase35Py3
docker build -t mediakraken/mkbase35py3 .

cd ../ComposeMediaKrakenBase36Py3
docker build -t mediakraken/mkbase36py3 .

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

# nuke old images (commented due to base ffmpeg)
#../../purge_images_none.sh
