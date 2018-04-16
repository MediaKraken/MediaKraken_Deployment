# Download base image
FROM mediakraken/mkbase37

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image loads the debug"

# copy PIP requirements
ADD requirements.txt /mediakraken
WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --update \
  && pip install -r requirements.txt \
  && rm requirements.txt \
  && rm -rf /var/cache/apk/*

# Copy the source files for the app
ADD src /mediakraken

CMD ["/bin/ash"]



