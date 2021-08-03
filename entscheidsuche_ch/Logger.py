import logging

def _logger(errorlog_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s: %(message)s')

    file_handler = logging.FileHandler(errorlog_file)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger