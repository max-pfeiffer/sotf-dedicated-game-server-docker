[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/max-pfeiffer/sotf-dedicated-game-server-docker/graph/badge.svg?token=O3Y6wQopoG)](https://codecov.io/gh/max-pfeiffer/sotf-dedicated-game-server-docker)
![pipeline workflow](https://github.com/max-pfeiffer/sotf-dedicated-game-server-docker/actions/workflows/pipeline.yaml/badge.svg)

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

## Environment Variables:

### Server Configuration
| Key                          | Values                                                                | Default Value  | Description                                                                                                                                                                                                                                                                                                                                                                 |
|------------------------------|-----------------------------------------------------------------------|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IPADDRESS                    | Any IPv4 address formatted string                                     | 0.0.0.0        | Listening interface for the game server, usually 0.0.0.0 if listening on all interfaces.                                                                                                                                                                                                                                                                                    | 
| GAMEPORT                     | Integer                                                               | 8766           | UDP port used for gameplay netcode (Bolt).                                                                                                                                                                                                                                                                                                                                  |
| QUERYPORT                    | Integer                                                               | 27016          | UDP port used by Steam to list the server and enable the discovery services.                                                                                                                                                                                                                                                                                                |
| BLOBSYNCPORT                 | Integer                                                               | 9700           | BlobSyncPort UDP port used by the BlobSync system to initialize game systems and exchange data.                                                                                                                                                                                                                                                                             |
| SERVERNAME                   | String                                                                | My Sotf Server | Name of the server visible in the server list, and in the Steam contacts.                                                                                                                                                                                                                                                                                                   |
| MAXPLAYERS                   | Integer                                                               | 8              | The maximum number of players allowed simultaneously on the server. (1 - 8)                                                                                                                                                                                                                                                                                                 |
| PASSWORD                     | String                                                                |                | Adds a password to make your server “private”. Upon connection, this password will be requested before the client can proceed. (Max. 40 chars)                                                                                                                                                                                                                              |
| LANONLY                      | Bool                                                                  | false          | Allows or restricts the server visibility to LAN only.                                                                                                                                                                                                                                                                                                                      |
| SAVESLOT                     | Integer                                                               | 1              | When creating a new save, this number will be the id of the save.                                                                                                                                                                                                                                                                                                           |
| SAVEMODE                     | New<br/>Continue                                                      | Continue       | Game save initialization mode.<br/>“**continue**”: will create a new save on SaveSlot if it doesn’t exist, or load it if it exist.<br/>“**new**”: will create a new game, with a new game id, and overwrite any game previously saved on the SaveSlot. If the server stops and restarts, the previous save will be overwritten for as long as the mode is set to “**new**”. |
| GAMEMODE                     | Normal<br/>Hard<br/>Hardsurvival<br/>Peaceful<br/>Creative<br/>Custom | Normal         | Sets the difficulty game mode when creating a new save. This parameter is ignored if loading a save (save mode set to “**continue**” with a save that exists on the slot). If the game mode is set to “**custom**”, then the custom game mode settings will be read from **CustomGameModeSettings** option, described later.                                                |
| SAVEINTERVAL                 | Integer                                                               | 600            | How often the game server automatically saves the game to SaveSlot, in seconds.                                                                                                                                                                                                                                                                                             |
| IDLEDAYCYCLESPEED            | Float                                                                 | 0.0            | A multiplier to how quickly the time passes compared to normal gameplay when the server is considered idle (no player connected).                                                                                                                                                                                                                                           |
| IDLETARGETFRAMERATE          | Integer                                                               | 5              | Target framerate of the server when it’s considered idle (no player connected).                                                                                                                                                                                                                                                                                             |
| ACTIVETARGETFRAMERATE        | Integer                                                               | 60             | Target framerate of the server when it’s NOT considered idle (one or more player connected).                                                                                                                                                                                                                                                                                |
| LOGFILESENABLED              | Bool                                                                  | true           | Defines if the logs will be written to files. The logs will be output in **<user data folder>/logs**.                                                                                                                                                                                                                                                                       |
| TIMESTAMPLOGFILENAMES        | Bool                                                                  | true           | Enabled log files timestamping.<br/>“**true**”: every time the server runs will dump log output to a new file, with filename having the following format: **sotf_log_{DateTime:yyyy-MM-dd_HH-mm-ss}.txt** <br/>“**false**”: the filename will be sotf_log.txt and previous log will be overwritten if it already exists.                                                    |
| TIMESTAMPLOGENTRIES          | Bool                                                                  | true           | Enables each log entry written to file to be timestamped.                                                                                                                                                                                                                                                                                                                   |
| SKIPNETWORKACCESSIBILITYTEST | Bool                                                                  | false          | Opt-out of network accessibility self tests: retrieval of the public IP and listing on Steam Master Server, as well as port accessibility check. Please note that only IPv4 is officially supported.                                                                                                                                                                        |

### Game Configuration

| Key             | Value  | Default Value | Description                                              |
|-----------------|--------|---------------|----------------------------------------------------------|
| TREEREGROWTH    | Bool   | true          | Enable automatic tree regrowth, triggered when sleeping. |
| STRUCTUREDAMAGE | Bool   | true          | Allow buildings to be damaged.                           |


### Custom game mode settings
These settings are only required if the game mode is set to **Custom**

| Key                     | Value                                    | Default Value | Description                                                                                                     |
|-------------------------|------------------------------------------|---------------|-----------------------------------------------------------------------------------------------------------------|
| CHEATS                  | Bool                                     | false         | Allows cheats on the server.                                                                                    |
| ENEMYSPAWN              | Bool                                     | true          | Enable enemies spawning.                                                                                        |
| ENEMYHEALTH             | Low<br/>Normal<br/>High                  | Normal        | Adjust enemy starting health.                                                                                   |
| ENEMYDAMAGE             | Low<br/>Normal<br/>High                  | Normal        | Adjust damage enemies can do.                                                                                   |
| ENEMYARMOUR             | Low<br/>Normal<br/>High                  | Normal        | Adjust enemies armor strength.                                                                                  |
| ENEMYAGGRESSION         | Low<br/>Normal<br/>High                  | Normal        | Adjust enemy aggression level.                                                                                  |
| ANIMALSPAWNRATE         | Low<br/>Normal<br/>High                  | Normal        | Adjust animal spawn rate.                                                                                       |
| ENEMYSEARCHPARTIES      | Low<br/>Normal<br/>High                  | Normal        | Adjust the frequency of enemy search parties.                                                                   |
| STARTINGSEASON          | Spring<br/>Summer<br/>Autumn<br/>Winter  | Summer        | Set environmental starting season.                                                                              |
| SEASONLENGTH            | Short<br/>Default<br/>Long<br/>Realistic | default       | Adjust season length.                                                                                           |
| DAYLENGTH               | Short<br/>Default<br/>Long<br/>Realistic | default       | Adjust day length.                                                                                              |
| PRECIPITATIONFREQUENCY  | Low<br/>Default<br/>High                 | default       | Adjust the frequency of rain and snow.                                                                          |
| CONSUMABLEEFFECTS       | Normal<br/>Hard                          | Normal        | Enable damage taken when low hydration and low fullness.                                                        |
| PLAYERSTATSDAMAGE       | Off<br/>Normal<br/>Hard                  | Normal        | Enable damage from each bad or rotten food and drink.                                                           |
| COLDPENALTIES           | Off<br/>Normal<br/>Hard                  | Normal        | Adjusts the severity that cold will affect health and stamina regeneration.                                     |
| STATREGENERATIONPENALTY | Off<br/>Normal<br/>Hard                  | Normal        | Reduces the rate that health and stamina will regenerate.                                                       |
| REDUCEDFOODINCONTAINERS | Bool                                     | false         | Reduces the amount of food found in containers.                                                                 |
| SINGLEUSECONTAINERS     | Bool                                     | true          | Containers can only be opened once.                                                                             |
| BUILDINGRESISTANCE      | Low<br/>Normal<br/>High                  | Normal        | Adjust building resistance to attacks.                                                                          |
| CREATIVEMODE            | Bool                                     | false         | Enable creative mode game.                                                                                      |
| PLAYERSIMMORTALMODE     | Bool                                     | false         | Enable god mode for all players.                                                                                |
| FORCEPLACEFULLLOAD      | Bool                                     | false         | If true, everything players have in hands will be placed in a single click (stones, stone floors, wood floors)  |
| NOCUTTINGSSPAWN         | Bool                                     | false         | If true, disable cuttings spawning.                                                                             |
| ONEHITTOCUTTREE         | Bool                                     | false         | Enable chopping tree with a single hit.                                                                         |




All descriptions are from [Dedicated Server Configuration Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2992700419&snr=1_2108_9__2107)