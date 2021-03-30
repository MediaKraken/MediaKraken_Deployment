# Download base image
FROM alpine:3.13.2

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the base image"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
COPY requirements.txt /mediakraken

WORKDIR /mediakraken

# pip3 is installed now in community, hence the first sed
RUN sed -i "2 s/^#//" /etc/apk/repositories \
  && sed -i "s/dl-2.cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --no-cache \
  python3 \
  py3-pip \
  && pip3 install --no-cache-dir --upgrade pip \
  && pip3 install --no-cache-dir --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && rm requirements.txt \
  && adduser -DHs /sbin/nologin metaman

# Do NOT do the below as other containers won't have rights to install/build.
# USER metaman

CMD ["/bin/ash"]
