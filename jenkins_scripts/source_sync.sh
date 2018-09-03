# broadcast
cp /home/metaman/MediaKraken_Deployment/source/subprogram_broadcast.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenBroadcast/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenBroadcast/src/.

# cron
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenCron/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenCron/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/network /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenCron/src/.
cp /home/metaman/MediaKraken_Deployment/source/subprogram_cron_checker.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenCron/src/.

# devicescanner
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDevicescan/src/.
cp /home/metaman/MediaKraken_Deployment/source/main_hardware_discover.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDevicescan/src/.

# download
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDownload/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDownload/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/network /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDownload/src/.
cp /home/metaman/MediaKraken_Deployment/source/main_download.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenDownload/src/.

# ffprobe
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenFFProbe/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenFFProbe/src/.
cp /home/metaman/MediaKraken_Deployment/source/subprogram_ffprobe_metadata.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenFFProbe/src/.

# load game/metadata
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenGameData/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenGameData/src/.
cp /home/metaman/MediaKraken_Deployment/source/subprogram_metadata_games.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenGameData/src/.

# hardware
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenHardware/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenHardware/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/network /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenHardware/src/.
cp /home/metaman/MediaKraken_Deployment/source/main_hardware.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenHardware/src/.

# metadata
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/metadata /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/source/main_server_metadata_api.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/source/main_server_metadata_api_worker.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/source/build_image_directory.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/source/build_trailer_directory.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/source/subprogram*.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.
cp /home/metaman/MediaKraken_Deployment/source/bulk_themoviedb_netfetch.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenMetadata/src/.

# prefetch tmdb
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenPrefetchTMDB/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenPrefetchTMDB/src/.
cp /home/metaman/MediaKraken_Deployment/source/bulk_themoviedb_netfetch.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenPrefetchTMDB/src/.

# prefetch tvmaze
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenPrefetchTVMaze/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenPrefetchTVMaze/src/.
cp /home/metaman/MediaKraken_Deployment/source/bulk_tvmaze_netfetch.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenPrefetchTVMaze/src/.

# reactor
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenReactor/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenReactor/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/network /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenReactor/src/.
cp /home/metaman/MediaKraken_Deployment/source/subprogram*.py  /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenReactor/src/.

# ripper
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenRipper/src/.
cp /home/metaman/MediaKraken_Deployment/source/main_ripper.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenRipper/src/.

# roku thumb
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenRokuThumb/src/.
cp /home/metaman/MediaKraken_Deployment/source/subprogram_roku_thumbnail_generate.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenRokuThumb/src/.

# server
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/network /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/source/db_create_update.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/source/db_update_version.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/source/main_server.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/source/main_server_link.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.
cp /home/metaman/MediaKraken_Deployment/source/subprogram*.py  /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenServer/src/.

# slave
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.
cp /home/metaman/MediaKraken_Deployment/source/main_server_slave.py /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenSlave/src/.

# webserver
cp -R /home/metaman/MediaKraken_Deployment/source/common /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/database /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/network /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
cp -R /home/metaman/MediaKraken_Deployment/source/web_app /home/metaman/MediaKraken_Deployment/docker/alpine/ComposeMediaKrakenWebServer/src/.
