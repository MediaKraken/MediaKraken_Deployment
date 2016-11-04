# Download base image
FROM mediakraken/mkbase:dev-0.1.12

MAINTAINER Quinn D Granfor, spootdev@gmail.com

# Copy the files so the pip requirements file is there
ADD src /home/mediakraken
ADD requirements.txt /home/mediakraken
WORKDIR /home/mediakraken

# Update Software repository
RUN apt-get -y install nginx postgresql-server-dev-9.5 redis-server && pip install -r requirements.txt && apt-get autoremove && apt-get clean && apt-get autoclean&& mkdir /home/mediakraken/backups && mkdir /home/mediakraken/passwordmeter && mkdir /home/mediakraken/passwordmeter/res
ENTRYPOINT ["python", "/home/mediakraken/main_server.py"]
