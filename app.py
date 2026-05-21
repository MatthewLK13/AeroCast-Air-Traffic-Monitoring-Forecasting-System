import sqlite3
import pandas as pd
import geopandas as gpd
import streamlit as st
import pydeck as pdk
import json
from FlightRadarAPI import FlightRadar24API
from neuralprophet import NeuralProphet
from shapely.geometry import Point, Polygon
import torch

# Vá lỗi PyTorch 2.6 chặn NeuralProphet tải model do mặc định weights_only=True
_original_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = _patched_load

# --- CẤU HÌNH GIAO DIỆN STREAMLIT ---
st.set_page_config(page_title="AeroCast - Luong Minh Khoi", layout="wide")

# Tiêm CSS cao cấp (Premium UI)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Thiết kế thẻ Glassmorphism cho Metric */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(20, 30, 48, 0.8), rgba(36, 59, 85, 0.8));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 229, 255, 0.2);
        border: 1px solid rgba(0, 229, 255, 0.3);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #A0AEC0 !important;
        font-size: 1rem !important;
        font-weight: 400;
        margin-bottom: 5px;
    }
    
    div[data-testid="stMetricValue"] {
        color: #00E5FF !important;
        font-size: 2.5rem !important;
        font-weight: 600;
        text-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
    }
    
    /* Làm đẹp thanh trượt (Slider) */
    div[data-baseweb="slider"] {
        margin-top: 10px;
    }
    
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }
    
    hr {
        border-color: rgba(255, 255, 255, 0.1);    
    }
</style>
""", unsafe_allow_html=True)


# --- TIÊU ĐỀ DỰ ÁN ---
st.markdown("<h1 style='text-align: center; color: #4facfe;'>HỆ THỐNG GIÁM SÁT VÀ DỰ BÁO KHÔNG LƯU - PHÂN KHU 2 </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.1em; margin-top: -15px;'><i>Created by <b>Luong Minh Khoi</b></i></p>", unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([4, 2, 4])
with col_btn2:
    if st.button("Cập nhật dữ liệu mới nhất", use_container_width=True):
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)


@st.cache_data
def load_and_cut_polygon():
    vn_gdf = gpd.read_file('vn.json')
    vn_geom = vn_gdf.geometry.union_all() if hasattr(vn_gdf.geometry, 'union_all') else vn_gdf.geometry.unary_union
    
    aviation_points = [
        (107.6078, 13.3056), (107.9908, 13.3308), (108.5061, 13.3639), (108.6575, 13.2606), 
        (108.6486, 12.5097), (108.3619, 12.0281), (107.9728, 12.2983), (106.9792, 10.8792), 
        (106.6383, 11.0881), (105.9103, 11.2625)
    ]
    
    # Ép phẳng phần gọt tại vĩ độ D01 để tránh lố sừng Bắc
    overshoot_points = [(105.0000, 11.0000), (105.0000, 13.3056), (107.6078, 13.3056)]
    oversized_poly = Polygon(aviation_points + overshoot_points)
    
    polygon_large = oversized_poly.intersection(vn_geom)
    polygon_small = Polygon([(108.6486, 12.5097), (108.6408, 11.8339), (108.3619, 12.0281)])
    
    gdf = gpd.GeoDataFrame({
        'part_id': ['Part_A', 'Part_B'],
        'max_altitude': [26500, 30500],
        'geometry': [polygon_large, polygon_small]
    }, crs="EPSG:4326")
    
    # Cấu hình màu sắc dạng mảng RGB [R, G, B, Alpha] cho lớp phủ PyDeck
    gdf['fill_color'] = [[255, 182, 193, 70], [144, 238, 144, 70]]  # Hồng và Xanh lá nhạt
    gdf['line_color'] = [[255, 0, 0, 255], [0, 128, 0, 255]]        # Viền Đỏ và Xanh đậm
    return gdf

gdf_sectors = load_and_cut_polygon()
bounds = "13.5,10.5,105.5,109.5"

col1, col2 = st.columns([1, 1])

# --- CỘT 1: BẢN ĐỒ RADAR 3D PYDECK ---
with col1:
    st.header("BẢN ĐỒ RADAR 3D THỜI GIAN THỰC")
    try:
        fr_api = FlightRadar24API()
        raw_flights = fr_api.get_flights(bounds=bounds)
        
        flight_table_data = []
        valid_flights_df = pd.DataFrame()
        
        if raw_flights:
            df_f = pd.DataFrame([{"callsign": f.callsign, "latitude": f.latitude, "longitude": f.longitude, "altitude": f.altitude, "ground_speed": f.ground_speed} for f in raw_flights])
            gdf_flights = gpd.GeoDataFrame(df_f, geometry=gpd.points_from_xy(df_f.longitude, df_f.latitude), crs="EPSG:4326")
            
            joined = gpd.sjoin(gdf_flights, gdf_sectors, how="inner", predicate="within")
            gdf_valid = joined[joined['altitude'] <= joined['max_altitude']]
            
            st.metric(label="Số lượng máy bay hợp lệ", value=len(gdf_valid))
            valid_flights_df = pd.DataFrame(gdf_valid)
            
            for _, row in gdf_valid.iterrows():
                flight_table_data.append({"Chuyến bay": row['callsign'], "Độ cao (ft)": row['altitude'], "Vận tốc (kts)": row['ground_speed']})
        else:
            st.metric(label="Số lượng máy bay hợp lệ", value=0)
            
        # KHỞI TẠO LỚP ĐA GIÁC VÙNG KHÔNG LƯU (GEOMATRIX LAYER)
        layer_polygon = pdk.Layer(
            "GeoJsonLayer",
            json.loads(gdf_sectors.to_json()),
            pickable=False,
            stroked=True,
            filled=True,
            extruded=False,
            get_fill_color="properties.fill_color",
            get_line_color="properties.line_color",
            get_line_width=2500,
        )
        layers = [layer_polygon]
        
        # KHỞI TẠO LỚP ĐỊNH VỊ MÁY BAY (AIRCRAFT LAYER)
        if not valid_flights_df.empty:
            layer_aircraft = pdk.Layer(
                "ScatterplotLayer",
                valid_flights_df,
                get_position="[longitude, latitude]",
                get_color="[0, 80, 255, 220]", # Xanh radar chuyên dụng
                get_radius=3500,
                pickable=True,
                auto_highlight=True
            )
            layers.append(layer_aircraft)
            
        # CẤU HÌNH TRẠNG THÁI GÓC NHÌN NGHIÊNG 3D
        view_state = pdk.ViewState(
            latitude=12.2,
            longitude=107.5,
            zoom=6,
            pitch=45,      # Tạo góc nghiêng 45 độ toàn cảnh không gian
            bearing=0
        )
        
        # KẾT XUẤT PYDECK - SỬ DỤNG TRỰC TIẾP ĐƯỜNG LINK STYLE ĐỂ HIỂN THỊ ĐẦY ĐỦ TỈNH THÀNH QUỐC GIA
        r = pdk.Deck(
            layers=layers,
            initial_view_state=view_state,
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            tooltip={"html": "<b>Chuyến bay: {callsign}</b><br>Độ cao: {altitude} ft<br>Vận tốc: {ground_speed} kts"}
        )
        
        st.pydeck_chart(r)
        
        st.subheader("Danh sách chuyến bay đang hoạt động")
        if flight_table_data:
            st.dataframe(pd.DataFrame(flight_table_data), use_container_width=True, hide_index=True)
        else:
            st.info("Trạm Radar hiện không ghi nhận chuyến bay nào trong Phân khu 2.")
            
    except Exception as e:
        st.error(f"Lỗi tải bản đồ radar: {e}")

# --- CỘT 2: DỰ BÁO MẬT ĐỘ BẰNG AI PROPHET ---
with col2:
    st.header("PHÂN TÍCH VÀ DỰ BÁO BẰNG TRÍ TUỆ NHÂN TẠO")
    # Luôn dự báo full 24 giờ (144 mốc 10 phút)
    calculated_periods = 144
    
    try:
        conn = sqlite3.connect('flight_data.db')
        df_all = pd.read_sql_query("SELECT timestamp, aircraft_count FROM sector_density ORDER BY timestamp ASC", conn)
        conn.close()
        
        if len(df_all) > 5:
            df_prophet = df_all.copy()
            df_prophet.columns = ['ds', 'y']
            # Chuyển đổi datetime an toàn (errors='coerce') và lọc sạch các dòng lỗi (NaT)
            df_prophet['ds'] = pd.to_datetime(df_prophet['ds'], errors='coerce').dt.tz_localize(None)
            df_prophet = df_prophet.dropna(subset=['ds', 'y'])
            df_prophet = df_prophet.drop_duplicates(subset=['ds']).sort_values('ds') # Xóa trùng lặp và sắp xếp lại
            
            if len(df_prophet) < 5:
                st.warning("Dữ liệu hợp lệ quá ít, vui lòng chờ hệ thống thu thập thêm...")
                st.stop()
            
            # Giữ cho NeuralProphet ổn định, không thay đổi ngẫu nhiên mỗi lần refresh
            from neuralprophet import set_random_seed
            set_random_seed(42)
            
            # Cấu hình NeuralProphet
            # Bắt buộc bật daily_seasonality để tạo ra biểu đồ có độ cong (có lên có xuống)
            # Nếu tắt, AI sẽ chỉ vẽ một đường thẳng trung bình ngang (rất vô lý với người xem).
            m = NeuralProphet(
                yearly_seasonality=False,
                weekly_seasonality=False, # Tạm tắt chu kỳ tuần để tránh nhiễu
                daily_seasonality=True,   # Ép bật chu kỳ ngày
                epochs=80 # Tăng nhẹ vòng lặp để AI học đường cong tốt hơn
            )
            
            # Giảm log của pytorch-lightning
            import logging
            logging.getLogger("pytorch_lightning").setLevel(logging.WARNING)
            
            m.fit(df_prophet, freq='10min', minimal=True)
            
            # Tạo data tương lai và dự báo
            future = m.make_future_dataframe(df_prophet, periods=calculated_periods)
            forecast_future = m.predict(future)
            
            # Lấy đúng mốc thời gian hiện tại từ dự báo lịch sử làm điểm bắt đầu biểu đồ
            # (Phải dự báo cả tập để AI nhận diện được chu kỳ freq, tránh lỗi Invalid frequency)
            forecast_historic = m.predict(df_prophet)
            current_point = forecast_historic.tail(1)
            forecast_display = pd.concat([current_point, forecast_future])
            
            # Đặt index để vẽ biểu đồ từ hiện tại đến tương lai
            df_res = forecast_display[['ds', 'yhat1']].set_index('ds')
            
            # Khử giá trị âm: Số chuyến bay không thể nhỏ hơn 0
            df_res['yhat1'] = df_res['yhat1'].clip(lower=0)
            
            st.subheader("Xu Hướng Mật Độ 24 Giờ Tới")
            st.line_chart(df_res['yhat1'])
            
            # --- Thống kê & Bảng dự kiến chi tiết ---
            st.write("---")
            stat_col, table_col = st.columns([1, 2])
            
            with stat_col:
                st.subheader("Trạng thái")
                if len(df_prophet) > 0:
                    current_val = int(df_prophet['y'].iloc[-1])
                    avg_1h = int(df_prophet['y'].tail(6).mean()) if len(df_prophet) >= 6 else current_val
                    avg_prev_1h = int(df_prophet['y'].tail(12).head(6).mean()) if len(df_prophet) >= 12 else avg_1h
                    delta = avg_1h - avg_prev_1h
                    
                    st.metric(label="Mật độ hiện tại", value=f"{current_val} chuyến")
                    st.metric(label="Trung bình 1h qua", value=f"{avg_1h} chuyến", delta=f"{delta} chuyến")
            
            with table_col:
                st.subheader("Dự kiến chi tiết (10 mốc tới)")
                future_preview = forecast_future[['ds', 'yhat1']].copy()
                future_preview.columns = ['Thời gian', 'Mật độ dự kiến']
                # Đảm bảo không có máy bay âm
                future_preview['Mật độ dự kiến'] = future_preview['Mật độ dự kiến'].clip(lower=0).round(0).astype(int)
                st.dataframe(future_preview.head(10), use_container_width=True, hide_index=True)
        else:
            st.warning("Hệ thống đang tiếp tục tích lũy thêm chuỗi dữ liệu lịch sử lịch trình...")
    except Exception as e:
        st.error(f"Lỗi khi chạy AI: {e}")

st.markdown(
    """
    <br><br>
    <hr style="border-color: #333;">
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p><b>AeroCast: Air Traffic Monitoring & Forecasting System</b></p>
        <p>&copy; 2026 Bản quyền thuộc về <b>Luong Minh Khoi</b>. All rights reserved.</p>
    </div>
    """, 
    unsafe_allow_html=True
)
