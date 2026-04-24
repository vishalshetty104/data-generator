import csv
from typing import Dict, Any, List, Iterator


class BatchCSVWriter:
    """Write data rows to CSV file in batches for memory efficiency.

    Buffers rows in memory and flushes them in batches to avoid
    excessive memory usage when writing large datasets.
    """

    def __init__(self, output_path: str, batch_size: int = 10000):
        """Initialize BatchCSVWriter.

        Args:
            output_path: Path to output CSV file.
            batch_size: Number of rows to buffer before flushing to disk.
        """
        self.output_path = output_path
        self.batch_size = batch_size
        self.batch: List[Dict[str, Any]] = []
        self.total_rows_written = 0
        self.file_handle = None
        self.writer = None
        self.header_written = False

    def open(self) -> None:
        """Open the output file and prepare for writing."""
        self.file_handle = open(self.output_path, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file_handle)
        self.header_written = False
        self.batch = []
        self.total_rows_written = 0

    def write_row(self, row: Dict[str, Any]) -> None:
        """Write a single row to the CSV file.

        Args:
            row: Dictionary mapping column names to values.
        """
        if not self.header_written:
            self.writer.writerow(row.keys())
            self.header_written = True

        self.batch.append(row.values())

        if len(self.batch) >= self.batch_size:
            self._flush_batch()

    def write_batch(self, rows: Iterator[Dict[str, Any]]) -> int:
        """Write multiple rows to the CSV file.

        Args:
            rows: Iterator of row dictionaries.

        Returns:
            Number of rows written.
        """
        batch_count = 0
        for row in rows:
            self.write_row(row)
            batch_count += 1
        return batch_count

    def _flush_batch(self) -> None:
        """Write buffered rows to disk and clear the buffer."""
        if self.batch:
            self.writer.writerows(self.batch)
            self.total_rows_written += len(self.batch)
            self.batch = []
            

    def close(self) -> None:
        """Close the output file, flushing any remaining buffered rows."""
        if self.batch:
            self._flush_batch()
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
            self.writer = None

    def get_total_rows_written(self) -> int:
        """Return the total number of rows written to the file."""
        return self.total_rows_written
