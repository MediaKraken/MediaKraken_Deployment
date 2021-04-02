# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbasenodeffmpeg:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the main slave app"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# had to go back to update instead of no-cache......throws errors
RUN echo '@edge http://nl.alpinelinux.org/alpine/edge/main' >> /etc/apk/repositories \
  && apk add --no-cache \
  cifs-utils==6.12-r0 \
  nfs-utils==2.5.2-r0 \
  bash==5.1.0-r0 \
  alpine-sdk==1.0-r0 \
  libffi-dev==3.3-r2 \
  libxml2-dev==2.9.10-r6 \
  libxslt-dev==1.1.34-r0 \
  linux-headers==5.7.8-r0 \
  libressl==3.1.5-r0 \
  musl-dev==1.2.2-r0 \
  net-snmp==5.9-r2 \
  net-snmp-dev==5.9-r2 \
  nginx-mod-rtmp@edge \
  python3==3.8.8-r0 \
  python3-dev==3.8.8-r0 \
  openrc==0.42.1-r19 \
  py3-pip==20.3.4-r0 \
  py3-service_identity==18.1.0-r3 \
  py3-setuptools==51.3.3-r0 \
  && pip3 install --no-cache-dir --upgrade pip==21.0.1 \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
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
  && apk add --no-cache \
  py-setuptools=51.3.3-r0 \
  && rm requirements.txt \
  && rm -r /root/.npm \
  && rc-update add netmount \
  && rc-update add rpcbind

# Forward logs to Docker
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Set up config file
COPY nginx_conf/nginx.conf /etc/nginx/nginx.conf

COPY wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
