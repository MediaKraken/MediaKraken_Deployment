# Download base image
FROM alpine:3.8

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the base image"

ARG ALPMIRROR
ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
ADD requirements.txt /mediakraken

WORKDIR /mediakraken

# pip3 is installed with python3
RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPMIRROR}/" /etc/apk/repositories \
  && apk add --update \
  python3 \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple --upgrade pip \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && rm requirements.txt \
  && rm -rf /var/cache/apk/* \
  && adduser -DHs /sbin/nologin metaman

USER metaman

CMD ["/bin/ash"]
