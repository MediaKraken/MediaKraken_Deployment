#!/bin/sh
echo "Killing running server, if any"
if killall arma3server ; then
        echo "Killed"
fi

cp server.cfg ~/ARMA/server.cfg

echo "Starting new vanilla server"
rm ~/ARMA/server.log-last
mv ~/ARMA/server.log ~/srv/server.log-last
cd ~/ARMA
nohup ./arma3server -name=SteamLUG -config=server.cfg -port=2402 > ~/ARMA/server.log 2>&1 &
