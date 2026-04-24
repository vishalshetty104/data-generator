from datetime import datetime
from random import random, choice, randint
from typing import Dict, Any, List


class QualityIssues:
    """Apply realistic data quality issues to generated rows.

    Injects missing values, invalid values, and formatting inconsistencies
    into data rows according to a configured error rate.
    """

    _INVALID_VALUES = {
        "integer": ["", "abc", "-999", "999999999"],
        "decimal": ["", "xyz", "-999.99", "not.a.number"],
        "email": ["notanemail", "@missing.com", "spaces in@email.com", ""],
        "date": ["2024-13-45", "invalid", "99/99/9999", ""],
        "phone": ["123", "abc-def-ghij", ""],
        "string": [""],
        "name": [""],
        "boolean": ["maybe", "truee", "false_", "2"],
    }

    _DATE_FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y", "%d/%m/%Y", "%Y%m%d"]
    _PHONE_FORMATS = [
        "+1-555-123-4567",
        "(555) 123-4567",
        "555-123-4567",
        "5551234567",
        "+1 555 123 4567"
    ]
    _MISSING_TYPES = ["null", "empty", "whitespace", "none_string"]

    def __init__(self, error_rate: float):
        """Initialize QualityIssues with specified error rate.

        Args:
            error_rate: Probability (0.0-1.0) that quality issues will be applied.
        """
        self.error_rate = error_rate

    def apply_issues(self, row: Dict[str, Any], column_types: Dict[str, str]) -> tuple:
        issues_applied = []
        modified_row = row
        row_keys = list(row.keys())

        if random() < self.error_rate * 0.3:
            col_name = row_keys[randint(0, len(row_keys) - 1)]
            modified_row, issue = self._apply_missing_value(row, col_name)
            if issue:
                issues_applied.append(issue)

        if random() < self.error_rate * 0.25:
            col_name = row_keys[randint(0, len(row_keys) - 1)]
            modified_row, issue = self._apply_invalid_value(row, column_types, col_name)
            if issue:
                issues_applied.append(issue)

        if random() < self.error_rate * 0.15:
            col_name = row_keys[randint(0, len(row_keys) - 1)]
            modified_row, issue = self._apply_formatting_inconsistency(row, column_types, col_name)
            if issue:
                issues_applied.append(issue)

        return modified_row, issues_applied

    def _apply_missing_value(self, row: Dict[str, Any], col_name: str) -> tuple:
        """Apply a missing value issue to a random column.

        Args:
            row: Dictionary representing a data row.
            column_types: Dictionary mapping column names to their types.

        Returns:
            Tuple of (modified row, issue description string).
        """
        
        original_value = row[col_name]
        missing_type = choice(self._MISSING_TYPES)

        if missing_type == "null":
            row[col_name] = None
        elif missing_type == "empty":
            row[col_name] = ""
        elif missing_type == "whitespace":
            row[col_name] = "   "
        elif missing_type == "none_string":
            row[col_name] = "N/A"

        return row, f"missing:{col_name}"

    def _apply_invalid_value(self, row: Dict[str, Any], column_types: Dict[str, str], col_name: str) -> tuple:
        col_type = column_types.get(col_name, "string")

        if col_type in self._INVALID_VALUES:
            row[col_name] = choice(self._INVALID_VALUES[col_type])
        else:
            row[col_name] = "INVALID"

        return row, f"invalid:{col_name}"

    def _apply_formatting_inconsistency(self, row: Dict[str, Any], column_types: Dict[str, str], col_name: str) -> tuple:
        col_type = column_types.get(col_name, "string")

        if col_type == "date":
            try:
                current_value = row[col_name]
                for fmt in self._DATE_FORMATS:
                    try:
                        dt = datetime.strptime(current_value, fmt)
                        row[col_name] = dt.strftime(choice(self._DATE_FORMATS))
                        return row, f"format:{col_name}"
                    except ValueError:
                        pass
            except Exception:
                pass

        elif col_type == "phone":
            row[col_name] = choice(self._PHONE_FORMATS)
            return row, f"format:{col_name}"

        elif col_type == "email":
            email = row[col_name]
            if email and "@" in email:
                local, domain = email.rsplit("@", 1)
                inconsistent_variants = [
                    email.lower(),
                    email.upper(),
                    f"{local}@{domain.upper()}",
                    f"{local.upper()}@{domain}",
                ]
                row[col_name] = choice(inconsistent_variants)
                return row, f"format:{col_name}"

        return row, None

    def mark_duplicate_rows(self, batch: List[Dict[str, Any]], duplicate_indices: List[int]) -> List[Dict[str, Any]]:
        if not duplicate_indices:
            return batch

        modified_batch = list(batch)
        n = len(modified_batch)
        for idx in duplicate_indices:
            if idx < n:
                dup_idx = idx
                while dup_idx == idx:
                    dup_idx = randint(0, n - 1)
                modified_batch[idx] = modified_batch[dup_idx]

        return modified_batch
