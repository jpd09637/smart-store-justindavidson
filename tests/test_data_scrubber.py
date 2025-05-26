import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
import unittest
import pandas as pd
from utils.data_scrubber import DataScrubber
print("Loaded DataScrubber from:", DataScrubber.__module__)

class TestDataScrubber(unittest.TestCase):

    def setUp(self):
        # Sample dataframe with duplicates and missing values for testing
        data = {
            'A': [1, 2, 2, 3, None],
            'B': ['foo', 'bar', 'bar', 'baz', 'qux'],
            'C': [10, 20, 20, 30, 40]
        }
        self.df = pd.DataFrame(data)
        self.scrubber = DataScrubber(self.df)

    def test_remove_duplicate_records(self):
        self.scrubber.remove_duplicate_records()
        self.assertEqual(self.scrubber.df.duplicated().sum(), 0)

    def test_handle_missing_data_drop(self):
        self.scrubber.handle_missing_data(drop=True)
        self.assertFalse(self.scrubber.df.isnull().values.any())

    def test_handle_missing_data_fill(self):
        self.scrubber.handle_missing_data(fill_value=0)
        self.assertFalse(self.scrubber.df.isnull().values.any())
        self.assertIn(0, self.scrubber.df.values)

    def test_convert_column_to_new_data_type(self):
        self.scrubber.convert_column_to_new_data_type('A', float)
        self.assertTrue(self.scrubber.df['A'].dtype == float)

if __name__ == '__main__':
    unittest.main()