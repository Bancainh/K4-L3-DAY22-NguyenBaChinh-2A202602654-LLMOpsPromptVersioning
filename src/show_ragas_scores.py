"""In bảng so sánh từ báo cáo RAGAS đã lưu để kiểm tra và chụp evidence."""

import json
import math
from pathlib import Path


REPORT = Path(__file__).parent.parent / "data" / "ragas_report.json"
METRICS = ("faithfulness", "answer_relevancy", "context_recall", "context_precision")


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    v1 = report["prompt_v1_scores"]
    v2 = report["prompt_v2_scores"]

    print("Day 22 - RAGAS Evaluation (50 QA pairs per prompt)")
    print("Source: data/ragas_report.json")
    print("=" * 64)
    print(f"  {'Metric':30s} {'V1':>8s} {'V2':>8s}  Winner")
    print("=" * 64)
    for metric in METRICS:
        score1, score2 = float(v1[metric]), float(v2[metric])
        if not math.isfinite(score1) or not math.isfinite(score2):
            raise ValueError(f"Diem khong hop le: {metric}")
        winner = "V1" if score1 > score2 else "V2" if score2 > score1 else "Tie"
        print(f"  {metric:30s} {score1:8.4f} {score2:8.4f}  {winner}")
    print("=" * 64)
    print("Faithfulness >= 0.8:", "PASS" if report["target_met"] else "FAIL")


if __name__ == "__main__":
    main()
