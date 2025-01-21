FROM steamcmd/steamcmd:ubuntu-noble

RUN apt update && \
    apt install -y --no-install-recommends wine wine64 winbind xvfb

WORKDIR /srv/sotf

RUN steamcmd +@sSteamCmdForcePlatformType windows +force_install_dir /srv/sotf +login anonymous +app_update 2465200 validate +quit

COPY entrypoint.sh  config/steam_appid.txt /srv/sotf/
COPY config/dedicatedserver.cfg config/ownerswhitelist.txt /srv/sotf/userdata/

RUN chmod +x entrypoint.sh

EXPOSE 8766/udp 27016/udp 9700/udp

ENTRYPOINT ["/srv/sotf/entrypoint.sh"]
