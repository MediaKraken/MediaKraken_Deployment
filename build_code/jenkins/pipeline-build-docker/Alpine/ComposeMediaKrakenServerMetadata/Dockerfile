# Download base image
FROM alpine:3.4 

MAINTAINER Quinn D Granfor, spootdev@gmail.com

# Copy the files so the pip requirements file is there
ADD src /home/mediakraken
ADD requirements.txt /home/mediakraken
WORKDIR /home/mediakraken

# Update Software repository
RUN apk add --update py-pip && pip install pytest-runner && pip install -r requirements.txt && pip uninstall pytest_runner
ENTRYPOINT ["python", "/home/mediakraken/main_server_trigger.py"]
