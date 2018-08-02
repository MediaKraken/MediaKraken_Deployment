# Download base image
FROM mediakraken/mkbasenodeffmpeg:latest

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the Roku thumbnail generator app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
ADD requirements.txt /mediakraken

WORKDIR /mediakraken

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --update \
  cifs-utils \
  nfs-utils \
  libressl \
  net-snmp \
  python3 \
  openrc \
  && pip3 install -i http://${PIPMIRROR} -r requirements.txt \
  && rm -rf /var/cache/apk/* \
  && rm requirements.txt \
  && rc-update add netmount \
  && rc-update add rpcbind

ADD wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
