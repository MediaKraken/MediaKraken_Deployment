FROM ubuntu:20.10
WORKDIR /root
RUN apt update -y
RUN apt install wine-stable wine-development winetricks xdotool -y
RUN dpkg –add-architecture i386
RUN apt-get update && apt-get install wine32 -y
RUN apt install zenity -y
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install keyboard-configuration -y
RUN apt install xfce4 xfce4-goodies -y
RUN apt install xvfb -y
RUN apt install winbind -y
ENV DISPLAY :99

WORKDIR /root
ADD display.sh display.sh
RUN chmod a+x display.sh

CMD { bash display.sh; }