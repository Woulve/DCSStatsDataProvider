<h1>Woulve's DCSStatsDataProvider</h1>

- [1. About](#1-about)
- [2. Setup](#2-setup)
  - [2.1. .env files](#21-env-files)
  - [2.2. config file](#22-config-file)
  - [2.3. Docker Setup](#23-docker-setup)
- [3. How it works](#3-how-it-works)
  - [3.1. Real-Time data updates](#31-real-time-data-updates)
  - [3.2. Weather Injection](#32-weather-injection)


# 1. About
This is a passion Project I developed in my free time, to provide a Stats website for my squadron, and to improve my skills in web development and python. There is no full test coverage, and there might be bugs. I did my best to provide error handling, but if you find any issues, feel free to fix them, or contact me.

It can be run either directly with python, or with docker.

See it in action here: https://vikingsquadron.de/

**This Project features**
- Fastapi REST Server
- Dockerized containers
- Traefik reverse proxy with letsencrypt certificate
- Serializing SLMod lua files from lua to python
- (Almost) Real time updates
- Pytest e2e & unit Tests
- Customizable config
- Realtime Weather updates for DCS Mission
- WebDAV integration to get files from remote server
- Fully Raspberry Pi compatible

# 2. Setup

## 2.1. .env files
For docker secrets and for the DCSStatsDataProvider backend configuration I use two .env files.
- [./.env](.env), which is for the Docker-Compose config (you don't need this if you don't run it with docker)
- [./DCSStatsDataProvider/.env](./DCSStatsDataProvider/.env), for the webdav and checkwx configuration.

There is a handy initialize.py script, which you can run to initially create files so docker doesn't complain, and to generate blueprints for the .env files.

## 2.2. config file
There is also a [config.cfg](./DCSStatsDataProvider/config.cfg) file, to choose which options are enabled, and to select the paths to the files. You'll likely have to midify this for your setup.

| Section       | Field                       | Type    | Description                                                                           | Depends on                                      | Default                                                           |
| ------------- | --------------------------- | ------- | ------------------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------- |
| configuration | enablerealtimeupdates       | Boolean | Enables the real-time serialization of the SLModStats.lua file. More on this [here](#31-real-time-data-updates) |                                                 | True                                                              |
| realweather   | enableweatherchanges        | Boolean | Enables the real weather injector                                                     |                                                 | False                                                             |
| realweather   | webdavmission               | Boolean | If true, fetches the mission from webdav before running the weather injector          | enableweatherchanges=True,<br>enablewebdav=True | False                                                             |
| realweather   | icao                        | String  | The icao of the airport to get weather from                                           | enableweatherchanges=True                       | UGSB                                                              |
| webdav        | enablewebdav                | Boolean | Enable or disable webdav                                                              |                                                 | False                                                             |
| webdav        | remoteinputmissionlocation  | String  | The path to the mission that will be fetched from the server.                         | enableweatherchanges=True,<br>enablewebdav=True | Active/mission.miz                                                |
| webdav        | remoteoutputmissionlocation | String  | The path to the mission that will be written to the server.                           | enableweatherchanges=True,<br>enablewebdav=True | Active/foothold_remastered_realweather.miz                        |
| localfiles    | slmodstatsluapath           | String  | Path to the SlmodStats.lua file                                                       |                                                 | ./SlmodStats.lua                                                  |
| localfiles    | slmodstatsdebuggingluapath  | String  | Path to the SlmodStatsDebugging.lua file for testing                                  |                                                 | ./SlmodStatsDebugging.lua                                         |
| localfiles    | localinputmissionlocation   | String  | The local path to the input .miz file                                                       | enableweatherchanges=True                       | ./src/util/realweather/Active/mission.miz                         |
| localfiles    | localoutputmissionlocation  | String  | The local path to the output .miz file                                                      | enableweatherchanges=True                       | ./src/util/realweather/Active/foothold_remastered_realweather.miz |

For a simple setup, without docker, weather changes and webdav, you don't have to modify the config file and env variables.

But you will need to have to specify a valid path to your SlmodStats.lua file in the config.cfg file.
By default it set to be in the project root.

To start the DCSStatsDataProvider backend on your local machine, without docker, make sure you have python 3.10.9 installed. To install the required dependencies, run

``cd DCSStatsDataProvider``

``pip install --upgrade -r ./DCSStatsDataProvider/requirements.txt``

and then run it with

``uvicorn main:app --reload --port 8000``

You should now be able to access the backend on http://127.0.0.1:8000

Since this is written with [FastApi](https://fastapi.tiangolo.com/), there is a generated OpenAPI specification, accessible under http://127.0.0.1:8000/docs, containing all the possible REST endpoints.

I am using pre-commit, to run all tests before committing. More information is in the [.pre-commit-config.yaml](.pre-commit-config.yaml) file.

## 2.3. Docker Setup
To use the application as a docker container, you have to build the image first with the Dockerfile.
Either use the VSCode Task I made, or the command ``"docker build --no-cache -t name:tag ."``
Replace name and tag with values of your choice.

Now you can run the container with: <br>
``docker run \``<br>
    ``--name dcsstatsdataprovider \``<br>
    ``-p 8000:8000 \``<br>
    ``-v $(pwd)/DCSStatsDataProvider/serverlog.log:/DCSStatsDataProvider/serverlog.log \``<br>
    ``-v $(pwd)/DCSStatsDataProvider/config.cfg:/DCSStatsDataProvider/config.cfg \``<br>
    ``-v $(pwd)/DCSStatsDataProvider/src/util/realweather/:/DCSStatsDataProvider/src/util/realweather/ \``<br>
    ``-v $(pwd)/DCSStatsDataProvider/SlmodStats.lua:/DCSStatsDataProvider/SlmodStats.lua \``<br>
    ``-e TZ=Europe/Berlin \``<br>
    ``name:tag``<br>

Replace name and tag with the values you set when building the image.

To make this easier, there is a [docker-compose file](docker-compose.yml), that runs the application, along with a traefik reverse proxy, a grafana dashboard for live graphs, prometheus for graph data, and dozzle to view logs.
This is just my personal setup, feel free to modify the docker-compose file.
The docker-compose takes values from the .env file, so set these accordingly.

# 3. How it works

This application uses [SLmod](https://github.com/mrSkortch/DCS-SLmod) for access to DCS statistics.
SLmod uses LUA, so I wrote a parser, that parses the SlmodStats.lua file, and converts it into a python object, that can be accessed via a REST API.
Due to some constraints, the LUA file gets serialized in DCS only on every server restart, which would mean you only had the Stats from the last server restart.
All new data is appended to the File in a new line, containing the path to the value, and the value itself.

## 3.1. Real-Time data updates
To get real-time Data, I added an option, that can serialize these values as well by iterating over every one of these lines.
Because this might impact performance when the LUA file is very big, I made this optional with the "enablerealtimeupdates" cfg option.
When enabled, the application serializes the data every 30 minutes.
When disabled, the data is serialized once on application startup.

## 3.2. Weather Injection
This Application can optionally provide real weather injection, with a custom modified [fork](https://github.com/Woulve/DCS-real-weather-vikings) of the [DCS-real-weather tool](https://github.com/evogelsa/DCS-real-weather).
Big kudos to ``evogelsa`` for this. To use this option you'll have to enable the config options, and set the paths to the mission files in the [config.cfg file](./DCSStatsDataProvider/config.cfg).
The Application checks if the weather hasn't been updated for 24 Hours, and optionally pulls the mission file from a webdav server before updating the weather.
Then, it will run either realweather_amd64, realweather_arm64 or realweather.exe, depending on your operating System. After successfully updating the weather, it will save the mission, and optionally upload it via webdav.




------
Feel free to modify my project, or use parts of it in your own projects.
If you have questions, <a href="mailto:contact@elias-cecetka.tech">send me an email</a> to ``contact@elias-cecetka.tech``
