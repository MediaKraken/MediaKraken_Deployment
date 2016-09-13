
and there is a seperate ffmpeg build
fix linefeeds

# install packages
apk add tzdata readline-dev tcl-dev libxml2-dev git cython-dev nano yasm cmake autoconf automake bash gettext-dev freetype-dev py-openssl libtool postgresql-dev py-setuptools build-base alpine-sdk linux-headers py-six libffi-dev py-crypto py-pip nfs-utils cifs-utils py-curl nginx ack py-redis redis python-dev py-setuptools uwsgi uwsgi-python uwsgi-router_uwsgi

rc-update add nfsmount
rc-update add postgresql
rc-update add nginx
rc-update add redis

# setup postgresql user
# TODO

# import sql_dataset
# TODO

# setup pid dir which need to be retired imho
mkdir /home/metaman/github/pid

# install apps via pip
pip install --upgrade pip
pip install -r pip_packages_alpine.txt
pip install 'requests[security]'

# as root again
cd /home/metaman/github/MediaKraken_Deployment/build_code/lib
# as root again to build newer psutils
tar -xvzf psutil*
cd psutil-release-3.4.2
python setup.py install

cd /home/metaman/github/MediaKraken_Deployment/build_code/lib
unzip isoparser-master.zip
cd isoparser-master
python setup.py install

cd /home/metaman/github/MediaKraken_Deployment/build_code/lib
tar -xvzf ip2c*
cd ip2c*
python setup.py install

cd /home/metaman/github/MediaKraken_Deployment/build_code/lib
tar -xvzf pythonfutures*
cd pythonfutures-3.0.5
python setup.py install

# setup nginx
nano /etc/nginx/nginx.conf
uncomment - gzip on
# TODO have this as a file to copy
# kick up worker threads to 2
- replace server with this
'''
server {
    root /home/metaman/github/Meta-Man.Server/web_app;
    listen      80;
    server_name localhost;
    charset     utf-8;
    client_max_body_size 75M;
    access_log /var/log/nginx/metaman.net_access.log;
    error_log /var/log/nginx/metaman.net_error.log;

    location  /static {
      alias  /home/metaman/github/Meta-Man.Server/web_app/MetaMan/;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/metaman_uwsgi.sock;
    }
}
'''
# copy the plugin
to get uwsgi to work had to copy the cp /usr/lib/uwsgi/python_plugin.so /home/metaman/github/MediaKraken_Deployment/.


# build ffmpeg libs
mkdir /root/ffmpeg_build
mkdir /root/ffmpeg_sources



**********************************************************
run script to create db schema

run ./FFMPEG_Build_Alpine.sh in Meta-Man.Build/scripts to build ffmpeg with codecs
cp /root/bin/* /usr/local/bin/.

