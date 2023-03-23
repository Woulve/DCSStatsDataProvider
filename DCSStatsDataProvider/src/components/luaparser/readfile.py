from src.util.serverlogger import serverLogger
from fastapi import HTTPException
import os

LOGGER = serverLogger()

def readfile(file_path):
    if not os.path.isfile(file_path):
        LOGGER.error(file_path + " not found")
        raise HTTPException(status_code=500)
    try:
        f = open(file_path, "r")
    except Exception as e:
        LOGGER.error("Error opening " + file_path)
        LOGGER.exception(e)
        raise HTTPException(status_code=500)
    filecontent = f.read()
    f.close()
    return filecontent