import csv
import os
import json
import urllib.request
import urllib.error
from datetime import datetime


class Logger:
    """
    Handles all error logging for the pharmaceutical
    data management tool.

    Each log entry is assigned a UUID retrieved from
    the UUIDTools external API, ensuring every error
    event is uniquely and permanently identifiable.

    If the API is unavailable (e.g. no internet),
    the system falls back to Python's built-in uuid
    module so logging never fails.
    """

    # External API endpoint for UUID generation
    API_ENDPOINT = "https://www.uuidtools.com/api/generate/v1"

    # Fallback to built-in uuid if API unavailable
    FALLBACK_TO_LOCAL = True

    # Log file location
    LOG_FOLDER = "logs"
    LOG_FILENAME = "error_log.csv"

    # Column headers for the error log
    LOG_HEADERS = [
        "guid",
        "timestamp",
        "filename",
        "reason"
    ]

    def __init__(self):
        """
        Initialises the logger and creates the log file
        if it does not already exist.
        """
        self._ensure_log_folder()
        self._ensure_log_file()

    def _ensure_log_folder(self):
        """Creates the logs folder if it does not exist."""
        if not os.path.exists(self.LOG_FOLDER):
            os.makedirs(self.LOG_FOLDER)
            print(f"[Logger] Created folder: {self.LOG_FOLDER}/")

    def _ensure_log_file(self):
        """
        Creates the error log CSV file with headers
        if it does not already exist.
        """
        log_path = self._get_log_path()
        if not os.path.exists(log_path):
            with open(log_path, 'w',
                      newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.LOG_HEADERS)
            print(f"[Logger] Created log file: {log_path}")

    def _get_log_path(self):
        """Returns the full path to the error log file."""
        return os.path.join(self.LOG_FOLDER, self.LOG_FILENAME)

    def _fetch_uuid_from_api(self):
        """
        Makes an HTTP GET request to the UUIDTools API
        and returns the generated UUID string.

        This demonstrates the use of an external API
        as required by assessment criterion 2M1.

        Returns:
            str: UUID from API, or None if request fails
        """
        try:
            print(f"[Logger] Calling API: {self.API_ENDPOINT}")

            # Make the HTTP request to the external API
            with urllib.request.urlopen(
                self.API_ENDPOINT,
                timeout=5
            ) as response:

                # Read and decode the response
                raw_data = response.read().decode('utf-8')

                # Parse the JSON response
                # API returns: ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"]
                uuid_list = json.loads(raw_data)
                uuid = uuid_list[0]

                print(f"[Logger] ✓ UUID received from API: {uuid}")
                return uuid

        except urllib.error.URLError as e:
            print(f"[Logger] ✗ API unavailable: {e}")
            return None
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"[Logger] ✗ API response parsing failed: {e}")
            return None

    def _get_fallback_uuid(self):
        """
        Generates a UUID locally using Python's built-in
        uuid module as a fallback when the API is unavailable.
        """
        import uuid
        fallback_uuid = str(uuid.uuid4())
        print(f"[Logger] Using local fallback UUID: {fallback_uuid}")
        return fallback_uuid

    def _get_uuid(self):
        """
        Gets a UUID — tries the external API first,
        falls back to local generation if unavailable.
        """
        uuid = self._fetch_uuid_from_api()

        if uuid is None and self.FALLBACK_TO_LOCAL:
            print("[Logger] Falling back to local UUID generation.")
            uuid = self._get_fallback_uuid()

        return uuid

    def log_error(self, filename, reason):
        """
        Logs a rejected file to the error log CSV.

        For each entry:
        1. Calls the UUIDTools API to get a unique GUID
        2. Records the current timestamp
        3. Records the filename and rejection reason
        4. Appends the entry to the error log CSV

        Args:
            filename (str): Name of the rejected file
            reason (str): Specific reason for rejection
        """
        # Step 1: Get UUID from external API
        guid = self._get_uuid()

        # Step 2: Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Step 3: Build the log entry
        log_entry = [guid, timestamp, filename, reason]

        # Step 4: Append to error log
        log_path = self._get_log_path()
        with open(log_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(log_entry)

        print(f"[Logger] ✓ Logged: {filename}")
        print(f"         Reason:  {reason}")
        print(f"         GUID:    {guid}")
        print(f"         Time:    {timestamp}")
        return log_entry

    def get_all_logs(self):
        """
        Reads and returns all entries from the error log.

        Returns:
            list: All log entries as dictionaries
        """
        log_path = self._get_log_path()
        entries = []

        with open(log_path, 'r',
                  newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append(row)

        return entries

    def display_log(self):
        """Prints all log entries to the terminal."""
        entries = self.get_all_logs()

        if not entries:
            print("[Logger] No errors logged yet.")
            return

        print("\n" + "=" * 70)
        print("  ERROR LOG")
        print("=" * 70)
        print(f"  {'GUID':<38} {'FILENAME':<35} REASON")
        print("-" * 70)

        for entry in entries:
            print(
                f"  {entry['guid']:<38} "
                f"{entry['filename']:<35} "
                f"{entry['reason']}"
            )

        print("=" * 70)
        print(f"  Total entries: {len(entries)}")
        print("=" * 70 + "\n")