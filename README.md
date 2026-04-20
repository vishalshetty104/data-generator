# Synthetic Data Generator

Generate realistic synthetic data with intentional data quality issues for testing purposes.

## Features

- **Flexible Schema**: Define columns with types, ranges, and constraints via JSON
- **Scalable**: Generate millions of rows with configurable batch processing
- **Data Quality Issues**: Simulate real-world data problems:
  - Missing values (null, empty, whitespace, N/A)
  - Invalid values (out-of-range, malformed)
  - Duplicate rows
  - Inconsistent formatting (dates, phones, emails)
- **Memory Management**: Auto-detect system memory and optimize batch size
- **Streaming Output**: Writes directly to CSV without buffering all rows

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/generator.py --schema schemas/schema_example.json --rows 1000
```

### Generate 10,000 rows

```bash
python src/generator.py --schema schemas/schema_example.json --rows 10000 --verbose
```

### Generate 1 million rows with custom batch size

```bash
python src/generator.py --schema schemas/schema_example.json --rows 1000000 --batch-size 50000 --verbose
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--schema` | Path to JSON schema file | Required |
| `--rows` | Number of rows to generate | Required |
| `--output` | Output CSV path | `output/output_TIMESTAMP.csv` |
| `--error-rate` | Probability of quality issues (0.0-1.0) | `0.1` |
| `--batch-size` | Rows per batch | Auto-detected |
| `--verbose` | Show detailed progress | False |

## Schema Format

```json
{
  "columns": [
    {"name": "id", "type": "integer", "min": 1, "max": 1000000},
    {"name": "name", "type": "name"},
    {"name": "email", "type": "email"},
    {"name": "phone", "type": "phone"},
    {"name": "birth_date", "type": "date", "format": "%Y-%m-%d", "min": "1960-01-01", "max": "2005-12-31"},
    {"name": "salary", "type": "decimal", "min": 30000, "max": 150000, "precision": 2},
    {"name": "department", "type": "enum", "values": ["Engineering", "Sales", "Marketing"]},
    {"name": "is_active", "type": "boolean"}
  ]
}
```

### Supported Column Types

| Type | Options | Description |
|------|---------|-------------|
| `integer` | `min`, `max` | Integer values in range |
| `decimal` | `min`, `max`, `precision` | Decimal numbers |
| `string` | `min_length`, `max_length` | Random strings |
| `name` | - | Realistic names |
| `email` | - | Email addresses |
| `phone` | - | Phone numbers |
| `date` | `format`, `min`, `max` | Date values |
| `boolean` | - | True/false |
| `enum` | `values` | Pick from list |

## Project Structure

```
data-generator/
├── src/
│   ├── __init__.py
│   ├── generator.py       # Main entry point
│   ├── schema_parser.py   # JSON schema validation
│   ├── data_generator.py  # Data generation by type
│   ├── quality_issues.py  # Inject quality issues
│   ├── output.py          # Batch CSV writer
│   └── memory_utils.py    # Memory detection
├── schemas/
│   ├── schema_example.json
│   ├── products.json      # E-commerce products
│   ├── customers.json     # Customer profiles
│   ├── employees.json     # HR records
│   ├── transactions.json  # Financial transactions
│   └── orders.json       # Order records
├── output/                # Generated CSV files
│   └── .gitkeep
├── benchmark.py          # Performance benchmarking
├── requirements.txt
└── README.md
```
## Performance

[Performance Benchmark Report](./output/benchmark_report.md)
