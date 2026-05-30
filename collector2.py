import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')
import time
import requests
from datetime import datetime
from FlightRadarAPI import FlightRadar24API
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, LineString
import math
import logging

logging.disable(logging.CRITICAL)

fr_api = FlightRadar24API()

try:
    vn_gdf = gpd.read_file('vn.json')
    vn_geom = vn_gdf.geometry.union_all() if hasattr(vn_gdf.geometry, 'union_all') else vn_gdf.geometry.unary_union
except Exception as e:
    print(f"Lỗi đọc file vn.json (Kiểm tra lại xem file đã nằm trong thư mục chưa): {e}")
    exit()

aviation_points = [
    (107.6078, 13.3056),
    (107.9908, 13.3308),
    (108.5061, 13.3639),
    (108.6575, 13.2606),
    (108.6486, 12.5097),
    (108.3619, 12.0281),
    (107.9728, 12.2983),
    (106.9792, 10.8792),
    (106.6383, 11.0881),
    (105.9103, 11.2625)
]

overshoot_points = [
        (105.0000, 11.0000),
        (105.0000, 13.3056),
        (107.6078, 13.3056)
    ]

oversized_poly = Polygon(aviation_points + overshoot_points)

polygon_large = oversized_poly.intersection(vn_geom)

polygon_small = Polygon([(108.6486, 12.5097), (108.6408, 11.8339), (108.3619, 12.0281)])

gdf_sectors = gpd.GeoDataFrame({
    'part_id': ['Part_A', 'Part_B'],
    'max_altitude': [46000, 30500],
    'geometry': [polygon_large, polygon_small]
}, crs="EPSG:4326")

core_geom = gdf_sectors.geometry.union_all() if hasattr(gdf_sectors.geometry, 'union_all') else gdf_sectors.geometry.unary_union
buffer_geom = core_geom.buffer(2.5).difference(core_geom)
gdf_buffer = gpd.GeoDataFrame({'geometry': [buffer_geom]}, crs="EPSG:4326")

bounds = "16.0,8.0,103.0,112.0"

def init_db():
    conn = sqlite3.connect('flight_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sector_density
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, aircraft_count INTEGER, precipitation REAL DEFAULT 0.0, wind_speed REAL DEFAULT 0.0, cloud_cover REAL DEFAULT 0.0, visibility REAL DEFAULT 10000.0, buffer_count INTEGER DEFAULT 0, buffer_n INTEGER DEFAULT 0, buffer_s INTEGER DEFAULT 0, buffer_e INTEGER DEFAULT 0, buffer_w INTEGER DEFAULT 0)''')
    conn.commit()
    return conn

def fetch_and_save_data(conn):
    try:
        raw_flights = fr_api.get_flights(bounds=bounds)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        valid_aircraft_count = 0
        buffer_aircraft_count = 0

        precipitation = 0.0
        wind_speed = 0.0
        cloud_cover = 0.0
        visibility = 10000.0
        try:
            w_url = "https://api.open-meteo.com/v1/forecast?latitude=12.6667&longitude=108.0383&current=precipitation,wind_speed_10m,cloud_cover,visibility"
            w_resp = requests.get(w_url, timeout=5).json()
            if "current" in w_resp:
                precipitation = float(w_resp["current"].get("precipitation", 0.0))
                wind_speed = float(w_resp["current"].get("wind_speed_10m", 0.0))
                cloud_cover = float(w_resp["current"].get("cloud_cover", 0.0))
                visibility = float(w_resp["current"].get("visibility", 10000.0))
        except Exception as e:
            print(f"Lỗi lấy thời tiết: {e}")

        if raw_flights:
            df_flights = pd.DataFrame([{
                "longitude": f.longitude,
                "latitude": f.latitude,
                "altitude": f.altitude,
                "heading": getattr(f, 'heading', 0),
                "speed": getattr(f, 'speed', getattr(f, 'ground_speed', 0))
            } for f in raw_flights])

            gdf_flights = gpd.GeoDataFrame(df_flights, geometry=gpd.points_from_xy(df_flights.longitude, df_flights.latitude), crs="EPSG:4326")

            joined = gpd.sjoin(gdf_flights, gdf_sectors, how="inner", predicate="within")
            gdf_valid = joined[joined['altitude'] <= joined['max_altitude']]
            valid_aircraft_count = len(gdf_valid)

            joined_buffer = gpd.sjoin(gdf_flights, gdf_buffer, how="inner", predicate="within")
            raw_buffer_count = len(joined_buffer)

            inbound_threat_count = 0
            buffer_n = 0
            buffer_s = 0
            buffer_e = 0
            buffer_w = 0

            cx, cy = core_geom.centroid.x, core_geom.centroid.y

            for idx, row in joined_buffer.iterrows():
                speed = row.get('speed', 0)
                heading = row.get('heading', 0)

                if speed < 100:
                    continue

                distance_km = speed * 1.852 * 0.75

                lat, lon = row['latitude'], row['longitude']

                dy_km = distance_km * math.cos(math.radians(heading))
                dx_km = distance_km * math.sin(math.radians(heading))

                dy_deg = dy_km / 111.32
                dx_deg = dx_km / (111.32 * math.cos(math.radians(lat)))

                new_lat = lat + dy_deg
                new_lon = lon + dx_deg

                flight_vector = LineString([(lon, lat), (new_lon, new_lat)])

                if flight_vector.intersects(core_geom):
                    inbound_threat_count += 1
                    dlat = lat - cy
                    dlon = lon - cx
                    if abs(dlat) > abs(dlon):
                        if dlat > 0: buffer_n += 1
                        else: buffer_s += 1
                    else:
                        if dlon > 0: buffer_e += 1
                        else: buffer_w += 1

        cursor = conn.cursor()
        cursor.execute("INSERT INTO sector_density (timestamp, aircraft_count, precipitation, wind_speed, cloud_cover, visibility, buffer_count, buffer_n, buffer_s, buffer_e, buffer_w) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (current_time, valid_aircraft_count, precipitation, wind_speed, cloud_cover, visibility, buffer_aircraft_count, buffer_n, buffer_s, buffer_e, buffer_w))
        conn.commit()

        threat_level = "WARN" if buffer_aircraft_count > 0 else "OK  "
        print(f"[OK]   {current_time} | SECTOR_CORE   | Active Aircraft: {valid_aircraft_count}")
        print(f"[{threat_level}] {current_time} | KINEMATICS    | Inbound Threats: {buffer_aircraft_count} [N:{buffer_n} | S:{buffer_s} | E:{buffer_e} | W:{buffer_w}]")
        print(f"[INFO] {current_time} | WEATHER_METAR | Precip: {precipitation}mm | Wind: {wind_speed}km/h | Clouds: {cloud_cover}%")
        print(f"[OK]   {current_time} | DB_STORAGE    | Data committed to flight_data.db")
        print("-" * 85)

    except Exception as e:
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ERR]  {error_time} | SYSTEM_CRASH  | {e}")

if __name__ == "__main__":
    db_conn = init_db()
    print("==================================================================")
    print("ENGINE GEOFENCING VỚI VN.JSON ĐANG CHẠY...")
    print("==================================================================")
    try:
        while True:
            fetch_and_save_data(db_conn)
            time.sleep(600)
    except KeyboardInterrupt:
        db_conn.close()
