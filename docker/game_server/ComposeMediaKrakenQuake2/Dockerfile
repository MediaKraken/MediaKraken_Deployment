FROM ubuntu:20.10
LABEL maintainer="Tim Sogard <docker@timsogard.com>"
COPY . /opt/quake2
RUN useradd -m -s /bin/bash quake2
RUN chown -R quake2:quake2 /opt/quake2
RUN apt-get update
RUN apt-get install wget -y
RUN wget https://skuller.net/q2pro/nightly/q2pro-server_linux_amd64.tar.gz -O- | tar zxvf - -C /opt/quake2
EXPOSE 27910
WORKDIR /opt/quake2
USER quake2

CMD ./q2proded +exec server.cfg +set dedicated 1 +set deathmatch 1