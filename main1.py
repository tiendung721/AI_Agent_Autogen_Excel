import subprocess
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Danh sách các agent theo thứ tự pipeline
PIPELINE = [
    ("ExtractorAgent", "extractor.py"),
    ("AnalyzerAgent", "analyzer.py"),
    ("PlannerAgent", "planner.py"),
    ("CriticAgent", "critic.py"),
    ("ReflectiveAgent", "reflector.py")
]

def run_agent(name, script):
    print(f"\n Đang chạy {name} ({script})...")
    try:
        result = subprocess.run(["python", script], check=True, capture_output=True, text=True,  encoding="utf-8")
        print(f" {name} hoàn tất.\n--- Output ---\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f" {name} thất bại.\n--- STDOUT ---\n{e.stdout}\n--- STDERR ---\n{e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    print(" Bắt đầu chạy pipeline AI Agent...\n")
    for name, script in PIPELINE:
        run_agent(name, script)
    print("\n Tất cả agent đã hoàn thành.")
