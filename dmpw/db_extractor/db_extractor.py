import sqlite3
import re
import geojson


# function that makes query results return lists of dictionaries instead of lists of tuples
def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DB_Extractor:

    def __init__(self, db_path:str = None):
        self.db_path = db_path
        self._db = None
        self._cur = None
        self.geometry_column_name = None

        self.geo_statistic = {}

    def init_db(self) -> None:
        if self.db_path is not None:
            try:
                self._db = sqlite3.connect(self.db_path)
                self._db.enable_load_extension(True)
                self._db.load_extension("mod_spatialite")
                self._cur = self._db.cursor()
                self._db.row_factory = dict_factory
            except Exception as e:
                print(f"EXCEPTION {e}")
    
    def set_db_path(self, db_name: str) -> None:
        self.db_path = db_name

    def extract_geometry_column_name(self):
        if self._cur is not None:
            self.geometry_column_name = self._cur.execute('SELECT f_table_name from geometry_columns')

    
    def del_char(text) -> str:
        characters_to_remove = '(),\''
        pattern = f'[{characters_to_remove}]'
        return re.sub(pattern, "", str(text))

    def process_geometry(self):
        geo_objects = dict()
        self.extract_geometry_column_name()
        if self.geometry_column_name is not None:
            for column_name in self.geometry_column_name:
                column_name = DB_Extractor.del_char(column_name)
                geom_result = self._db.execute(f'SELECT AsGeoJSON(Geometry) FROM {column_name}').fetchall()
                geo_objects[column_name] = []
                for row in geom_result:
                    geom = geojson.loads(row['AsGeoJSON(Geometry)'])
                    geo_objects[column_name].append(geom)
        return geo_objects
    
    def extract_geometry(self) -> tuple:
        geo_objects = self.process_geometry()
        geo_linestrings = {}
        geo_poligons = {}
        geo_points = {}
        for key in geo_objects.keys():
            array_objects = geo_objects[key]
            for array_object in array_objects:
                if array_object['type'] == 'LineString' or array_object['type'] == 'MultiLineString':
                    if key in geo_linestrings:
                        geo_linestrings[key].append(array_object['coordinates'])
                    else:
                        geo_linestrings[key] = [array_object['coordinates']]
                elif array_object['type'] == 'Polygon' or array_object['type'] == 'MultiPolygon':
                    if key in geo_poligons:
                        geo_poligons[key].append(array_object['coordinates'])
                    else:
                        geo_poligons[key] = [array_object['coordinates']]
                elif array_object['type'] == 'Point' or array_object['type'] == 'MultiPoint':
                    if key in geo_points:
                        geo_points[key].append(array_object['coordinates'])
                    else:
                        geo_points[key] = [array_object['coordinates']]
        return (geo_linestrings, geo_poligons, geo_points)



    def get_geometry_statistic(self):
        result = None
        try:
            result = self._db.execute(f'SELECT MIN(extent_min_x), MIN(extent_min_y), MAX(extent_max_x), MAX(extent_max_y) FROM geometry_columns_statistics').fetchone()
            
        except sqlite3.OperationalError as e:
            result = None
            print(e)

        if result is not None:
            self.geo_statistic['MIN_X'] = result["MIN(extent_min_x)"]
            self.geo_statistic['MIN_Y'] = result["MIN(extent_min_y)"]
            self.geo_statistic['MAX_X'] = result["MAX(extent_max_x)"]
            self.geo_statistic['MAX_Y'] = result["MAX(extent_max_y)"]