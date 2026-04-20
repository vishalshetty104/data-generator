import argparse
import time
from datetime import datetime
from typing import Dict, Any
from random import shuffle

from schema_parser import SchemaParser
from data_generator import DataGenerator
from quality_issues import QualityIssues
from output import BatchCSVWriter
from memory_utils import calculate_batch_size, get_system_info


def get_default_output_path():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return f"output/output_{timestamp}.csv"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Synthetic Data Generator with Data Quality Issues"
    )
    parser.add_argument(
        "--schema",
        required=True,
        help="Path to JSON schema file"
    )
    parser.add_argument(
        "--rows",
        required=True,
        type=int,
        help="Number of rows to generate"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output CSV file path (default: output/output_TIMESTAMP.csv)"
    )
    parser.add_argument(
        "--error-rate",
        type=float,
        default=0.1,
        help="Probability of data quality issues 0.0-1.0 (default: 0.1)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="Rows per batch (auto-detected if not specified)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress"
    )
    return parser.parse_args()


def generate_synthetic_data(
    schema_path: str,
    num_rows: int,
    output_path: str,
    error_rate: float,
    batch_size: int,
    verbose: bool = False
) -> Dict[str, Any]:
    parser = SchemaParser(schema_path)

    if not parser.load():
        raise ValueError(f"Failed to load schema: {parser.get_errors()}")

    if not parser.validate():
        raise ValueError(f"Invalid schema: {parser.get_errors()}")

    columns = parser.get_columns()
    data_gen = DataGenerator(columns)
    quality_issues = QualityIssues(error_rate)
    writer = BatchCSVWriter(output_path, batch_size)

    column_types = {col["name"]: col["type"] for col in columns}

    stats = {
        "total_rows": 0,
        "rows_with_issues": 0,
        "issue_counts": {}
    }

    writer.open()
    start_time = time.time()

    try:
        while stats["total_rows"] < num_rows:
            remaining = num_rows - stats["total_rows"]
            current_batch_size = min(batch_size, remaining)

            batch = list(data_gen.generate_rows(current_batch_size))

            if error_rate > 0 and error_rate * 0.15 > 0:
                dup_count = max(1, int(current_batch_size * error_rate * 0.05))
                dup_indices = list(range(current_batch_size))
                shuffle(dup_indices)
                dup_indices = dup_indices[:dup_count]
                batch = quality_issues.mark_duplicate_rows(batch, dup_indices)

            for row in batch:
                modified_row, issues = quality_issues.apply_issues(row, column_types)
                writer.write_row(modified_row)
                stats["total_rows"] += 1

                if issues:
                    stats["rows_with_issues"] += 1
                    for issue in issues:
                        issue_type = issue.split(":")[0]
                        stats["issue_counts"][issue_type] = stats["issue_counts"].get(issue_type, 0) + 1

            if verbose:
                elapsed = time.time() - start_time
                rate = stats["total_rows"] / elapsed if elapsed > 0 else 0
                print(f"Generated {stats['total_rows']:,}/{num_rows:,} rows "
                      f"({rate:.0f} rows/sec)")

    finally:
        writer.close()

    stats["elapsed_time"] = time.time() - start_time
    return stats


def main():
    args = parse_arguments()

    if args.error_rate < 0 or args.error_rate > 1:
        raise ValueError("--error-rate must be between 0.0 and 1.0")

    if args.rows <= 0:
        raise ValueError("--rows must be a positive integer")

    if args.output is None:
        args.output = get_default_output_path()

    if args.batch_size is None:
        args.batch_size = calculate_batch_size()

    if args.batch_size <= 0:
        raise ValueError("--batch-size must be a positive integer")

    if args.verbose:
        sys_info = get_system_info()
        print(f"Available memory: {sys_info['available_memory_mb']:.0f}MB")
        print(f"Suggested batch size: {sys_info['suggested_batch_size']:,}")
        print(f"Using batch size: {args.batch_size:,}")
        print(f"Generating {args.rows:,} rows with {args.error_rate:.1%} error rate")
        print("-" * 50)

    try:
        stats = generate_synthetic_data(
            schema_path=args.schema,
            num_rows=args.rows,
            output_path=args.output,
            error_rate=args.error_rate,
            batch_size=args.batch_size,
            verbose=args.verbose
        )

        if args.verbose:
            print("-" * 50)
            print(f"Completed in {stats['elapsed_time']:.2f} seconds")
            print(f"Output file: {args.output}")
            print(f"Total rows: {stats['total_rows']:,}")
            print(f"Rows with issues: {stats['rows_with_issues']:,}")
            if stats["issue_counts"]:
                print("Issue breakdown:")
                for issue_type, count in sorted(stats["issue_counts"].items()):
                    print(f"  {issue_type}: {count:,}")
        else:
            print(f"Generated {stats['total_rows']:,} rows -> {args.output}")

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
