# test_csv_validator.py

import unittest
import os
import tempfile
from csv_validator import CSVValidator


class TestCSVValidator(unittest.TestCase):

    def setUp(self):
        self.validator = CSVValidator()
        self.test_dir = tempfile.mkdtemp()

    def _create_test_file(self, filename, content):
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            f.write(content)
        return file_path

    def _valid_content(self):
        return (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,9.875,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701\n'
            '64,14:01:04,4.168,9.247,1.958,1.65,3.631,'
            '9.317,8.182,9.292,5.978,3.06\n'
        )

    def test_valid_file_passes_all_checks(self):
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv',
            self._valid_content()
        )
        self.assertTrue(self.validator.validate(file_path))

    def test_empty_file_is_rejected(self):
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', '')
        self.assertFalse(self.validator.validate(file_path))
        self.assertIn('empty', self.validator.error_message.lower())

    def test_correct_filename_passes(self):
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv',
            self._valid_content()
        )
        self.assertTrue(self.validator.validate(file_path))

    def test_filename_missing_prefix_is_rejected(self):
        file_path = self._create_test_file(
            'medical_data_20230603140104.csv',
            self._valid_content()
        )
        self.assertFalse(self.validator.validate(file_path))
        self.assertIn('filename', self.validator.error_message.lower())

    def test_filename_with_letters_in_date_is_rejected(self):
        file_path = self._create_test_file(
            'MED_DATA_2023AB03140104.csv',
            self._valid_content()
        )
        self.assertFalse(self.validator.validate(file_path))

    def test_filename_with_wrong_extension_is_rejected(self):
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.txt',
            self._valid_content()
        )
        self.assertFalse(self.validator.validate(file_path))

    def test_filename_with_spaces_is_rejected(self):
        file_path = self._create_test_file(
            'MED DATA 20230603140104.csv',
            self._valid_content()
        )
        self.assertFalse(self.validator.validate(file_path))

    def test_correct_headers_pass(self):
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv',
            self._valid_content()
        )
        self.assertTrue(self.validator.validate(file_path))

    def test_misspelled_header_is_rejected(self):
        content = (
            'batch,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,9.875,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertFalse(self.validator.validate(file_path))
        self.assertIn('header', self.validator.error_message.lower())

    def test_missing_header_row_is_rejected(self):
        content = (
            '55,14:01:04,9.875,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertFalse(self.validator.validate(file_path))

    def test_extra_column_in_header_is_rejected(self):
        content = (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10,reading11\n'
            '55,14:01:04,9.875,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701,1.234\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertFalse(self.validator.validate(file_path))

    def test_row_with_missing_columns_is_rejected(self):
        content = (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,9.875,9.138\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertFalse(self.validator.validate(file_path))
        self.assertIn('column', self.validator.error_message.lower())

    def test_row_with_extra_columns_is_rejected(self):
        content = (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,9.875,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701,5.555,6.666\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertFalse(self.validator.validate(file_path))

    def test_unique_batch_ids_pass(self):
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv',
            self._valid_content()
        )
        self.assertTrue(self.validator.validate(file_path))

    def test_duplicate_batch_id_is_rejected(self):
        content = (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,9.875,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701\n'
            '55,14:01:05,4.168,9.247,1.958,1.65,3.631,'
            '9.317,8.182,9.292,5.978,3.06\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertFalse(self.validator.validate(file_path))
        self.assertIn('duplicate', self.validator.error_message.lower())

    def test_readings_within_range_pass(self):
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv',
            self._valid_content()
        )
        self.assertTrue(self.validator.validate(file_path))

    def test_reading_equal_to_ten_is_rejected(self):
        content = (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,10.0,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertFalse(self.validator.validate(file_path))
        self.assertIn('exceed', self.validator.error_message.lower())

    def test_reading_greater_than_ten_is_rejected(self):
        content = (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,9.875,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,15.5\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertFalse(self.validator.validate(file_path))

    def test_non_numeric_reading_is_rejected(self):
        content = (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,9.875,ERROR,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertFalse(self.validator.validate(file_path))
        self.assertIn('valid number', self.validator.error_message.lower())

    def test_reading_of_zero_is_valid(self):
        content = (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,0.0,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertTrue(self.validator.validate(file_path))

    def test_reading_of_9_9_is_valid(self):
        content = (
            'batch_id,timestamp,reading1,reading2,reading3,'
            'reading4,reading5,reading6,reading7,reading8,'
            'reading9,reading10\n'
            '55,14:01:04,9.9,9.138,1.115,8.006,3.84,'
            '4.952,9.038,1.046,2.179,8.701\n'
        )
        file_path = self._create_test_file(
            'MED_DATA_20230603140104.csv', content)
        self.assertTrue(self.validator.validate(file_path))


if __name__ == '__main__':
    unittest.main(verbosity=2)




