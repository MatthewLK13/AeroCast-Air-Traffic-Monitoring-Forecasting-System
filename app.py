import sqlite3
import pandas as pd
import geopandas as gpd
import streamlit as st
import pydeck as pdk
import json
import altair as alt
from FlightRadarAPI import FlightRadar24API
from neuralprophet import NeuralProphet
from shapely.geometry import Point, Polygon
import torch

_original_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = _patched_load

st.set_page_config(page_title="AeroCast 3D", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {

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

    overshoot_points = [(105.0000, 11.0000), (105.0000, 13.3056), (107.6078, 13.3056)]
    oversized_poly = Polygon(aviation_points + overshoot_points)

    polygon_large = oversized_poly.intersection(vn_geom)
    polygon_small = Polygon([(108.6486, 12.5097), (108.6408, 11.8339), (108.3619, 12.0281)])

    gdf = gpd.GeoDataFrame({
        'part_id': ['Part_A', 'Part_B'],
        'max_altitude': [46000, 30500],
        'geometry': [polygon_large, polygon_small]
    }, crs="EPSG:4326")

    gdf['fill_color'] = [[255, 182, 193, 70], [144, 238, 144, 70]]
    gdf['line_color'] = [[255, 0, 0, 255], [0, 128, 0, 255]]
    return gdf

gdf_sectors = load_and_cut_polygon()
bounds = "16.0,8.0,103.0,112.0"

core_geom = gdf_sectors[gdf_sectors['part_id'] == 'Part_A'].geometry.iloc[0].union(gdf_sectors[gdf_sectors['part_id'] == 'Part_B'].geometry.iloc[0])
cx, cy = core_geom.centroid.x, core_geom.centroid.y

col1, col2 = st.columns([1, 1])

with col1:
    st.header("BẢN ĐỒ RADAR 3D THỜI GIAN THỰC")
    show_vectors = st.toggle("Kích hoạt Quỹ đạo Động học (Spatio-Temporal)", value=False)

    @st.fragment(run_every=10)
    def render_radar():
        try:
            fr_api = FlightRadar24API()
            raw_flights = fr_api.get_flights(bounds=bounds)

            flight_table_data = []
            valid_flights_df = pd.DataFrame()

            if raw_flights:
                df_f = pd.DataFrame([{"callsign": f.callsign, "latitude": f.latitude, "longitude": f.longitude, "altitude": f.altitude, "ground_speed": f.ground_speed, "heading": f.heading} for f in raw_flights])
                gdf_flights = gpd.GeoDataFrame(df_f, geometry=gpd.points_from_xy(df_f.longitude, df_f.latitude), crs="EPSG:4326")

                joined = gpd.sjoin(gdf_flights, gdf_sectors, how="inner", predicate="within")
                gdf_valid = joined[joined['altitude'] <= joined['max_altitude']]

                st.session_state['live_aircraft_count'] = len(gdf_valid)
                st.metric(label="TRẠM RADAR (Trực tiếp)", value=len(gdf_valid))
                valid_flights_df = pd.DataFrame(gdf_valid)

                for _, row in gdf_valid.iterrows():
                    flight_table_data.append({"Chuyến bay": row['callsign'], "Độ cao (ft)": row['altitude'], "Vận tốc (kts)": row['ground_speed']})
            else:
                st.metric(label="TRẠM RADAR (Trực tiếp)", value=0)

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


            if show_vectors:
                import math
                from shapely.geometry import LineString

                gdf_buffer = gdf_sectors.copy()
                gdf_buffer['geometry'] = gdf_sectors.geometry.buffer(2.52)

                layer_buffer = pdk.Layer(
                    "GeoJsonLayer",
                    json.loads(gdf_buffer.to_json()),
                    pickable=False,
                    stroked=True,
                    filled=False,
                    get_line_color=[255, 255, 255, 100],
                    get_line_width=3000,
                )
                layers.append(layer_buffer)

                if raw_flights:
                    joined_buffer = gpd.sjoin(gdf_flights, gdf_buffer, how="inner", predicate="within")
                    vector_data = []
                    for idx, row in joined_buffer.iterrows():
                        speed = row.get('ground_speed', 0)
                        heading = row.get('heading', 0)
                        if pd.isna(speed) or speed < 100: continue

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
                            dlat = lat - cy
                            dlon = lon - cx
                            if abs(dlat) > abs(dlon):
                                color = [0, 255, 0, 255] if dlat > 0 else [0, 150, 255, 255]
                            else:
                                color = [255, 0, 255, 255] if dlon > 0 else [255, 255, 0, 255]

                            vector_data.append({
                                "start": [lon, lat],
                                "end": [new_lon, new_lat],
                                "color": color
                            })

                    if vector_data:
                        layer_vectors = pdk.Layer(
                            "LineLayer",
                            pd.DataFrame(vector_data),
                            get_source_position="start",
                            get_target_position="end",
                            get_color="color",
                            get_width=3,
                            pickable=False
                        )
                        layers.append(layer_vectors)

            all_plot_flights = pd.DataFrame()
            if not valid_flights_df.empty:
                all_plot_flights = pd.concat([all_plot_flights, valid_flights_df])
            if raw_flights and show_vectors and 'joined_buffer' in locals() and not joined_buffer.empty:
                all_plot_flights = pd.concat([all_plot_flights, joined_buffer])

            if not all_plot_flights.empty:
                layer_aircraft = pdk.Layer(
                    "ScatterplotLayer",
                    all_plot_flights,
                    get_position="[longitude, latitude]",
                    get_color="[0, 80, 255, 255]",
                    get_radius=4000,
                    pickable=True,
                    auto_highlight=True
                )
                layers.append(layer_aircraft)

            zoom_level = 4.8 if show_vectors else 6
            view_state = pdk.ViewState(
                latitude=12.2,
                longitude=107.5,
                zoom=zoom_level,
                pitch=45,
                bearing=0
            )

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

    render_radar()

with col2:
    @st.fragment(run_every=60)
    def render_ai_panel():
        st.header("PHÂN TÍCH VÀ DỰ BÁO BẰNG TRÍ TUỆ NHÂN TẠO")
        calculated_periods = 6
        try:
            conn = sqlite3.connect('flight_data.db')
            df_all = pd.read_sql_query("SELECT timestamp, aircraft_count, precipitation, wind_speed, cloud_cover, visibility, buffer_n, buffer_s, buffer_e, buffer_w FROM sector_density ORDER BY timestamp ASC", conn)
            conn.close()

            if len(df_all) > 10:
                df_prophet = df_all.copy()
                df_prophet.columns = ['ds', 'y', 'precipitation', 'wind_speed', 'cloud_cover', 'visibility', 'buffer_n', 'buffer_s', 'buffer_e', 'buffer_w']
                df_prophet['ds'] = pd.to_datetime(df_prophet['ds'], errors='coerce').dt.tz_localize(None)

                df_prophet = df_prophet.dropna(subset=['ds', 'y'])
                df_prophet = df_prophet.set_index('ds').resample('5min').mean().interpolate(method='linear').bfill().ffill().reset_index()

                min_required_rows = 18
                if len(df_prophet) < min_required_rows:
                    st.warning(f"Dữ liệu Radar chưa đủ dày ({len(df_prophet)}/{min_required_rows} mốc). Cần tối thiểu 90 phút thu thập liên tục để Mạng Nơ-ron Deep AR-Net bắt đầu học và dự báo. Vui lòng giữ cửa sổ này...")
                    st.stop()

                import numpy as np
                regressor_cols = ['precipitation', 'wind_speed', 'cloud_cover', 'visibility', 'buffer_n', 'buffer_s', 'buffer_e', 'buffer_w']
                for col in regressor_cols:
                    if col in df_prophet.columns:
                        df_prophet[col] = df_prophet[col].astype(float) + np.random.normal(0, 1e-5, size=len(df_prophet))

                @st.cache_resource(show_spinner=False, max_entries=1)
                def get_trained_model(_df, data_hash):
                    from neuralprophet import set_random_seed, NeuralProphet
                    set_random_seed(42)

                    m = NeuralProphet(
                        n_lags=12,
                        n_forecasts=calculated_periods,
                        ar_layers=[32, 32],
                        quantiles=[0.1, 0.9],
                        yearly_seasonality=False,
                        weekly_seasonality=True,
                        daily_seasonality=True,
                    )

                    m.add_country_holidays(country_name="VN")
                    valid_cols = ['ds', 'y'] + regressor_cols

                    for col in ['precipitation', 'wind_speed', 'cloud_cover', 'visibility']:
                        m.add_future_regressor(col)

                    for col in ['buffer_n', 'buffer_s', 'buffer_e', 'buffer_w']:
                        m.add_lagged_regressor(col)
                    import logging
                    logging.getLogger("pytorch_lightning").setLevel(logging.WARNING)

                    df_train = _df[valid_cols]
                    m.fit(df_train, freq='5min', minimal=True)
                    return m, valid_cols

                current_data_hash = f"{len(df_prophet)}_{df_prophet.iloc[-1]['ds']}_v10_5min"
                m, valid_cols = get_trained_model(df_prophet, current_data_hash)

                latest_weather = df_prophet.iloc[-1]
                future_regressors_df = pd.DataFrame({
                    'precipitation': [latest_weather['precipitation']] * calculated_periods,
                    'wind_speed': [latest_weather['wind_speed']] * calculated_periods,
                    'cloud_cover': [latest_weather['cloud_cover']] * calculated_periods,
                    'visibility': [latest_weather['visibility']] * calculated_periods
                })

                df_predict = df_prophet[valid_cols]
                future = m.make_future_dataframe(df_predict, periods=calculated_periods, regressors_df=future_regressors_df, n_historic_predictions=True)
                forecast_future = m.predict(future)

                yhat_cols = [f"yhat{i+1}" for i in range(calculated_periods) if f"yhat{i+1}" in forecast_future.columns]
                q10_cols = [f"yhat{i+1} 10.0%" for i in range(calculated_periods) if f"yhat{i+1} 10.0%" in forecast_future.columns]
                q90_cols = [f"yhat{i+1} 90.0%" for i in range(calculated_periods) if f"yhat{i+1} 90.0%" in forecast_future.columns]

                actual_current_val = st.session_state.get('live_aircraft_count', 0)
                actual_current_time = pd.Timestamp.now()

                future_times = list(forecast_future.tail(calculated_periods)['ds'])

                last_n_rows = forecast_future.tail(calculated_periods)

                def extract_safe(cols):
                    res = []
                    for c in cols:
                        valid_series = last_n_rows[c].dropna()
                        if len(valid_series) > 0:
                            val = valid_series.iloc[-1]
                            res.append(max(0, round(float(val))))
                        else:
                            res.append(actual_current_val)
                    return res

                df_plot = pd.DataFrame({
                    'ds': [actual_current_time] + future_times,
                    'Số lượng (chiếc)': [actual_current_val] + extract_safe(yhat_cols),
                })

                if q10_cols and q90_cols:
                    df_plot['q10'] = [actual_current_val] + extract_safe(q10_cols)
                    df_plot['q90'] = [actual_current_val] + extract_safe(q90_cols)
                else:
                    df_plot['q10'] = df_plot['Số lượng (chiếc)']
                    df_plot['q90'] = df_plot['Số lượng (chiếc)']


                df_plot['Giờ'] = df_plot['ds'].dt.strftime('%H:%M')

                base = alt.Chart(df_plot)

                line_chart = base.mark_line(color='#00E5FF', strokeWidth=3, interpolate='monotone').encode(
                    x=alt.X('Giờ:N', axis=alt.Axis(labelAngle=0, title="")),
                    y=alt.Y('Số lượng (chiếc):Q', axis=alt.Axis(title="Mật độ (chuyến)", tickMinStep=1)),
                    tooltip=['Giờ', 'Số lượng (chiếc)']
                )

                area_chart = base.mark_area(opacity=0.3, color='#00E5FF', interpolate='monotone').encode(
                    x=alt.X('Giờ:N'),
                    y=alt.Y('q10:Q'),
                    y2=alt.Y2('q90:Q'),
                    tooltip=['Giờ', 'q10', 'q90']
                )

                chart = (area_chart + line_chart).properties(height=350)

                st.subheader("Xu Hướng Mật Độ 30 Phút Tới")

                st.markdown("""
                <div style="display: flex; gap: 20px; font-size: 13px; color: #b0b0b0; margin-bottom: 15px; margin-top: -5px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 25px; height: 3px; background-color: #00E5FF; border-radius: 2px;"></div>
                        <span>Quỹ đạo Dự báo Chính</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 25px; height: 14px; background-color: rgba(0, 229, 255, 0.3); border-radius: 3px; border: 1px dashed rgba(0, 229, 255, 0.5);"></div>
                        <span>Vùng Dao động An toàn</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.altair_chart(chart, use_container_width=True)

                st.write("---")
                stat_col, table_col = st.columns([1, 2])

                with stat_col:
                    st.subheader("Trạng thái")
                    if len(df_prophet) > 0:
                        current_val = int(df_prophet['y'].iloc[-1])
                        last_record_time = df_prophet['ds'].iloc[-1].strftime('%H:%M')

                        avg_1h = int(df_prophet['y'].tail(12).mean()) if len(df_prophet) >= 12 else current_val
                        avg_prev_1h = int(df_prophet['y'].tail(24).head(12).mean()) if len(df_prophet) >= 24 else avg_1h
                        delta = avg_1h - avg_prev_1h

                        accuracy_display = "Đang thu thập..."
                        try:
                            hist_actual = forecast_future['y'].iloc[:-calculated_periods].dropna()
                            hist_pred = forecast_future['yhat1'].iloc[:-calculated_periods].dropna()

                            common_idx = hist_actual.index.intersection(hist_pred.index)
                            if len(common_idx) > 0:
                                mae = (hist_actual[common_idx] - hist_pred[common_idx]).abs().mean()
                                mean_y = hist_actual[common_idx].mean()
                                if mean_y > 0:
                                    acc_percentage = max(0.0, 100.0 - (mae / mean_y) * 100.0)
                                    accuracy_display = f"{acc_percentage:.1f}%"
                                else:
                                    accuracy_display = "100%" if mae < 1 else "0%"
                        except Exception as e:
                            accuracy_display = f"Lỗi: {e}"

                        st.metric(label=f"CẬP NHẬT LÚC {last_record_time}", value=f"{current_val}")
                        st.metric(label="TRUNG BÌNH (1 GIỜ)", value=f"{avg_1h}", delta=f"{delta} chuyến")
                        st.metric(label="ĐỘ CHÍNH XÁC DỰ BÁO", value=accuracy_display)

                with table_col:
                    st.subheader("Dự kiến chi tiết (6 mốc 5 phút)")
                    forecast_future['yhat_combined'] = forecast_future[yhat_cols].bfill(axis=1).iloc[:, 0]

                    future_preview = forecast_future.tail(calculated_periods)[['ds', 'yhat_combined']].copy()
                    future_preview['ds'] = future_preview['ds'].dt.strftime('%H:%M')
                    future_preview.columns = ['Thời gian', 'Mật độ dự kiến']

                    future_preview['Mật độ dự kiến'] = future_preview['Mật độ dự kiến'].fillna(0).clip(lower=0).round(0).astype(int)
                    st.dataframe(future_preview, use_container_width=True, hide_index=True)
            else:
                st.warning("Hệ thống đang tiếp tục tích lũy thêm chuỗi dữ liệu lịch sử lịch trình...")
        except Exception as e:
            st.error(f"Lỗi khi chạy AI: {e}")

    render_ai_panel()

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
