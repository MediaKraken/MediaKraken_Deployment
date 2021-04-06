#!/bin/bash

SERVER_REMOTE_FILE=http://www.tasharen.com/windward/WWServer.zip
SERVER_TEMP_FILE=/tmp/WWServer.zip
SERVER_LOCAL_FILE=/home/windward/WWServer.zip

echo "Downloading latest dedicated server"

curl -s -o ${SERVER_TEMP_FILE} ${SERVER_REMOTE_FILE}

if [ -f ${SERVER_LOCAL_FILE} ]; then
	echo "Checking local dedicated server is the latest version..."
	SERVER_LOCAL_MD5=`md5sum ${SERVER_LOCAL_FILE} | cut -d' ' -f1`
	SERVER_TEMP_MD5=`md5sum ${SERVER_TEMP_FILE} | cut -d' ' -f1`
	if ! [ "${SERVER_LOCAL_MD5}" = "${SERVER_TEMP_MD5}" ]; then
	
		echo "Newer version available - Upgrading"
		mv -f ${SERVER_TEMP_FILE} ${SERVER_LOCAL_FILE}
		unzip ${SERVER_LOCAL_FILE} -d /home/windward/

	fi

else

	echo "Newer version available - Upgrading"
	mv ${SERVER_TEMP_FILE} ${SERVER_LOCAL_FILE}
	unzip ${SERVER_LOCAL_FILE} -d /home/windward/
fi

if [ "${WINDWARD_SERVER_PUBLIC}" = "1" ]; then
	WINDWARD_SERVER_IS_PUBLIC="-public"
fi

if [ "${WINDWARD_SERVER_ADMIN}" ]; then
	mkdir -p /data/windward/Windward/ServerConfig
	if [ ! -f /data/windward/Windward/ServerConfig/admin.txt ]; then
		echo "${WINDWARD_SERVER_ADMIN}" > /data/windward/Windward/ServerConfig/admin.txt
	fi
fi

cd /home/windward

mono WWServer.exe -service -name "${WINDWARD_SERVER_NAME}" -world "${WINDWARD_SERVER_WORLD}" ${WINDWARD_SERVER_IS_PUBLIC} -tcp ${WINDWARD_SERVER_PORT} -http

