# built-in dependencies
import os
import logging
from datetime import datetime


# pylint: disable=broad-except
class Logger:
    def __init__(self, module=None):
        self.module = module
        log_level = os.environ.get("LOG_LEVEL", str(logging.INFO))
        try:
            self.log_level = int(log_level)
        except Exception as err:
            self.dump_log(
                f"Exception while parsing $LOG_LEVEL."
                f"Expected int but it is {log_level} ({str(err)})."
                "Setting app log level to info."
            )
            self.log_level = logging.INFO

        if self.log_level == logging.DEBUG:
            logging.basicConfig(level=logging.DEBUG)

    def info(self, message):
        if self.log_level <= logging.INFO:
            self.dump_log(f"{message}")

    def debug(self, message):
        if self.log_level <= logging.DEBUG:
            self.dump_log(f"🕷️ {message}")

    def warn(self, message):
        if self.log_level <= logging.WARNING:
            self.dump_log(f"⚠️ {message}")

    def error(self, message):
        if self.log_level <= logging.ERROR:
            self.dump_log(f"🔴 {message}")

    def critical(self, message):
        if self.log_level <= logging.CRITICAL:
            self.dump_log(f"💥 {message}")

    def dump_log(self, message):
        print(
            f"{str(datetime.now())[2:-7]} - w{str(os.getpid()).zfill(2)} - {message}"
        )
