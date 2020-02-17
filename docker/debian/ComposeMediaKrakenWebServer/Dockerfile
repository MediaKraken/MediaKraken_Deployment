# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase311_3py3:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the image for the web server app"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  ack \
  curl-dev \
  git \
  gcc \
  jpeg-dev \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers \
  musl-dev \  
  openrc \
  libressl-dev \
  py3-cffi \
  py3-redis \
  python3-dev \
  cifs-utils \
  nfs-utils \
  ca-certificates \
  libressl \
  py3-numpy \
  py3-psycopg2 \
  py3-psutil \
  py3-gevent \
  && export PYCURL_SSL_LIBRARY=openssl \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple pycurl \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && pip3 install git+https://github.com/MediaKraken/Flask-Paginate \
  && pip3 install -e git+https://github.com/LevPasha/Instagram-API-python.git#egg=InstagramAPI \
  && apk del \
  gcc \
  git \
  musl-dev \
  linux-headers \
  python3-dev \
  libressl-dev \
  && rm requirements.txt \
  && apk add --no-cache \
  uwsgi \
  uwsgi-http \
  uwsgi-gevent3 \
  uwsgi-python3 \
  uwsgi-router_uwsgi \
  py-setuptools \
  && cp /usr/lib/uwsgi/python3_plugin.so /mediakraken/. \
  && rc-update add netmount \
  && rc-update add rpcbind

COPY wait-for-it-ash-busybox130.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

EXPOSE 8080
CMD ["/bin/ash"]
