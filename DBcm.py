import sqlite3


class DBcm:
    configuration = {}

    def __init__(self, iparam: dict) -> None:
        self.configuration = iparam

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.configuration['database'])
            self.cursor = self.conn.cursor()
            return self.cursor
        except ConnectionError:
            print('No connection to database')

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def __repr__(self):
        pass
