import os
import sys
import time
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path


OUTPUT_DIR = Path("output")
REPORT_PATH = OUTPUT_DIR / "benchmark_report.md"

BENCHMARK_ROWS = 50000
ERROR_RATE = 0.1
MEMORY_PERCENTAGE = 5.0

SCHEMAS = [
    ("products", "schemas/products.json"),
    ("customers", "schemas/customers.json"),
    ("employees", "schemas/employees.json"),
    ("transactions", "schemas/transactions.json"),
    ("orders", "schemas/orders.json"),
]


def parse_verbose_output(output):
    data = {
        "batch_size": None,
        "total_rows": None,
        "rows_with_issues": None,
        "issue_breakdown": {},
        "rows_per_sec": None
    }

    lines = output.strip().split("\n")
    for line in lines:
        if "Using batch size:" in line:
            num = re.search(r"[\d,]+", line)
            if num:
                data["batch_size"] = int(num.group().replace(",", ""))

        if "rows with issues:" in line.lower():
            num = re.search(r"[\d,]+", line)
            if num:
                data["rows_with_issues"] = int(num.group().replace(",", ""))

        if "format:" in line.lower():
            nums = re.findall(r"[\d,]+", line)
            if nums:
                data["issue_breakdown"]["format"] = int(nums[-1].replace(",", ""))

        if "invalid:" in line.lower():
            nums = re.findall(r"[\d,]+", line)
            if nums:
                data["issue_breakdown"]["invalid"] = int(nums[-1].replace(",", ""))

        if "missing:" in line.lower():
            nums = re.findall(r"[\d,]+", line)
            if nums:
                data["issue_breakdown"]["missing"] = int(nums[-1].replace(",", ""))

        if "rows/sec" in line:
            match = re.search(r"\(([\d,]+)\s*rows/sec\)", line)
            if match:
                data["rows_per_sec"] = float(match.group(1).replace(",", ""))

    return data


def run_benchmark(schema_name, schema_path):
    print(f"  Benchmarking {schema_name}...", end=" ", flush=True)

    start_time = time.time()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"benchmark_{schema_name}_{timestamp}.csv"

    with open(schema_path) as f:
        schema = json.load(f)
        num_columns = len(schema["columns"])

    cmd = [
        sys.executable, "src/generator.py",
        "--schema", schema_path,
        "--rows", str(BENCHMARK_ROWS),
        "--output", str(output_path),
        "--error-rate", str(ERROR_RATE),
        "--memory-percentage", str(MEMORY_PERCENTAGE),
        "--verbose"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start_time

    if result.returncode != 0:
        print(f"FAILED\n{result.stderr}")
        return None

    parsed = parse_verbose_output(result.stdout)
    csv_size_mb = output_path.stat().st_size / (1024 * 1024)

    print(f"{parsed.get('rows_per_sec', 0):,.0f} rows/sec")

    return {
        "schema_name": schema_name,
        "num_columns": num_columns,
        "batch_size": parsed.get("batch_size"),
        "total_time_sec": round(elapsed, 2),
        "rows_per_sec": parsed.get("rows_per_sec", 0),
        "csv_size_mb": round(csv_size_mb, 2),
        "rows_with_issues": parsed.get("rows_with_issues", 0),
        "issue_breakdown": parsed.get("issue_breakdown", {}),
        "output_path": str(output_path),
    }


def generate_report(results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    valid_results = [r for r in results if r is not None]

    fastest = max(valid_results, key=lambda x: x["rows_per_sec"])
    slowest = min(valid_results, key=lambda x: x["rows_per_sec"])
    largest_csv = max(valid_results, key=lambda x: x["csv_size_mb"])
    smallest_csv = min(valid_results, key=lambda x: x["csv_size_mb"])

    col_range_min = min(r["num_columns"] for r in valid_results if r["num_columns"])
    col_range_max = max(r["num_columns"] for r in valid_results if r["num_columns"])

    lines = [
        f"# Performance Benchmark Report",
        f"",
        f"**Generated:** {timestamp}",
        f"",
        f"## Configuration",
        f"",
        f"| Parameter | Value |",
        f"|-----------|-------|",
        f"| Rows per schema | {BENCHMARK_ROWS:,} |",
        f"| Error rate | {ERROR_RATE:.1%} |",
        f"| Memory percentage | {MEMORY_PERCENTAGE:.1f}% |",
        f"",
        f"## Summary",
        f"",
        f"| Schema | Time (sec) | Rows/sec | CSV Size (MB) |",
        f"|--------|------------|----------|---------------|",
    ]

    for r in sorted(valid_results, key=lambda x: x["rows_per_sec"], reverse=True):
        lines.append(
            f"| {r['schema_name']} | {r['total_time_sec']} | {r['rows_per_sec']:,.0f} | {r['csv_size_mb']:.2f} |"
        )

    lines.extend([
        f"",
        f"## Insights",
        f"",
        f"- **Fastest:** {fastest['schema_name']} ({fastest['rows_per_sec']:,.0f} rows/sec)",
        f"- **Slowest:** {slowest['schema_name']} ({slowest['rows_per_sec']:,.0f} rows/sec)",
        f"- **Largest CSV:** {largest_csv['schema_name']} ({largest_csv['csv_size_mb']:.2f} MB)",
        f"- **Smallest CSV:** {smallest_csv['schema_name']} ({smallest_csv['csv_size_mb']:.2f} MB)",
        f"- **Column range:** {col_range_min} to {col_range_max} columns",
        f"",
        f"## Issue Breakdown",
        f"",
    ])

    for r in sorted(valid_results, key=lambda x: x["schema_name"]):
        issue_str = ", ".join([f"{k}: {v}" for k, v in r["issue_breakdown"].items()]) if r["issue_breakdown"] else "none"
        lines.append(f"- **{r['schema_name']}:** {issue_str}")

    lines.extend([
        f"",
        f"## Output Files",
        f"",
    ])

    for r in sorted(valid_results, key=lambda x: x["schema_name"]):
        lines.append(f"- `{r['output_path']}`")

    return "\n".join(lines)


def main():
    print("=" * 60)
    print("Synthetic Data Generator - Performance Benchmark")
    print("=" * 60)
    print(f"Rows per schema: {BENCHMARK_ROWS:,}")
    print(f"Error rate: {ERROR_RATE:.1%}")
    print(f"Memory percentage: {MEMORY_PERCENTAGE:.1f}%")
    print("-" * 60)

    OUTPUT_DIR.mkdir(exist_ok=True)

    results = []
    for schema_name, schema_path in SCHEMAS:
        result = run_benchmark(schema_name, schema_path)
        results.append(result)

    print("-" * 60)
    print("Generating report...")

    report = generate_report(results)
    with open(REPORT_PATH, "w") as f:
        f.write(report)

    print(f"Report saved to: {REPORT_PATH}")

    print("\n" + "=" * 60)
    print("Benchmark Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
