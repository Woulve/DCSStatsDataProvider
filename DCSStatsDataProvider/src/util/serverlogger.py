import logging
from logging.handlers import RotatingFileHandler
import sys

def serverLogger():
    logFile = 'serverlog.log'
    logging.basicConfig(
        handlers=[
                  RotatingFileHandler(logFile, mode='a', maxBytes=1000000, backupCount=0, encoding=None, delay=True),
                  logging.StreamHandler(sys.stdout),
                  ],
        format='%(levelname)s:     %(asctime)s.%(msecs)d %(funcName)s:%(lineno)d %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',
    )
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.INFO)
    return LOGGER