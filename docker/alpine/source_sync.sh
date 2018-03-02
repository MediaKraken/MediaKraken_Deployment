# broadcast
cp /home/metaman/MediaKraken_Deployment/subprogram_broadcast.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenBroadcast/src/.
cp -R /home/metaman/MediaKraken_Deployment/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenBroadcast/src/.

# devicescanner
cp -R /home/metaman/MediaKraken_Deployment/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDevicescan/src/.
cp /home/metaman/MediaKraken_Deployment/main_hardware_discover.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDevicescan/src/.

# download
cp -R /home/metaman/MediaKraken_Deployment/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDownload/src/.
cp /home/metaman/MediaKraken_Deployment/main_download.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDownload/src/.

# metadata
cp -R /home/metaman/MediaKraken_Deployment/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp -R /home/metaman/MediaKraken_Deployment/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp -R /home/metaman/MediaKraken_Deployment/metadata /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/main_server_metadata_api.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/main_server_metadata_api_worker.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/main_server_metadata_api_worker_image.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/build_image_directory.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/build_trailer_directory.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/subprogram*.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/bulk_themoviedb_netfetch.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.

# ripper
cp -R /home/metaman/MediaKraken_Deployment/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenRipper/src/.
cp /home/metaman/MediaKraken_Deployment/main_ripper.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenRipper/src/.

# server
cp -R /home/metaman/MediaKraken_Deployment/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/network /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/db_create_update.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/db_update_version.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/main_server.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/main_server_link.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/subprogram*.py  /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.

# slave
cp -R /home/metaman/MediaKraken_Deployment/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.
cp -R /home/metaman/MediaKraken_Deployment/common/common_docker.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/stream2chromecast/common/.
cp -R /home/metaman/MediaKraken_Deployment/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.
cp /home/metaman/MediaKraken_Deployment/main_server_slave.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.
cp /home/metaman/MediaKraken_Deployment/subprogram_ffprobe_metadata.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.

# webserver
cp -R /home/metaman/MediaKraken_Deployment/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/network /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/web_app /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
