# Download base image
FROM mediakraken/mkbase37py3

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image sets up tvmaze preload"

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --update \
  ca-certificates \
  gcc \
  linux-headers \
  musl-dev \
  python3-dev \
  libffi-dev \
  openrc \
  py3-psycopg2 \
  && pip3 install -r requirements.txt \
  && apk del gcc linux-headers musl-dev python3-dev \
  && rm requirements.txt \
  && apk add \
  py-setuptools \
  && rm -rf /var/cache/apk/*

ADD wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
