# ✈️ AEROCAST-VAA-SYSTEM: HỆ THỐNG QUẢN LÝ LUỒNG KHÔNG LƯU (ATFM) DỰA TRÊN TRÍ TUỆ NHÂN TẠO

**Bản quyền & Phát triển bởi: Lương Minh Khôi (Luong Minh Khoi) © 2026**

Chào mừng bạn đến với AeroCast - Hệ thống Quản lý Luồng và Dự báo Không lưu (Air Traffic Flow Management) tích hợp Trí tuệ Nhân tạo. Hệ thống được thiết kế chuyên biệt để hỗ trợ kiểm soát viên không lưu trong việc giám sát Phân khu 2 (FIR Hồ Chí Minh), đưa ra các cảnh báo tắc nghẽn và phân tích lưu lượng bay theo chuẩn ICAO.

---

## 🌟 TÍNH NĂNG NỔI BẬT (CORE FEATURES)

### 1. 📡 Giám sát Radar Vệ tinh (Live ADS-B Tracking)
- Tự động thu thập dữ liệu tọa độ (Lat/Lon), độ cao, vận tốc và hướng mũi bay của tàu bay thực tế theo thời gian thực (Real-time) từ API FlightRadar24.
- Sử dụng công nghệ Nội suy Không gian (Spatial GIS) với `Geopandas` và `Shapely` để nhận diện các tàu bay bay ngang qua đa giác vùng trời Phân khu 2.

### 2. 🧠 Phân tích & Dự báo bằng AI (NeuralProphet)
- Khai thác sức mạnh của mạng nơ-ron **Deep AR-Net (NeuralProphet - PyTorch)** để học hỏi chuỗi thời gian mật độ không lưu.
- Khả năng dự báo quỹ đạo 6 bước thời gian (trong 30 phút tương lai).
- Đo lường và hiển thị sai số tự động bằng thuật toán MAE (Mean Absolute Error) để đánh giá độ tin cậy của mô hình so với Ngưỡng Năng lực (Capacity).

### 3. 📊 Phân tích Số liệu Chuyên sâu (Advanced Analytics)
Hệ thống giải quyết 3 khái niệm cốt lõi của ngành ATFM:
- **Traffic Density (Mật độ):** Phân tích và đối chiếu số lượng tàu bay có mặt tại một thời điểm so với Năng lực Khai thác.
- **Traffic Intensity (Cường độ):** Thống kê tần suất xảy ra các sự cố dồn ứ kéo dài theo khung giờ trong ngày (Bar Chart).
- **Traffic Flow (Luồng đường bay):** Xếp loại tàu bay vào các luồng bay huyết mạch tương ứng ở Việt Nam (VD: *Đường bay dọc Q1/Q2/W1* và *Đường bay ngang A202/L759*) để xác định Trục nào đang gánh tải nặng nhất (Donut Chart).

### 4. 🎮 Kịch bản Giả lập (Mock Simulation Scenarios)
- Tích hợp 3 Kịch bản Giả lập (Bình thường, Quá tải Mật độ, Quá tải Cường độ kéo dài) phục vụ cho công tác Đào tạo và Trình diễn (Demo).
- Mọi biểu đồ và cảnh báo sẽ đồng bộ thay đổi tự động để phản ứng với kịch bản được chọn.

---

## 🛠 CÔNG NGHỆ SỬ DỤNG (TECH STACK)
- **Frontend & Dashboard:** Streamlit, PyDeck (Bản đồ 3D), Altair (Biểu đồ tương tác).
- **Backend & GIS:** Geopandas, Shapely, Python.
- **Cơ sở Dữ liệu:** SQLite3.
- **Trí tuệ Nhân tạo (AI):** NeuralProphet (PyTorch backend).

---

## 🚀 HƯỚNG DẪN KHỞI ĐỘNG TỰ ĐỘNG

Chỉ với 1 cú click chuột, hệ thống sẽ tự thiết lập toàn bộ môi trường.

1. Giải nén toàn bộ thư mục này ra máy tính của bạn (đừng chạy trực tiếp trong file ZIP).
2. Tìm và nhấp đúp chuột (Double-click) vào file **`run.bat`** (Có biểu tượng hình bánh răng/cửa sổ đen).
3. **Quá trình tự động:**
   - Hệ thống sẽ tự động tạo Môi trường Ảo (Virtual Environment) và cài đặt toàn bộ thư viện cần thiết. 
   - **Vui lòng kiên nhẫn chờ 5-10 phút** ở lần khởi chạy đầu tiên.
4. **Hoàn tất:** Khi cài xong, hệ thống sẽ mở ra 2 thứ:
   - **Cửa sổ dòng lệnh đen:** Trạm thu thập dữ liệu Radar chạy ngầm (Không được tắt).
   - **Trình duyệt Web:** Tự động mở Giao diện Bảng điều khiển (Dashboard).

---

## 💻 HƯỚNG DẪN SỬ DỤNG GIAO DIỆN

- **Bản đồ Radar 3D:**
  - Dùng chuột trái: Kéo để di chuyển bản đồ.
  - Dùng chuột phải: Kéo lên/xuống để nghiêng bản đồ (xem góc độ không gian 3D).
  - Lăn chuột: Phóng to/Thu nhỏ.
  - Các cột sáng màu là máy bay thực tế đang nằm trong Phân khu.

- **Biểu đồ Dự Báo AI:**
  - Trên biểu đồ dự báo, bạn có thể **Lăn con lăn chuột** để zoom vào chi tiết, và **nhấn giữ chuột kéo** để xem các mốc lịch sử/tương lai khác.
  - Bạn có thể chuyển đổi chế độ thu thập Radar Thực tế hoặc Giả lập ở thanh Sidebar (Cột Trái).

---
*Dự án Nghiên cứu & Tốt nghiệp | Chúc bạn có một phiên bảo vệ xuất sắc trước Hội đồng!*
