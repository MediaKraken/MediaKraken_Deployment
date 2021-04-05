# Double Action: Boogaloo Dedicated Server

The follwing docker image allows for running a Insurgency dedicated server

Container Runtime Environment Variables:

* APP_SERVER_PORT 		- Port for the game to run on (default 27019)
* APP_SERVER_MAXPLAYERS 	- Max number of players (default 24)
* APP_SERVER_MAP 		- Starting map (default da_cocaine)
* APP_SERVER_NAME		- Server name
* APP_SERVER_TOKEN		- Use access token from [http://steamcommunity.com/dev/managegameservers](http://steamcommunity.com/dev/managegameservers)

Example docker run:
```
docker run --name dab                 \
  -e APP_SERVER_PORT=27019      	     \
  -e APP_SERVER_MAX_PLAYERS=24		     \
  -e APP_SERVER_MAP=da_cocaine              \
  -e APP_SERVER_TOKEN=abc123                 \
  -e APP_SERVER_NAME="Double Action: Boogalooo Server"     \
  -v ~/DockerVolumes/DAB:/home/steamsrv/dab  \
  -p 27019:27019                             \
  -p 27019:27019/udp                         \
  gameservers/doubleaction
```


