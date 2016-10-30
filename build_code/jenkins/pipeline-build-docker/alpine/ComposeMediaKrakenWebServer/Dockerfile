# Download base image
FROM mediakraken/mkwebbase

MAINTAINER Quinn D Granfor, spootdev@gmail.com

LABEL www.mediakraken.org.version="dev-0.1.12"
LABEL www.mediakraken.org.release-date="2016-10-28"
LABEL Description="This image holds the image for the web server app"

# copy the src files
COPY src /mediakraken

WORKDIR /mediakraken

ENTRYPOINT["uwsgi", "--socket", "0.0.0.0:8080", "--protocol", "http", "--chdir=./web_app", "--ini", "./web_app/mediakraken_uwsgi_alpine.ini"]

