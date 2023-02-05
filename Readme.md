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

## Quick setup
There are some files and folders that need to be initialized first. You can simply run the initialize script on linux, or initialize.bat on windows, to create them. That creates two .env files, that are not yet populated.
For a simple setup, without docker, weather changes and webdav, you don't have to modify them. You can toggle these options on and off in the config.cfg file in the DCSStatsDataProvider folder.