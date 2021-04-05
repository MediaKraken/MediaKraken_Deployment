FROM gameservers/steamcmd

ENV APPID=233780
ENV APPDIR=/home/steamsrv/ARMA
ENV APP_SERVER_PORT 2302
ENV STEAMCMD_OPTS -beta legacyports -betapassword Arma3LegacyPorts

ADD a3Vanilla.sh /home/steamsrv/a3Vanilla.sh
ADD server.cfg /home/steamsrv/server.cfg
ADD RunServer.sh /home/steamsrv/RunServer.sh

expose 2302/udp
expose 2303/udp
expose 2304/udp

cmd /home/steamsrv/RunServer.sh

