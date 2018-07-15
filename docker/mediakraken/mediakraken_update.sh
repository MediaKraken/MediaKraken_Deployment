docker-compose down
docker-compose pull
docker pull mediakraken/mkbasecuda
docker pull mediakraken/mkbaseffmpeg
docker pull mediakraken/mkdevicescan
docker pull mediakraken/mkelk
docker pull mediakraken/mkmusicbrainz
docker pull mediakraken/mkmumble
docker pull mediakraken/mknginxrtmp
docker pull mediakraken/mkopenldap
docker pull mediakraken/mkslave
docker pull mediakraken/mkstream
docker pull mediakraken/mkteamspeak
docker pull mediakraken/mktransmission
docker pull mediakraken/mkwireshark
docker pull dpage/pgadmin4
docker pull portainer/portainer
./purge_images_none.sh
docker-compose up -d
