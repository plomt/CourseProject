import logging

FILENAME_TO_LOG = r"C:\Users\pavel\PycharmProjects\UIR\model_code\logs_files\log_file.log"


def get_file_handler():
    simple_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = logging.FileHandler(
        filename=FILENAME_TO_LOG
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(simple_formatter)
    return file_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    return logger