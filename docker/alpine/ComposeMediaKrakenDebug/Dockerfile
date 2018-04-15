# Download base image
FROM mediakraken/mkbase37

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image loads the debug"

WORKDIR /mediakraken

# Update repository and install packages
RUN apk add --update \
  && rm -rf /var/cache/apk/*

# Copy the source files for the app
ADD src /mediakraken

CMD ["python /mediakraken/main_debug.py"]



