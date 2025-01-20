FROM steamcmd/steamcmd:debian-bookworm

RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests software-properties-common apt-transport-https gnupg2 wget procps winbind xvfb \
    && mkdir -pm755 /etc/apt/keyrings \
    && wget --output-document /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key \
    && wget --timestamping --directory-prefix=/etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests winehq-stable \
    && apt-get remove -y --purge software-properties-common apt-transport-https gnupg2 wget \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /srv/sotf

RUN steamcmd +force_install_dir /srv/sotf +login anonymous +app_update 2465200 validate +quit
