git pull
./source_sync.sh
docker-compose build
cd ComposeMediaKrakenSlave
docker build -t mediakraken/mkslave .