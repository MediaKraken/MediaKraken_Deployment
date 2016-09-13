# setup ip of save stage
SRV_IP=10.0.0.28

# copy over the ffmpeg bins
scp ~/ffmpeg_build/bin/ff* root@$SRV_IP:/usr/local/bin/.

# copy over the motd
scp ../motd/motd_server.txt root@$SRV_IP:/etc/motd

# copy the uwsgi script
scp -r metaman_uwsgi_alpine.ini root@$SRV_IP:/home/metaman/MediaKraken.Deployment/web_app/.
