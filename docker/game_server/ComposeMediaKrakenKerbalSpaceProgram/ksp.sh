#!/bin/bash

SERVER_TEMP_FILE=/tmp/DMPServer.zip
SERVER_LOCAL_FILE=/data/ksp/DMPServer.zip
DMPDIR=/data/ksp/DMPServer
CONFIGDIR=/data/ksp/config
KSPCONFIGDIR=/data/ksp/kspconfig

echo "Downloading latest dedicated server"

wget -qO ${SERVER_TEMP_FILE} ${SERVER_REMOTE_FILE}

if [ -f ${SERVER_LOCAL_FILE} ]; then
	echo "Checking local dedicated server is the latest version..."
	SERVER_LOCAL_MD5=`md5sum ${SERVER_LOCAL_FILE} | cut -d' ' -f1`
	SERVER_TEMP_MD5=`md5sum ${SERVER_TEMP_FILE} | cut -d' ' -f1`
	if ! [ "${SERVER_LOCAL_MD5}" = "${SERVER_TEMP_MD5}" ]; then
	
		echo "Newer version available - Upgrading"
		mv -f ${SERVER_TEMP_FILE} ${SERVER_LOCAL_FILE}
		unzip ${SERVER_LOCAL_FILE} -d /data/ksp/

	fi

else

	echo "Newer version available - Upgrading"
	mv ${SERVER_TEMP_FILE} ${SERVER_LOCAL_FILE}
	unzip ${SERVER_LOCAL_FILE} -d /data/ksp/
fi

echo "Checking configs"

if [ -f ${CONFIGDIR}/DMPAdmins.txt ]; then
	cp ${CONFIGDIR}/DMPAdmins.txt $DMPDIR/
else
	cp ${KSPCONFIGDIR}/DMPAdmins.txt $DMPDIR/
fi

if [ -f ${CONFIGDIR}/DMPIPBans.txt ]; then
	cp ${CONFIGDIR}/DMPIPBans.txt $DMPDIR/
else
	cp ${KSPCONFIGDIR}/DMPIPBans.txt $DMPDIR/
fi

if [ -f ${CONFIGDIR}/DMPKeyBans.txt ]; then
	cp ${CONFIGDIR}/DMPKeyBans.txt $DMPDIR/
else
	cp ${KSPCONFIGDIR}/DMPKeyBans.txt $DMPDIR/
fi

if [ -f ${CONFIGDIR}/DMPModControl.txt ]; then
	cp ${CONFIGDIR}/DMPModControl.txt $DMPDIR/
else
	cp ${KSPCONFIGDIR}/DMPModControl.txt $DMPDIR/
fi

if [ -f ${CONFIGDIR}/DMPPlayerBans.txt ]; then
	cp ${CONFIGDIR}/DMPPlayerBans.txt $DMPDIR/
else
	cp ${KSPCONFIGDIR}/DMPPlayerBans.txt $DMPDIR/
fi

if [ -f ${CONFIGDIR}/DMPServerSettings.txt ]; then
	cp ${CONFIGDIR}/DMPServerSettings.txt $DMPDIR/
else
	cp ${KSPCONFIGDIR}/DMPServerSettings.txt $DMPDIR/
fi

if [ "${KSP_SERVER_PORT}" ]; then
	sed -i "s/port,6702/port,${KSP_SERVER_PORT}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_NAME}" ]; then
	sed -i "s/servername,KSP-DMP Server/servername,${KSP_SERVER_NAME}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_WARPMODE}" ]; then
	sed -i "s/warpmode,4/warpmode,${KSP_SERVER_WARPMODE}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_GAMEMODE}" ]; then
	sed -i "s/gamemode,0/gamemode,${KSP_SERVER_GAMEMODE}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_DIFFICULTY}" ]; then
	sed -i "s/gamedifficulty,1/gamedifficulty,${KSP_SERVER_DIFFICULTY}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_MODCONTROL}" ]; then
	sed -i "s/modcontrol,1/modcontrol,${KSP_SERVER_MODCONTROL}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_OFFLINETICKS}" ]; then
	sed -i "s/keeptickingwhileoffline,1/keeptickingwhileoffline,${KSP_SERVER_OFFLINETICKS}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_LOGLEVEL}" ]; then
	sed -i "s/loglevel,0/loglevel,${KSP_SERVER_LOGLEVEL}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_CHEATS}" ]; then
	sed -i "s/cheats,1/cheats,${KSP_SERVER_CHEATS}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_HTTPSTATUS}" ]; then
	sed -i "s/httpport,0/httpport,${KSP_SERVER_HTTPSTATUS}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_MAXPLAYERS}" ]; then
	sed -i "s/maxplayers,20/maxplayers,${KSP_SERVER_MAXPLAYERS}/" ${DMPDIR}/DMPServerSettings.txt
fi
if [ "${KSP_SERVER_MOTD}" ]; then
	sed -i "s/servermotd.*20/servermotd,${KSP_SERVER_MOTD}/" ${DMPDIR}/DMPServerSettings.txt
fi

mono /data/ksp/DMPServer/DMPServer.exe
