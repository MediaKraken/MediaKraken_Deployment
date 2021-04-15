
![Battlefield 1942](https://raw.githubusercontent.com/InAnimaTe/docker-battlefield1942/master/bf1942_logo.jpg)

bf42-dock
===

Dockerized battlefield 1942


Prerequisites
---

* [docker](https://docker.com/)


Building
---

    $ docker build -t bf42 .
    $ docker run -d -p 14567:14567/udp bf42
    
The above run command with published port 14567 is the bare minimum for direct connecting to the server. If you want to host a LAN or internet game and have the game show up in the battlefield server browser, you need to publish more ports.

LAN game:

    $ docker run -d -p 14567:14567/udp -p 3117:3117/udp bf42
    
Internet game:

    $ ?? not tested yet


Notes
---

Battlefield 1942 needs these ports:

* 14567/udp - game traffic
* 3117/udp  - server browser client request (LAN only)
* 22000/udp - server browser response (LAN only)
* 27900/tcp - gamespy heartbeat

