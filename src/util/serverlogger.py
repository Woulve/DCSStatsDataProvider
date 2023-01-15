import logging

def serverLogger():
    logging.basicConfig(filename="serverlog.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)
    return LOGGER