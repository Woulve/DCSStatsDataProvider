import logging
from logging.handlers import RotatingFileHandler
import sys

def serverLogger():
    logFile = 'serverlog.log'
    # my_handler =
    logging.basicConfig(
        handlers=[
                  RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0),
                  logging.StreamHandler(sys.stdout),
                  ],
        format='%(asctime)s.%(msecs)d %(funcName)s:%(lineno)d %(name)s %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',
    )
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.INFO)
    return LOGGER