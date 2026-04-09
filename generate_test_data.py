
import os
import csv
import random
from datetime import datetime, timedelta


OUTPUT_FOLDER = "test_data"

VALID_HEADERS = [
    "batch_id", "timestamp",
    "reading1", "reading2", "reading3", "reading4", "reading5",
    "reading6", "reading7", "reading8", "reading9", "reading10"
]


def ensure_output_folder():
    """Creates the test_data folder if it doesn't exist."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"[Setup] Created folder: {OUTPUT_FOLDER}/")
    else:
        print(f"[Setup] Folder already exists: {OUTPUT_FOLDER}/")


def generate_valid_row(batch_id, timestamp):
    """
    Generates one valid data row with:
    - A unique batch_id
    - A timestamp
    - 10 readings between 0.001 and 9.899
    """
    readings = [
        round(random.uniform(0.001, 9.899), 3)
        for _ in range(10)
    ]
    return [batch_id, timestamp] + readings


def get_timestamp():
    """Returns a formatted timestamp string."""
    return datetime.now().strftime("%H:%M:%S")


def get_valid_filename(date_str=None):
    """
    Returns a correctly formatted filename.
    Format: MED_DATA_YYYYMMDDHHMMSS.csv
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"MED_DATA_{date_str}.csv"


def write_csv(filepath, headers, rows):
    """Writes headers and rows to a CSV file."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in rows:
            writer.writerow(row)


def generate_valid_file_1():
    """
    Generates a perfectly valid CSV file with 10 data rows.
    All headers correct, all values in range, no duplicates.
    """
    filename = "MED_DATA_20230603140104.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    rows = [
        generate_valid_row(batch_id, "14:01:04")
        for batch_id in random.sample(range(1, 500), 10)
    ]

    write_csv(filepath, VALID_HEADERS, rows)
    print(f"[VALID]   Created: {filename}")
    return filepath


def generate_valid_file_2():
    """
    Generates a valid CSV file with a different date stamp.
    Tests that multiple valid files from the same day are handled.
    """
    filename = "MED_DATA_20230603140512.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    rows = [
        generate_valid_row(batch_id, "14:05:12")
        for batch_id in random.sample(range(500, 999), 10)
    ]

    write_csv(filepath, VALID_HEADERS, rows)
    print(f"[VALID]   Created: {filename}")
    return filepath


def generate_valid_file_3():
    """
    Generates a valid file with readings at boundary values.
    Tests that 0.001 and 9.899 are correctly accepted.
    """
    filename = "MED_DATA_20230603141000.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    # Mix of boundary and normal values
    rows = [
        [101, "14:10:00",
         0.001, 9.899, 5.000, 1.234, 7.777,
         3.141, 6.283, 0.500, 9.500, 4.444],
        [102, "14:10:01",
         1.111, 2.222, 3.333, 4.444, 5.555,
         6.666, 7.777, 8.888, 0.001, 9.899],
    ]

    write_csv(filepath, VALID_HEADERS, rows)
    print(f"[VALID]   Created: {filename} (boundary values)")
    return filepath


def generate_invalid_empty_file():
    """
    Invalid Type 1: Empty file (0 bytes).
    Should be caught by Gate 1.
    """
    filename = "INVALID_empty_file_MED_DATA_20230603150000.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    # Create a completely empty file
    open(filepath, 'w').close()

    print(f"[INVALID] Created: {filename} (empty — 0 bytes)")
    return filepath


def generate_invalid_filename():
    """
    Invalid Type 2: Incorrectly formatted filename.
    Should be caught by Gate 2.
    The file contents are valid — only the name is wrong.
    """
    filename = "medical_data_june_2023.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    rows = [generate_valid_row(i, "15:00:00") for i in range(1, 4)]
    write_csv(filepath, VALID_HEADERS, rows)

    print(f"[INVALID] Created: {filename} (wrong filename format)")
    return filepath


def generate_invalid_headers():
    """
    Invalid Type 3: Misspelled/incorrect headers.
    'batch' instead of 'batch_id' — caught by Gate 4.
    """
    filename = "MED_DATA_20230603150200.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    # Wrong headers — 'batch' instead of 'batch_id'
    wrong_headers = [
        "batch", "timestamp",
        "reading1", "reading2", "reading3", "reading4", "reading5",
        "reading6", "reading7", "reading8", "reading9", "reading10"
    ]

    rows = [generate_valid_row(i, "15:02:00") for i in range(1, 4)]
    write_csv(filepath, wrong_headers, rows)

    print(f"[INVALID] Created: {filename} (misspelled header)")
    return filepath


def generate_invalid_missing_column():
    """
    Invalid Type 4: Missing column in data rows.
    Rows have only 11 values instead of 12 — caught by Gate 5.
    """
    filename = "MED_DATA_20230603150300.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    # Each row is missing the last reading (only 11 columns)
    rows = [
        [i, "15:03:00",
         1.1, 2.2, 3.3, 4.4, 5.5,
         6.6, 7.7, 8.8, 9.1]   # Only 9 readings — missing 1
        for i in range(1, 4)
    ]

    write_csv(filepath, VALID_HEADERS, rows)
    print(f"[INVALID] Created: {filename} (missing column)")
    return filepath


def generate_invalid_duplicate_batch_id():
    """
    Invalid Type 5: Duplicate batch_id within same file.
    batch_id 55 appears twice — caught by Gate 6.
    """
    filename = "MED_DATA_20230603150400.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    rows = [
        # First row — batch_id 55
        [55, "15:04:00",
         9.1, 8.2, 7.3, 6.4, 5.5,
         4.6, 3.7, 2.8, 1.9, 0.1],
        # Second row — batch_id 55 again (duplicate!)
        [55, "15:04:01",
         1.1, 2.2, 3.3, 4.4, 5.5,
         6.6, 7.7, 8.8, 9.1, 0.2],
        # Third row — unique batch_id (valid)
        [99, "15:04:02",
         5.5, 5.5, 5.5, 5.5, 5.5,
         5.5, 5.5, 5.5, 5.5, 5.5],
    ]

    write_csv(filepath, VALID_HEADERS, rows)
    print(f"[INVALID] Created: {filename} (duplicate batch_id: 55)")
    return filepath


def generate_invalid_value_too_high():
    """
    Invalid Type 6: Reading value of 10.0 or above.
    reading1 = 10.5 in first row — caught by Gate 7.
    """
    filename = "MED_DATA_20230603150500.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    rows = [
        # First row — reading1 is 10.5 (invalid!)
        [201, "15:05:00",
         10.5, 8.2, 7.3, 6.4, 5.5,
         4.6, 3.7, 2.8, 1.9, 0.1],
        [202, "15:05:01",
         1.1, 2.2, 3.3, 4.4, 5.5,
         6.6, 7.7, 8.8, 9.1, 0.2],
    ]

    write_csv(filepath, VALID_HEADERS, rows)
    print(
        f"[INVALID] Created: {filename} "
        f"(reading value 10.5 exceeds maximum)"
    )
    return filepath


def generate_invalid_malformed():
    """
    Invalid Type 7: Malformed file structure.
    Inconsistent delimiters and broken row structure.
    Caught by Gate 3.
    """
    filename = "MED_DATA_20230603150600.csv"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    # Write raw malformed content that breaks CSV structure
    malformed_content = (
        'batch_id,timestamp,reading1,reading2\n'
        '55,"15:06:00,9.1,8.2\n'       # Unclosed quote
        '64,15:06:01,"broken,,data\n'   # Broken structure
        ',,,,,\n'                        # Empty row
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(malformed_content)

    print(f"[INVALID] Created: {filename} (malformed structure)")
    return filepath



def print_summary(valid_files, invalid_files):
    """Prints a summary of all generated files."""
    print("\n" + "=" * 60)
    print("  TEST DATA GENERATION COMPLETE")
    print("=" * 60)
    print(f"\n  Output folder: {OUTPUT_FOLDER}/")
    print(f"\n  Valid files generated:   {len(valid_files)}")
    for f in valid_files:
        print(f"    ✓ {os.path.basename(f)}")

    print(f"\n  Invalid files generated: {len(invalid_files)}")
    for f in invalid_files:
        print(f"    ✗ {os.path.basename(f)}")

    print(f"\n  Total files: {len(valid_files) + len(invalid_files)}")
    print("=" * 60)


def main():
    print("\n" + "=" * 60)
    print("  AUTOMATED TEST DATA GENERATOR")
    print("  Centrala University Pharmaceutical Data Tool")
    print("=" * 60 + "\n")

    # Create output folder
    ensure_output_folder()
    print()

    # Generate valid files
    print("Generating VALID test files...")
    valid_files = [
        generate_valid_file_1(),
        generate_valid_file_2(),
        generate_valid_file_3(),
    ]

    print()

    # Generate invalid files
    print("Generating INVALID test files...")
    invalid_files = [
        generate_invalid_empty_file(),
        generate_invalid_filename(),
        generate_invalid_headers(),
        generate_invalid_missing_column(),
        generate_invalid_duplicate_batch_id(),
        generate_invalid_value_too_high(),
        generate_invalid_malformed(),
    ]

    # Print summary
    print_summary(valid_files, invalid_files)


if __name__ == '__main__':
    main()
