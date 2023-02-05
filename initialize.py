import os

# create the first file
first_file_contents = """# This env file is only needed when running the Project with Docker Compose.

#Domain for Traefik
MY_DOMAIN=

#Login user and password, encrypted with htpasswd
DASHBOARD_LOGIN=

#Email for Let's Encrypt
EMAIL=contact@elias-cecetka.tech

#Platform for Docker
PLATFORM=

#Image name
IMAGE_NAME=

#UID and GID for the user inside the container (can be found with id -u and id -g)
CURRENT_UID="""

first_file_path = "./.env"
if not os.path.exists(first_file_path):
    with open(first_file_path, "w") as file:
        file.write(first_file_contents)

# create the second file
second_file_contents = """#This env file is used for the DCSSStatsDataProvider fastapi python backend.

#The webdav can be toggled in the config file, leave blank if not used.
WEBDAV_HOSTNAME=
WEBDAV_LOGIN=
WEBDAV_PASSWORD=

#The checkwx api key for weather updates, can be toggled in the config file, leave blank if not used.
CHECKWX_APIKEY="""
second_file_path = "./DCSStatsDataProvider/.env"
if not os.path.exists(second_file_path):
    with open(second_file_path, "w") as file:
        file.write(second_file_contents)

if not os.path.exists("./letsencrypt/acme.json"):
    with open("./letsencrypt/acme.json", "w") as file:
        file.write("")

if not os.path.exists("./traefik/traefik.log"):
    with open("./traefik/traefik.log", "w") as file:
        file.write("")

if not os.path.exists("./DCSStatsDataProvider/serverlog.log"):
    with open("./DCSStatsDataProvider/serverlog.log", "w") as file:
        file.write("")
