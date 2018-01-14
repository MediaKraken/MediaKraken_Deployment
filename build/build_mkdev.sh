#@IgnoreInspection BashAddShebang
apk update
apk upgrade
apk add alpine-sdk linux-headers postgresql-dev python-dev libffi-dev openldap-dev \
    jpeg-dev libxml2-dev libxslt-dev musl-dev net-snmp-dev openldap-dev portaudio-dev \
    mesa-dev gstreamer-dev sdl2-dev sdl2_ttf-dev sdl2_image-dev sdl2_mixer-dev

pip install -r ../testing/pip_requirements.txt
pip install -r ../docker/alpine/ComposeMediaKrakenMetadata/requirements.txt
pip install -r ../docker/alpine/ComposeMediaKrakenServer/requirements.txt
pip install -r ../docker/alpine/ComposeMediaKrakenTheater/requirements.txt
pip install -r ../docker/alpine/ComposeMediaKrakenWebServer/requirements.txt

./theater_client_build_alpine.sh
