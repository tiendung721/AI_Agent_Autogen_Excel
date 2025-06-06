# AI Agent  - Phân tích báo cáo công việc theo tháng
🧠 Mục tiêu chương trình
Hệ thống AI Agent được thiết kế để tự động đọc và phân tích file Excel chứa nhật ký công việc theo tháng, sau đó:

Trích xuất dữ liệu thô từ từng sheet

Phân tích các yếu tố chính: dừng lò, nhân sự, dự án

Xuất file báo cáo tổng hợp (.xlsx) và báo cáo văn bản (.txt)

Kiểm tra độ đầy đủ và chính xác đầu ra

🗂️ Cấu trúc thư mục
css
Sao chép
Chỉnh sửa
.
├── data/
│   └── 2025 Báo cáo công việc.xlsx     # File Excel gốc
├── output/
│   ├── extracted.json                  # Dữ liệu trích xuất từ Excel
│   ├── analyzed.json                   # Dữ liệu sau phân tích
│   ├── final_report.xlsx               # File báo cáo tổng hợp dạng Excel
│   ├── final_report.txt                # Báo cáo văn bản do GPT viết lại
│   └── verification.txt                # Kết quả kiểm chứng cuối cùng
├── extractor.py                        # Agent trích xuất dữ liệu
├── analyzer.py                         # Agent phân tích dữ liệu
├── planner.py                          # Agent lập báo cáo Excel
├── critic.py                           # Agent tạo báo cáo văn bản với GPT
├── reflector.py                        # Agent kiểm chứng đầu ra
└── main1.py                            # Pipeline chạy toàn bộ agent
🔁 Luồng hoạt động (Pipeline)
Chương trình được điều phối theo thứ tự sau:

Agent	Tác vụ chính
ExtractorAgent	Trích xuất dữ liệu từ file Excel vào extracted.json
AnalyzerAgent	Phân tích dữ liệu để tạo analyzed.json: thời gian dừng lò, công nhân viên, dự án
PlannerAgent	Tạo file final_report.xlsx gồm các sheet "Tháng 2", "Tháng 3"
CriticAgent	Gửi tóm tắt dữ liệu cho GPT viết lại báo cáo văn bản trong final_report.txt
ReflectiveAgent	Kiểm chứng tính đầy đủ và chính xác của analyzed.json và final_report.xlsx

▶️ Cách chạy chương trình
bash
Sao chép
Chỉnh sửa
python main1.py
Hệ thống sẽ lần lượt chạy từng agent, xuất tiến trình và lưu đầu ra tương ứng trong thư mục output/.

📌 Chi tiết các file output
extracted.json: gồm nhật ký, dự án tổng hợp, kế hoạch tháng tới cho mỗi sheet.

analyzed.json: tổng hợp kết quả phân tích, gồm:

Thời gian dừng lò

Số công của từng nhân viên

Dự án thực hiện trong tháng

So sánh tiến độ thực tế với kế hoạch

Dự án không theo đuổi hoặc không thấy báo cáo lại

final_report.xlsx: báo cáo định dạng bảng với phân loại từng mục

final_report.txt: báo cáo chuyên nghiệp do GPT viết lại

verification.txt: xác nhận có đủ sheet và mục dữ liệu quan trọng không

✅ Yêu cầu thư viện
bash
Sao chép
Chỉnh sửa
pip install pandas openpyxl python-dotenv openai
Lưu ý: Nếu dùng openai>=1.0, phải cập nhật các đoạn gọi GPT theo API mới.

🧩 Cấu hình .env (nếu dùng GPT)
ini
Sao chép
Chỉnh sửa
OPENAI_API_KEY=sk-...
