LABEL www.mediakraken.org.version="dev-0.1.12"
LABEL www.mediakraken.org.release-date="2016-10-28"
LABEL Description="This image downloads and maintains all metadata"

# Download base image
FROM alpine:3.4 

MAINTAINER Quinn D Granfor, spootdev@gmail.com

# Copy the source files for the app
ADD src /home/mediakraken
# copy PIP requirements
ADD requirements.txt /home/mediakraken
WORKDIR /home/mediakraken

# Update repository and install packages
RUN apk add --update \
  gcc \
  linux-headers \
  musl-dev \
  postgresql-dev \
  python-dev \
  py-pip \
  && pip install pytest-runner \
  && pip install -r requirements.txt \
  && pip uninstall -y pytest_runner \
  && apk del gcc linux-headers musl-dev postgresql-dev python-dev py-pip
CMD ["python", "/home/mediakraken/main_server_trigger.py"]
