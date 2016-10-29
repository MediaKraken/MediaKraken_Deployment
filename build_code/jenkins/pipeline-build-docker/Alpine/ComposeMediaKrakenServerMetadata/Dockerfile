# Download base image
FROM alpine:3.4 

MAINTAINER Quinn D Granfor, spootdev@gmail.com

# Copy the files so the pip requirements file is there
ADD src /home/mediakraken
ADD requirements.txt /home/mediakraken
WORKDIR /home/mediakraken

# Update Software repository
RUN apk add --update py-pip postgresql-dev python-dev linux-headers musl-dev gcc \
  && pip install pytest-runner && pip install -r requirements.txt \
  && pip uninstall -y pytest_runner \
  && apk del py-pip postgresql-dev python-dev linux-headers musl-dev gcc
ENTRYPOINT ["python", "/home/mediakraken/main_server_trigger.py"]
