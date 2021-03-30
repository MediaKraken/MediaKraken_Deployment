# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbasedeb10_4py3:dev

LABEL author="Quinn D Granfor, spootdev@gmail.com"
LABEL description="This image holds the main abcde app"

ARG PIPMIRROR

WORKDIR /mediakraken

RUN apt-get update && apt-get install -y \
    abcde \
    libcdparanoia0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/bash"]
