class FTPClient:
    """
    FTP Client implemented as a Singleton.

    Design Pattern: Singleton (Creational)
    Purpose: Ensures only one FTP connection instance exists
    throughout the application lifecycle, preventing resource
    waste and connection conflicts.

    Reference: Gamma et al. (1994) Design Patterns:
    Elements of Reusable Object-Oriented Software.
    Addison-Wesley.
    """

    # Class-level variable that holds the single instance.
    # Starts as None — no instance exists yet.
    _instance = None

    def __new__(cls, host=None, username=None, password=None):
        """
        __new__ is called before __init__ every time someone
        tries to create an instance of this class.

        This is where the Singleton logic lives:
        - If no instance exists yet, create one and store it
        - If an instance already exists, return it immediately
          without creating a new one
        """
        if cls._instance is None:
            print("[FTPClient] No existing instance found.")
            print("[FTPClient] Creating new Singleton instance...")
            cls._instance = super().__new__(cls)
            cls._instance._initialised = False
        else:
            print("[FTPClient] Existing instance found.")
            print("[FTPClient] Returning existing Singleton instance.")
        return cls._instance

    def __init__(self, host=None, username=None, password=None):
        """
        __init__ runs after __new__.
        The _initialised flag ensures the setup code only
        runs once, even if __init__ is called multiple times.
        """
        if self._initialised:
            return  # Already set up — do nothing

        self.host = host
        self.username = username
        self.password = password
        self.connected = False
        self.processed_files = set()
        self._initialised = True
        print(f"[FTPClient] Instance initialised for host: {self.host}")

    def connect(self):
        """
        Establishes connection to the FTP server.
        In production: uses ftplib.FTP to connect.
        Here: simulated for demonstration purposes.
        """
        if self.connected:
            print("[FTPClient] Already connected — reusing connection.")
            return

        # In production this would be:
        # from ftplib import FTP
        # self.ftp = FTP(self.host)
        # self.ftp.login(self.username, self.password)

        self.connected = True
        print(f"[FTPClient] ✓ Connected to {self.host}")

    def disconnect(self):
        """Closes the FTP connection."""
        if self.connected:
            # In production: self.ftp.quit()
            self.connected = False
            print(f"[FTPClient] Disconnected from {self.host}")

    def list_files(self):
        """
        Returns a list of available files on the FTP server.
        In production: uses self.ftp.nlst()
        Here: returns simulated sample filenames.
        """
        if not self.connected:
            print("[FTPClient] Error: Not connected.")
            return []

        # Simulated file list for demonstration
        simulated_files = [
            "MED_DATA_20230603140104.csv",
            "MED_DATA_20230603140512.csv",
            "MED_DATA_20230603141000.csv",
            "MED_DATA_20230603141530.csv",
        ]
        print(f"[FTPClient] Found {len(simulated_files)} file(s) on server.")
        return simulated_files

    def download_file(self, filename):
        """
        Downloads a single file from the FTP server.
        In production: uses self.ftp.retrbinary()
        Here: simulates the download.
        """
        if not self.connected:
            print("[FTPClient] Error: Not connected.")
            return False

        if filename in self.processed_files:
            print(f"[FTPClient] Skipping {filename} — already downloaded.")
            return False

        # In production:
        # with open(local_path, 'wb') as f:
        #     self.ftp.retrbinary(f'RETR {filename}', f.write)

        self.processed_files.add(filename)
        print(f"[FTPClient] ✓ Downloaded: {filename}")
        return True

    @classmethod
    def reset_instance(cls):
        """
        Resets the Singleton instance.
        Used in testing only — allows tests to create
        a fresh instance each time.
        """
        cls._instance = None
        print("[FTPClient] Singleton instance reset.")