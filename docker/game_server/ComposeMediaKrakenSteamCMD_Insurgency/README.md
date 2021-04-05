# Insurgency Dedicated Server

The follwing docker image allows for running a Insurgency dedicated server

Container Runtime Environment Variables:

* APP_SERVER_PORT 		- Port for the game to run on (default 27018)
* APP_SERVER_MAXPLAYERS 	- Max number of players (default 24)
* APP_SERVER_MAP 		- Starting map (default market_coop)
* APP_SERVER_NAME		- Server name
* APP_SERVER_TOKEN		- Use access token from [http://steamcommunity.com/dev/managegameservers](http://steamcommunity.com/dev/managegameservers)

Example docker run:
```
docker run --name Insurgency                 \
  -e APP_SERVER_PORT=27018      	     \
  -e APP_SERVER_MAX_PLAYERS=24		     \
  -e APP_SERVER_MAP=market_coop              \
  -e APP_SERVER_TOKEN=abc123                 \
  -e APP_SERVER_NAME="Insurgency Server"     \
  -v ~/DockerVolumes/Insurgency:/home/steamsrv/Insurgency  \
  -p 27018:27018                             \
  -p 27018:27018/udp                         \
  gameservers/insurgency
```


