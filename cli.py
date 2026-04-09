# cli.py
# Command Line Interface for the CU Pharmaceutical Data Tool

import os
import re
from datetime import datetime


def print_header():
    """Prints the application header."""
    print("\n" + "=" * 60)
    print("   CENTRALA UNIVERSITY — PHARMACEUTICAL DATA TOOL v1.0")
    print("=" * 60)
    print("\nWelcome. This tool connects to the partner FTP server,")
    print("downloads new trial data files, validates them, and stores")
    print("approved files securely.\n")


def print_menu():
    """Prints the main menu options."""
    print("Please select an option:\n")
    print("  [1]  Download today's data files")
    print("  [2]  Download data files for a specific date")
    print("  [3]  View validation error log")
    print("  [4]  View download history")
    print("  [5]  Exit")
    print("\n" + "=" * 60)


def get_valid_date():
    """
    Prompts the user for a date in YYYY-MM-DD format.
    Keeps asking until a valid date is entered or
    the user presses 0 to go back.
    Demonstrates: Error Prevention (Nielsen Heuristic 5)
    """
    print("\n" + "-" * 60)
    print("Enter the date you wish to download data for.")
    print("Format: YYYY-MM-DD  (example: 2023-06-03)")
    print("-" * 60)

    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    while True:
        user_input = input("Enter date (or 0 to go back): ").strip()

        if user_input == '0':
            return None

        if date_pattern.match(user_input):
            try:
                datetime.strptime(user_input, '%Y-%m-%d')
                return user_input
            except ValueError:
                pass

        print("\n  ⚠  Invalid date format. Please use YYYY-MM-DD.")
        print("     Example: 2023-06-03")
        print("     Try again or press [0] to return to main menu.\n")


def simulate_download(target_date):
    """
    Simulates the download and validation process.
    In the real system this calls FTPClient and CSVValidator.
    Demonstrates: Visibility of System Status (Nielsen Heuristic 1)
    """
    print("\n" + "-" * 60)
    print(f"Connecting to FTP server...          ✓ Connected")
    print(f"Searching for files dated {target_date}...")
    print(f"  Found 3 new file(s) to download.\n")

    files = [
        (f"MED_DATA_{target_date.replace('-', '')}140104.csv", True),
        (f"MED_DATA_{target_date.replace('-', '')}140512.csv", False),
        (f"MED_DATA_{target_date.replace('-', '')}141000.csv", True),
    ]

    for filename, is_valid in files:
        print(f"Downloading {filename}...   ✓ Done")

    print("\nRunning validation checks...")
    stored = 0
    rejected = 0

    for filename, is_valid in files:
        if is_valid:
            status = "✓ VALID   — Stored"
            stored += 1
        else:
            status = "✗ INVALID — Logged"
            rejected += 1
        print(f"  {filename}  →  {status}")

    print("\n" + "-" * 60)
    print("Summary:")
    print(f"  Files downloaded:   {len(files)}")
    print(f"  Files stored:       {stored}")
    print(f"  Files rejected:     {rejected}")
    print(f"  Error log updated:  /logs/error_log.csv")
    print("-" * 60)
    input("\nPress [Enter] to return to the main menu.")


def view_error_log():
    """Displays the error log if it exists."""
    log_path = "logs/error_log.csv"
    print("\n" + "-" * 60)
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            print(f.read())
    else:
        print("  No error log found. No files have been rejected yet.")
    print("-" * 60)
    input("\nPress [Enter] to return to the main menu.")


def view_history():
    """Displays the download history if it exists."""
    history_path = "logs/download_history.txt"
    print("\n" + "-" * 60)
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            print(f.read())
    else:
        print("  No download history found yet.")
    print("-" * 60)
    input("\nPress [Enter] to return to the main menu.")


def run_cli():
    """
    Main loop for the CLI application.
    Demonstrates: User Control and Freedom (Nielsen Heuristic 3)
    """
    while True:
        print_header()
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            today = datetime.now().strftime('%Y-%m-%d')
            simulate_download(today)

        elif choice == '2':
            selected_date = get_valid_date()
            if selected_date:
                simulate_download(selected_date)

        elif choice == '3':
            view_error_log()

        elif choice == '4':
            view_history()

        elif choice == '5':
            print("\n  Goodbye. Exiting the application.\n")
            break

        else:
            print("\n  ⚠  Invalid choice. Please enter a number between 1 and 5.")
            input("  Press [Enter] to try again.")
