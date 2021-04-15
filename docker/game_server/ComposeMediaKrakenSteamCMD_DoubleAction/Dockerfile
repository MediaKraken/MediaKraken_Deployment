FROM gameservers/steamcmd

ENV APPID=317800
ENV APPDIR=/home/steamsrv/dab
ENV APP_GAME_NAME dab
ENV APP_SERVER_PORT 27019
ENV APP_SERVER_MAXPLAYERS 24
ENV APP_SERVER_MAP da_cocaine
ENV APP_SERVER_NAME SteamLUG [UK]
ENV APP_SRCDS_FLAGS -insecure
ENV USE_SRCDS true

ADD server.cfg /tmp/server.cfg

expose ${APP_SERVER_PORT}/udp
expose ${APP_SERVER_PORT}

cmd /scripts/StartServer
