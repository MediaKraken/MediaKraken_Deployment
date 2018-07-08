# Download base image
FROM mediakraken/mkbase38py3

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image sets up tmdb preload"

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --update \
  ca-certificates \
  openrc \
  py3-psycopg2 \
  py3-psutil \
  && pip3 install -r requirements.txt \
  && rm requirements.txt \
  && apk add \
  py-setuptools \
  && rm -rf /var/cache/apk/*

# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]
