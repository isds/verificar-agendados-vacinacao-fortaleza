import logging
import traceback


def log_error(exception, message: str):
    logging.error(message)
    logging.error(exception)
    traceback.print_exc()
