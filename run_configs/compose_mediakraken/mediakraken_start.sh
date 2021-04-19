host_ip="$(hostname -I | awk '{print $1}')"
export HOST_IP=$host_ip && docker-compose up -d