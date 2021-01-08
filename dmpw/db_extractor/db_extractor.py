import sqlite3
import re
import geojson
import pyproj



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
        self.coord_sys_name = None

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
                    print(geom)
        return geo_objects
    
    def extract_geometry(self) -> tuple:
        self.get_geometry_statistic()
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
        try:
            proj4text = self._db.execute(f'SELECT proj4text FROM geom_cols_ref_sys').fetchone()
            statistic = self._db.execute(f'SELECT MIN(extent_min_x), MIN(extent_min_y), MAX(extent_max_x), MAX(extent_max_y) FROM geometry_columns_statistics').fetchone()
        except sqlite3.OperationalError as e:
            print(e)
            return

        p = pyproj.Proj(proj4text['proj4text'])
        coord_sys_name = proj4text['proj4text'].split(' ')[0].split('=')[1]
        self.coord_sys_name = coord_sys_name

        if coord_sys_name == 'merc':
            self.geo_statistic['MIN_X'] = statistic["MIN(extent_min_x)"]
            self.geo_statistic['MIN_Y'] = statistic["MIN(extent_min_y)"]
            self.geo_statistic['MAX_X'] = statistic["MAX(extent_max_x)"]
            self.geo_statistic['MAX_Y'] = statistic["MAX(extent_max_y)"]
            lon, lat = p(self.geo_statistic['MIN_X'], self.geo_statistic['MIN_Y'], inverse=True)
            self.geo_statistic['MIN_LON'] = lon
            self.geo_statistic['MIN_LAT'] = lat
            lon, lat = p(self.geo_statistic['MAX_X'], self.geo_statistic['MAX_Y'], inverse=True)
            self.geo_statistic['MAX_LON'] = lon
            self.geo_statistic['MAX_LAT'] = lat
        elif coord_sys_name == 'longlat':
            self.geo_statistic['MIN_LON'] = statistic["MIN(extent_min_x)"]
            self.geo_statistic['MIN_LAT'] = statistic["MIN(extent_min_y)"]
            self.geo_statistic['MAX_LON'] = statistic["MAX(extent_max_x)"]
            self.geo_statistic['MAX_LAT'] = statistic["MAX(extent_max_y)"]
            min_x, min_y = p(self.geo_statistic['MIN_LON'], self.geo_statistic['MIN_LAT'], inverse=True)
            self.geo_statistic['MIN_X'] = min_x
            self.geo_statistic['MIN_Y'] = min_y
            max_x, max_y = p(self.geo_statistic['MAX_X'], self.geo_statistic['MAX_Y'], inverse=True)
            self.geo_statistic['MAX_X'] = max_x
            self.geo_statistic['MAX_Y'] = max_y

