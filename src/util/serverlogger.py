import logging
from logging.handlers import RotatingFileHandler

def serverLogger():
    logFile = 'serverlog.log'
    # my_handler =
    logging.basicConfig(
        handlers=[ RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0) ],
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S',
    )
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)
    return LOGGER