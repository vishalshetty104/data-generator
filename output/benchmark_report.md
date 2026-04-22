# Performance Benchmark Report

**Generated:** 2026-04-22 20:38:10

## Configuration

| Parameter | Value |
|-----------|-------|
| Rows per schema | 50,000 |
| Error rate | 10.0% |
| Memory percentage | 5.0% |

## Summary

| Schema | Time (sec) | Rows/sec | CSV Size (MB) |
|--------|------------|----------|---------------|
| transactions | 1.1 | 58,863 | 5.07 |
| orders | 1.82 | 32,161 | 5.07 |
| products | 1.99 | 31,751 | 22.20 |
| customers | 8.91 | 5,816 | 11.49 |
| employees | 9.2 | 5,619 | 8.49 |

## Insights

- **Fastest:** transactions (58,863 rows/sec)
- **Slowest:** employees (5,619 rows/sec)
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

- `output\benchmark_customers_20260422_203749.csv`
- `output\benchmark_employees_20260422_203758.csv`
- `output\benchmark_orders_20260422_203809.csv`
- `output\benchmark_products_20260422_203747.csv`
- `output\benchmark_transactions_20260422_203808.csv`