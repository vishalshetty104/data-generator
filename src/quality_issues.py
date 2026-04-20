from datetime import datetime
from random import random, choice, shuffle
from typing import Dict, Any, List


class QualityIssues:
    def __init__(self, error_rate: float):
        self.error_rate = error_rate

    def apply_issues(self, row: Dict[str, Any], column_types: Dict[str, str]) -> Dict[str, Any]:
        modified_row = row.copy()
        issues_applied = []

        if random() < self.error_rate * 0.3:
            modified_row, issue = self._apply_missing_value(modified_row, column_types)
            if issue:
                issues_applied.append(issue)

        if random() < self.error_rate * 0.25:
            modified_row, issue = self._apply_invalid_value(modified_row, column_types)
            if issue:
                issues_applied.append(issue)

        if random() < self.error_rate * 0.15:
            modified_row, issue = self._apply_formatting_inconsistency(modified_row, column_types)
            if issue:
                issues_applied.append(issue)

        return modified_row, issues_applied

    def _apply_missing_value(self, row: Dict[str, Any], column_types: Dict[str, str]) -> tuple:
        col_name = choice(list(row.keys()))
        original_value = row[col_name]

        missing_type = choice(["null", "empty", "whitespace", "none_string"])

        if missing_type == "null":
            row[col_name] = None
        elif missing_type == "empty":
            row[col_name] = ""
        elif missing_type == "whitespace":
            row[col_name] = "   "
        elif missing_type == "none_string":
            row[col_name] = "N/A"

        return row, f"missing:{col_name}"

    def _apply_invalid_value(self, row: Dict[str, Any], column_types: Dict[str, str]) -> tuple:
        col_name = choice(list(row.keys()))
        col_type = column_types.get(col_name, "string")

        invalid_values = {
            "integer": ["", "abc", "-999", "999999999"],
            "decimal": ["", "xyz", "-999.99", "not.a.number"],
            "email": ["notanemail", "@missing.com", "spaces in@email.com", ""],
            "date": ["2024-13-45", "invalid", "99/99/9999", ""],
            "phone": ["123", "abc-def-ghij", ""],
            "string": [""],
            "name": [""],
            "boolean": ["maybe", "truee", "false_", "2"],
        }

        if col_type in invalid_values:
            row[col_name] = choice(invalid_values[col_type])
        else:
            row[col_name] = "INVALID"

        return row, f"invalid:{col_name}"

    def _apply_formatting_inconsistency(self, row: Dict[str, Any], column_types: Dict[str, str]) -> tuple:
        date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y", "%d/%m/%Y", "%Y%m%d"]
        phone_formats = [
            "+1-555-123-4567",
            "(555) 123-4567",
            "555-123-4567",
            "5551234567",
            "+1 555 123 4567"
        ]

        col_name = choice(list(row.keys()))
        col_type = column_types.get(col_name, "string")

        if col_type == "date":
            try:
                current_value = row[col_name]
                for fmt in date_formats:
                    try:
                        dt = datetime.strptime(current_value, fmt)
                        row[col_name] = dt.strftime(choice(date_formats))
                        return row, f"format:{col_name}"
                    except ValueError:
                        pass
            except Exception:
                pass

        elif col_type == "phone":
            row[col_name] = choice(phone_formats)
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
        modified_batch = [row.copy() for row in batch]

        for idx in duplicate_indices:
            if idx < len(modified_batch):
                dup_idx = choice([i for i in range(len(modified_batch)) if i != idx])
                modified_batch[idx] = modified_batch[dup_idx].copy()

        return modified_batch
