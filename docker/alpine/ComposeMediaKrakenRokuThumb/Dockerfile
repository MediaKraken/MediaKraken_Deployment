# Download base image
FROM mediakraken/mkbasenodeffmpeg:latest

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the Roku thumbnail generator app"

# create work dir
RUN mkdir /mediakraken

WORKDIR /mediakraken

RUN apk add --update \
  cifs-utils \
  nfs-utils \
  libressl \
  net-snmp \
  python3 \
  && rm -rf /var/cache/apk/* \
  && rc-update add netmount \
  && rc-update add rpcbind

ADD wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
