# Download base image
FROM th-registry-1.beaverbay.local:5000/mediakraken/mkbase_alpinepy3:dev

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the castpy app"

WORKDIR /mediakraken

# Copy the source files for the app
COPY src /mediakraken

CMD ["/bin/ash"]
