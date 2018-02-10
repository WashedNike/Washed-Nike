import logging
import os
import time
import traceback

def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    os.makedirs('logs', exist_ok=True)
    log_file_path = 'logs/{}'.format(logger_name)
    handler = logging.FileHandler(log_file_path, 'a')
    handler.setFormatter(formatter)
    logger.addHandler(handler) # Log to file

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler) # Log to console

    return logger