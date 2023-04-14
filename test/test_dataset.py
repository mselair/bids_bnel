import shutil
import unittest
import pandas as pd
import os
import tempfile
import json
from pandas.testing import assert_frame_equal, assert_series_equal
from bids_bnel.dataset import BIDS_json, BIDSDataset, BIDS_TSV
from time import sleep


class TestBIDSTSV(unittest.TestCase):
    def setUp(self):
        # Set up test data and objects
        self.temp_dir = tempfile.mkdtemp()
        self.path_tsv = os.path.join(self.temp_dir, 'test_participants.tsv')
        self.path_json = os.path.join(self.temp_dir, 'test_participants.json')
        self.row = {'participant_id': 'AAA', 'species': 'human', 'sex': 'M'}

    def tearDown(self):
        # Clean up after the test
        os.remove(self.path_tsv)
        os.remove(self.path_json)

    def assert_data_frames_equal(self, df1, df2):
        """Helper method to assert that two data frames are equal"""
        keys1 = list(df1.keys())
        keys2 = list(df2.keys())
        self.assertListEqual(keys1, keys2)

        for k in keys1:
            self.assertEqual((df1[k] == df2[k]).sum(), len(df1))

    def test_save_read_empty(self):
        # Test if BIDS_TSV object is initialized correctly


        tsv = BIDS_TSV(self.path_tsv, path_json=self.path_json)
        tsv.dump()

        tsv2 = BIDS_TSV(self.path_tsv, path_json=self.path_json)
        assert_frame_equal(tsv, tsv2)

        tsv2.add_row(self.row)
        tsv2.dump()

        tsv3 = BIDS_TSV(self.path_tsv, path_json=self.path_json)
        assert_frame_equal(tsv2, tsv3)

        tsv3.metadata['participant_id'] = 'kokotsky popisek'
        tsv3['frnda'] = 1
        tsv3.dump()

        tsv4 = BIDS_TSV(self.path_tsv, path_json=self.path_json)
        self.assert_data_frames_equal(tsv3, tsv4)










class TestBids_json(unittest.TestCase):
    def setUp(self):
        # Create a temporary json file
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.json')
        self.test_data = {'key1': 'value1', 'key2': 'value2'}
        with open(self.test_file, 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        # Clean up the temporary json file
        os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_load_existing_json_file(self):
        # Create an instance of Bids_json class to load the json file
        bids_json = BIDS_json(self.test_file)

        # Check if the loaded data matches the original data
        self.assertEqual(bids_json._data, self.test_data, 'Loaded JSON data does not match original data')

    def test_save_json_file(self):
        # Create an instance of Bids_json class to save the json file
        bids_json = BIDS_json(self.test_file)
        new_data = {'key3': 'value3'}
        bids_json.update(new_data)
        bids_json.save()

        # Load the saved json file and check if the loaded data matches the original data
        with open(self.test_file, 'r') as f:
            loaded_data = json.load(f)
        expected_data = {**self.test_data, **new_data}
        self.assertEqual(loaded_data, expected_data, 'Saved JSON data does not match original data')



class TestBIDSDataset(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for the dataset
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir = os.path.join(self.temp_dir, 'dataset_test') # os.mkdir(self.temp_dir)

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.temp_dir)

    def test_create_dataset(self):
        # Create an instance of BIDSDataset class with create_dataset=True
        dataset = BIDSDataset(self.temp_dir, create_dataset=True)

        # Check if the dataset directory exists
        self.assertTrue(os.path.exists(self.temp_dir), 'Dataset directory was not created')

        # Check if the JSON files were created and saved
        self.assertTrue(os.path.exists(dataset._jsons['dataset_description']._path), 'dataset_description.json was not created')
        self.assertTrue(os.path.exists(dataset._jsons['events']._path), 'events.json was not created')
        self.assertTrue(os.path.exists(dataset._jsons['coordsystem']._path), 'coordsystem.json was not created')
        self.assertTrue(os.path.exists(dataset._jsons['electrodes']._path), 'electrodes.json was not created')
        self.assertTrue(os.path.exists(dataset._jsons['channels']._path), 'channels.json was not created')
        self.assertTrue(os.path.exists(dataset._jsons['participants']._path), 'participants.json was not created')

        # Check if the participants.tsv file was created
        self.assertTrue(os.path.exists(dataset._participants_path), 'participants.tsv was not created')

    def test_load_dataset(self):
        # Create an instance of BIDSDataset class with create_dataset=True
        dataset = BIDSDataset(self.temp_dir, create_dataset=True)

        # Create a new instance of BIDSDataset class with create_dataset=False
        dataset2 = BIDSDataset(self.temp_dir, create_dataset=False)

        # Check if the JSON files were loaded
        self.assertIsNotNone(dataset2._jsons['dataset_description'], 'dataset_description.json was not loaded')
        self.assertIsNotNone(dataset2._jsons['events'], 'events.json was not loaded')
        self.assertIsNotNone(dataset2._jsons['coordsystem'], 'coordsystem.json was not loaded')
        self.assertIsNotNone(dataset2._jsons['electrodes'], 'electrodes.json was not loaded')
        self.assertIsNotNone(dataset2._jsons['channels'], 'channels.json was not loaded')
        self.assertIsNotNone(dataset2._jsons['participants'], 'participants.json was not loaded')

        # Check if the participants.tsv file was loaded
        self.assertIsNotNone(dataset2._participants_meta, 'participants.tsv was not loaded')

        # Check if the data in dataset and dataset2 is the same
        self.assertEqual(dataset._jsons['dataset_description'], dataset2._jsons['dataset_description'], 'dataset_description data is not the same')
        self.assertEqual(dataset._jsons['events'], dataset2._jsons['events'], 'events data is not the same')
        self.assertEqual(dataset._jsons['coordsystem'], dataset2._jsons['coordsystem'], 'coordsystem data is not the same')
        self.assertEqual(dataset._jsons['electrodes'], dataset2._jsons['electrodes'], 'electrodes data is not the same')
        self.assertEqual(dataset._jsons['channels'], dataset2._jsons['channels'], 'channels data is not the same')
        self.assertEqual(dataset._jsons['participants'], dataset2._jsons['participants'], 'participants data is not the same')
        assert_frame_equal(dataset._participants_meta, dataset2._participants_meta, 'participants.tsv data is not the same')


if __name__ == '__main__':
    unittest.main()



