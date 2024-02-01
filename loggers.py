import logging


logging.basicConfig(
    filename="logs.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=f"{name}.log")
    handler.setFormatter(
        logging.Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s")
    )
    logger.addHandler(handler)
    return logger
