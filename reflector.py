import json
import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ANALYZED_FILE = "output/analyzed.json"
EXCEL_FILE = "output/final_report.xlsx"

def verify_excel_sheets():
    try:
        xl = pd.ExcelFile(EXCEL_FILE)
        sheets = xl.sheet_names
        assert "Tháng 2" in sheets and "Tháng 3" in sheets, "Thiếu sheet Tháng 2 hoặc Tháng 3 trong file Excel"
        return True, "✅ Excel có đủ 2 sheet Tháng 2 và Tháng 3"
    except Exception as e:
        return False, f" Lỗi Excel: {str(e)}"

def verify_analyzed_json():
    try:
        with open(ANALYZED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for month in ["Tháng 2", "Tháng 3"]:
            assert month in data, f"Thiếu dữ liệu {month} trong analyzed.json"
            for key in ["tong_thoi_gian_dung_lo", "so_cong_nhan_vien", "du_an_trong_thang", "so_sanh_tien_do"]:
                assert key in data[month], f"Thiếu mục {key} trong {month}"

        return True, "✅ analyzed.json đầy đủ và hợp lệ"
    except Exception as e:
        return False, f" Lỗi JSON: {str(e)}"

def main():
    print("🔎 ReflectiveAgent: Đang xác minh đầu ra...")

    os.makedirs("output", exist_ok=True)
    results = []

    success_excel, msg_excel = verify_excel_sheets()
    print(msg_excel)
    results.append(msg_excel)

    success_json, msg_json = verify_analyzed_json()
    print(msg_json)
    results.append(msg_json)

    verified = success_excel and success_json
    final = "✅ Kết quả cuối cùng: TẤT CẢ ĐẦU RA ĐẦY ĐỦ" if verified else " Kết quả cuối cùng: CẦN KIỂM TRA LẠI DỮ LIỆU"

    print(final)
    with open("output/verification.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results + [final]))

if __name__ == "__main__":
    main()
