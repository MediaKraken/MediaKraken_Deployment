# Windward Game Server

See more about Windward at: [http://www.tasharen.com/windward/](http://www.tasharen.com/windward/)


You can use the following environment variables passed to the Docker container to configure your server.

* WINDWARD_SERVER_NAME - The name of the windward server.
* WINDWARD_SERVER_WORLD - The name of the world to create on the server.
* WINDWARD_SERVER_PORT - The port number to use for the server (Note - This will require you exposing other ports within your container)
* WINDWARD_SERVER_PUBLIC - 1 = public, anything else will make this server private (default: 0).
* WINDWARD_SERVER_ADMIN - Steam ID of the server admin (Currently only supports a single server admin).

Example docker run:
```
docker run --name "Windward-Server"        \
  -e WINDWARD_SERVER_NAME="My Server"      \
  -e WINDWARD_SERVER_WORLD="world"         \
  -e WINDWARD_SERVER_ADMIN=123456787453234 \
  -v ~/WindwardServer:/data/windward       \
  -p 5127:5127                             \
  gameservers/windward:latest
```

For more information on the Windward Dedicated server see the windward wiki at gamepedia: [http://windward.gamepedia.com/Dedicated_Server](http://windward.gamepedia.com/Dedicated_Server)
