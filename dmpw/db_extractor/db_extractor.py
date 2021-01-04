import sqlite3

class DB_Extractor:

    def __init__(self, db_path:str = None):
        self.db_path = db_path
        self._db = None
        self._cur = None
        self.geometry_column_name = None

    def init_db(self) -> None:
        if self.db_path is not None:
            try:
                self._db = sqlite3.connect(self.db_path)
                self._db.enable_load_extension(True)
                self._db.load_extension("mod_spatialite")
                self._cur = self._db.cursor()
            except Exception as e:
                print(f"EXCEPTION {e}")
    
    def set_db_path(self, db_name: str) -> None:
        self.db_path = db_name

    def extract_geometry_column_name(self):
        if self._cur is not None:
            self.geometry_column_name = self._cur.execute('SELECT f_table_name from geometry_columns')





