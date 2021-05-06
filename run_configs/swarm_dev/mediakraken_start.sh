#!/bin/sh
host_ip="$(hostname -I | awk '{print $1}')"
export HOST_IP=$host_ip && docker stack deploy --compose-file docker-compose-stack.yml mkstack