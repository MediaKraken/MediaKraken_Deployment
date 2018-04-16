docker-compose down
docker-compose pull
docker pull mediakraken/mkdevicescan
docker pull mediakraken/mkelk
docker pull mediakraken/mkmusicbrainz
docker pull mediakraken/mkmumble
docker pull mediakraken/mkopenldap
docker pull dpage/pgadmin4
docker pull portainer/portainer
./purge_images_none.sh
docker-compose up -d
