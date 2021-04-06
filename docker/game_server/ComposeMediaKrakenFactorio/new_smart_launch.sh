#!/bin/bash
echo '      ___         ___           ___                       ___           ___                       ___     '
echo '     /  /\       /  /\         /  /\          ___        /  /\         /  /\        ___          /  /\    '
echo '    /  /:/_     /  /::\       /  /:/         /  /\      /  /::\       /  /::\      /  /\        /  /::\   '
echo '   /  /:/ /\   /  /:/\:\     /  /:/         /  /:/     /  /:/\:\     /  /:/\:\    /  /:/       /  /:/\:\  '
echo '  /  /:/ /:/  /  /:/~/::\   /  /:/  ___    /  /:/     /  /:/  \:\   /  /:/~/:/   /__/::\      /  /:/  \:\ '
echo ' /__/:/ /:/  /__/:/ /:/\:\ /__/:/  /  /\  /  /::\    /__/:/ \__\:\ /__/:/ /:/___ \__\/\:\__  /__/:/ \__\:\'
echo ' \  \:\/:/   \  \:\/:/__\/ \  \:\ /  /:/ /__/:/\:\   \  \:\ /  /:/ \  \:\/:::::/    \  \:\/\ \  \:\ /  /:/'
echo '  \  \::/     \  \::/       \  \:\  /:/  \__\/  \:\   \  \:\  /:/   \  \::/~~~~      \__\::/  \  \:\  /:/ '
echo '   \  \:\      \  \:\        \  \:\/:/        \  \:\   \  \:\/:/     \  \:\          /__/:/    \  \:\/:/  '
echo '    \  \:\      \  \:\        \  \::/          \__\/    \  \::/       \  \:\         \__\/      \  \::/   '
echo '     \__\/       \__\/         \__\/                     \__\/         \__\/                     \__\/    '
echo ''
echo 'Downloading latest Factorio version'

if [ -z $FACTORIO_SERVER_VERSION ]; then

    if [ "$FACTORIO_BUILD" == "experimental" ]; then
        factorio_build="experimental"
        factorio_url="https://www.factorio.com/download-headless/${factorio_build}"
    else
        factorio_build=""
        factorio_url="https://www.factorio.com/download-headless"
    fi
    echo "Downloading Factorio latest ${factorio_build} release"
    wget -q -O - ${factorio_url} | grep -o -m1 "/get-download/.*/headless/linux64" | awk '{print "--no-check-certificate https://www.factorio.com"$1" -O /tmp/factorio.tar.xz"}' | xargs wget
else
    echo "Downloading Factorio version ${FACTORIO_SERVER_VERSION}"
    wget --no-check-certificate -O /tmp/factorio.tar.xz https://www.factorio.com/get-download/${FACTORIO_SERVER_VERSION}/headless/linux64

fi
    tar xf /tmp/factorio.tar.xz -C /opt
    rm -rf /tmp/factorio.tar.xz

# Checking if server is ready 
if [ $FACTORIO_WAITING == true ] 
then 
  until [ -f /opt/factorio/saves/ready ] 
  do 
    echo "# Waiting for backup daemon to be ready" 
    sleep 1 
  done 
fi
# Setting initial command
factorio_command="/opt/factorio/bin/x64/factorio"
# Include server-settings.json if one or more variables are populated
if [ "$FACTORIO_SERVER_NAME" ] \
|| [ "$FACTORIO_SERVER_DESCRIPTION" ] \
|| [ "$FACTORIO_SERVER_MAX_PLAYERS" ] \
|| [ "$FACTORIO_SERVER_VISIBILITY_PUBLIC" ] \
|| [ "$FACTORIO_USER_USERNAME" ] \
|| [ "$FACTORIO_USER_PASSWORD" ] \
|| [ "$FACTORIO_USER_TOKEN" ] \
|| [ "$FACTORIO_SERVER_GAME_PASSWORD" ] \
|| [ "$FACTORIO_SERVER_VERIFY_IDENTITY" ]
then
  factorio_command="$factorio_command --server-settings /opt/factorio/server-settings.json"
  # Set Server Name default value if not set by user param
  if [ -z "$FACTORIO_SERVER_NAME" ]
  then
    FACTORIO_SERVER_NAME="Factorio Server $VERSION"
  fi
  # Set Verify User Identity default value if not set by user param
  if [ -z "$FACTORIO_SERVER_VERIFY_IDENTITY" ]
  then
    FACTORIO_SERVER_VERIFY_IDENTITY="false"
  fi
  # Check for supplied credentials if visibility is set to public
  if [ "$FACTORIO_SERVER_VISIBILITY_PUBLIC" == "true" ]
  then
    if [ -z "$FACTORIO_USER_USERNAME" ]
    then
      echo "###"
      echo "# Server Visibility is set to public but no factorio.com Username is supplied!"
      echo "# Append: --env FACTORIO_USER_USERNAME=[USERNAME]"
      echo "# Defaulting back to Public Server Visibility: false"
      echo "###"
      FACTORIO_SERVER_VISIBILITY="\"public\": false,"
    else [ "$FACTORIO_USER_USERNAME" ]
      if [ -z $FACTORIO_USER_PASSWORD ]
      then
        echo "###"
        echo "# Server Visibility is set to public but neither factorio.com Password is supplied!"
        echo "# Append: --env FACTORIO_USER_PASSWORD=[PASSWORD]"
        echo "# Defaulting back to Server Visibility: hidden"
        echo "###"
        FACTORIO_SERVER_VISIBILITY="\"public\": false,"
      else
        FACTORIO_SERVER_VISIBILITY="\"public\": true,"
      fi
    fi
  fi
  FACTORIO_SERVER_VISIBILITY="${FACTORIO_SERVER_VISIBILITY} \"lan\": true"
fi
# Populate server-settings.json
SERVER_SETTINGS=/opt/factorio/server-settings.json
cat << EOF > $SERVER_SETTINGS
{
  "name": "${FACTORIO_SERVER_NAME}",
  "description": "${FACTORIO_SERVER_DESCRIPTION}",
  "tags": ["game", "tags"],
  "max_players": "${FACTORIO_SERVER_MAX_PLAYERS}",

  "visibility": {${FACTORIO_SERVER_VISIBILITY}},

  "username": "${FACTORIO_USER_USERNAME}",
  "password": "${FACTORIO_USER_PASSWORD}",

  "_comment_token": "Authentication token. May be used instead of 'password' above.",
  "token": "${FACTORIO_USER_TOKEN}",

  "game_password": "${FACTORIO_SERVER_GAME_PASSWORD}",

  "_comment_verify_user_identity": "When set to true, the server will only allow clients that have a valid Factorio.com account",
  "verify_user_identity": ${FACTORIO_SERVER_VERIFY_IDENTITY},
  "_commend_max_upload_in_kilobytes_per_second" : "optional, default value is 0. 0 means unlimited.",
  "max_upload_in_kilobytes_per_second": 0
}
EOF
# Setting heavy mode option
if [ "$FACTORIO_MODE" == "heavy" ]
then
factorio_command="$factorio_command --heavy"
fi
# Setting complete mode option
if [ "$FACTORIO_MODE" == "complete" ]
then
factorio_command="$factorio_command --complete"
fi
# Setting auto-pause option
if [ "$FACTORIO_NO_AUTO_PAUSE" == true ] 
then
factorio_command="$factorio_command --no-auto-pause"
fi
# Setting rcon-port option
factorio_command="$factorio_command --rcon-port 27015"
# Setting rcon password option
if [ -z $FACTORIO_RCON_PASSWORD ]
then
  FACTORIO_RCON_PASSWORD=$(cat /dev/urandom | tr -dc 'a-f0-9' | head -c16)
  echo "###"
  echo "# RCON password is '$FACTORIO_RCON_PASSWORD'"
  echo "###"
fi
factorio_command="$factorio_command --rcon-password $FACTORIO_RCON_PASSWORD"
# Show server-settings.json config
# removed FACTORIO_USER_TOKEN condition cause of bug (https://github.com/zopanix/docker_factorio_server/issues/23)
if [ "$FACTORIO_SERVER_NAME" ] \
|| [ "$FACTORIO_SERVER_DESCRIPTION" ] \
|| [ "$FACTORIO_SERVER_MAX_PLAYERS" ] \
|| [ "$FACTORIO_SERVER_VISIBILITY_PUBLIC" ] \
|| [ "$FACTORIO_USER_USERNAME" ] \
|| [ "$FACTORIO_USER_PASSWORD" ] \
|| [ "$FACTORIO_SERVER_GAME_PASSWORD" ] \
|| [ "$FACTORIO_SERVER_VERIFY_IDENTITY" ]
then
  echo "###"
  echo "# Server Config:"
  echo "# Server Name = '$FACTORIO_SERVER_NAME'"
  echo "# Server Description = '$FACTORIO_SERVER_DESCRIPTION'"
  echo "# Server Password = '$FACTORIO_SERVER_GAME_PASSWORD'"
  echo "# Max Players = '$FACTORIO_SERVER_MAX_PLAYERS'"
  echo "# Server Public Visibility = '$FACTORIO_SERVER_VISIBILITY_PUBLIC'"
  echo "# Verify User Identify = '$FACTORIO_SERVER_VERIFY_IDENTITY'"
  echo "# Factorio Username = '$FACTORIO_USER_USERNAME'"
  echo "# Factorio Password = '$FACTORIO_USER_PASSWORD'"
#  echo "# Factorio User Token = '$FACTORIO_USER_TOKEN'"
  echo "###"
fi

if [ "$FACTORIO_SERVER_PORT" ]; then
    sed -i -s "s/^port=.*/port=${FACTORIO_SERVER_PORT}/" /opt/factorio/config/config.ini
fi
# TODO Adding this because of bug, will need to be removed once bug in factorio is fixed
cd /opt/factorio/saves
# Handling save settings
save_dir="/opt/factorio/saves"
if [ -z $FACTORIO_SAVE ]
then
  if [ "$(ls -A $save_dir)" ]
  then
    echo "###"
    echo "# Taking latest save"
    echo "###"
  else
    echo "###"
    echo "# Creating a new map [server.zip]"
    echo "###"
    /opt/factorio/bin/x64/factorio --create server.zip
  fi
  factorio_command="$factorio_command --start-server-load-latest"
else
  factorio_command="$factorio_command --start-server $FACTORIO_SAVE"
fi
echo "###"
echo "# Launching Game"
echo "###"
# Closing stdin
exec 0<&-
exec $factorio_command
