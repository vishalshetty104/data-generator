from datetime import datetime, timedelta
from typing import Dict, Any, Iterator, Optional
from random import randint, uniform, choice, random
import random as random_module
from unittest import case

from faker import Faker


class DataGenerator:
    """Generate structured random data rows based on a column schema.

    Usage::

        columns = [
            {"name": "id", "type": "integer", "min": 1, "max": 10000},
            {"name": "email", "type": "email"},
            {"name": "status", "type": "enum", "values": ["active", "inactive"]},
        ]
        gen = DataGenerator(columns)
        for row in gen.generate_rows(10):
            print(row)

    Supported column types: integer, decimal, string, name, email, phone, date, boolean, enum
    """
    def __init__(self, columns: list):
        """Initialize DataGenerator with column schema.

        Args:
            columns: List of column definitions with name, type, and optional constraints.
        """
        self.columns = columns
        self.faker = Faker()
        random_module.seed(42)

    def generate_row(self) -> Dict[str, Any]:
        """Generate a single random data row.

        Returns:
            Dictionary mapping column names to generated values.
        """
        row = {}
        for col in self.columns:
            row[col["name"]] = self._generate_value(col)
        return row

    def generate_rows(self, count: int) -> Iterator[Dict[str, Any]]:
        """Generate multiple random data rows.

        Args:
            count: Number of rows to generate.

        Yields:
            Dictionaries representing each generated row.
        """
        for _ in range(count):
            yield self.generate_row()

    def _generate_value(self, col: Dict[str, Any]) -> Any:
        """Generate a value for a single column based on its type.

        Args:
            col: Column definition with type and optional constraints.

        Returns:
            Generated value appropriate for the column type.
        """
        col_type = col["type"]

        match col_type:
            case "integer":
                return randint(col.get("min", 0), col.get("max", 1000))
            case "decimal":
                precision = col.get("precision", 2)
                value = uniform(col.get("min", 0), col.get("max", 1000))
                return round(value, precision)

            case "string":
                min_len = col.get("min_length", 5)
                max_len = col.get("max_length", 20)
                length = randint(min_len, max_len)
                return ''.join(random_module.choices('abcdefghijklmnopqrstuvwxyz', k=length))

            case "name":
                return self.faker.name()

            case "email":
                return self.faker.email()

            case "phone":
                return self.faker.phone_number()

            case "date":
                return self._generate_date(col)

            case "boolean":
                return choice([True, False])

            case "enum":
                return choice(col["values"])

            case _:
                return None
        

    def _generate_date(self, col: Dict[str, Any]) -> str:
        """Generate a random date within specified bounds.

        Args:
            col: Column definition with optional min, max, and format.

        Returns:
            Formatted date string.
        """
        date_format = col.get("format", "%Y-%m-%d")
        min_date = col.get("min", "1970-01-01")
        max_date = col.get("max", "2024-12-31")

        try:
            min_dt = datetime.strptime(min_date, "%Y-%m-%d")
            max_dt = datetime.strptime(max_date, "%Y-%m-%d")
        except ValueError:
            min_dt = datetime(1970, 1, 1)
            max_dt = datetime(2024, 12, 31)

        delta = (max_dt - min_dt).days
        random_days = randint(0, max(1, delta))
        random_date = min_dt + timedelta(days=random_days)

        return random_date.strftime(date_format)
