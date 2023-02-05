# 1. Woulve's DCS Stats Backend

## 1.1. About
This is a passion Project I developed in my free time, to provide a Stats website for my squadron, and to improve my skills in web development and python. There is no full test coverage, and there might still be things missing. I did my best to provide error handling, but if you find any issues, feel free to fix them, or contact me.

It can be run either directly with python, or with docker.

**This Project features**
- Fastapi REST Server
- Dockerized containers
- Traefik reverse proxy with letsencrypt certificate
- Serializing SLMod lua files from lua to python
- (Almost) Real time updates
- Pytest Tests (not good coverage yet)
- Customizable config
- Realtime Weather updates for DCS Mission (can be toggled on and off)
- WebDAV integration to get files from remote server (can be toggled on and off)

## 2. Setup

### 2.1. .env files
There are two unpopulated .env files for configuration.
- [./.env](.env), which is for the Docker-Compose config
- [./DCSStatsDataProvider/.env](./DCSStatsDataProvider/.env), for the webdav and checkwx configuration.

### 2.2. config file
There is also a [config.cfg](./DCSStatsDataProvider/config.cfg) file, to choose which options are enabled, and to select the paths to the files.

| Section       | Field                      | Type    | Description                                                                           | Depends on                                      |
| ------------- | -------------------------- | ----- | ------------------------------------------------------------------------------------- | ----------------------------------------------- |
| configuration | enablerealtimeupdates      | Boolean | Enables the real-time serialization of the SLModStats.lua file. More on this [here]() |                                                 |
| realweather   | enableweatherchanges       | Boolean | Enables the real weather injector                                                     |                                                 |
| realweather   | webdavmission              | Boolean | If true, fetches the mission from webdav before running the weather injector          | enableweatherchanges=True,<br>enablewebdav=True |
| realweather   | icao                       | String  | The icao of the airport to get weather from                                           | enableweatherchanges=True                       |
| realweather   | update-time                | Boolean | The icao of the airport to get weather from                                           | enableweatherchanges=True                       |
| realweather   | inputmissionlocation       | String  | The path to the input .miz file                                                       | enableweatherchanges=True                       |
| realweather   | outputmissionlocation      | String  | The path to the output .miz file                                                      | enableweatherchanges=True                       |
| webdav        | enablewebdav               | Boolean | Enable or disable webdav                                                              |                                                 |
| localfiles    | slmodstatsluapath          | String  | Path to the SlmodStats.lua file                                                       |                                                 |
| localfiles    | slmodstatsdebuggingluapath | String  | Path to the SlmodStatsDebugging.lua file for testing                                  |                                                 |

For a simple setup, without docker, weather changes and webdav, you don't have to modify the config file and env variables.

But you will need to have to specify a valid path to your SlmodStats.lua file in the config.cfg file.
By default it is in the project root.

To start the DCSStatsDataProvider backend on your local machine, without docker, make sure you have python 3.10.9 installed. To install the required dependencies, run

```cd DCSStatsDataProvider```

```pip install --upgrade -r ./DCSStatsDataProvider/requirements.txt```

and then run it with

```uvicorn main:app --reload --port 8000```

