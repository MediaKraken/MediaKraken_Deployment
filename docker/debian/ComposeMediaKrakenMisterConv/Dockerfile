# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase_debianpy3:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the Mister rom/chd converter"

WORKDIR /mediakraken

RUN apt update && apt -y install \
  mame-tools=0.206+dfsg.1-1 \
  && apt clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/bash"]
