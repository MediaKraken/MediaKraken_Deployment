# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbasedeb10_2py3:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the image for the web server app"

ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apt update && apt -y install \
  ack \
  libcurl4-openssl-dev \
  git \
  gcc \
  libjpeg-dev \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  linux-headers-amd64 \
  openrc \
  libssl-dev \
  python3-cffi \
  python3-redis \
  python3-dev \
  cifs-utils \
  nfs-common \
  ca-certificates \
  libssl1.1 \
  python3-numpy \
  python3-psycopg2 \
  python3-psutil \
  python3-gevent \
  python3-psycogreen \
  && export PYCURL_SSL_LIBRARY=openssl \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple pycurl \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && pip3 install git+https://github.com/MediaKraken/Flask-Paginate \
  && pip3 install -e git+https://github.com/LevPasha/Instagram-API-python.git#egg=InstagramAPI \
  && apt -y remove \
  gcc \
  git \
  linux-headers-amd64 \
  python3-dev \
  libssl-dev \
  && rm requirements.txt \
  && apt -y install \
  uwsgi \
  uwsgi-plugin-python3 \
  # uwsgi-plugin-greenlet-python3 \  # this didn't help
  uwsgi-plugin-router-access \
  python3-setuptools \
  && cp /usr/lib/uwsgi/plugins/python3_plugin.so /mediakraken/.

COPY wait-for-it-bash.sh /mediakraken
# Copy the source files for the app
COPY src /mediakraken

EXPOSE 8080
CMD ["/bin/bash"]
