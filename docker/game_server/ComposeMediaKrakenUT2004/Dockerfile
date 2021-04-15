FROM debian:jessie

ENV UT2004_DIR=/usr/src/ut2004 \
    UT2004_ARCH=32 \
    UT2004_UCC32=/usr/src/ut2004/System/ucc-bin \
    UT2004_UCC64=/usr/src/ut2004/System/ucc-bin-linux-amd64 \
    UT2004_HOME=/home/ut2004 \
    UT2004_CMD=CTF-FACECLASSIC?game=XGame.xCTFGame

COPY scripts /usr/local/bin/

RUN echo "install packages" \
 && dpkg --add-architecture i386 \
 && apt-get --quiet update \
 && apt-get --quiet install --yes --no-install-recommends \
      ca-certificates \
      curl \
      libstdc++5 \
      libstdc++5:i386 \
      p7zip-full \
 && rm -rf /var/lib/apt/lists/* \
 && echo "install tini" \
 && curl --silent --show-error --location --output /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/v0.13.2/tini-amd64" \
 && echo "790c9eb6e8a382fdcb1d451f77328f1fac122268fa6f735d2a9f1b1670ad74e3 /usr/local/bin/tini" | sha256sum --check - \
 && chmod +x /usr/local/bin/tini \
 && tini -s true \
 && echo "install gosu" \
 && curl --silent --show-error --location --output /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.10/gosu-amd64" \
 && echo "5b3b03713a888cee84ecbf4582b21ac9fd46c3d935ff2d7ea25dd5055d302d3c /usr/local/bin/gosu" | sha256sum --check - \
 && chmod +x /usr/local/bin/gosu \
 && gosu nobody true \
 && echo "install modini" \
 && curl --silent --show-error --location --output /usr/local/bin/modini "https://github.com/reflectivecode/modini/releases/download/v0.6.0/modini-amd64" \
 && echo "38ce4a2a590ab95d174feebcff38b9fdbb311f138d0bd8855f91196d4d64267b /usr/local/bin/modini" | sha256sum --check - \
 && chmod +x /usr/local/bin/modini \
 && modini --version \
 && echo "add ut2004 user" \
 && groupadd --system --gid 2000 ut2004 \
 && useradd --system --uid 2000 --home-dir "${UT2004_HOME}" --create-home --gid ut2004 ut2004 \
 && echo "install ut2004" \
 && install.sh \
    https://www.dropbox.com/s/mijyaxho8ktzuxq/dedicatedserver3339-bonuspack-lnxpatch.7z?dl=1 \
    199093da475daaf9b4d660e551d2040c4cbebb6c \
    dedicatedserver3339-bonuspack-lnxpatch.7z \
    "${UT2004_DIR}" \
 && chown -R root:ut2004 "${UT2004_DIR}" \
 && chmod -R a=,ug=rX "${UT2004_DIR}" \
 && chmod 550 "${UT2004_UCC32}" "${UT2004_UCC64}" \
 && echo "tweak settings" \
 && modini \
      --input "${UT2004_DIR}/System/UT2004.ini" \
      --output "${UT2004_DIR}/System/UT2004.ini" \
      --modify "[IpDrv.MasterServerUplink];UplinkToGamespy=False;" \
 && cd "${UT2004_DIR}/System" \
 && "${UT2004_UCC32}" \
 && "${UT2004_UCC64}" \
 && echo "done"

WORKDIR ${UT2004_DIR}/System

EXPOSE 7777/udp 7778/udp 28902 80

ENTRYPOINT ["/usr/local/bin/tini", "--"]

CMD ["run-root.sh"]
