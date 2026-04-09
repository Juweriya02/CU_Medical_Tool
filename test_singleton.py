import unittest
from ftp_client import FTPClient


class TestSingletonPattern(unittest.TestCase):
    """
    Tests that prove the Singleton pattern is correctly
    implemented in the FTPClient class.
    """

    def setUp(self):
        """Reset the Singleton before each test."""
        FTPClient.reset_instance()

    def test_only_one_instance_is_created(self):
        """
        The most important Singleton test:
        Two separate calls to create an FTPClient must
        return the exact same object in memory.
        """
        client_one = FTPClient(
            host="ftp.centrala.ac.uk",
            username="med_user",
            password="secure123"
        )
        client_two = FTPClient(
            host="ftp.centrala.ac.uk",
            username="med_user",
            password="secure123"
        )

        # 'is' checks whether they are the same object
        # in memory — not just equal, but identical
        self.assertIs(client_one, client_two)
        print("\n✓ Both variables point to the same instance.")

    def test_instance_id_is_identical(self):
        """
        The memory address (id) of both instances must
        be identical — proving they are the same object.
        """
        client_one = FTPClient(host="ftp.centrala.ac.uk")
        client_two = FTPClient(host="ftp.centrala.ac.uk")

        self.assertEqual(id(client_one), id(client_two))
        print(f"\n✓ Both instances share memory address: {id(client_one)}")

    def test_state_is_shared_across_references(self):
        """
        Changes made through one reference must be visible
        through the other — because they are the same object.
        """
        client_one = FTPClient(host="ftp.centrala.ac.uk")
        client_one.connect()

        client_two = FTPClient(host="ftp.centrala.ac.uk")

        # client_two should see the connection made by client_one
        self.assertTrue(client_two.connected)
        print("\n✓ Connection state is shared across both references.")

    def test_processed_files_shared_across_references(self):
        """
        Files downloaded through one reference must appear
        in the processed_files set of the other reference.
        """
        client_one = FTPClient(host="ftp.centrala.ac.uk")
        client_one.connect()
        client_one.download_file("MED_DATA_20230603140104.csv")

        client_two = FTPClient(host="ftp.centrala.ac.uk")

        self.assertIn(
            "MED_DATA_20230603140104.csv",
            client_two.processed_files
        )
        print("\n✓ Processed files set is shared across both references.")

    def test_duplicate_download_is_prevented(self):
        """
        Attempting to download the same file twice must
        return False the second time — duplicate prevention.
        """
        client = FTPClient(host="ftp.centrala.ac.uk")
        client.connect()

        first_download = client.download_file(
            "MED_DATA_20230603140104.csv"
        )
        second_download = client.download_file(
            "MED_DATA_20230603140104.csv"
        )

        self.assertTrue(first_download)
        self.assertFalse(second_download)
        print("\n✓ Duplicate download correctly prevented.")

    def test_reset_allows_new_instance(self):
        """
        After a reset, a genuinely new instance must be created.
        This confirms the reset mechanism works for testing.
        """
        client_one = FTPClient(host="ftp.centrala.ac.uk")
        FTPClient.reset_instance()
        client_two = FTPClient(host="ftp.centrala.ac.uk")

        self.assertIsNot(client_one, client_two)
        print("\n✓ Reset correctly allows a new instance to be created.")


if __name__ == '__main__':
    unittest.main(verbosity=2)