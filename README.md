# Sons of the Forest Dedicated Game Server - Docker Image

## Docker build
```shell
docker build --tag sotf .
```
## Docker Run
```shell
docker run --rm -it --publish 8766:8766/udp --publish 9700:9700/tcp --publish 27016:27016/tcp sotf
```

## Information Sources
* [SteamDB](https://steamdb.info/app/2465200/info/)
* [Dedicated Server Configuration Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2992700419)
* [How To Install and use Wine on Debian](https://forums.debian.net/viewtopic.php?t=154513)