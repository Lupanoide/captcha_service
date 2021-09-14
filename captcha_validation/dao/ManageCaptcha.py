from captcha_validation.dao.ConfigDAO import ConfigDAO
from captcha_validation.utils.InitializeSQLite import SQLite
from captcha_validation.model.Protocolz import Outcome




class ManageCaptcha(ConfigDAO):
    def __init__(self):
        ConfigDAO.__init__(self)


    def ingest(self, address, solution):
        try:
            with SQLite(self.config.get_sqlite_file()) as cur:
                    cur.execute(
                        f"""
                        insert into "{self.captcha_table}" values (?, ?, datetime('now')) ;
                        """, (address, solution)
                    )
            self.log.debug("Data ingestion successfully completed")
        except Exception as e:
            self.log.exception(f"Something goes wrong during data ingestion: {e}")
            return Outcome(f"Something goes wrong during data ingestion: {e}",False)


    def query_for_validation(self, solution, address):
        try:
            with SQLite(self.config.get_sqlite_file()) as cur:
                raw = cur.execute(f"""
                        SELECT * FROM {self.captcha_table} WHERE solution="{solution}" AND address="{address}";
                        """
                            ).fetchone()
                if not raw:
                    self.log.debug("Solution string not found. Maybe th captcha_validation has expired -180 sec until timeout. Try to generate another captcha_validation")
                    return Outcome("Solution string not found. Maybe th captcha_validation has expired -180 sec until timeout. Try to generate another captcha_validation", False)
                self.log.debug("Captcha successfully validate")
                return Outcome("Captcha successfully validate", True)
        except Exception as e:
            self.log.exception(f"Something goes wrong during query for validation: {e}")
            return Outcome(f"Something goes wrong during query for validation: {e}",False)
