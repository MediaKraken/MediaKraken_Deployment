# Download base image
FROM alpine:3.12

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the base image"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
COPY requirements.txt /mediakraken

WORKDIR /mediakraken

# pip3 is installed now in community, hence the first sed
RUN sed -i "2 s/^#//" /etc/apk/repositories \
  && sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  python3 \
  py3-pip \
  gcc \
  python3-dev \
  linux-headers \
  musl-dev \
  && pip3 install --upgrade pip \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && apk del \
    gcc \
    python3-dev \
    linux-headers \
    musl-dev \
  && rm requirements.txt \
  && adduser -DHs /sbin/nologin metaman

# Do NOT do the below as other containers won't have rights to install/build.
# USER metaman

CMD ["/bin/ash"]
