# Download base image
FROM mediakraken/mkbase37

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
  python-dev \
  && pip install -r requirements.txt \
  && apk del alpine-sdk \
  postgresql-client \
  python-dev \
  && rm -rf /var/cache/apk/*

ADD wait-for-it-ash.sh /mediakraken

# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]



