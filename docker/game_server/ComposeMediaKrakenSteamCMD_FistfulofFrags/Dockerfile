FROM gameservers/steamcmd
MAINTAINER Jason Rivers <docker@jasonrivers.co.uk>

ENV APPID=295230
ENV APPDIR=/home/steamsrv/fof
ENV APP_SERVER_PORT 27015
ENV APP_GAME_NAME fof
ENV APP_SERVER_MAXPLAYERS 20
ENV APP_SERVER_MAP fof_fistful
ENV USE_SRCDS true

RUN mkdir -p /home/steamsrv/.steam/sdk32/              && \
    ln -s /home/steamsrv/steamcmd/linux32/steamclient.so /home/steamsrv/.steam/sdk32/steamclient.so


EXPOSE ${APP_SERVER_PORT}

USER steamsrv

CMD /scripts/StartServer
