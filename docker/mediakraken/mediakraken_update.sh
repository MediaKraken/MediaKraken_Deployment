docker-compose down
docker-compose pull
docker pull mediakraken/mkbaseffmpeg
docker pull mediakraken/mkdevicescan
docker pull mediakraken/mkelk
docker pull mediakraken/mkgamedata
docker pull mediakraken/mkmusicbrainz
docker pull mediakraken/mkmumble
docker pull mediakraken/mknginxrtmp
docker pull mediakraken/mkopenldap
docker pull mediakraken/mkpgadmin
docker pull mediakraken/mkslave
docker pull mediakraken/mkstream
docker pull mediakraken/mkteamspeak
docker pull mediakraken/mktransmission
docker pull mediakraken/mkwireshark
docker pull portainer/portainer
./purge_images_none.sh
docker-compose up -d
