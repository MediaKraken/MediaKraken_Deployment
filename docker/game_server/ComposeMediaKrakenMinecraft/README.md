[![Docker Pulls](https://img.shields.io/docker/pulls/itzg/minecraft-server.svg)](https://hub.docker.com/r/itzg/minecraft-server/)
[![Docker Stars](https://img.shields.io/docker/stars/itzg/minecraft-server.svg?maxAge=2592000)](https://hub.docker.com/r/itzg/minecraft-server/)
[![GitHub Issues](https://img.shields.io/github/issues-raw/itzg/docker-minecraft-server.svg)](https://github.com/itzg/docker-minecraft-server/issues)
[![Discord](https://img.shields.io/discord/660567679458869252?label=Discord&logo=discord)](https://discord.gg/DXfKpjB)
[![Build and Publish](https://github.com/itzg/docker-minecraft-server/workflows/Build%20and%20Publish/badge.svg)](https://github.com/itzg/docker-minecraft-server/actions)
[![](https://img.shields.io/badge/Donate-Buy%20me%20a%20coffee-orange.svg)](https://www.buymeacoffee.com/itzg)

This docker image provides a Minecraft Server that will automatically download the latest stable
version at startup. You can also run/upgrade to any specific version or the
latest snapshot. See the _Versions_ section below for more information.

To simply use the latest stable version, run

    docker run -d -it -p 25565:25565 -e EULA=TRUE itzg/minecraft-server

where the standard server port, 25565, will be exposed on your host machine.

If you want to serve up multiple Minecraft servers or just use an alternate port,
change the host-side port mapping such as

    ... -p 25566:25565 ...

will serve your Minecraft server on your host's port 25566 since the `-p` syntax is
`host-port`:`container-port`.

Speaking of multiple servers, it's handy to give your containers explicit names using `--name`, such as naming this one "mc"

    ... --name mc itzg/minecraft-server

With that you can easily view the logs, stop, or re-start the container:

    docker logs -f mc
        ( Ctrl-C to exit logs action )

    docker stop mc

    docker start mc

> Be sure to always include `-e EULA=TRUE` in your commands, as Mojang/Microsoft requires EULA acceptance.

## Looking for a Bedrock Dedicated Server

For Minecraft clients running on consoles, mobile, or native Windows, you'll need to
use this image instead:

[itzg/minecraft-bedrock-server](https://hub.docker.com/r/itzg/minecraft-bedrock-server)

## Interacting with the server

[RCON](http://wiki.vg/RCON) is enabled by default, so you can `exec` into the container to
access the Minecraft server console:

```
docker exec -i mc rcon-cli
```

Note: The `-i` is required for interactive use of rcon-cli.

To run a simple, one-shot command, such as stopping a Minecraft server, pass the command as
arguments to `rcon-cli`, such as:

```
docker exec mc rcon-cli stop
```

_The `-i` is not needed in this case._

In order to attach and interact with the Minecraft server, add `-it` when starting the container, such as

    docker run -d -it -p 25565:25565 --name mc itzg/minecraft-server

With that you can attach and interact at any time using

    docker attach mc

and then Control-p Control-q to **detach**.

For remote access, configure your Docker daemon to use a `tcp` socket (such as `-H tcp://0.0.0.0:2375`)
and attach from another machine:

    docker -H $HOST:2375 attach mc

Unless you're on a home/private LAN, you should [enable TLS access](https://docs.docker.com/articles/https/).

## Data Directory

Everything the container manages is located under the **container's** `/data` path, as shown here:

![](docs/level-vs-world.drawio.png)

> NOTE: The container path `/data` is pre-declared as a volume, so if you do nothing then it will be allocated as an anonymous volume. As such, it is subject to removal when the container is removed. 

### Attaching data directory to host filesystem

In most cases the easier way to persist and work with the minecraft data files is to use the `-v` argument to map a directory on your host machine to the container's `/data` directory, such as the following where `/home/user/minecraft-data` would be a directory of your choosing on your host machine:

    docker run -d -v /home/user/minecraft-data:/data ...

When attached in this way you can stop the server, edit the configuration under your attached directory and start the server again to pick up the new configuration.

With Docker Compose, setting up a host attached directory is even easier since relative paths can be configured. For example, with the following `docker-compose.yml` Docker will automatically create/attach the relative directory `minecraft-data` to the container.

```yaml
version: "3"

services:
  mc:
    image: itzg/minecraft-server
    ports:
      - 25565:25565
    environment:
      EULA: "TRUE"
    volumes:
      # attach a directory relative to the directory containing this compose file
      - ./minecraft-data:/data
```

### Converting anonymous `/data` volume to named volume

If you had used the commands in the first section, without the `-v` volume attachment, then an anonymous data volume was created by Docker. You can later bring over that content to a named or host attached volume using the following procedure.

> In this example, it is assumed the original container was given a `--name` of "mc", so change the container identifier accordingly.

First, stop the existing container:
```shell
docker stop mc
```

Use a temporary container to copy over the anonymous volume's content into a named volume, "mc" in this case:
```shell
docker run --rm --volumes-from mc -v mc:/new alpine cp -avT /data /new
```

Now you can recreate the container with any environment variable changes, etc by attaching the named volume created from the previous step:
```shell
docker run -d -it --name mc-new -v mc:/data -p 25565:25565 -e EULA=TRUE -e MEMORY=2G itzg/minecraft-server
```

## Versions

To use a different Minecraft version, pass the `VERSION` environment variable, which can have the value

- LATEST (the default)
- SNAPSHOT
- or a specific version, such as "1.7.9"

For example, to use the latest snapshot:

    docker run -d -e VERSION=SNAPSHOT ...

or a specific version:

    docker run -d -e VERSION=1.7.9 ...

When using "LATEST" or "SNAPSHOT" an upgrade can be performed by simply restarting the container.
During the next startup, if a newer version is available from the respective release channel, then
the new server jar file is downloaded and used. _NOTE: over time you might see older versions of
the server jar remain in the `/data` directory. It is safe to remove those._

## Running Minecraft server on different Java version

To use a different version of Java, please use a docker tag to run your Minecraft server.

| Tag name       | Java version | Linux  | JVM Type | Architecture      |
| -------------- | -------------|--------|----------|-------------------|
| latest         | 11           | Alpine | Hotspot  | amd64             |
| java8          | 8            | Alpine | Hotspot  | amd64             |
| java8-multiarch | 8           | Debian | Hotspot  | amd64,arm64,armv7 |
| java15         | 15           | Debian | Hotspot  | amd64,arm64,armv7 |
| java15-openj9  | 15           | Debian | OpenJ9   | amd64,arm64       |
| adopt11        | 11           | Alpine | Hotspot  | amd64             |
| openj9         | 8            | Alpine | OpenJ9   | amd64             |
| openj9-11      | 11           | Alpine | OpenJ9   | amd64             |
| multiarch      | 11           | Debian | Hotspot  | amd64,arm64,armv7 |
| multiarch-latest | 15+        | Debian | Hotspot  | amd64,arm64,armv7 |

For example, to use Java version 15 on any supported architecture:

    docker run --name mc itzg/minecraft-server:java15

> Keep in mind that some versions of Minecraft server can't work on the newest versions of Java. Also, FORGE doesn't support openj9 JVM implementation.

### Deprecated Image Tags

The following image tags have been deprecated and are no longer receiving updates:
- adopt13
- adopt14
- adopt15
- openj9-nightly

## Healthcheck

This image contains [mc-monitor](https://github.com/itzg/mc-monitor) and uses
its `status` command to continually check on the container's. That can be observed
from the `STATUS` column of `docker ps`

```
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                    PORTS                                 NAMES
b418af073764        mc                  "/start"            43 seconds ago      Up 41 seconds (healthy)   0.0.0.0:25565->25565/tcp, 25575/tcp   mc
```

You can also query the container's health in a script friendly way:

```
> docker container inspect -f "{{.State.Health.Status}}" mc
healthy
```

Some orchestration systems, such as Portainer, don't allow for disabling the default `HEALTHCHECK` declared by this image. In those cases you can approximate the disabling of healthchecks by setting the environment variable `DISABLE_HEALTHCHECK` to `true`.

## Deployment Templates and Examples

### Helm Charts

- [stable/minecraft](https://hub.helm.sh/charts/stable/minecraft) ([chart source](https://github.com/helm/charts/tree/master/stable/minecraft))
- [mcsh/server-deployment](https://github.com/mcserverhosting-net/charts)

### Examples

The [examples directory](https://github.com/itzg/docker-minecraft-server/tree/master/examples) also provides examples of deploying the [itzg/minecraft-server](https://hub.docker.com/r/itzg/minecraft-server/) Docker image.

### Amazon Web Services (AWS) Deployment

If you're looking for a simple way to deploy this to the Amazon Web Services Cloud, check out the [Minecraft Server Deployment (CloudFormation) repository](https://github.com/vatertime/minecraft-spot-pricing). This repository contains a CloudFormation template that will get you up and running in AWS in a matter of minutes. Optionally it uses Spot Pricing so the server is very cheap, and you can easily turn it off when not in use.

## Running a Forge Server

Enable [Forge server](http://www.minecraftforge.net/wiki/) mode by adding a `-e TYPE=FORGE` to your command-line.

The overall version is specified by `VERSION`, [as described in the section above](#versions) and will run the recommended Forge version by default. You can also choose to run a specific Forge version with `FORGEVERSION`, such as `-e FORGEVERSION=14.23.5.2854`.

    $ docker run -d -v /path/on/host:/data \
        -e TYPE=FORGE \
        -e VERSION=1.12.2 -e FORGEVERSION=14.23.5.2854 \
        -p 25565:25565 -e EULA=TRUE --name mc itzg/minecraft-server

To use a pre-downloaded Forge installer, place it in the attached `/data` directory and
specify the name of the installer file with `FORGE_INSTALLER`, such as:

    $ docker run -d -v /path/on/host:/data ... \
        -e FORGE_INSTALLER=forge-1.11.2-13.20.0.2228-installer.jar ...

To download a Forge installer from a custom location, such as your own file repository, specify
the URL with `FORGE_INSTALLER_URL`, such as:

    $ docker run -d -v /path/on/host:/data ... \
        -e FORGE_INSTALLER_URL=http://HOST/forge-1.11.2-13.20.0.2228-installer.jar ...

In both of the cases above, there is no need for the `VERSION` or `FORGEVERSION` variables.

### Managing mods

In order to manage mods, you have two options:

1. [Attach a host directory to the /data path](#attaching-data-directory-to-host-filesystem) and manage the contents of the `mods` subdirectory

2. Using a mods-mount

If the container paths `/mods` and/or `/config` exist, such as by attaching a docker volume or host path, then any files in either of these directories will be copied over to the respective `/data` subdirectory before starting Minecraft. 

If you want old mods to be removed as the `/mods` content is updated, then add `-e REMOVE_OLD_MODS=TRUE`. You can fine tune the removal process by specifying the `REMOVE_OLD_MODS_INCLUDE` and `REMOVE_OLD_MODS_EXCLUDE` variables. By default, everything will be removed. You can also specify the `REMOVE_OLD_MODS_DEPTH` (default is 16) variable to only delete files up to a certain level.

For example: `-e REMOVE_OLD_MODS=TRUE -e REMOVE_OLD_MODS_INCLUDE="*.jar" -e REMOVE_OLD_MODS_DEPTH=1` will remove all old jar files that are directly inside the `plugins/` or `mods/` directory.

You can specify the destination of the files that are copied from `/config` by setting the `COPY_CONFIG_DEST` variable, where the default is `/data/config`. For example, `-v ./config:/config -e COPY_CONFIG_DEST=/data` will allow you to copy over files like `bukkit.yml` and so on directly into the server directory.

> NOTE: If a file was updated in the destination path and is newer than the source file from `/config`, then it will not be overwritten.
    
## Running a Bukkit/Spigot server

Enable Bukkit/Spigot server mode by adding a `-e TYPE=BUKKIT` or `-e TYPE=SPIGOT` to your command-line.

    docker run -d -v /path/on/host:/data \
        -e TYPE=SPIGOT \
        -p 25565:25565 -e EULA=TRUE --name mc itzg/minecraft-server

If you are hosting your own copy of Bukkit/Spigot you can override the download URLs with:

- -e BUKKIT_DOWNLOAD_URL=<url>
- -e SPIGOT_DOWNLOAD_URL=<url>

You can build spigot from source by adding `-e BUILD_FROM_SOURCE=true`

Plugins can either be managed within the `plugins` subdirectory of the [data directory](#data-directory) or you can also [attach a `/plugins` volume](#deploying-plugins-from-attached-volume). If you add plugins while the container is running, you'll need to restart it to pick those up.

[You can also auto-download plugins using `SPIGET_RESOURCES`.](#auto-downloading-spigotmcbukkitpapermc-plugins)

> NOTE some of the `VERSION` values are not as intuitive as you would think, so make sure to click into the version entry to find the **exact** version needed for the download. For example, "1.8" is not sufficient since their download naming expects `1.8-R0.1-SNAPSHOT-latest` exactly.

## Running a Paper server

Enable Paper server mode by adding a `-e TYPE=PAPER` to your command-line.

By default the container will run the latest build of [Paper server](https://papermc.io/downloads)
but you can also choose to run a specific build with `-e PAPERBUILD=205`.

    docker run -d -v /path/on/host:/data \
        -e TYPE=PAPER \
        -p 25565:25565 -e EULA=TRUE --name mc itzg/minecraft-server

If you are hosting your own copy of Paper you can override the download URL with:

- -e PAPER_DOWNLOAD_URL=<url>

An example compose file is provided at
[examples/docker-compose-paper.yml](examples/docker-compose-paper.yml).

If you have attached a host directory to the `/data` volume, then you can install plugins via the `plugins` subdirectory. You can also [attach a `/plugins` volume](#deploying-plugins-from-attached-volume). If you add plugins while the container is running, you'll need to restart it to pick those up.

[You can also auto-download plugins using `SPIGET_RESOURCES`.](#auto-downloading-spigotmcbukkitpapermc-plugins)

## Running a Tuinity server

A [Tuinity](https://github.com/Spottedleaf/Tuinity) server, which is a fork of Paper aimed at improving server performance at high playercounts.

    -e TYPE=TUINITY

> **NOTE** only `VERSION=LATEST` is supported

## Running a Purpur server

A [Purpur](https://purpur.pl3x.net/) server, which is "a fork of Paper and Tuinity with the goal of providing new and interesting configuration options".

    -e TYPE=PURPUR

> NOTE: the `VERSION` variable is used to lookup a build of Purpur to download

Extra variables:
- `PURPUR_BUILD=LATEST` : set a specific Purpur build to use
- `FORCE_REDOWNLOAD=false` : set to true to force the located server jar to be re-downloaded

## Running a Yatopia server

A [Yatopia](https://github.com/YatopiaMC/Yatopia) server, which is a "blazing fast Tuinity fork with best in class performance".

    -e TYPE=YATOPIA

> NOTE: the `VERSION` variable is used to locate the Yatopia version to download

Extra variables:
- `RELEASE=stable` : set to `stable` or `latest`
- `FORCE_REDOWNLOAD=false` : set to true to force the located server jar to be re-downloaded

## Running a Magma server

A [Magma](https://magmafoundation.org/) server, which is a combination of Forge and PaperMC, can be used with

    -e TYPE=MAGMA

> **NOTE** there are limited base versions supported, so you will also need to  set `VERSION`, such as "1.12.2"


## Running a Mohist server

A [Mohist](https://github.com/Mohist-Community/Mohist) server can be used with

    -e TYPE=MOHIST

> **NOTE** there are limited base versions supported, so you will also need to  set `VERSION`, such as "1.12.2"

By default the latest build will be used; however, a specific build number can be selected by setting `MOHIST_BUILD`, such as

    -e VERSION=1.16.5 -e MOHIST_BUILD=374

## Running a Catserver type server

A [Catserver](http://catserver.moe/) type server can be used with

    -e TYPE=CATSERVER

> **NOTE** Catserver only provides a single release stream, so `VERSION` is ignored

## Running a server with a Feed the Beast modpack

> **NOTE** requires one of the Debian based images listed in [the Java versions section](#running-minecraft-server-on-different-java-version).

[Feed the Beast application](https://www.feed-the-beast.com/) modpacks are supported by using `-e TYPE=FTBA` (**note** the "A" at the end of the type). This server type will automatically take care of downloading and installing the modpack and appropriate version of Forge, so the `VERSION` does not need to be specified.

### Environment Variables:
- `FTB_MODPACK_ID`: **required**, the numerical ID of the modpack to install. The ID can be located by [finding the modpack](https://www.feed-the-beast.com/modpack) and using the "ID" displayed next to the name
- `FTB_MODPACK_VERSION_ID`: optional, the numerical Id of the version to install. If not specified, the latest version will be installed. The "Version ID" can be obtained by drilling into the Versions tab and clicking a specific version.

### Upgrading

If a specific `FTB_MODPACK_VERSION_ID` was not specified, simply restart the container to pick up the newest modpack version. If using a specific version ID, recreate the container with the new version ID.

### Example

The following example runs the latest version of [FTB Presents Direwolf20 1.12](https://ftb.neptunepowered.org/pack/ftb-presents-direwolf20-1-12/):

```
docker run -d --name mc-ftb -e EULA=TRUE \
  -e TYPE=FTBA -e FTB_MODPACK_ID=31 \
  -p 25565:25565 \
  itzg/minecraft-server:multiarch
```

> Normally you will also add `-v` volume for `/data` since the mods and config are installed there along with world data.

## Running a server with a CurseForge modpack

Enable this server mode by adding `-e TYPE=CURSEFORGE` to your command-line,
but note the following additional steps needed...

You need to specify a modpack to run, using the `CF_SERVER_MOD` environment
variable. A CurseForge server modpack is available together with its respective
client modpack at <https://www.curseforge.com/minecraft/modpacks> .

Now you can add a `-e CF_SERVER_MOD=name_of_modpack.zip` to your command-line.

    docker run -d -v /path/on/host:/data -e TYPE=CURSEFORGE \
        -e CF_SERVER_MOD=SkyFactory_4_Server_4.1.0.zip \
        -p 25565:25565 -e EULA=TRUE --name mc itzg/minecraft-server

If you want to keep the pre-download modpacks separate from your data directory,
then you can attach another volume at a path of your choosing and reference that.
The following example uses `/modpacks` as the container path as the pre-download area:

    docker run -d -v /path/on/host:/data -v /path/to/modpacks:/modpacks \
        -e TYPE=CURSEFORGE \
        -e CF_SERVER_MOD=/modpacks/SkyFactory_4_Server_4.1.0.zip \
        -p 25565:25565 -e EULA=TRUE --name mc itzg/minecraft-server

#### Modpack data directory

By default, CurseForge modpacks are expanded into the sub-directory `/data/FeedTheBeast` and executed from there. (The default location was chosen for legacy reasons, when Curse and FTB were maintained together.)

The directory can be changed by setting `CF_BASE_DIR`, such as `-e CF_BASE_DIR=/data`.

#### Buggy start scripts

Some modpacks have buggy or overly complex start scripts. You can avoid using the bundled start script and use this image's standard server-starting logic by adding `-e USE_MODPACK_START_SCRIPT=false`.

### Fixing "unable to launch forgemodloader"

If your server's modpack fails to load with an error [like this](https://support.feed-the-beast.com/t/cant-start-crashlanding-server-unable-to-launch-forgemodloader/6028/2):

    unable to launch forgemodloader

then you apply a workaround by adding this to the run invocation:

    -e FTB_LEGACYJAVAFIXER=true

## Running a SpongeVanilla server

Enable SpongeVanilla server mode by adding a `-e TYPE=SPONGEVANILLA` to your command-line.
By default the container will run the latest `STABLE` version.
If you want to run a specific version, you can add `-e SPONGEVERSION=1.11.2-6.1.0-BETA-19` to your command-line.

    docker run -d -v /path/on/host:/data -e TYPE=SPONGEVANILLA \
        -p 25565:25565 -e EULA=TRUE --name mc itzg/minecraft-server

You can also choose to use the `EXPERIMENTAL` branch.
Just change it with `SPONGEBRANCH`, such as:

    $ docker run -d -v /path/on/host:/data ... \
        -e TYPE=SPONGEVANILLA -e SPONGEBRANCH=EXPERIMENTAL ...

## Running a Fabric Server

Enable [Fabric server](http://fabricmc.net/use/) mode by adding a `-e TYPE=FABRIC` to your command-line. By default, the container will run the latest version, but you can also choose to run a specific version with `VERSION`.

```
docker run -d -v /path/on/host:/data \
    -e TYPE=FABRIC \
    -p 25565:25565 -e EULA=TRUE --name mc itzg/minecraft-server
```

A specific installer version can be requested using `FABRIC_INSTALLER_VERSION`. 

To use a pre-downloaded Fabric installer, place it in a directory attached into the container, such as the `/data` volume and specify the name of the installer file with `FABRIC_INSTALLER`, such as:

```
docker run -d -v /path/on/host:/data ... \
    -e FABRIC_INSTALLER=fabric-installer-0.5.0.32.jar ...
```

To download a Fabric installer from a custom location, such as your own file repository, specify the URL with `FABRIC_INSTALLER_URL`, such as:

```
docker run -d -v /path/on/host:/data ... \
    -e FABRIC_INSTALLER_URL=http://HOST/fabric-installer-0.5.0.32.jar ...
```

In order to add mods, you have two options:

### Using the /data volume

This is the easiest way if you are using a persistent `/data` mount.

To do this, you will need to attach the container's `/data` directory
(see "Attaching data directory to host filesystem”).
Then, you can add mods to the `/path/on/host/mods` folder you chose. From the example above,
the `/path/on/host` folder contents look like:

```
/path/on/host
├── mods
│   └── ... INSTALL MODS HERE ...
├── config
│   └── ... CONFIGURE MODS HERE ...
├── ops.json
├── server.properties
├── whitelist.json
└── ...
```

If you add mods while the container is running, you'll need to restart it to pick those
up:

    docker stop mc
    docker start mc

### Using separate mounts

This is the easiest way if you are using an ephemeral `/data` filesystem,
or downloading a world with the `WORLD` option.

There are two additional volumes that can be mounted; `/mods` and `/config`.
Any files in either of these filesystems will be copied over to the main
`/data` filesystem before starting Minecraft.

This works well if you want to have a common set of modules in a separate
location, but still have multiple worlds with different server requirements
in either persistent volumes or a downloadable archive.

## Deploying plugins from attached volume

If the `/plugins` directory exists in the container, such as from an attached volume, any files in this directory will be copied over to `/data/plugins` before starting Minecraft. Set `PLUGINS_SYNC_UPDATE=false` if you want files from `/plugins` to take precedence over newer files in `/data/plugins`.

This works well if you want to have a common set of plugins in a separate location, but still have multiple worlds with different server requirements in either persistent volumes or a downloadable archive.

## Auto-downloading SpigotMC/Bukkit/PaperMC plugins

The `SPIGET_RESOURCES` variable can be set with a comma-separated list of SpigotMC resource IDs to automatically download [SpigotMC resources/plugins](https://www.spigotmc.org/resources/) using [the spiget API](https://spiget.org/). Resources that are zip files will be expanded into the plugins directory and resources that are simply jar files will be moved there.

> NOTE: the variable is purposely spelled SPIG**E**T with an "E"

The **resource ID** can be located from the numerical part of the URL after the shortname and a dot. For example, the ID is **9089** from

    https://www.spigotmc.org/resources/essentialsx.9089/
                                                   ====

For example, the following will auto-download the [EssentialsX](https://www.spigotmc.org/resources/essentialsx.9089/) and [Vault](https://www.spigotmc.org/resources/vault.34315/) plugins:

    -e SPIGET_RESOURCES=9089,34315

## Replacing variables inside configs

Sometimes you have mods or plugins that require configuration information that is only available at runtime.
For example if you need to configure a plugin to connect to a database,
you don't want to include this information in your Git repository or Docker image.
Or maybe you have some runtime information like the server name that needs to be set
in your config files after the container starts.

For those cases there is the option to replace defined variables inside your configs
with environment variables defined at container runtime.

If you set the enviroment variable `REPLACE_ENV_VARIABLES` to `TRUE` the startup script
will go thru all files inside your `/data` volume and replace variables that match your
defined environment variables. Variables that you want to replace need to be wrapped
inside `${YOUR_VARIABLE}` curly brackets and prefixed with a dollar sign. This is the regular
syntax for enviromment variables inside strings or config files.

Optionally you can also define a prefix to only match predefined environment variables.

`ENV_VARIABLE_PREFIX="CFG_"` <-- this is the default prefix

If you want use file for value (like when use secrets) you can add suffix `_FILE` to your variable name (in  run command).

There are some limitations to what characters you can use.

| Type  | Allowed Characters  |
| ----- | ------------------- |
| Name  | `0-9a-zA-Z_-`       |
| Value | `0-9a-zA-Z_-:/=?.+` |

Variables will be replaced in files with the following extensions:
`.yml`, `.yaml`, `.txt`, `.cfg`, `.conf`, `.properties`.

Specific files can be excluded by listing their name (without path) in the variable `REPLACE_ENV_VARIABLES_EXCLUDES`.

Paths can be excluded by listing them in the variable `REPLACE_ENV_VARIABLES_EXCLUDE_PATHS`. Path
excludes are recursive. Here is an example:
```
REPLACE_ENV_VARIABLES_EXCLUDE_PATHS="/data/plugins/Essentials/userdata /data/plugins/MyPlugin"
```

Here is a full example where we want to replace values inside a `database.yml`.

```yml

---
database:
  host: ${CFG_DB_HOST}
  name: ${CFG_DB_NAME}
  password: ${CFG_DB_PASSWORD}
```

This is how your `docker-compose.yml` file could look like:

```yml
version: "3"
# Other docker-compose examples in /examples

services:
  minecraft:
    image: itzg/minecraft-server
    ports:
      - "25565:25565"
    volumes:
      - "mc:/data"
    environment:
      EULA: "TRUE"
      ENABLE_RCON: "true"
      RCON_PASSWORD: "testing"
      RCON_PORT: 28016
      # enable env variable replacement
      REPLACE_ENV_VARIABLES: "TRUE"
      # define an optional prefix for your env variables you want to replace
      ENV_VARIABLE_PREFIX: "CFG_"
      # and here are the actual variables
      CFG_DB_HOST: "http://localhost:3306"
      CFG_DB_NAME: "minecraft"
      CFG_DB_PASSWORD_FILE: "/run/secrets/db_password"
    restart: always
  rcon:
    image: itzg/rcon
    ports:
      - "4326:4326"
      - "4327:4327"
    volumes:
      - "rcon:/opt/rcon-web-admin/db"

volumes:
  mc:
  rcon:

secrets:
  db_password:
    file: ./db_password
```

The content of `db_password`:

    ug23u3bg39o-ogADSs

## Running with a custom server JAR

If you would like to run a custom server JAR, set `-e TYPE=CUSTOM` and pass the custom server
JAR via `CUSTOM_SERVER`. It can either be a URL or a container path to an existing JAR file.

If it is a URL, it will only be downloaded into the `/data` directory if it wasn't already. As
such, if you need to upgrade or re-download the JAR, then you will need to stop the container,
remove the file from the container's `/data` directory, and start again.

## Force re-download of the server file

For VANILLA, FORGE, BUKKIT, SPIGOT, PAPER, CURSEFORGE, SPONGEVANILLA server types, set
`$FORCE_REDOWNLOAD` to some value (e.g. 'true) to force a re-download of the server file for
the particular server type. by adding a `-e FORCE_REDOWNLOAD=true` to your command-line.

For example, with PaperSpigot, it would look something like this:

```
docker run -d -v /path/on/host:/data \
    -e TYPE=PAPER -e FORCE_REDOWNLOAD=true \
    -p 25565:25565 -e EULA=TRUE --name mc itzg/minecraft-server
```

## Using Docker Compose

Rather than type the server options below, the port mappings above, etc
every time you want to create new Minecraft server, you can now use
[Docker Compose](https://docs.docker.com/compose/). Start with a
`docker-compose.yml` file like the following:

```
minecraft-server:
  image: itzg/minecraft-server

  ports:
    - "25565:25565"

  environment:
    EULA: "TRUE"

  tty: true
  stdin_open: true
  restart: always
```

and in the same directory as that file run

    docker-compose up -d

Now, go play...or adjust the `environment` section to configure
this server instance.

## Server configuration

By default the server configuration will be created and set based on the following
environment variables, but only the first time the server is started. If the
`server.properties` file already exists, the values in them will not be changed.

If you would like to override the server configuration each time the container
starts up, you can set the OVERRIDE_SERVER_PROPERTIES environment variable like:

    docker run -d -e OVERRIDE_SERVER_PROPERTIES=true ...

This will reset any manual configuration of the `server.properties` file, so if
you want to make any persistent configuration changes you will need to make sure
you have properly set the proper environment variables in your docker run command (described below).

### Server name

The server name (e.g. for bungeecord) can be set like:

    docker run -d -e SERVER_NAME=MyServer ...

### Server port

> **WARNING:** only change this value if you know what you're doing. It is only needed when using host networking and it is rare that host networking should be used. Use `-p` port mappings instead.

If you must, the server port can be set like:

    docker run -d -e SERVER_PORT=25566 ...

**however**, be sure to change your port mapping accordingly and be prepared for some features to break.

### Difficulty

The difficulty level (default: `easy`) can be set like:

    docker run -d -e DIFFICULTY=hard ...

Valid values are: `peaceful`, `easy`, `normal`, and `hard`, and an
error message will be output in the logs if it's not one of these
values.

### Whitelist Players

To whitelist players for your Minecraft server, pass the Minecraft usernames separated by commas via the `WHITELIST` environment variable, such as

    docker run -d -e WHITELIST=user1,user2 ...

If the `WHITELIST` environment variable is not used, any user can join your Minecraft server if it's publicly accessible.

> NOTE: When `WHITELIST` is used the server property `white-list` will automatically get set to `true`.

> By default, the players in `WHITELIST` are **added** to the final `whitelist.json` file by the Minecraft server. If you set `OVERRIDE_WHITELIST` to "true" then the `whitelist.json` file will be recreated on each server startup.

### Op/Administrator Players

To add more "op" (aka adminstrator) users to your Minecraft server, pass the Minecraft usernames separated by commas via the `OPS` environment variable, such as

    docker run -d -e OPS=user1,user2 ...

> By default, the players in `OPS` are **added** to the final `ops.json` file by the Minecraft server. If you set `OVERRIDE_OPS` to "true" then the `ops.json` file will be recreated on each server startup.

### Server icon

A server icon can be configured using the `ICON` variable. The image will be automatically
downloaded, scaled, and converted from any other image format:

    docker run -d -e ICON=http://..../some/image.png ...

The server icon which has been set doesn't get overridden by default. It can be changed and overridden by setting `OVERRIDE_ICON` to `TRUE`.

    docker run -d -e ICON=http://..../some/other/image.png -e OVERRIDE_ICON=TRUE...

### Rcon

To use rcon use the `ENABLE_RCON` and `RCON_PASSORD` variables.
By default rcon port will be `25575` but can easily be changed with the `RCON_PORT` variable.

    docker run -d -e ENABLE_RCON=true -e RCON_PASSWORD=testing

### Query

Enabling this will enable the gamespy query protocol.
By default the query port will be `25565` (UDP) but can easily be changed with the `QUERY_PORT` variable.

    docker run -d -e ENABLE_QUERY=true

### Max players

By default max players is 20, you can increase this with the `MAX_PLAYERS` variable.

    docker run -d -e MAX_PLAYERS=50

### Max world size

This sets the maximum possible size in blocks, expressed as a radius, that the world border can obtain.

    docker run -d -e MAX_WORLD_SIZE=10000

### Allow Nether

Allows players to travel to the Nether.

    docker run -d -e ALLOW_NETHER=true

### Announce Player Achievements

Allows server to announce when a player gets an achievement.

    docker run -d -e ANNOUNCE_PLAYER_ACHIEVEMENTS=true

### Enable Command Block

Enables command blocks

     docker run -d -e ENABLE_COMMAND_BLOCK=true

### Force Gamemode

Force players to join in the default game mode.

- false - Players will join in the gamemode they left in.
- true - Players will always join in the default gamemode.

  `docker run -d -e FORCE_GAMEMODE=false`

### Generate Structures

Defines whether structures (such as villages) will be generated.

- false - Structures will not be generated in new chunks.
- true - Structures will be generated in new chunks.

  `docker run -d -e GENERATE_STRUCTURES=true`

### Hardcore

If set to true, players will be set to spectator mode if they die.

    docker run -d -e HARDCORE=false

### Snooper

If set to false, the server will not send data to snoop.minecraft.net server.

    docker run -d -e SNOOPER_ENABLED=false

### Max Build Height

The maximum height in which building is allowed.
Terrain may still naturally generate above a low height limit.

    docker run -d -e MAX_BUILD_HEIGHT=256

### Max Tick Time

The maximum number of milliseconds a single tick may take before the server watchdog stops the server with the message, A single server tick took 60.00 seconds (should be max 0.05); Considering it to be crashed, server will forcibly shutdown. Once this criteria is met, it calls System.exit(1).
Setting this to -1 will disable watchdog entirely

    docker run -d -e MAX_TICK_TIME=60000

### Spawn Animals

Determines if animals will be able to spawn.

    docker run -d -e SPAWN_ANIMALS=true

### Spawn Monsters

Determines if monsters will be spawned.

    docker run -d -e SPAWN_MONSTERS=true

### Spawn NPCs

Determines if villagers will be spawned.

    docker run -d -e SPAWN_NPCS=true

### Set spawn protection

Sets the area that non-ops can not edit (0 to disable)

    docker run -d -e SPAWN_PROTECTION=0

### View Distance

Sets the amount of world data the server sends the client, measured in chunks in each direction of the player (radius, not diameter).
It determines the server-side viewing distance.

    docker run -d -e VIEW_DISTANCE=10

### Level Seed

If you want to create the Minecraft level with a specific seed, use `SEED`, such as

    -e SEED=1785852800490497919

If using a negative value for the seed, make sure to quote the value such as:

    -e SEED="-1785852800490497919"

### Game Mode

By default, Minecraft servers are configured to run in Survival mode. You can
change the mode using `MODE` where you can either provide the [standard
numerical values](http://minecraft.gamepedia.com/Game_mode#Game_modes) or the
shortcut values:

- creative
- survival
- adventure
- spectator (only for Minecraft 1.8 or later)

For example:

    docker run -d -e MODE=creative ...

### Message of the Day

The message of the day, shown below each server entry in the UI, can be changed with the `MOTD` environment variable, such as

    -e MOTD="My Server"

If you leave it off, a default is computed from the server type and version, such as

    A Paper Minecraft Server powered by Docker

That way you can easily differentiate between several servers you may have started.

### PVP Mode

By default, servers are created with player-vs-player (PVP) mode enabled. You can disable this with the `PVP`
environment variable set to `false`, such as

    docker run -d -e PVP=false ...

### Level Type and Generator Settings

By default, a standard world is generated with hills, valleys, water, etc. A different level type can
be configured by setting `LEVEL_TYPE` to an expected type, for example

- DEFAULT
- FLAT
- LARGEBIOMES
- AMPLIFIED
- CUSTOMIZED
- BUFFET
- BIOMESOP (Biomes O' Plenty for 1.12 and older)
- BIOMESOPLENTY (Biomes O' Plenty for 1.15 and above)

Descriptions are available at the [gamepedia](http://minecraft.gamepedia.com/Server.properties).

When using a level type of `FLAT`, `CUSTOMIZED`, and `BUFFET`, you can further configure the world generator
by passing [custom generator settings](http://minecraft.gamepedia.com/Superflat).
**Since generator settings usually have ;'s in them, surround the -e value with a single quote, like below.**

For example (just the `-e` bits):

    -e LEVEL_TYPE=flat -e 'GENERATOR_SETTINGS=3;minecraft:bedrock,3*minecraft:stone,52*minecraft:sandstone;2;'

### Custom Server Resource Pack

You can set a link to a custom resource pack and set it's checksum using the `RESOURCE_PACK` and `RESOURCE_PACK_SHA1` options respectively, the default is blank:

    docker run -d -e 'RESOURCE_PACK=http\://link.com/to/pack.zip?\=1' -e 'RESOURCE_PACK_SHA1=d5db29cd03a2ed055086cef9c31c252b4587d6d0'

**NOTE:** `:` and `=` must be escaped using `\`. The checksum plain-text hexadecimal.

### World Save Name

You can either switch between world saves or run multiple containers with different saves by using the `LEVEL` option,
where the default is "world":

    docker run -d -e LEVEL=bonus ...

**NOTE:** if running multiple containers be sure to either specify a different `-v` host directory for each
`LEVEL` in use or don't use `-v` and the container's filesystem will keep things encapsulated.

### Downloadable world

Instead of mounting the `/data` volume, you can instead specify the URL of a ZIP file containing an archived world. It will be searched for a file `level.dat` and the containing subdirectory moved to the directory named by `$LEVEL`. This means that most of the archived Minecraft worlds downloadable from the Internet will already be in the correct format.

    docker run -d -e WORLD=http://www.example.com/worlds/MySave.zip ...

**NOTE:** This URL must be accessible from inside the container. Therefore,
you should use an IP address or a globally resolvable FQDN, or else the
name of a linked container.

**NOTE:** If the archive contains more than one `level.dat`, then the one to select can be picked with `WORLD_INDEX`, which defaults to 1.

### Cloning world from a container path

The `WORLD` option can also be used to reference a directory or zip file that will be used as a source to clone or unzip the world directory.

For example, the following would initially clone the world's content
from `/worlds/basic`. Also notice in the example that you can use a
read-only volume attachment to ensure the clone source remains pristine.

```
docker run ... -v $HOME/worlds:/worlds:ro -e WORLD=/worlds/basic
```

### Overwrite world on start
The world will only be downloaded or copied if it doesn't exist already. Set `FORCE_WORLD_COPY=TRUE` to force overwrite the world on every server start.

### Downloadable mod/plugin pack for Forge, Bukkit, and Spigot Servers

Like the `WORLD` option above, you can specify the URL of a "mod pack"
to download and install into `mods` for Forge or `plugins` for Bukkit/Spigot.
To use this option pass the environment variable `MODPACK`, such as

    docker run -d -e MODPACK=http://www.example.com/mods/modpack.zip ...

**NOTE:** The referenced URL must be a zip file with one or more jar files at the
top level of the zip archive. Make sure the jars are compatible with the
particular `TYPE` of server you are running.

You may also download individual mods using the `MODS` environment variable and supplying the URL
to the jar files. Multiple mods/plugins should be comma separated.

    docker run -d -e MODS=https://www.example.com/mods/mod1.jar,https://www.example.com/mods/mod2.jar ...

### Remove old mods/plugins

When the option above is specified (`MODPACK`) you can also instruct script to
delete old mods/plugins prior to installing new ones. This behaviour is desirable
in case you want to upgrade mods/plugins from downloaded zip file.
To use this option pass the environment variable `REMOVE_OLD_MODS="TRUE"`, such as

    docker run -d -e REMOVE_OLD_MODS="TRUE" -e MODPACK=http://www.example.com/mods/modpack.zip ...

**WARNING:** All content of the `mods` or `plugins` directory will be deleted
before unpacking new content from the MODPACK or MODS.

### Online mode

By default, server checks connecting players against Minecraft's account database. If you want to create an offline server or your server is not connected to the internet, you can disable the server to try connecting to minecraft.net to authenticate players with environment variable `ONLINE_MODE`, like this

    docker run -d -e ONLINE_MODE=FALSE ...

### Allow flight

Allows users to use flight on your server while in Survival mode, if they have a mod that provides flight installed.

    -e ALLOW_FLIGHT=TRUE|FALSE

### Other server property mappings

| Environment Variable              | Server Property                   |
| --------------------------------- | --------------------------------- |
| PLAYER_IDLE_TIMEOUT               | player-idle-timeout               |
| BROADCAST_CONSOLE_TO_OPS          | broadcast-console-to-ops          |
| BROADCAST_RCON_TO_OPS             | broadcast-rcon-to-ops             |
| ENABLE_JMX                        | enable-jmx-monitoring             |
| SYNC_CHUNK_WRITES                 | sync-chunk-writes                 |
| ENABLE_STATUS                     | enable-status                     |
| ENTITY_BROADCAST_RANGE_PERCENTAGE | entity-broadcast-range-percentage |
| FUNCTION_PERMISSION_LEVEL         | function-permission-level         |
| NETWORK_COMPRESSION_THRESHOLD     | network-compression-threshold     |
| OP_PERMISSION_LEVEL               | op-permission-level               |
| PREVENT_PROXY_CONNECTIONS         | prevent-proxy-connections         |
| USE_NATIVE_TRANSPORT              | use-native-transport              |
| ENFORCE_WHITELIST                 | enforce-whitelist                 |

## Miscellaneous Options

### Running as alternate user/group ID

By default, the container will switch to user ID 1000 and group ID 1000;
however, you can override those values by setting `UID` and/or `GID` as environmental entries, during the `docker run` command.

    -e UID=1234
    -e GID=1234

The container will also skip user switching if the `--user`/`-u` argument
is passed to `docker run`.

### Memory Limit

By default, the image declares an initial and maximum Java memory-heap limit of 1 GB. There are several ways to adjust the memory settings:

- `MEMORY`: "1G" by default, can be used to adjust both initial (`Xms`) and max (`Xmx`) memory heap settings of the JVM
- `INIT_MEMORY`: independently sets the initial heap size
- `MAX_MEMORY`: independently sets the max heap size

The values of all three are passed directly to the JVM and support format/units as `<size>[g|G|m|M|k|K]`. For example:

    -e MEMORY=2G

> NOTE: the settings above only set the Java **heap** limits. Memory resource requests and limits on the overall container should also account for non-heap memory usage. An extra 25% is [a general best practice](https://dzone.com/articles/best-practices-java-memory-arguments-for-container).

### JVM Options

General JVM options can be passed to the Minecraft Server invocation by passing a `JVM_OPTS`
environment variable. Options like `-X` that need to proceed general JVM options can be passed
via a `JVM_XX_OPTS` environment variable.

For some cases, if e.g. after removing mods, it could be necessary to startup minecraft with an additional `-D` parameter like `-Dfml.queryResult=confirm`. To address this you can use the environment variable `JVM_DD_OPTS`, which builds the params from a given list of values separated by space, but without the `-D` prefix. To make things running under systems (e.g. Plesk), which doesn't allow `=` inside values, a `:` (colon) could be used instead. The upper example would look like this:
`JVM_DD_OPTS=fml.queryResult:confirm`, and will be converted to `-Dfml.queryResult=confirm`.

### Interactive and Color Console

If you would like to attach to the Minecraft server console with color and interactive capabilities, then add

```
  -e EXEC_DIRECTLY=true
```

> **NOTE** this will bypass graceful server shutdown handling when using `docker stop`, so be sure to use `rcon-cli` or console commands to `stop` the server.

### OpenJ9 Specific Options

The openj9 image tags include specific variables to simplify configuration:

- `-e TUNE_VIRTUALIZED=TRUE` : enables the option to
  [optimize for virtualized environments](https://www.eclipse.org/openj9/docs/xtunevirtualized/)
- `-e TUNE_NURSERY_SIZES=TRUE` : configures nursery sizes where the initial size is 50%
  of the `MAX_MEMORY` and the max size is 80%.

### Enabling rolling logs

By default the vanilla log file will grow without limit. The logger can be reconfigured to use a rolling log files strategy by using:

```
  -e ENABLE_ROLLING_LOGS=true
```

> **NOTE** this will interfere with interactive/color consoles [as described in the section above](#interactive-and-color-console)

## Timezone Configuration

You can configure the timezone to match yours by setting the `TZ` environment variable:

        -e TZ=Europe/London

such as:

        docker run -d -it -e TZ=Europe/London -p 25565:25565 --name mc itzg/minecraft-server

Or mounting `/etc/timezone` as readonly (not supported on Windows):

        -v /etc/timezone:/etc/timezone:ro

such as:

        docker run -d -it -v /etc/timezone:/etc/timezone:ro -p 25565:25565 --name mc itzg/minecraft-server

### Enable Remote JMX for Profiling

To enable remote JMX, such as for profiling with VisualVM or JMC, add the environment variable `ENABLE_JMX=true`, set `JMX_HOST` to the IP/host running the Docker container, and add a port forwarding of TCP port 7091, such as:

```
-e ENABLE_JMX=true -e JMX_HOST=$HOSTNAME -p 7091:7091
```

### Enable Aikar's Flags

[Aikar has does some research](https://mcflags.emc.gs/) into finding the optimal JVM flags for GC tuning, which becomes more important as more users are connected concurrently. The set of flags documented there can be added using

    -e USE_AIKAR_FLAGS=true

When `MEMORY` is greater than or equal to 12G, then the Aikar flags will be adjusted according to the article.

Large page support can also be enabled by adding

    -e USE_LARGE_PAGES=true

### HTTP Proxy

You may configure the use of an HTTP/HTTPS proxy by passing the proxy's URL via the `PROXY`
environment variable. In [the example compose file](examples/docker-compose-proxied.yml) it references
a companion squid proxy by setting the equivalent of

    -e PROXY=proxy:3128

### Using "noconsole" option

Some older versions (pre-1.14) of Spigot required `--noconsole` to be passed when detaching stdin, which can be done by setting `-e CONSOLE=FALSE`.

### Explicitly disable GUI

Some older servers get confused and think that the GUI interface is enabled. You can explicitly
disable that by passing `-e GUI=FALSE`.

### Stop Duration

When the container is signalled to stop, the Minecraft process wrapper will attempt to send a "stop" command via RCON or console and waits for the process to gracefully finish. By defaul it waits 60 seconds, but that duration can be configured by setting the environment variable `STOP_DURATION` to the number of seconds.

## Autopause

### Description

There are various bug reports on [Mojang](https://bugs.mojang.com) about high CPU usage of servers with newer versions, even with few or no clients connected (e.g. [this one](https://bugs.mojang.com/browse/MC-149018), in fact the functionality is based on [this comment in the thread](https://bugs.mojang.com/browse/MC-149018?focusedCommentId=593606&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-593606)).

An autopause functionality has been added to this image to monitor whether clients are connected to the server. If for a specified time no client is connected, the Java process is stopped. When knocking on the server port (e.g. by the ingame Multiplayer server overview), the process is resumed. The experience for the client does not change.

Of course, even loaded chunks are not ticked when the process is stopped.

**You must greatly increase or disable max-tick-time watchdog functionality.** From the server's point of view, the pausing causes a single tick to take as long as the process is stopped, so the server watchdog might intervene after the process is continued, possibly forcing a container restart. To prevent this, ensure that the `max-tick-time` in the `server.properties` file is set to a very large value or -1 to disable it entirely, which is highly recommended. That can be set with `MAX_TICK_TIME` as described in [the section below](#max-tick-time).

> **NOTE:** Non-vanilla versions might have their own configuration file, you might have to disable their watchdogs separately (e.g. PAPER Servers).

On startup the `server.properties` file is checked and, if applicable, a warning is printed to the terminal. When the server is created (no data available in the persistent directory), the properties file is created with the Watchdog disabled.

The utility used to wake the server (`knock(d)`) works at network interface level. So the correct interface has to be set using the `AUTOPAUSE_KNOCK_INTERFACE` variable when using non-default networking environments (e.g. host-networking, Portainer oder NAS solutions). See the description of the variable below.

A starting, example compose file has been provided in [examples/docker-compose-autopause.yml](examples/docker-compose-autopause.yml).

### Enabling Autopause

Enable the Autopause functionality by setting:

```
-e ENABLE_AUTOPAUSE=TRUE
```

The following environment variables define the behaviour of auto-pausing:
* `AUTOPAUSE_TIMEOUT_EST`, default `3600` (seconds)
  describes the time between the last client disconnect and the pausing of the process (read as timeout established)
* `AUTOPAUSE_TIMEOUT_INIT`, default `600` (seconds)
  describes the time between server start and the pausing of the process, when no client connects inbetween (read as timeout initialized)
* `AUTOPAUSE_TIMEOUT_KN`, default `120` (seconds)
  describes the time between knocking of the port (e.g. by the main menu ping) and the pausing of the process, when no client connects inbetween (read as timeout knocked)
* `AUTOPAUSE_PERIOD`, default `10` (seconds)
  describes period of the daemonized state machine, that handles the pausing of the process (resuming is done independently)
* `AUTOPAUSE_KNOCK_INTERFACE`, default `eth0`
  <br>Describes the interface passed to the `knockd` daemon. If the default interface does not work, run the `ifconfig` command inside the container and derive the interface receiving the incoming connection from its output. The passed interface must exist inside the container. Using the loopback interface (`lo`) does likely not yield the desired results.

## Running on RaspberryPi

To run this image on a RaspberryPi 3 B+, 4, or newer, use any of the image tags [list in the Java version section](#running-minecraft-server-on-different-java-version) that specify `armv7` for the architecture, such as

    itzg/minecraft-server:multiarch

> NOTE: you may need to lower the memory allocation, such as `-e MEMORY=750m`

> If experiencing issues such as "sleep: cannot read realtime clock: Operation not permitted", ensure `libseccomp` is up to date on your host. In some cases adding `:Z` flag to the `/data` mount may be needed, [but use cautiously](https://docs.docker.com/storage/bind-mounts/#configure-the-selinux-label).
