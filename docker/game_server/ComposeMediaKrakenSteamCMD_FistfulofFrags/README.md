# Fistful Of Frags Dedicated Server

The follwing docker image allows for running a Fistful Of Frags server

Container Runtime Environment Variables:

* APP_SERVER_PORT 		- Port for the game to run on (default 27015)
* APP_SERVER_MAXPLAYERS 	- Max number of players (default 20)
* APP_SERVER_MAP 		- Starting map (default fof_fistful)

Example docker run:
```
docker run --name "FOF-Server"		     \
  -e APP_SERVER_PORT=27015      	     \
  -e APP_SERVER_MAX_PLAYERS=10		     \
  -e APP_SERVER_MAP=fof_fistful              \
  -v ~/DockerVolumes/fof:/home/steamsrv/fof  \
  -p 27015:27015                             \
  gameservers/fistfuloffrags:latest
```

