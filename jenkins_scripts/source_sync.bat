:: broadcast
xcopy ..\source\subprogram_broadcast.py ..\docker\alpine\ComposeMediaKrakenBroadcast\src\. /y /e /h
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenBroadcast\src\. /y /e /h

:: cast images
xcopy ..\..\castpy\cast.py ..\docker\alpine\ComposeMediaKrakenCastImage\src\. /y /e /h

:: cron
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenCron\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenCron\src\. /y /e /h
xcopy ..\source\network ..\docker\alpine\ComposeMediaKrakenCron\src\. /y /e /h
xcopy ..\source\subprogram_cron_checker.py ..\docker\alpine\ComposeMediaKrakenCron\src\. /y /e /h

:: devicescanner
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenDevicescan\src\. /y /e /h
xcopy ..\source\main_hardware_discover.py ..\docker\alpine\ComposeMediaKrakenDevicescan\src\. /y /e /h

:: download
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenDownload\src\/. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenDownload\src\. /y /e /h
xcopy ..\source\network ..\docker\alpine\ComposeMediaKrakenDownload\src\. /y /e /h
xcopy ..\source\main_download.py ..\docker\alpine\ComposeMediaKrakenDownload\src\. /y /e /h

:: ffprobe
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenFFProbe\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenFFProbe\src\. /y /e /h
xcopy ..\source\subprogram_ffprobe_metadata.py ..\docker\alpine\ComposeMediaKrakenFFProbe\src\. /y /e /h

:: load game/metadata
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenGameData\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenGameData\src\. /y /e /h
xcopy ..\source\subprogram_metadata_games.py ..\docker\alpine\ComposeMediaKrakenGameData\src\. /y /e /h

:: hardware
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenHardware\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenHardware\src\. /y /e /h
xcopy ..\source\network ..\docker\alpine\ComposeMediaKrakenHardware\src\. /y /e /h
xcopy ..\source\main_hardware.py ..\docker\alpine\ComposeMediaKrakenHardware\src\. /y /e /h

:: metadata
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenMetadata\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenMetadata\src\. /y /e /h
xcopy ..\source\metadata ..\docker\alpine\ComposeMediaKrakenMetadata\src/. /y /e /h
xcopy ..\source\main_server_metadata_api.py ..\docker\alpine\ComposeMediaKrakenMetadata\src\. /y /e /h
xcopy ..\source\main_server_metadata_api_worker.py ..\docker\alpine\ComposeMediaKrakenMetadata\src\. /y /e /h
xcopy ..\source\build_image_directory.py ..\docker\alpine\ComposeMediaKrakenMetadata\src\. /y /e /h
xcopy ..\source\build_trailer_directory.py ..\docker\alpine\ComposeMediaKrakenMetadata\src\. /y /e /h
xcopy ..\source\subprogram*.py ..\docker\alpine\ComposeMediaKrakenMetadata\src\. /y /e /h

:: prefetch tmdb
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenPrefetchTMDB\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenPrefetchTMDB\src\. /y /e /h
xcopy ..\source\bulk_themoviedb_netfetch.py ..\docker\alpine\ComposeMediaKrakenPrefetchTMDB\src\. /y /e /h

:: prefetch tvmaze
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenPrefetchTVMaze\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenPrefetchTVMaze\src\. /y /e /h
xcopy ..\source\bulk_tvmaze_netfetch.py ..\docker\alpine\ComposeMediaKrakenPrefetchTVMaze\src\. /y /e /h

:: pika
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenPika\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenPika\src\. /y /e /h
xcopy ..\source\network ..\docker\alpine\ComposeMediaKrakenPika\src\. /y /e /h
xcopy ..\source\metadata ..\docker\alpine\ComposeMediaKrakenPika\src/. /y /e /h
xcopy ..\source\subprogram*.py  ..\docker\alpine\ComposeMediaKrakenPika\src\. /y /e /h

:: reactor
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenReactor\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenReactor\src\. /y /e /h
xcopy ..\source\network ..\docker\alpine\ComposeMediaKrakenReactor\src\. /y /e /h
xcopy ..\source\subprogram*.py  ..\docker\alpine\ComposeMediaKrakenReactor\src\. /y /e /h

:: ripper
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenRipper\src\. /y /e /h
xcopy ..\source\main_ripper.py ..\docker\alpine\ComposeMediaKrakenRipper\src\. /y /e /h

:: roku thumb
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenRokuThumb\src\. /y /e /h
xcopy ..\source\subprogram_roku_thumbnail_generate.py ..\docker\alpine\ComposeMediaKrakenRokuThumb\src\. /y /e /h

:: server
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenServer\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenServer\src\. /y /e /h
xcopy ..\source\network ..\docker\alpine\ComposeMediaKrakenServer\src\. /y /e /h
xcopy ..\source\db_create_update.py ..\docker\alpine\ComposeMediaKrakenServer\src\. /y /e /h
xcopy ..\source\db_update_version.py ..\docker\alpine\ComposeMediaKrakenServer\src\. /y /e /h
xcopy ..\source\main_server.py ..\docker\alpine\ComposeMediaKrakenServer\src\. /y /e /h
xcopy ..\source\main_server_link.py ..\docker\alpine\ComposeMediaKrakenServer\src\. /y /e /h
xcopy ..\source\subprogram*.py  ..\docker\alpine\ComposeMediaKrakenServer\src\. /y /e /h

:: slave
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenSlave\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenSlave\src\. /y /e /h
xcopy ..\source\main_server_slave.py ..\docker\alpine\ComposeMediaKrakenSlave\src\. /y /e /h

:: webserver
xcopy ..\source\common ..\docker\alpine\ComposeMediaKrakenWebServer\src\. /y /e /h
xcopy ..\source\database ..\docker\alpine\ComposeMediaKrakenWebServer\src\. /y /e /h
xcopy ..\source\network ..\docker\alpine\ComposeMediaKrakenWebServer\src\. /y /e /h
xcopy ..\source\web_app ..\docker\alpine\ComposeMediaKrakenWebServer\src\. /y /e /h
