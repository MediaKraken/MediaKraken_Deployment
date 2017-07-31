# broadcast
cp /home/spoot/MediaKraken_Deployment/subprogram_broadcast.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenBroadcast/src/.
cp -R /home/spoot/MediaKraken_Deployment/common /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenBroadcast/src/.

# devicescanner
cp -R /home/spoot/MediaKraken_Deployment/common /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDevicescan/src/.
cp /home/spoot/MediaKraken_Deployment/main_hardware_discover.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDevicescan/src/.

# metadata
cp -R /home/spoot/MediaKraken_Deployment/common /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp -R /home/spoot/MediaKraken_Deployment/database /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp -R /home/spoot/MediaKraken_Deployment/metadata /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/spoot/MediaKraken_Deployment/main_server_metadata_api.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/spoot/MediaKraken_Deployment/main_server_metadata_api_worker.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/spoot/MediaKraken_Deployment/main_server_metadata_api_worker_image.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/spoot/MediaKraken_Deployment/build_image_directory.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/spoot/MediaKraken_Deployment/build_trailer_directory.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/spoot/MediaKraken_Deployment/subprogram*.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.

# metdata builder
cp -R /home/spoot/MediaKraken_Deployment/common /home/spoot/MediaKraken_Deployment/docker/alpine_preload/ComposeMediaKrakenMetadataPreload/src/.
cp -R /home/spoot/MediaKraken_Deployment/database /home/spoot/MediaKraken_Deployment/docker/alpine_preload/ComposeMediaKrakenMetadataPreload/src/.
cp -R /home/spoot/MediaKraken_Deployment/metadata /home/spoot/MediaKraken_Deployment/docker/alpine_preload/ComposeMediaKrakenMetadataPreload/src/.
cp /home/spoot/MediaKraken_Deployment/bulk_themoviedb_netfetch.py  /home/spoot/MediaKraken_Deployment/docker/alpine_preload/ComposeMediaKrakenMetadataPreload/src/.

# server
cp -R /home/spoot/MediaKraken_Deployment/common /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp -R /home/spoot/MediaKraken_Deployment/database /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp -R /home/spoot/MediaKraken_Deployment/network /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/spoot/MediaKraken_Deployment/db_create_update.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/spoot/MediaKraken_Deployment/db_update_version.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/spoot/MediaKraken_Deployment/main_server.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/spoot/MediaKraken_Deployment/main_server_link.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/spoot/MediaKraken_Deployment/main_server_trigger.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/spoot/MediaKraken_Deployment/subprogram*.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.

# slave
cp -R /home/spoot/MediaKraken_Deployment/common /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.
cp -R /home/spoot/MediaKraken_Deployment/common/common_docker.py /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/stream2chromecast/common/.
cp -R /home/spoot/MediaKraken_Deployment/database /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.
cp /home/spoot/MediaKraken_Deployment/main_server_slave.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.

# theater 
cp -R /home/spoot/MediaKraken_Deployment/common /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenTheater/src/.
cp -R /home/spoot/MediaKraken_Deployment/network /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenTheater/src/.
cp /home/spoot/MediaKraken_Deployment/main_theater.py  /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenTheater/src/.

# webapi
cp -R /home/spoot/MediaKraken_Deployment/common /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebAPI/src/.
cp -R /home/spoot/MediaKraken_Deployment/database /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebAPI/src/.
cp -R /home/spoot/MediaKraken_Deployment/web_app /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebAPI/src/.

# webserver
cp -R /home/spoot/MediaKraken_Deployment/common /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
cp -R /home/spoot/MediaKraken_Deployment/database /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
cp -R /home/spoot/MediaKraken_Deployment/network /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
cp -R /home/spoot/MediaKraken_Deployment/web_app /home/spoot/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.

