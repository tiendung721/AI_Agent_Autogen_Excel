import pandas as pd
import json
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT_FILE = "data/2025 Báo cáo công việc.xlsx"
OUTPUT_FILE = "output/extracted.json"

sheet_config = {
    "Tháng 2": {
        "log": (6, 262),
        "summary": (263, 281),
        "plan": (282, 296)
    },
    "Tháng 3": {
        "log": (6, 283),
        "summary": (284, 298),
        "plan": (299, 315)
    }
}

expected_columns = ["Ngày", "Mô tả công việc", "Thời gian dừng lò", "Ghi chú"]

def extract_excel(filepath):
    xl = pd.ExcelFile(filepath)
    result = {}

    for sheet, bounds in sheet_config.items():
        data = {}

        # --- 1. Nhật ký công việc ---
        log_df = xl.parse(sheet_name=sheet,
                          skiprows=bounds["log"][0] - 1,
                          nrows=bounds["log"][1] - bounds["log"][0],
                          header=None)
        
        actual_cols = log_df.shape[1]
        if actual_cols < len(expected_columns):
            raise ValueError(f"[{sheet}] Nhật ký công việc thiếu cột (chỉ có {actual_cols})")

        log_df = log_df.iloc[:, :len(expected_columns)]
        log_df.columns = expected_columns
        log_df = log_df.dropna(how="all")

        # Chuyển thời gian dừng sang phút
        log_df["Thời gian dừng (phút)"] = pd.to_numeric(log_df["Thời gian dừng lò"], errors="coerce").fillna(0) * 60
        log_df = log_df.drop(columns=["Thời gian dừng lò"])

        data["log"] = log_df.to_dict(orient="records")

        # --- 2. Tổng hợp dự án làm trong tháng ---
        df_summary = xl.parse(sheet_name=sheet,
                              skiprows=bounds["summary"][0] - 1,
                              nrows=bounds["summary"][1] - bounds["summary"][0])
        df_summary.columns = df_summary.iloc[0].fillna("").astype(str).str.strip()
        df_summary = df_summary[1:].dropna(how="all").reset_index(drop=True)

        if "Dự án" in df_summary.columns:
            data["summary"] = df_summary["Dự án"].dropna().astype(str).tolist()
        else:
            data["summary"] = []

        # --- 3. Kế hoạch tháng sau ---
        df_plan = xl.parse(sheet_name=sheet,
                           skiprows=bounds["plan"][0] - 1,
                           nrows=bounds["plan"][1] - bounds["plan"][0])
        df_plan.columns = df_plan.iloc[0].fillna("").astype(str).str.strip()
        df_plan = df_plan[1:].dropna(how="all").reset_index(drop=True)

        if "Dự án" in df_plan.columns:
            data["plan"] = df_plan["Dự án"].dropna().astype(str).tolist()
        else:
            data["plan"] = []

        result[sheet] = data

    return result

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    data = extract_excel(INPUT_FILE)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f" ExtractorAgent: Đã trích xuất thành công vào {OUTPUT_FILE}")
