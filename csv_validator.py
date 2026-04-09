# csv_validator.py

import csv
import os
import re


class CSVValidator:
    """
    Responsible for validating pharmaceutical trial CSV files
    against all seven quality checks specified by the university brief.
    """

    REQUIRED_HEADERS = [
        "batch_id", "timestamp",
        "reading1", "reading2", "reading3", "reading4", "reading5",
        "reading6", "reading7", "reading8", "reading9", "reading10"
    ]

    FILENAME_PATTERN = re.compile(r'^MED_DATA_\d{14}\.csv$')

    def __init__(self):
        self.error_message = ""

    def validate(self, file_path):
        checks = [
            self._check_not_empty,
            self._check_filename_format,
            self._check_not_malformed,
            self._check_headers,
            self._check_rows,
        ]
        for check in checks:
            if not check(file_path):
                return False
        return True

    def _check_not_empty(self, file_path):
        if os.path.getsize(file_path) == 0:
            self.error_message = "File is empty (0 bytes)"
            return False
        return True

    def _check_filename_format(self, file_path):
        filename = os.path.basename(file_path)
        if not self.FILENAME_PATTERN.match(filename):
            self.error_message = (
                f"Filename '{filename}' does not match "
                f"required format MED_DATA_YYYYMMDDHHMMSS.csv"
            )
            return False
        return True

    def _check_not_malformed(self, file_path):
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                list(reader)
            return True
        except Exception as e:
            self.error_message = f"File is malformed and cannot be parsed: {e}"
            return False

    def _check_headers(self, file_path):
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers != self.REQUIRED_HEADERS:
                self.error_message = (
                    f"Incorrect headers. "
                    f"Expected: {self.REQUIRED_HEADERS}, "
                    f"Found: {headers}"
                )
                return False
        return True

    def _check_rows(self, file_path):
        seen_batch_ids = set()
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row_number, row in enumerate(reader, start=2):

                if len(row) != 12:
                    self.error_message = (
                        f"Row {row_number} has {len(row)} columns, "
                        f"expected 12"
                    )
                    return False

                batch_id = row[0]
                if batch_id in seen_batch_ids:
                    self.error_message = (
                        f"Duplicate batch_id '{batch_id}' "
                        f"found at row {row_number}"
                    )
                    return False
                seen_batch_ids.add(batch_id)

                for col_index in range(2, 12):
                    try:
                        value = float(row[col_index])
                    except ValueError:
                        self.error_message = (
                            f"Row {row_number}, column {col_index + 1}: "
                            f"'{row[col_index]}' is not a valid number"
                        )
                        return False
                    if value >= 10.0:
                        self.error_message = (
                            f"Row {row_number}, column {col_index + 1}: "
                            f"value {value} exceeds maximum allowed (9.9)"
                        )
                        return False
        return True