import logging
from captcha_validation.config.Config import Config
import sqlite3


class ConfigDAO:

    def __init__(self):
        self.config = Config()
        logLevel = self.config.get_log_level()
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(getattr(logging, logLevel))
        self.captcha_table = self.config.get_table_name()