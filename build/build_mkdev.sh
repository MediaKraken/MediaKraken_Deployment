apk update
apk upgrade
apk add alpine-sdk

pip install -r ../testing/pip_requirements.txt
pip install -r ../docker/alpine/ComposeMediaKrakenWebServer/requirements.txt
pip install -r ../docker/alpine/ComposeMediaKrakenServer/requirements.txt

./theater_client_build_alpine.sh
