# setup ip of save stage
SLAVE_IP=10.0.0.23

# copy over the ffmpeg bins
scp ~/ffmpeg_build/bin/ff* root@$SLAVE_IP:/usr/local/bin/.

# copy over the motd
scp ../motd/motd_slave.txt root@$SLAVE_IP:/etc/motd

# this is to move the data for pyinstaller
#cp -Rf /root/Meta-Man* /home/metaman/.
#chown -R metaman: /home/metaman/Meta-Man*

# pyinstaller
#su - metaman
#pyinstaller -y -F ./Meta-Man.Server/main_slave.py
#exit

# copy folder to slave machine
#scp /home/metaman/dist/main_slave/* root@$SLAVE_IP:/home/metaman/.

