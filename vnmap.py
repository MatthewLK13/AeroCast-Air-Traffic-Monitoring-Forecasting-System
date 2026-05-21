import json
import folium
import webbrowser
import os

# Đọc file GeoJSON
with open("vn.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tạo map
m = folium.Map(
    location=[16, 108],
    zoom_start=5,
    tiles="CartoDB positron"
)

# Thêm layer GeoJSON
folium.GeoJson(data).add_to(m)

# Lưu HTML
map_file = "vietnam_map.html"
m.save(map_file)

# Mở tab mới trên browser
webbrowser.open(
    "file://" + os.path.realpath(map_file),
    new=2
)

print("Đã mở map trên browser")