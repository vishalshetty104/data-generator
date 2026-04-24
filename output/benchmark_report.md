# Performance Benchmark Report

**Generated:** 2026-04-22 21:41:51

## Configuration

| Parameter | Value |
|-----------|-------|
| Rows per schema | 50,000 |
| Error rate | 10.0% |
| Memory percentage | 5.0% |

## Summary

| Schema | Time (sec) | Rows/sec | CSV Size (MB) |
|--------|------------|----------|---------------|
| transactions | 1.06 | 60,460 | 5.07 |
| orders | 1.72 | 33,943 | 5.07 |
| products | 1.92 | 32,748 | 22.19 |
| customers | 8.72 | 5,928 | 11.50 |
| employees | 9.28 | 5,555 | 8.49 |

## Insights

- **Fastest:** transactions (60,460 rows/sec)
- **Slowest:** employees (5,555 rows/sec)
- **Largest CSV:** products (22.19 MB)
- **Smallest CSV:** transactions (5.07 MB)
- **Column range:** 11 to 15 columns

## Issue Breakdown

- **customers:** format: 152, invalid: 1242, missing: 1444
- **employees:** format: 198, invalid: 1255, missing: 1535
- **orders:** format: 167, invalid: 1274, missing: 1530
- **products:** format: 44, invalid: 1241, missing: 1538
- **transactions:** format: 75, invalid: 1212, missing: 1494

