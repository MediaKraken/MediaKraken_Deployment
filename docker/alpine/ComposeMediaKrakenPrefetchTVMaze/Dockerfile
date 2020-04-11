# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase311_5py3:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image sets up tvmaze preload"

ARG ALPMIRROR
ARG PIPMIRROR

WORKDIR /mediakraken

# Update repository and install packages
RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  ca-certificates \
  openrc \
  py3-psycopg2 \
  py3-psutil \
  && apk add \
  py-setuptools

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
