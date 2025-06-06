import json
import re
import os
import pandas as pd
from collections import defaultdict, Counter
import sys
sys.stdout.reconfigure(encoding="utf-8")

INPUT_FILE = "output/extracted.json"
OUTPUT_FILE = "output/analyzed.json"

def extract_lo(reason_text):
    return re.findall(r"lò\s*\d+", str(reason_text).lower())

def extract_people(desc):
    # Tách từ có chữ cái in hoa và không phải là từ mô tả
    return re.findall(r"\b[A-ZĐ][a-záàảãạăâđêôơưýỳỷỹỵếễệéèẻẽẹ]+", desc)

KNOWN_NAMES = [
    "Bình", "Toản", "Tải", "Hưng", "Sơn", "Thái", "Tuấn", "Long", "Thảo",
    "Hoàn", "Hải", "Nam", "Hùng", "Đạt", "Hiếu", "Phong", "Lâm", "Tiến"
]

def extract_names(text):
    """Tách tên nhân viên từ mô tả công việc dựa trên whitelist."""
    if not isinstance(text, str):
        return []
    names_found = []
    for name in KNOWN_NAMES:
        if re.search(rf"\b{name}\b", text):
            names_found.append(name)
    return names_found

def analyze_log(log_rows):
    tong_thoi_gian = {}
    so_cong = {}

    for row in log_rows:
        ly_do = str(row.get("Mô tả công việc", "")).strip()
        ghi_chu = str(row.get("Ghi chú", "")).strip()
        tg_dung = float(row.get("Thời gian dừng (phút)", 0))

        los = extract_lo(ghi_chu) or extract_lo(ly_do)
        for lo in los:
            tong_thoi_gian[lo] = tong_thoi_gian.get(lo, 0) + tg_dung

        for name in extract_names(ly_do):
            so_cong[name] = so_cong.get(name, 0) + 1

    return tong_thoi_gian, so_cong

def analyze_du_an(summary):
    return sorted({row.strip() for row in summary if row.strip()})

def so_sanh_tien_do(summary, plan):
    plan_set = set(plan)
    summary_set = set(summary)
    return {
        "Tiến độ kế hoạch": len(plan_set),
        "Thực tế hoàn thành": len(summary_set)
    }

def du_an_khong_theo_duoi(plan, summary):
    return sorted(list(set(plan) - set(summary)))

def du_an_khong_bao_cao_lai(plan, summary):
    return sorted(list(set(summary) - set(plan)))

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    output = {}
    for sheet, content in raw_data.items():
        log = content.get("log", [])
        summary = content.get("summary", [])
        plan = content.get("plan", [])

        tong_dung_lo, so_cong = analyze_log(log)
        du_an = analyze_du_an(summary)

        output[sheet] = {
            "tong_thoi_gian_dung_lo": tong_dung_lo,
            "so_cong_nhan_vien": so_cong,
            "du_an_trong_thang": du_an,
            "so_sanh_tien_do": so_sanh_tien_do(summary, plan),
            "du_an_khong_theo_duoi": du_an_khong_theo_duoi(plan, summary),
            "du_an_khong_bao_cao_lai": du_an_khong_bao_cao_lai(summary, plan)
        }

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f" AnalyzerAgent: Đã phân tích thành công và lưu vào {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
