###########################################################
# Dockerfile that builds a HoldfastNaW Gameserver
###########################################################
ARG BRANCHTAG
FROM mediakraken/mkbasesteamcmdroot:${BRANCHTAG}

LABEL maintainer="walentinlamonos@gmail.com"

ENV STEAMAPPID 1424230
ENV STEAMAPP holdfastnaw
ENV STEAMAPPDIR "${HOMEDIR}/${STEAMAPP}-dedicated"
ENV DLURL https://raw.githubusercontent.com/CM2Walki/HoldfastNaW

# Create autoupdate config
# Remove packages and tidy up
RUN set -x \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends --no-install-suggests \
		libsqlite3-0=3.27.2-3+deb10u1 \
		tini=0.18.0-1 \
	&& mkdir -p "${STEAMAPPDIR}" \
	&& wget "${DLURL}/master/etc/entry.sh" -O "${HOMEDIR}/entry.sh" \
	&& wget "${DLURL}/master/etc/tinientry.sh" -O "${HOMEDIR}/tinientry.sh" \
	&& chmod +x "${HOMEDIR}/entry.sh" "${HOMEDIR}/tinientry.sh" \
	&& chown -R "${USER}:${USER}" "${HOMEDIR}/entry.sh" "${HOMEDIR}/tinientry.sh" "${STEAMAPPDIR}" \	
	&& apt-get remove --purge -y \
		wget \
	&& apt-get clean autoclean \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/*

ENV FPSMAX=300 \
	SERVER_PORT=20100 \
	STEAM_COM_PORT=8700 \
	STEAM_QUERY_PORT=27000 \
	SCREEN_QUALITY="Fastest" \
	SCREEN_WIDTH=640 \
	SCREEN_HEIGHT=480 \
	SERVER_REGION="europe" \
	SERVER_CONFIG_PATH="serverconfig_default.txt" \
	SERVER_LOG_PATH="logs_output/outputlog_server.txt" \
	SERVER_LOG_ARCHIVE_PATH="logs_archive/" \
	ADDITIONAL_ARGS="" \
	STEAMCMD_UPDATE_ARGS=""

USER ${USER}

VOLUME ${STEAMAPPDIR}

WORKDIR ${HOMEDIR}

STOPSIGNAL SIGINT

ENTRYPOINT ["tini", "-g", "--", "/home/steam/tinientry.sh"]

# Expose ports
EXPOSE 20100 \
	8700 \
	27000
