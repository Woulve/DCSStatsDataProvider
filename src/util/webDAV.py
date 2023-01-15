from webdav3.client import Client
import os 
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()


options = {
 'webdav_hostname': os.getenv("WEBDAV_HOSTNAME"),
 'webdav_login':    os.getenv("WEBDAV_LOGIN"),
 'webdav_password': os.getenv("WEBDAV_PASSWORD")
}

def getFileFromWebDAV(file):
    client = Client(options)
    client.verify = False
    if client.check(file):
        client.download_sync(remote_path=file, local_path="./SlmodStats.lua")
        return 1
    else:
        return 0