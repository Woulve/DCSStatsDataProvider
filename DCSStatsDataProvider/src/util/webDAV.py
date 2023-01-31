from webdav3.client import Client
from src.util.serverlogger import serverLogger
from webdav3.exceptions import WebDavException
import os
from dotenv import load_dotenv
import urllib3

LOGGER = serverLogger()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Disable SSL warnings

load_dotenv()

#To use webdav, you need to set the following environment variables in a .env file in the root folder:
options = {
 'webdav_hostname': os.getenv("WEBDAV_HOSTNAME"),
 'webdav_login':    os.getenv("WEBDAV_LOGIN"),
 'webdav_password': os.getenv("WEBDAV_PASSWORD")
}

def getFileFromWebDAV(file, localpath):
    client = Client(options)
    client.verify = False
    if client.check(file):
        try:
            client.download_sync(remote_path=file, local_path=localpath)
            LOGGER.info("Successfully fetched "+file+" from WEBDav server to: "+localpath)
        except WebDavException as e:
            LOGGER.error("Couldn't fetch file from webdav server: "+str(e))
            return 0
        return 1
    else:
        return 0

def pushFileToWebdav(remotepath, localpath):
    client = Client(options)
    client.verify = False
    try:
        client.upload_sync(remote_path=remotepath, local_path=localpath)
        LOGGER.info("Successfully pushed "+localpath+" to WEBDav server: "+remotepath)
        return 1
    except WebDavException as e:
        LOGGER.error("Couldn't push file to webdav server: "+str(e))
        return 0

def checkExists(file):
    client = Client(options)
    client.verify = False
    try:
        return client.check(file)
    except Exception as e:
        LOGGER.error("Couldn't check if file exists: "+file)
        LOGGER.exception(e)