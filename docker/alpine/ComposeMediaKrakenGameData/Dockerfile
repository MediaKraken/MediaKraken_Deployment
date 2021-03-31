# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase_alpinepy3:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image sets up game metadata import/update"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  ca-certificates \
  openrc \
  py3-psycopg2 \
  py3-psutil \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && rm requirements.txt \
  && apk add --no-cache \
  py-setuptools

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
