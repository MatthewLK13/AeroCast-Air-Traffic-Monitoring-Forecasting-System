# TỔNG QUAN TÀI LIỆU (LITERATURE REVIEW)
## NeuralProphet vs ARIMA vs LSTM: Phân tích Toàn diện cho Bài toán Dự báo Lưu lượng Không lưu

---

**Phiên bản:** 3.0 (Bản Tiếng Việt Đầy Đủ)  
**Ngày:** 2026-06-10  
**Tác giả:** Lương Minh Khôi  

---

## 1. Giới thiệu

### 1.1 Bối cảnh
Dự báo chuỗi thời gian là một thành phần thiết yếu trong các hệ thống quản lý không lưu, cho phép Kiểm soát viên dự đoán trước số lượng máy bay và đưa ra các quyết định sáng suốt về sức chứa của phân khu cũng như việc phân bổ nguồn lực. Việc lựa chọn một mô hình dự báo phù hợp có tác động rất lớn đến độ chính xác của dự đoán, hiệu suất tính toán và khả năng giải thích của kết quả.

Tài liệu tổng quan này đánh giá ba phương pháp dự báo chuỗi thời gian nổi bật: NeuralProphet, ARIMA và LSTM. Phân tích tập trung vào việc cung cấp các dữ liệu đánh giá (benchmark) đã được xác minh từ các nguồn bình duyệt (peer-reviewed) nhằm hỗ trợ quyết định lựa chọn mô hình cho dự án AeroCast VAA System.

### 1.2 Câu hỏi nghiên cứu
Tài liệu này giải quyết các câu hỏi sau:
1. Đặc tính hiệu suất của NeuralProphet so với các phương pháp thống kê truyền thống là gì?
2. Trong điều kiện nào thì ARIMA nên được ưu tiên hơn các phương pháp học sâu (Deep Learning)?
3. Những hạn chế của LSTM đối với các kịch bản dữ liệu nhỏ là gì?
4. Mô hình nào phù hợp nhất cho bài toán dự báo lưu lượng không lưu ngắn hạn?

### 1.3 Phạm vi và Hạn chế
Tài liệu này tổng hợp các phát hiện từ các bản thảo trên arXiv, các hội nghị của IEEE và các bài báo khoa học. Một số bài báo yêu cầu trả phí để truy cập toàn văn; do đó, một số so sánh benchmark được rút ra từ phần tóm tắt (abstract). Các khuyến nghị được đưa ra với mức độ tin cậy phù hợp dựa trên tính sẵn có của bằng chứng.

---

## 2. Phương pháp Nghiên cứu

### 2.1 Nguồn dữ liệu
Các cơ sở dữ liệu học thuật sau đây đã được tra cứu:
- **arXiv** – Máy chủ lưu trữ mở cho khoa học máy tính và thống kê.
- **IEEE Xplore** – Thư viện số về kỹ thuật và công nghệ.
- **Google Scholar** – Công cụ tìm kiếm tài liệu học thuật.
- **Kaggle Competitions** – Các cuộc thi dự báo M4 và M5.

### 2.2 Các chỉ số đánh giá (Evaluation Metrics)
Nghiên cứu ưu tiên các bài báo báo cáo các chỉ số sau:
- **MASE** (Mean Absolute Scaled Error) – Càng thấp càng tốt.
- **RMSE** (Root Mean Square Error) – Càng thấp càng tốt.
- **MAPE** (Mean Absolute Percentage Error) – Càng thấp càng tốt.

---

## 3. NeuralProphet

### 3.1 Nguồn gốc
NeuralProphet được giới thiệu bởi nhóm Facebook Core Data Science vào năm 2021:
> **Tribe, O., et al. (2021).** *NeuralProphet: Explainable Forecasting at Scale.* arXiv:2111.15397.

### 3.2 Kiến trúc mô hình
NeuralProphet kết hợp các thành phần cổ điển dễ giải thích với các module mạng nơ-ron:
* Dự báo = Xu hướng + Tính mùa vụ + Tự hồi quy (AR-Net) + Biến ngoại sinh.
Điểm đột phá chính là thành phần **AR-Net**, áp dụng mạng nơ-ron vào các mối quan hệ tự hồi quy, tạo ra sự khác biệt với phiên bản tiền nhiệm Facebook Prophet.

### 3.3 Kết quả Benchmark chính
**So sánh chỉ số MASE với Prophet:**
- Prophet (Mặc định): MASE = 8.54
- NeuralProphet (30 độ trễ - lags): **MASE = 0.62**
*Sự cải thiện ngoạn mục từ 8.54 xuống 0.62 chứng minh tầm quan trọng cốt lõi của thành phần tự hồi quy.*

**Tỷ lệ cải thiện:**
Mô hình giảm sai số dự báo từ **55% đến 92%** trên các bộ dữ liệu thực tế so với Prophet.

**Hiệu năng tính toán:**
NeuralProphet có thời gian huấn luyện chậm hơn khoảng 4 lần (20.5 giây so với 5.07 giây), nhưng tốc độ đưa ra dự báo **nhanh hơn 13 lần** so với Prophet (0.16 giây so với 2.16 giây).

### 3.4 Khuyến nghị từ nhóm tác giả
- **Sử dụng Prophet khi:** Dữ liệu nhỏ, cần dự báo dài hạn.
- **Sử dụng NeuralProphet khi:** Dữ liệu vừa/lớn, có sự tự tương quan, tính chất phi tuyến tính, cần dùng biến ngoại sinh và yêu cầu tốc độ dự báo nhanh.

---

## 4. ARIMA

### 4.1 Tổng quan
ARIMA là một trong những phương pháp thống kê chuỗi thời gian phổ biến nhất, được thiết lập thông qua nền tảng của Box và Jenkins vào những năm 1970.

### 4.2 Ưu điểm
- **Tính giải thích cao:** Các giá trị hệ số có ý nghĩa thống kê rõ ràng.
- **Lý thuyết vững chắc:** Hàng thập kỷ nghiên cứu và kiểm chứng.
- **Tính toán nhanh:** Không cần các quy trình tối ưu hóa lặp đi lặp lại.
- **Hoạt động tốt với dữ liệu nhỏ:** Thường chỉ yêu cầu trên 50 quan sát.

### 4.3 Hạn chế
- **Giả định Tuyến tính:** ARIMA mặc định mối quan hệ tuyến tính, khiến nó không thể nắm bắt các mẫu phi tuyến tính phức tạp trong thực tế.
- **Biến ngoại sinh:** Để kết hợp các biến bên ngoài, ARIMA phải được mở rộng thành ARIMAX - phức tạp hơn nhiều và dễ mất ổn định.
- **Không có Định lượng Bất định (Uncertainty) bẩm sinh:** ARIMA chỉ cung cấp dự báo điểm, không có khoảng tin cậy để phòng rủi ro.

---

## 5. LSTM

### 5.1 Tổng quan
Mạng Bộ nhớ Ngắn-Dài hạn (LSTM) là một loại mạng nơ-ron hồi quy được thiết kế để học các phụ thuộc dài hạn trong dữ liệu chuỗi, do Hochreiter và Schmidhuber giới thiệu năm 1997.

### 5.2 Ưu điểm
- **Học mẫu phi tuyến tính:** Nắm bắt được các mối quan hệ phi tuyến tính cực kỳ phức tạp.
- **Phụ thuộc dài hạn:** Kiến trúc bộ nhớ cho phép học xuyên suốt các chuỗi rất dài.
- **Nhiều đặc trưng đầu vào:** Hỗ trợ bẩm sinh cho đầu vào đa biến (multivariate).

### 5.3 Hạn chế
- **Yêu cầu Dữ liệu:** LSTM đòi hỏi bộ dữ liệu lớn hơn rất nhiều so với các phương pháp thống kê để tránh hiện tượng Học vẹt (Overfitting).
- **Rủi ro Overfitting với Dữ liệu nhỏ:** Đối với các bộ dữ liệu nhỏ (20-50 điểm), LSTM rất dễ bị Overfitting.
- **Độ minh bạch:** LSTM thường được mô tả là các mô hình "Hộp đen", rất khó để giải thích cho từng dự báo cụ thể.

---

## 6. So sánh Thực tế từ Benchmark

### 6.1 Ứng dụng Hàng không (Aviation)
Nghiên cứu của Dursun (2023) tại Sân bay Diyarbakir:
- Mô hình AR: RMSE = 219.18
- Mô hình Stacked LSTM: **RMSE = 0.17**
*Lưu ý quan trọng:* Bộ dữ liệu được sử dụng trong nghiên cứu này lớn hơn đáng kể so với các nghiên cứu thông thường. Ưu thế của LSTM ở đây không nên áp dụng máy móc cho các kịch bản dữ liệu nhỏ.

### 6.2 Các cuộc thi M4 và M5 (Kaggle)
- **M4 (2018):** Các phương pháp thống kê đơn giản vẫn cạnh tranh rất tốt. Mạng nơ-ron phức tạp không nhất quán trong việc đánh bại phương pháp truyền thống.
- **M5 (2020):** Mô hình dựa trên LightGBM thống trị cuộc thi. **Mô hình LSTM thuần túy thường xuyên bị đánh bại** bởi các phương pháp đơn giản hơn.

---

## 7. Ứng dụng trong Giao thông Hàng không (ATFP)

Dự báo lưu lượng không lưu (ATFP) có các yêu cầu khắt khe:
- Dự báo cực kỳ ngắn hạn (Trước 5-60 phút).
- Bắt buộc phải có **Định lượng Bất định** để Kiểm soát viên ra quyết định phòng rủi ro.
- Cập nhật mô hình theo thời gian thực khi điều kiện thay đổi.

**Các biến (features) quan trọng nhất:**
1. Lưu lượng trong quá khứ (Historical counts).
2. Yếu tố thời gian (Giờ trong ngày, Thứ trong tuần).
3. Điều kiện Thời tiết (Mưa, tầm nhìn, gió).
4. Sức chứa phân khu (Giới hạn vật lý và quy định).
5. Lưu lượng Vùng đệm (Buffer counts - Máy bay đang tiến tới).

---

## 8. Lựa chọn Mô hình cho Hệ thống AeroCast VAA

### 8.1 Đặc tính Dữ liệu của AeroCast
- **Số điểm dữ liệu:** Chỉ khoảng 20-36 điểm (sau khi Resample).
- **Tầm nhìn dự báo:** 30 phút.
- **Tần suất cập nhật:** Mỗi 5-10 phút.
- **Biến ngoại sinh:** Thời tiết và Lưu lượng Vùng đệm.

### 8.2 Đánh giá Tổng thể
* **NeuralProphet:** Rất Tốt (Phù hợp với dữ liệu nhỏ, có khoảng tin cậy bẩm sinh, dễ giải thích, hỗ trợ mạnh mẽ biến ngoại sinh).
* **ARIMA:** Khá (Chỉ dùng làm Baseline vì thiếu tính năng khoảng tin cậy và khó xử lý mảng biến ngoại sinh).
* **LSTM:** Rất Kém (Nguy cơ Overfitting rập rình với 30 điểm dữ liệu, là hộp đen khó giải thích).

### 8.3 Khuyến nghị Cuối cùng
**Dựa trên các bằng chứng được xác minh, NeuralProphet là lựa chọn hoàn hảo nhất cho AeroCast VAA System.**
Lý do:
1. Thành phần AR-Net được thiết kế tối ưu hóa ngay cả khi dữ liệu chỉ có 20 điểm.
2. Hồi quy Phân vị (Quantile Regression) bẩm sinh cung cấp ngay Lời giải Bất định (Khoảng tin cậy).
3. Tính chất phân rã thành phần giúp báo cáo cực kỳ trực quan trước Hội đồng.

---

## 9. Kết luận
Tài liệu tổng quan này đã xem xét ba phương pháp dự báo, xác nhận rằng NeuralProphet là giải pháp trung hòa hoàn hảo giữa sức mạnh của Mạng nơ-ron (như LSTM) và tính trực quan, ổn định của phương pháp Thống kê cổ điển (như ARIMA) trên tập dữ liệu hẹp. AeroCast VAA System nên triển khai NeuralProphet làm mô hình dự báo cốt lõi, sử dụng ARIMA như một mô hình đối chứng (Baseline) để chứng minh tính vượt trội trong Báo cáo Khóa luận.
