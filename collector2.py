import sqlite3
import time
from datetime import datetime
from FlightRadarAPI import FlightRadar24API
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

fr_api = FlightRadar24API()

# 1. ĐỌC FILE BẢN ĐỒ VIỆT NAM (vn.json)
try:
    vn_gdf = gpd.read_file('vn.json')
    # Gộp tất cả các tỉnh/mảnh bản đồ thành 1 khối lãnh thổ duy nhất
    vn_geom = vn_gdf.geometry.union_all() if hasattr(vn_gdf.geometry, 'union_all') else vn_gdf.geometry.unary_union
except Exception as e:
    print(f"Lỗi đọc file vn.json (Kiểm tra lại xem file đã nằm trong thư mục chưa): {e}")
    exit()

# 2. KHỞI TẠO KHUÔN CẮT (OVERSIZED POLYGON)
aviation_points = [
    (107.6078, 13.3056),  # D01
    (107.9908, 13.3308),  # E01
    (108.5061, 13.3639),  # D23
    (108.6575, 13.2606),  # D24
    (108.6486, 12.5097),  # DN4
    (108.3619, 12.0281),  # E04
    (107.9728, 12.2983),  # E02
    (106.9792, 10.8792),  # E03
    (106.6383, 11.0881),  # RUNOP
    (105.9103, 11.2625)   # D15
]

# Vẽ các điểm đâm lố sang phía Tây (Campuchia) để tạo khuôn gọt
overshoot_points = [
        (105.0000, 11.0000),         # Bước 1: Từ D15 đâm lố sâu sang phía Tây (Campuchia)
        (105.0000, 13.3056),         # Bước 2: Kéo lên phía Bắc, NHƯNG DỪNG LẠI ĐÚNG ở vĩ độ của D01
        (107.6078, 13.3056)          # Bước 3: Kéo ngang sang Đông để chạm chuẩn xác vào D01
    ]

oversized_poly = Polygon(aviation_points + overshoot_points)

# 3. THỰC HIỆN PHÉP GIAO (INTERSECTION) THẦN THÁNH
# Lấy phần chung giữa Khuôn cắt và Bản đồ VN -> Ra chính xác Phân khu 2
polygon_large = oversized_poly.intersection(vn_geom)

# Đa giác nhỏ (Part B - nằm hoàn toàn trong nội địa nên giữ nguyên)
polygon_small = Polygon([(108.6486, 12.5097), (108.6408, 11.8339), (108.3619, 12.0281)])

# Đóng gói vào GeoPandas
gdf_sectors = gpd.GeoDataFrame({
    'part_id': ['Part_A', 'Part_B'],
    'max_altitude': [26500, 30500],
    'geometry': [polygon_large, polygon_small]
}, crs="EPSG:4326")

bounds = "13.5,10.5,105.5,109.5"

def init_db():
    conn = sqlite3.connect('flight_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sector_density 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, aircraft_count INTEGER)''')
    conn.commit()
    return conn

def fetch_and_save_data(conn):
    try:
        raw_flights = fr_api.get_flights(bounds=bounds)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        valid_aircraft_count = 0
        
        if raw_flights:
            df_flights = pd.DataFrame([{"longitude": f.longitude, "latitude": f.latitude, "altitude": f.altitude} for f in raw_flights])
            gdf_flights = gpd.GeoDataFrame(df_flights, geometry=gpd.points_from_xy(df_flights.longitude, df_flights.latitude), crs="EPSG:4326")
            
            joined = gpd.sjoin(gdf_flights, gdf_sectors, how="inner", predicate="within")
            gdf_valid = joined[joined['altitude'] <= joined['max_altitude']]
            valid_aircraft_count = len(gdf_valid)
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sector_density (timestamp, aircraft_count) VALUES (?, ?)", (current_time, valid_aircraft_count))
        conn.commit()
        print(f"[{current_time}] [GIS Intersection] Mật độ Phân khu 2: {valid_aircraft_count} chiếc.")
        
    except Exception as e:
        print(f"Lỗi: {e}")

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