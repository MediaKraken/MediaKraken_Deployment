git pull
./source_sync.sh
docker-compose build

cd ComposeMediaKrakenNvidia
docker build -t mediakraken/mkbasenvidia .

cd ../ComposeMediaKrakenBaseFFMPEG
docker build -t mediakraken/mkbaseffmpeg .

cd ../ComposeMediaKrakenBaseFFMPEGNvidia
docker build -t mediakraken/mkbaseffmpegnvidia .

cd ../ComposeMediaKrakenSlave
docker build -t mediakraken/mkslave .

cd ../ComposeMediaKrakenSlaveNvidia
docker build -t mediakraken/mkslavenvidia .


