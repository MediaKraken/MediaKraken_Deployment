docker-compose down
docker-compose pull
docker pull th-dockerhub-1:5000/mediakraken/mkbasecuda
docker pull th-dockerhub-1:5000/mediakraken/mkbaseffmpeg
docker pull th-dockerhub-1:5000/mediakraken/mkdebug
docker pull th-dockerhub-1:5000/mediakraken/mkdevicescan
docker pull th-dockerhub-1:5000/mediakraken/mkelk
docker pull th-dockerhub-1:5000/mediakraken/mkmusicbrainz
docker pull th-dockerhub-1:5000/mediakraken/mkmumble
docker pull th-dockerhub-1:5000/mediakraken/mknginxrtmp
docker pull th-dockerhub-1:5000/mediakraken/mkopenldap
docker pull th-dockerhub-1:5000/mediakraken/mkslave
docker pull th-dockerhub-1:5000/mediakraken/mkstream
docker pull th-dockerhub-1:5000/mediakraken/mkteamspeak
docker pull th-dockerhub-1:5000/mediakraken/mktransmission
docker pull th-dockerhub-1:5000/mediakraken/mkwireshark
docker pull dpage/pgadmin4
docker pull portainer/portainer
./purge_images_none.sh
docker-compose up -d
