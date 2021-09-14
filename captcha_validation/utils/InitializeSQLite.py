import logging
from captcha_validation.config.Config import Config
import sqlite3

class SQLite():
    def __init__(self, file):
        self.file=file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

class InitializeSQLite:

    def __init__(self):
        self.config = Config()
        logLevel = self.config.get_log_level()
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(getattr(logging, logLevel))
        self.captcha_table = self.config.get_table_name()

    def run(self):
        try:
            with SQLite(self.config.get_sqlite_file()) as cur:
                self.initialize_db(cur)
                self.remove_record_older_than_three_minutes(cur)
        except Exception as e:
            self.log.exception(f"An Exception has been raised during scheduled process: {e}")
            raise e


    def remove_record_older_than_three_minutes(self, cur):
            cur.execute(
                f"""
                DELETE FROM {self.captcha_table} WHERE expire_time <= datetime('now', '-180 seconds') ;
                """
            )


    def initialize_db(self, cur):
            cur.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS {self.captcha_table} 
                   (address TEXT, solution TEXT, expire_time TEXT) ;
                    """
            )

