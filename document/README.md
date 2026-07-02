# Tài liệu tham khảo đồ án — AeroCast VAA System

Folder này chứa **tài liệu tham khảo, bản nháp, hình ảnh** phục vụ đồ án. **Không cần thiết** cho việc chạy ứng dụng (chỉ cần `app.py`, `collector2.py`, `requirements.txt`, `flight_data.db`, `vn.json`, `run.bat`, `chương3.docx`, `chương4.docx` ở root).

## Cấu trúc

```
document/
├── literature/         # Bài literature review + báo cáo (LaTeX/Markdown/DOCX)
│   ├── Literature_Review.md          # bản gốc tiếng Anh
│   ├── Literature_Review_VN.md       # bản dịch tiếng Việt
│   ├── Literature_Review_LaTeX.md    # nguồn cho main.tex
│   ├── Literature_Review_HocThuat.docx
│   ├── Comparative_Analysis.md       # so sánh các mô hình time-series
│   ├── Report.docx                   # báo cáo tiến độ
│   ├── main.tex                      # LaTeX tiếng Anh
│   └── main_VN.tex                   # LaTeX tiếng Việt
│
├── chapters-archive/   # Bản cũ chương 3 + chương 4 (đã có bản mới ở root)
│   ├── Chương3.docx
│   └── chương4.docx
│
├── maps/               # Bản đồ Việt Nam dùng cho Phân khu 2
│   ├── bản đồ phân khu.pdf
│   ├── VN boundary.pdf
│   └── Ảnh chụp Màn hình 2026-05-16 lúc 00.17.59.png
│
├── figures/            # Hình ảnh minh họa cho báo cáo (giữ nguyên cấu trúc cũ)
├── spec/               # Đặc tả kỹ thuật, yêu cầu phi chức năng
└── scripts/            # Script build/convert LaTeX → DOCX
```

## File ở root (không thuộc document/)

- `chương3.docx` — bản **mới** đã viết lại với giải thích A→Z, dùng nộp đồ án
- `chương4.docx` — bản **mới** đã viết lại với giải thích A→Z, dùng nộp đồ án
- Bản cũ lưu trong `document/chapters-archive/` chỉ để tham khảo lịch sử sửa đổi

## Ghi chú

- Folder này có thể xoá khi đóng gói RAR nếu muốn gọn (chỉ giữ root code + 2 file docx)
- Hình trong `maps/` được tham chiếu bởi `chương3.docx` (phần Phân khu 2)
