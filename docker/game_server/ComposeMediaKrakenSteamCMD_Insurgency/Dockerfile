FROM gameservers/steamcmd

ENV APPID=237410
ENV APPDIR=/home/steamsrv/Insurgency
ENV APP_GAME_NAME insurgency
ENV APP_SERVER_PORT 27018
ENV APP_SERVER_MAXPLAYERS 24
ENV APP_SERVER_MAP market_coop
ENV APP_SERVER_NAME SteamLUG [UK]
ENV USE_SRCDS true

ADD server.cfg /home/steamsrv/server.cfg

expose ${APP_SERVER_PORT}/udp
expose ${APP_SERVER_PORT}

cmd /scripts/StartServer
