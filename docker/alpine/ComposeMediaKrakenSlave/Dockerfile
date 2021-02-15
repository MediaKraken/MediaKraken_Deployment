# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbasenodeffmpeg:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the main slave app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# had to go back to update instead of no-cache......throws errors
RUN echo '@edge http://nl.alpinelinux.org/alpine/edge/main' >> /etc/apk/repositories \
  && apk add --update \
  cifs-utils \
  nfs-utils \
  bash \
  alpine-sdk \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  libressl \
  musl-dev \
  net-snmp \
  net-snmp-dev \
  nginx-mod-rtmp@edge \
  python3 \
  python3-dev \
  openrc \
  py3-service_identity \
  py3-setuptools \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && npm install -g castnow \
  && apk del \
  alpine-sdk \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \
  net-snmp-dev \
  python3-dev \
  && apk add --update \
  py-setuptools \
  && rm requirements.txt \
  && rm -r /root/.npm \
  && rc-update add netmount \
  && rc-update add rpcbind \
  && rm -rf /var/cache/apk/*

# Forward logs to Docker
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Set up config file
COPY nginx_conf/nginx.conf /etc/nginx/nginx.conf

COPY wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
