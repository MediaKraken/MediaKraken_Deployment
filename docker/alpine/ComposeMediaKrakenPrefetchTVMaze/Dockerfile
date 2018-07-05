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
  openrc \
  py3-psycopg2 \
  py3-psutil \
  && apk add \
  py-setuptools \
  && rm -rf /var/cache/apk/*

ADD wait-for-it-ash.sh /mediakraken
# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
