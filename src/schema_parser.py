import json
from typing import Dict, List, Any


class SchemaParser:
    SUPPORTED_TYPES = {
        "integer", "decimal", "string", "name", "email",
        "phone", "date", "boolean", "enum"
    }

    REQUIRED_COLUMNS_FIELDS = ["name", "type"]

    def __init__(self, schema_path: str):
        self.schema_path = schema_path
        self.columns = []
        self.errors = []

    def load(self) -> bool:
        try:
            with open(self.schema_path, 'r') as f:
                data = json.load(f)
            self.columns = data.get("columns", [])
            return True
        except FileNotFoundError:
            self.errors.append(f"Schema file not found: {self.schema_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in schema file: {e}")
            return False

    def validate(self) -> bool:
        if not self.columns:
            self.errors.append("Schema must contain 'columns' array")
            return False

        for i, col in enumerate(self.columns):
            if not self._validate_column(col, i):
                return False

        return len(self.errors) == 0

    def _validate_column(self, col: Dict[str, Any], index: int) -> bool:
        for field in self.REQUIRED_COLUMNS_FIELDS:
            if field not in col:
                self.errors.append(f"Column {index}: missing required field '{field}'")
                return False

        col_type = col.get("type")
        if col_type not in self.SUPPORTED_TYPES:
            self.errors.append(
                f"Column '{col.get('name')}': unsupported type '{col_type}'. "
                f"Supported: {', '.join(self.SUPPORTED_TYPES)}"
            )
            return False

        if col_type == "enum" and "values" not in col:
            self.errors.append(f"Column '{col.get('name')}': enum type requires 'values' array")
            return False

        if col_type in ("integer", "decimal"):
            if "min" not in col or "max" not in col:
                self.errors.append(
                    f"Column '{col.get('name')}': {col_type} requires 'min' and 'max' values"
                )
                return False

        return True

    def get_columns(self) -> List[Dict[str, Any]]:
        return self.columns

    def get_errors(self) -> List[str]:
        return self.errors
