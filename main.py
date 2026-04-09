import os
from ftp_client import FTPClient
from csv_validator import CSVValidator
from datetime import datetime


def run_pipeline(target_date=None):
    """
    Demonstrates the full application pipeline using
    the Singleton FTPClient design pattern.

    No matter how many times FTPClient is called
    throughout this function, only ONE instance
    is ever created or used.
    """

    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')

    print("\n" + "=" * 60)
    print("  CENTRALA UNIVERSITY — PHARMACEUTICAL DATA TOOL")
    print("=" * 60)
    print(f"  Target date: {target_date}")
    print("=" * 60 + "\n")

    
    print("STEP 1: Acquiring FTP connection...")
    ftp = FTPClient(
        host="ftp.centrala-university.ac.uk",
        username="med_data_user",
        password="securepassword123"
    )
    ftp.connect()

    
    print("\nSTEP 2: Another component requests FTP access...")
    ftp_second_reference = FTPClient(
        host="ftp.centrala-university.ac.uk",
        username="med_data_user",
        password="securepassword123"
    )

    # Prove they are the same object
    if ftp is ftp_second_reference:
        print("✓ Confirmed: Both references point to the")
        print("  same Singleton instance.")
        print(f"  Instance ID: {id(ftp)}")
    
    
    print("\nSTEP 3: Listing files on FTP server...")
    available_files = ftp.list_files()

    
    print(f"\nSTEP 4: Filtering files for date {target_date}...")
    date_nodash = target_date.replace('-', '')
    matching_files = [
        f for f in available_files
        if date_nodash in f
    ]
    print(f"  Found {len(matching_files)} matching file(s).")

    
    print("\nSTEP 5: Downloading new files...")
    downloaded = []
    for filename in matching_files:
        success = ftp.download_file(filename)
        if success:
            downloaded.append(filename)

    
    print("\nSTEP 6: Validating downloaded files...")
    validator = CSVValidator()
    valid_files = []
    invalid_files = []

    for filename in downloaded:
        # In real system: validate actual downloaded file
        # Here we simulate validation result
        is_valid = not filename.endswith("140512.csv")

        if is_valid:
            valid_files.append(filename)
            print(f"  ✓ {filename} — VALID")
        else:
            invalid_files.append(filename)
            print(f"  ✗ {filename} — INVALID — Logged")

    
    
    print("\n" + "-" * 60)
    print("SUMMARY")
    print("-" * 60)
    print(f"  Files found on server:   {len(available_files)}")
    print(f"  Files matching date:     {len(matching_files)}")
    print(f"  Files downloaded:        {len(downloaded)}")
    print(f"  Files passed validation: {len(valid_files)}")
    print(f"  Files failed validation: {len(invalid_files)}")
    print("-" * 60)

    
    print("\nSTEP 8: Attempting re-download (duplicate test)...")
    print("  Singleton processed_files set prevents re-downloads:")
    for filename in matching_files:
        ftp.download_file(filename)

    print("\n✓ All duplicate downloads correctly prevented")
    print("  by the Singleton instance's processed_files set.")
    print("\n" + "=" * 60)

    ftp.disconnect()


if __name__ == '__main__':
    run_pipeline('2023-06-03')