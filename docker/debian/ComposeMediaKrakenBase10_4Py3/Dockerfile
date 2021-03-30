# Download base image
#FROM debian:10.4-slim
FROM python:3.8.6-slim-buster

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the base image"

ARG PIPMIRROR

# create work dir
RUN mkdir /mediakraken

# copy PIP requirements
COPY requirements.txt /mediakraken

WORKDIR /mediakraken

RUN apt update && apt -y install \
  && pip3 install --upgrade pip \
  && pip3 install --trusted-host ${PIPMIRROR} -i https://${PIPMIRROR}/simple -r requirements.txt \
  && rm requirements.txt \
  && apt clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Do NOT do the below as other containers won't have rights to install/build.
# USER metaman

CMD ["/bin/bash"]
