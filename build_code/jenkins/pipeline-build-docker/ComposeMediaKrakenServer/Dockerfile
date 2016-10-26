# Download base image
FROM mediakraken/mkbase:dev-0.1.12

MAINTAINER Quinn D Granfor, spootdev@gmail.com

# Copy the files so the pip requirements file is there
ADD . /mediakraken
WORKDIR /mediakraken

COPY /root/MediaKraken_Deployment/database /home/mediakraken/
COPY /root/MediaKraken_Deployment/metadata /home/mediakraken/
COPY /root/MediaKraken_Deployment/network /home/mediakraken/
COPY /root/MediaKraken_Deployment/web_app /home/mediakraken/
COPY /root/MediaKraken_Deployment/bulk_gamesdb_netfetch.py /home/mediakraken/
COPY /root/MediaKraken_Deployment/main_server.py /home/mediakraken/
COPY /root/MediaKraken_Deployment/main_server_api.py /home/mediakraken/
COPY /root/MediaKraken_Deployment/main_server_link.py /home/mediakraken/
COPY /root/MediaKraken_Deployment/main_server_metadata_api.py /home/mediakraken/
COPY /root/MediaKraken_Deployment/main_server_trigger.py /home/mediakraken/
COPY /root/MediaKraken_Deployment/subprogram*.py /home/mediakraken/
# Update Software repository
RUN apt-get -y install libdiscid-dev postgresql-server-dev-9.5 nginx redis-server && pip install -r requirements.txt && apt-get autoremove && apt-get clean && apt-get autoclean&& mkdir mediakraken/backups && mkdir mediakraken/passwordmeter && mkdir mediakraken/passwordmeter/res
ENTRYPOINT ["python", "/home/mediakraken/main_server.py"]
