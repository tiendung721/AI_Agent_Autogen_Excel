import os
import pandas as pd
import openai
from dotenv import load_dotenv
from openai import OpenAI
import sys
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INPUT_FILE = "output/final_report.xlsx"
OUTPUT_FILE = "output/final_report.txt"

def read_excel_summary(path):
    summaries = []
    xls = pd.ExcelFile(path)

    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        if "Phân loại" not in df.columns:
            continue

        sectioned = df.groupby("Phân loại")
        for section, data in sectioned:
            summaries.append(f" {sheet} – {section}:\n{data.drop(columns='Phân loại').head(10).to_markdown(index=False)}\n")

    return "\n".join(summaries)

def write_summary_to_gpt(text_summary):
    system_prompt = (
        "Bạn là chuyên gia báo cáo nội bộ. Dưới đây là dữ liệu tổng hợp từ một file Excel."
        "Hãy viết một báo cáo chuyên nghiệp, rõ ràng, chia theo mục: dừng lò, nhân viên, dự án, tiến độ..."
        "Báo cáo phải có tiêu đề, đoạn giới thiệu, từng mục tóm tắt ngắn gọn, chính xác và có kết luận cuối cùng."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_summary[:12000]},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()

def main():
    print(" CriticAgent: Đang đọc file Excel...")
    summary_text = read_excel_summary(INPUT_FILE)

    print(" CriticAgent: Đang yêu cầu GPT viết lại báo cáo...")
    final_report = write_summary_to_gpt(summary_text)

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_report)

    print(f" CriticAgent: Đã tạo báo cáo văn bản tại {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
