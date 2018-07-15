docker run -v /var/run/docker.sock:/var/run/docker.sock mediakraken/mkdebug python /mediakraken/main_debug.py
sleep 30
./mediakraken_start.sh
