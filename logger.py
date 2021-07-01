import logging
import os

loggers = {}


def setup_custom_logger(name='arbitrage', log_level=logging.DEBUG):
    if loggers.get(name):
        return loggers[name]

    if not os.path.exists('./logs'):
        os.mkdir('logs')

    logger = logging.getLogger(name)
    loggers[name] = logger

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.setLevel(log_level)

    logger.addHandler(sh)
    return logger
