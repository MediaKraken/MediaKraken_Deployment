# Download base image
FROM mediakraken/mkbase37py3

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image houses all the cloud access"

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --update \
  alpine-sdk \
  postgresql-client \
  py-setuptools \
  python3-dev \
  postgresql-dev \
  && pip3 install -r requirements.txt \
  && apk del alpine-sdk \
  python3-dev \
  postgresql-dev \
  && rm -rf /var/cache/apk/*

ADD wait-for-it-ash.sh /mediakraken

# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]



