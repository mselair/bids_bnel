import os
import json
import csv

import os
import shutil
import warnings

import pandas as pd
import json
from .templates import *

import unittest
import tempfile
import os
import json
import warnings
import time

import pandas as pd


BIDS_VERSION = '1.4.1'
DELIMITER = os.path.sep

class BIDS_json(dict):
    """
    Class for creating BIDS compatible json files

    This class extends the built-in `dict` class to provide functionality
    for creating and saving BIDS compatible json files.

    Attributes:
        _path (str): Path to the json file.
        _data (dict): Dictionary to store the json data.

    Args:
        path (str): Path to the json file.
    """

    def __init__(self, path):
        """
        Initialize Bids_json object with a path to a json file.

        Args:
            path (str): Path to the json file.
        """
        super().__init__()
        self._path = path

        # Load existing json file if it exists
        if os.path.exists(self._path):
            with open(self._path, 'r') as f:
                self._data = json.load(f)
                for key, value in self._data.items():
                    self[key] = value

    def dump(self):
        """
        Save the Bids_json object to the json file.

        This method saves the current Bids_json object to the json file
        specified during object initialization, with an indentation of 4 spaces.
        """
        with open(self._path, 'w') as f:
            json.dump(self, f, indent=4)

class BIDS_TSV(pd.DataFrame):
    """
    This class represents a BIDS (Brain Imaging Data Structure) TSV (Tab-Separated Values) file, which is a type of
    metadata file commonly used in neuroimaging research. It extends the functionality of a pandas DataFrame and
    provides additional methods for handling BIDS metadata.

    Attributes:
        - path_tsv (str): The path to the TSV file.
        - path_json (str, optional): The path to the associated JSON file containing metadata. If not provided, it is
          derived from the path_tsv by replacing the file extension with ".json".
        - metadata (BIDS_json): A dictionary-like object representing the metadata loaded from the JSON file.

    Methods:
        - __init__(self, path_tsv, path_json=None, *args, **kwargs): Constructor method that initializes the object.
        - set_template(self, template): Sets a metadata template for filling missing values.
        - dump(self): Saves the DataFrame to the TSV file and the metadata to the JSON file.
        - add_row(self, row): Adds a row to the DataFrame.

    Properties:
        - metadata: Property that provides access to the metadata as a dictionary-like object.

    """
    def __init__(self, path_tsv, path_json=None, *args, **kwargs):
        """
        Constructor for BIDS_TSV class.

        Args:
            path_tsv (str): Path to the TSV file.
            path_json (str, optional): Path to the JSON file. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            TypeError: If path_tsv is not a string.
        """
        super().__init__(*args, **kwargs)

        if not isinstance(path_tsv, str):
            raise TypeError('path_tsv must be a string')

        self._path_tsv = path_tsv
        self._name = path_tsv.split(DELIMITER)[-1][:-4].split('_')[-1]

        if not isinstance(path_json, str):
            self._path_json = path_tsv.replace('.tsv', '.json')
        else:
            self._path_json = path_json

        self._metadata = BIDS_json(self._path_json)

        if list(self._metadata.keys()).__len__():
            for k in self._metadata.keys():
                self[k] = None

        if os.path.exists(self._path_tsv) and self._metadata.__len__():
            self._load_tsv()

        if list(self._metadata.keys()).__len__() == 0:
            if self._name in templates.keys():
                self.set_template(templates[self._name])
            else:
                warnings.warn('No template found for {}'.format(self._name))

    @property
    def metadata(self):
        """
        Get the metadata associated with the TSV file.

        Returns:
            dict: Metadata associated with the TSV file.
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """
        Set the metadata associated with the TSV file.

        Args:
            value (dict): Metadata to be set.
        """
        self._metadata = value

    def set_template(self, template):
        """
        Set the metadata using a template.

        Args:
            template (dict): Template to set the metadata.

        Warnings:
            Warns if a key in the template is not found in the TSV and fills it with an empty value.
        """
        self._metadata.update(template)
        for key in self._metadata.keys():
            if key not in self.keys():
                warnings.warn("Key '{}' not found in tsv and was filled empty".format(key))
                self[key] = None

    def dump(self):
        """
        Dump the TSV and metadata to their respective files.

        Warnings:
            Warns if a key in the metadata is not found in the TSV and fills it with an empty value.
        """
        self.to_csv(self._path_tsv, sep='\t', index=False)

        for key in self.keys():
            if key not in self._metadata.keys():
                warnings.warn("Key '{}' not found in metadata and was filled empty".format(key))
                self._metadata[key] = {}

        self._metadata.dump()

    def _load_tsv(self):
        """
        Load data from the TSV file and add rows to the BIDS_TSV object.
        """
        df = pd.read_csv(self._path_tsv, sep='\t')
        if df.__len__():
            for idx, row in df.iterrows():
                self.add_row(row)

    def add_row(self, row):
        """
        Add a row to the DataFrame.

        Args:
            row (pd.Series): The row to be added as a pandas Series.

        """
        self.loc[self.index.__len__()] = row
        #return BIDS_TSV(self._path_tsv, self._path_json, (self._append(row, ignore_index=True)))

class BIDS_iEEG:
    def __init__(self, path):
        pass

class BIDS_session:
    def __init__(self, path):
        pass

class BID_subject:
    def __init__(self, path):
        self.path = path
        self._sessions = {}

    def create_session(self, session):
        pass

    def find_sessions(self):
        pass

class BIDSDataset(dict):
    """
    Class representing a BIDS dataset.

    This class provides methods to create and manipulate a BIDS dataset, including creating and updating metadata JSON
    files, and loading metadata from existing JSON files.

    Args:
        path (str): Path to the BIDS dataset directory.
        create_dataset (bool, optional): Flag indicating whether to create a new dataset. Defaults to False.

    Attributes:
        path (str): Path to the BIDS dataset directory.
        _participants_path (str): Path to the participants.tsv file.
        _jsons (dict): Dictionary to store instances of Bids_json class for each metadata JSON file.
        _participants_meta (pandas.DataFrame): DataFrame to store participant metadata.

    Raises:
        ValueError: If the specified directory does not exist.

    """

    def __init__(self, path: str, create_dataset=False):
        """
        Initialize a BIDSDataset instance.

        Args:
            path (str): Path to the BIDS dataset directory.
            create_dataset (bool, optional): Flag indicating whether to create a new dataset. Defaults to False. If true, overwrites existing dataset.

        """
        super().__init__()

        self.path = path
        self._participants_path = os.path.join(self.path, 'participants.tsv')
        self._jsons = {}

        if create_dataset:
            self._create_dataset()
        else:
            self._load_dataset()

        if not os.path.exists(self.path):
            raise ValueError(f'No such directory: {self.path}')

    def _create_dataset(self):
        """
        Create a new BIDS dataset.

        This method creates a new BIDS dataset by creating metadata JSON files using the provided templates, and
        optionally creating a participants.tsv file.

        """

        if os.path.exists(self.path):
            shutil.rmtree(self.path)
            time.sleep(0.1)
        else:
            os.mkdir(self.path)

            self['dataset_description'] = Bids_json(os.path.join(self.path, 'dataset_description.json'))
            self['events'] = Bids_json(os.path.join(self.path, 'events.json'))
            self['coordsystem'] = Bids_json(os.path.join(self.path, 'coordsystem.json'))
            self['electrodes'] = Bids_json(os.path.join(self.path, 'electrodes.json'))
            self['channels'] = Bids_json(os.path.join(self.path, 'channels.json'))
            self['participants'] = Bids_json(os.path.join(self.path, 'participants.json'))

            self._jsons['events'] = Bids_json(os.path.join(self.path, 'events.json'))
            self._jsons['events'].update(template_events)
            self._jsons['coordsystem'] = Bids_json(os.path.join(self.path, 'coordsystem.json'))
            self._jsons['coordsystem'].update(template_coordsystem)
            self._jsons['electrodes'] = Bids_json(os.path.join(self.path, 'electrodes.json'))
            self._jsons['electrodes'].update(template_electrodes)
            self._jsons['channels'] = Bids_json(os.path.join(self.path, 'channels.json'))
            self._jsons['channels'].update(template_channels)
            self._jsons['participants'] = Bids_json(os.path.join(self.path, 'participants.json'))
            self._jsons['participants'].update(template_participants)

            self.dump()

            if not os.path.exists(self._participants_path):
                self._participants_meta = pd.DataFrame([], columns=self._jsons['participants'].keys())
                self._participants_meta.to_csv(self._participants_path, sep='\t', index=False)


    def _load_dataset(self):
        """
        Load an existing BIDS dataset.

        This method loads an existing BIDS dataset by loading metadata from existing JSON files and participants.tsv file.

        """

        if os.path.exists(self.path):
            for file in os.listdir(self.path):
                if file.endswith('.json'):
                    self._jsons[file.split('.')[0]] = Bids_json(os.path.join(self.path, file))

            if os.path.exists(self._participants_path):
                self._participants_meta = pd.read_csv(self._participants_path, sep='\t')

    def dump(self):
        """
        Update JSON metadata files.
        """
        for key in self._jsons.keys():
            self._jsons[key].save()













