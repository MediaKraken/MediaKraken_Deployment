#!/bin/sh
docker-compose config | docker stack deploy --compose-file - mkstack
