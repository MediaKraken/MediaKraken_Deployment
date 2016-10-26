# Download base image
FROM mediakraken/mkbase:dev-0.1.12

MAINTAINER Quinn D Granfor, spootdev@gmail.com

# Copy the files so the pip requirements file is there
ADD . /mediakraken
WORKDIR /mediakraken

COPY /root/MediaKraken_Deployment/main_server_slave.py /home/mediakraken/
# Update Software repository
RUN pip install -r requirements.txt && apt-get autoremove && apt-get clean && apt-get autoclean
ENTRYPOINT ["python", "/home/mediakraken/main_server_slave.py"]
