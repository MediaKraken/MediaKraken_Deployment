############################################################
# Dockerfile that builds a Squad Gameserver
############################################################
ARG BRANCHTAG
FROM mediakraken/mkbasesteamcmdroot:${BRANCHTAG}

LABEL maintainer="walentinlamonos@gmail.com"

ENV STEAMAPPID 403240
ENV STEAMAPP squad
ENV STEAMAPPDIR "${HOMEDIR}/${STEAMAPP}-dedicated"
ENV DLURL https://raw.githubusercontent.com/CM2Walki/Squad

RUN set -x \
	&& apt-get update \
	&& wget "${DLURL}/master/etc/entry.sh" -O "${HOMEDIR}/entry.sh" \
	&& mkdir -p "${STEAMAPPDIR}" \
	&& chmod 755 "${HOMEDIR}/entry.sh" "${STEAMAPPDIR}" \
	&& chown "${USER}:${USER}" "${HOMEDIR}/entry.sh" "${STEAMAPPDIR}" \
	&& apt-get remove --purge -y \
		wget \
	&& apt-get clean autoclean \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/*

ENV PORT=7787 \
	QUERYPORT=27165 \
	RCONPORT=21114 \
	FIXEDMAXPLAYERS=80 \
	FIXEDMAXTICKRATE=50 \
	RANDOM=NONE

USER ${USER}

WORKDIR ${HOMEDIR}

CMD ["bash", "entry.sh"]

# Expose ports
EXPOSE 7787/udp \
	27165/tcp \
	27165/udp \
	21114/tcp \
	21114/udp
