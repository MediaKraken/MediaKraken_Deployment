# https://sick.codes/run-wine-windows-inside-docker-autoclick-winetricks-save-as-dotnet45-net46/
FROM ubuntu:20.10

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
ENV DISPLAY :99

WORKDIR /root

RUN apt update -y
  && apt install wine-stable wine-development winetricks xdotool -y
  && dpkg --add-architecture i386
  && apt-get update && apt-get install wine32 -y
  && apt install zenity -y
  && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
  && apt-get install keyboard-configuration -y
  && apt install xfce4 xfce4-goodies -y
  && apt install xvfb -y
  && apt install winbind -y

COPY display.sh display.sh
RUN chmod a+x display.sh

CMD { bash display.sh; }