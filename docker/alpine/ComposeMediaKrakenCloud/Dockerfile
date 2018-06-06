# Download base image
FROM mediakraken/mkbase37

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image houses all the cloud access"

WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --update \
  alpine-sdk \
  py-setuptools \
  python-dev \
  && apk del alpine-sdk \
  python-dev \
  && rm -rf /var/cache/apk/*

# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]



