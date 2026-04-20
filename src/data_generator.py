from datetime import datetime, timedelta
from typing import Dict, Any, Iterator, Optional
from random import randint, uniform, choice, random
import random as random_module

from faker import Faker


class DataGenerator:
    def __init__(self, columns: list):
        self.columns = columns
        self.faker = Faker()
        random_module.seed(42)

    def generate_row(self) -> Dict[str, Any]:
        row = {}
        for col in self.columns:
            row[col["name"]] = self._generate_value(col)
        return row

    def generate_rows(self, count: int) -> Iterator[Dict[str, Any]]:
        for _ in range(count):
            yield self.generate_row()

    def _generate_value(self, col: Dict[str, Any]) -> Any:
        col_type = col["type"]

        if col_type == "integer":
            return randint(col.get("min", 0), col.get("max", 1000))

        elif col_type == "decimal":
            precision = col.get("precision", 2)
            value = uniform(col.get("min", 0), col.get("max", 1000))
            return round(value, precision)

        elif col_type == "string":
            min_len = col.get("min_length", 5)
            max_len = col.get("max_length", 20)
            length = randint(min_len, max_len)
            return ''.join(random_module.choices('abcdefghijklmnopqrstuvwxyz', k=length))

        elif col_type == "name":
            return self.faker.name()

        elif col_type == "email":
            return self.faker.email()

        elif col_type == "phone":
            return self.faker.phone_number()

        elif col_type == "date":
            return self._generate_date(col)

        elif col_type == "boolean":
            return choice([True, False])

        elif col_type == "enum":
            return choice(col["values"])

        else:
            return None

    def _generate_date(self, col: Dict[str, Any]) -> str:
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
