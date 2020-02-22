# Download base image
#FROM debian:10.2-slim
FROM python:3.8.1-buster

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the base image"

ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
COPY requirements.txt /mediakraken

WORKDIR /mediakraken

RUN apt update && apt -y install \
  python3 \
  python3-pip \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && rm requirements.txt \
  && apt clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Do NOT do the below as other containers won't have rights to install/build.
# USER metaman

CMD ["/bin/bash"]
