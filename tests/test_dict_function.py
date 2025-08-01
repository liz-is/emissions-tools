import unittest
import os
import pandas as pd
from bin.utils import read_node_data

class TestNodeDataParsing(unittest.TestCase):
    def setUp(self):
        self.test_csv_path = "test_nodes.csv"
        self.expected_keys = {
            "cpu_cores", "embodied", "embodied_estimate",
            "max_power_draw", "min_power_draw", "model_id"
        }

    def test_dictionary_structure(self):
        node_dict = read_node_data(self.test_csv_path)

        # Check same number of entries
        df = pd.read_csv(self.test_csv_path)
        self.assertEqual(len(node_dict), len(df), "Mismatch between dictionary and CSV rows")

        # Check every node entry has expected keys
        for node_name, node_data in node_dict.items():
            self.assertEqual(set(node_data.keys()), self.expected_keys)
            for key in self.expected_keys:
                self.assertIsNotNone(node_data[key])

        # Check the estimate field is correct for known estimate value
        self.assertTrue(node_dict["node001"]["embodied_estimate"])
        self.assertFalse(node_dict["node002"]["embodied_estimate"])

if __name__ == "__main__":
    unittest.main()
