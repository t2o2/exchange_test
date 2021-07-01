import logging

loggers = {}


def setup_custom_logger(name='exchange_test', log_level=logging.DEBUG):
    if loggers.get(name):
        return loggers[name]

    logger = logging.getLogger(name)
    loggers[name] = logger

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.setLevel(log_level)

    logger.addHandler(sh)
    return logger
