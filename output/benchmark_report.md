# Performance Benchmark Report

**Generated:** 2026-04-20 15:09:29

## Configuration

| Parameter | Value |
|-----------|-------|
| Rows per schema | 50,000 |
| Error rate | 10.0% |
| Memory percentage | 5.0% |

## Summary

| Schema | Time (sec) | Rows/sec | CSV Size (MB) |
|--------|------------|----------|---------------|
| transactions | 1.12 | 57,789 | 5.07 |
| orders | 1.78 | 32,937 | 5.07 |
| products | 1.99 | 31,338 | 22.20 |
| customers | 9.03 | 5,732 | 11.50 |
| employees | 9.8 | 5,266 | 8.49 |

## Insights

- **Fastest:** transactions (57,789 rows/sec)
- **Slowest:** employees (5,266 rows/sec)
- **Largest CSV:** products (22.20 MB)
- **Smallest CSV:** transactions (5.07 MB)
- **Column range:** 11 to 15 columns

## Issue Breakdown

- **customers:** format: 152, invalid: 1242, missing: 1444
- **employees:** format: 198, invalid: 1255, missing: 1535
- **orders:** format: 167, invalid: 1274, missing: 1530
- **products:** format: 44, invalid: 1241, missing: 1538
- **transactions:** format: 75, invalid: 1212, missing: 1494

## Output Files

- `output\benchmark_customers_20260420_150907.csv`
- `output\benchmark_employees_20260420_150916.csv`
- `output\benchmark_orders_20260420_150927.csv`
- `output\benchmark_products_20260420_150905.csv`
- `output\benchmark_transactions_20260420_150926.csv`