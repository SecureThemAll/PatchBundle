#!/usr/bin/env python3
from typing import NoReturn

import pandas as pd

from abc import ABC, abstractmethod
from pathlib import Path

from utils.data_structs import DataPaths
from utils.patch_record import PatchRecord

# Decorators
from utils.decorators.filter import c_code, two_chunk_changes, no_nulls, max_line_changes


class Dataset(ABC):
    def __init__(self, name: str, paths: DataPaths):
        self.name = name
        self.dict_data = []
        self.paths = paths
        self.collected_path = self.paths.collected / Path(self.name)
        self.transformed_file = self.paths.transformed / Path(self.name + '.pkl')
        self.filtered_file = self.paths.filtered / Path(self.name + '.pkl')
        self.frame = None

    def __call__(self, patch_record_args: dict) -> NoReturn:
        patch_record = PatchRecord(**patch_record_args)

        if patch_record.has_patch():
            patch_records = patch_record.to_dict()
            self.dict_data.extend(patch_records)

    @abstractmethod
    def collect(self, source: str):
        pass

    @abstractmethod
    def transform(self):
        pass

    @max_line_changes(lines=20)
    @no_nulls
    @two_chunk_changes
    @c_code
    def filter(self):
        print(f"Filtering {self.name}")
        return pd.read_pickle(filepath_or_buffer=str(self.transformed_file))

    def data_to_pickle(self):
        frame = pd.DataFrame.from_dict(self.dict_data)
        print(f"Hunks count: {len(frame)}")
        frame.drop_duplicates(subset="hunk", keep=False, inplace=True)
        print(f"Unique hunks count: {len(frame)}")
        frame.to_pickle(path=self.transformed_file)
