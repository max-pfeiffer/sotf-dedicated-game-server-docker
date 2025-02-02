#!/usr/bin/env bash

# Start virtual X server
export DISPLAY=":99"
rm -rf /tmp/.X* 2> /dev/null
Xvfb :99 -screen 0 1024x768x16 -nolisten tcp -nolisten unix &
wineboot -r

# Create Config
python3 /config_creator.py > /srv/sotf/userdata/dedicatedserver.cfg

# Start SOTF server
wine /srv/sotf/SonsOfTheForestDS.exe -userdatapath /srv/sotf/userdata "$@"
