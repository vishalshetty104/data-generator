import json
from typing import Dict, List, Any


class SchemaParser:
    """Parse and validate JSON schema files for data generation.

    Loads schema from JSON file and validates column definitions
    against supported types and requirements.
    """

    SUPPORTED_TYPES = {
        "integer", "decimal", "string", "name", "email",
        "phone", "date", "boolean", "enum"
    }
    """Set of supported column types."""

    REQUIRED_COLUMNS_FIELDS = ["name", "type"]
    """Required fields for each column definition."""

    def __init__(self, schema_path: str):
        """Initialize SchemaParser with path to schema file.

        Args:
            schema_path: Path to JSON schema file.
        """
        self.schema_path = schema_path
        self.columns = []
        self.errors = []

    def load(self) -> bool:
        """Load schema from JSON file.

        Returns:
            True if file was loaded successfully, False otherwise.
        """
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
        """Validate all column definitions in the schema.

        Returns:
            True if all columns are valid, False otherwise.
        """
        if not self.columns:
            self.errors.append("Schema must contain 'columns' array")
            return False

        for i, col in enumerate(self.columns):
            if not self._validate_column(col, i):
                return False

        return len(self.errors) == 0

    def _validate_column(self, col: Dict[str, Any], index: int) -> bool:
        """Validate a single column definition.

        Args:
            col: Column definition dictionary.
            index: Index of the column for error reporting.

        Returns:
            True if column is valid, False otherwise.
        """
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
        """Get the list of column definitions.

        Returns:
            List of column definition dictionaries.
        """
        return self.columns

    def get_errors(self) -> List[str]:
        """Get list of validation errors.

        Returns:
            List of error messages from load and validation.
        """
        return self.errors
