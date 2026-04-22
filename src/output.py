import csv
from typing import Dict, Any, List, Iterator


class BatchCSVWriter:
    def __init__(self, output_path: str, batch_size: int = 10000):
        self.output_path = output_path
        self.batch_size = batch_size
        self.batch: List[Dict[str, Any]] = []
        self.total_rows_written = 0
        self.file_handle = None
        self.writer = None
        self.header_written = False

    def open(self) -> None:
        self.file_handle = open(self.output_path, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file_handle)
        self.header_written = False
        self.batch = []
        self.total_rows_written = 0

    def write_row(self, row: Dict[str, Any]) -> None:
        if not self.header_written:
            self.writer.writerow(row.keys())
            self.header_written = True

        self.batch.append(row.values())

        if len(self.batch) >= self.batch_size:
            self._flush_batch()

    def write_batch(self, rows: Iterator[Dict[str, Any]]) -> int:
        batch_count = 0
        for row in rows:
            self.write_row(row)
            batch_count += 1
        return batch_count

    def _flush_batch(self) -> None:
        if self.batch:
            self.writer.writerows(self.batch)
            self.total_rows_written += len(self.batch)
            self.batch = []
            

    def close(self) -> None:
        if self.batch:
            self._flush_batch()
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
            self.writer = None

    def get_total_rows_written(self) -> int:
        return self.total_rows_written
