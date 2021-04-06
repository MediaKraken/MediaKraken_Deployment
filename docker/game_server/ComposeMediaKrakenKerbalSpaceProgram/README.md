# Kerbal Space Program Game Server

See more about Kerbal Space Program at: [https://kerbalspaceprogram.com/en/](https://kerbalspaceprogram.com/en/)

To connect to the KSP server you will need the DMP mod from the DMP Website: [https://d-mp.org/](https://d-mp.org/)
You can use the following environment variables passed to the Docker container to configure your server.

* KSP_SERVER_NAME - The name of the KSP server.
* KSP_SERVER_PORT - The port number to use for the server (Note - This will require you exposing other ports within your container)
* KSP_SERVER_WARPMODE - 0:MCW_FORCE, 1:MCW_VOTE, 2:MCW_LOWEST, 3:SUBSPACE_SIMPLE, 4:SUBSPACE (Default), 5:NONE
* KSP_SERVER_GAMEMODE - 0:SANDBOX (default), 1:SCIENCE, 2:CAREER
* KSP_SERVER_DIFFICULTY - 0:EASY, 1:NORMAL (default), 2:MODERATE, 3:HARD, 4:CUSTOM
* KSP_SERVER_MODCONTROL - 0:DISABLED, 1:ENABLED_STOP_INVALID_PART_SYNC (default), 2:ENABLED_STOP_INVALID_PART_LAUNCH
* KSP_SERVER_OFFLINETICKS - 0:DISABLED, 1:ENABLED (default)
* KSP_SERVER_LOGLEVEL - 0:DEBUG (default), 1:INFO, 2:CHAT, 3:ERROR, 4:FATAL
* KSP_SERVER_CHEATS - 0:DISABLED, 1:ENABLED (default)
* KSP_SERVER_HTTPSTATUS - 0:DISABLED (default), 1:ENABLED
* KSP_SERVER_MAXPLAYERS - Number of players (default 20), 0:Unlimited
* KSP_SERVER_MOTD - Message of the day



Example docker run:
```
docker run --name "KSP-Server"        \
  -e KSP_SERVER_NAME="KSP-Server"      \
  -v ~/ksp/Universe:/data/ksp/DMPServer/Universe       \
  -p 6702:6702                             \
  gameservers/kerbal-space-program:latest
```

For more information on the Kerbal Space Program Dedicated server see the D-MP website at: [https://d-mp.org/](https://d-mp.org/)
