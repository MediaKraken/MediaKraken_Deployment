# Download base image
FROM mediakraken/mkbase37

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image sets up tmdb preload"

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --update \
  ca-certificates \
  postgresql-client \
  gcc \
  linux-headers \
  musl-dev \
  postgresql-dev \
  python-dev \
  libffi-dev \
  python \
  openrc \
  && pip install -r requirements.txt \
  && apk del gcc linux-headers musl-dev postgresql-dev python-dev py-pip \
  && rm requirements.txt \
  && apk add \
  py-setuptools \
  python \
  && rm -rf /var/cache/apk/*

ADD wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
