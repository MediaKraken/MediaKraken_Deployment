# Download base image
ARG BRANCHTAG
FROM mediakraken/mkbase_alpinepy3:${BRANCHTAG}

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image sets up game metadata import/update"

ARG ALPMIRROR
ARG PIPMIRROR

# copy PIP requirements
COPY requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --no-cache \
  ca-certificates==20191127-r5 \
  openrc==0.42.1-r20 \
  py3-psycopg2==2.8.6-r0 \
  py3-psutil==5.8.0-r0 \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && rm requirements.txt \
  && apk add --no-cache \
  py-setuptools

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
