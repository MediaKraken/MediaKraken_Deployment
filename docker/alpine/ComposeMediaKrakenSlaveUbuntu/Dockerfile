# Download base image
FROM mediakraken/mkbasenodeffmpegubuntu:latest

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the main slave app"

ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

RUN apt update \
  && apt -y install \
  python \
  cifs-utils \
  libnfs11 \
  build-essential \
  libffi-dev \
  libxml2-dev \
  libxslt1-dev \
  linux-headers-generic \
  openssl \
  python3 \
  python3-dev \
  python3-pip \
  python3-service-identity \
  python3-setuptools \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && npm install -g castnow \
  && apt -y remove \
  build-essential \
  libffi-dev \
  libxml2-dev \
  libxslt1-dev \
  linux-headers-generic \
  python3-dev \
  && apt -y install \
  python-setuptools \
  && rm requirements.txt \
  && rm -r /root/.npm

# Forward logs to Docker
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Set up config file
COPY nginx_conf/nginx.conf /etc/nginx/nginx.conf

ADD wait-for-it-bash.sh /mediakraken
# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]

