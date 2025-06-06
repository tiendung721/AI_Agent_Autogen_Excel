import json
import pandas as pd
import os
import sys  
sys.stdout.reconfigure(encoding="utf-8")

INPUT_FILE = "output/analyzed.json"
OUTPUT_FILE = "output/final_report.xlsx"

def main():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs("output", exist_ok=True)
    writer = pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl")

    for month in data:
        month_data = data[month]
        frames = []

        # 1. Thời gian dừng lò
        dung_lo_df = pd.DataFrame([
            {"Lò": lo, "Tổng thời gian dừng (phút)": time}
            for lo, time in month_data["tong_thoi_gian_dung_lo"].items()
        ])
        dung_lo_df.insert(0, "Phân loại", "Dừng lò")
        frames.append(dung_lo_df)

        # 2. Công nhân viên
        cong_nv_df = pd.DataFrame([
            {"Nhân viên": nv, "Số công": cong}
            for nv, cong in month_data["so_cong_nhan_vien"].items()
        ])
        cong_nv_df.insert(0, "Phân loại", "Nhân sự")
        frames.append(cong_nv_df)

        # 3. Dự án trong tháng
        duan_df = pd.DataFrame({"Dự án": month_data["du_an_trong_thang"]})
        duan_df.insert(0, "Phân loại", "Dự án thực hiện")
        frames.append(duan_df)

        # 4. So sánh tiến độ
        so_sanh = month_data.get("so_sanh_tien_do", {})
        tien_do = []
        for label, info in so_sanh.items():
            if not isinstance(info, dict):
                continue
            for ke_hoach in info.get("Tiến độ kế hoạch", {}):
                if ke_hoach.strip():
                    tien_do.append({
                        "Phân loại": "Kế hoạch",
                        "Dự án": ke_hoach.strip()
                    })
            for thuc_te in info.get("Thực tế hoàn thành", {}):
                if thuc_te.strip():
                    tien_do.append({
                        "Phân loại": "Thực tế",
                        "Dự án": thuc_te.strip()
                    })

        # 5. Dự án không theo đuổi
        not_pursued = pd.DataFrame({"Dự án": month_data["du_an_khong_theo_duoi"]})
        if not not_pursued.empty:
            not_pursued.insert(0, "Phân loại", "Không theo đuổi")
            frames.append(not_pursued)

        # 6. Dự án không báo cáo lại
        not_reported = pd.DataFrame({"Dự án": month_data["du_an_khong_bao_cao_lai"]})
        if not not_reported.empty:
            not_reported.insert(0, "Phân loại", "Không báo cáo")
            frames.append(not_reported)

        # Gộp tất cả và ghi ra Excel
        final_df = pd.concat(frames, ignore_index=True)
        final_df.to_excel(writer, sheet_name=month, index=False)

    writer.close()
    print(f" PlannerAgent: Đã tạo báo cáo tại {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
